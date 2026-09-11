with open('snake.rtm', 'r', encoding='utf-8') as f:
    text = f.read()

data_sec = text[text.find('.section ".data"'):text.find('.section ".text"')]
text_sec = text[text.find('.section ".text"'):]

new_text = """.section ".text"
    j inicio
    .word 0
    .word 0
    .word 0
""" + text_sec.replace('.section ".text"', 'inicio:') + "\n" + data_sec

with open('snake.rtm', 'w', encoding='utf-8') as f:
    f.write(new_text)
