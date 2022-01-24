from discord.opus import Encoder
#from discord import FFmpegPCMAudio
from discord import ClientException
from discord import AudioSource

from io import BytesIO
import gtts

import asyncio
import subprocess
import shlex

class FFmpegPCMAudio(AudioSource):
    def __init__(self, source, *, executable='ffmpeg', pipe=False, stderr=None, before_options=None, options=None):
        stdin = None if not pipe else source
        args = [executable]

        if isinstance(before_options, str):
            args.extend(shlex.split(before_options))
        
        args.append('-i')
        args.append('-' if pipe else source)
        args.extend(('-f', 's16le', '-ar', '48000', '-ac', '2', '-loglevel', 'warning'))

        if isinstance(options, str):
            args.extend(shlex.split(options))
        
        args.append('pipe:1')
        self._process = None

        try:
            self._process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr)
            self._stdout = BytesIO(
                self._process.communicate(input=stdin)[0]
            )
        except FileNotFoundError:
            raise ClientException(executable + ' was not found.') from None
        except subprocess.SubprocessError as exc:
            raise ClientException('Popen failed: {0.__class__.__name__}: {0}'.format(exc)) from exc
    
    def read(self):
        ret = self._stdout.read(Encoder.FRAME_SIZE)
        
        if len(ret) != Encoder.FRAME_SIZE:
            return b''
        return ret

    def cleanup(self):
        proc = self._process
        if proc is None:
            return
        
        proc.kill()
        if proc.poll() is None:
            proc.communicate()

        self._process = None

async def play(stream, channel):
    vc = await channel.connect()
    source = FFmpegPCMAudio(stream.read(), pipe=True)
    vc.play(source)

    while vc.is_playing():
        await asyncio.sleep(1)
        
    await vc.disconnect()

async def tts(text, channel):
    with BytesIO() as stream:    
        tts = gtts.gTTS(text)
        tts.write_to_fp(stream)

        stream.seek(0)
        await play(stream, channel)