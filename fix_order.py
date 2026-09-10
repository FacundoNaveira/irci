with open('snake.rtm', 'r') as f:
    text = f.read()

parts = text.split('.section ".text"')
data_section = parts[0]
text_section = '.section ".text"' + parts[1]

with open('snake.rtm', 'w') as f:
    f.write(text_section + '\n\n' + data_section)
