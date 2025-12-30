import time
with open('test.txt','rb') as f:
    letters=b''
    while True:
        letter=f.read(1)
        if not letter:
            break
        letters+=letter
        print(f'\rLetters: {letters}',end='',flush=True)
        time.sleep(0.5)
    print()

s='rrr'
s.split(' ',1)