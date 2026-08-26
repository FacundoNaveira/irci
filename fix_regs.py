import os

with open("snake.rtm", "r", encoding="utf-8") as f:
    code = f.read()

code = code.replace("$t6", "$a3")
code = code.replace("$t7", "$a4")
code = code.replace("$t8", "$a5")
code = code.replace("$t9", "$lr0")

with open("snake.rtm", "w", encoding="utf-8") as f:
    f.write(code)

print("Replaced registers.")
