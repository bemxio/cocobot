import msgpack

path = input("Path for the text file: ")

with open(path, "r") as file:
    messages = file.readlines()

with open("memory.msgpack", "w") as file:
   msgpack.dump(messages, file)

print("Done!")