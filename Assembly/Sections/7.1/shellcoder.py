#!/home/ahm4d_312/Codes_Vault/Assembly/.pwntools_env/bin/python3

import sys
from pwn import *

context(os='linux',arch='amd64',log_level='error')
file=ELF(sys.argv[1])

shellcode=file.section('.text')
print(shellcode.hex())
