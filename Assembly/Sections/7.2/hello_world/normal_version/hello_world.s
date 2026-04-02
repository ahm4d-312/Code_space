global _start

section .data
  msg db "Hello HTB Academy!"


section .text
  _start:
    mov rsi,msg
    mov rdi, 1
    mov rdx, 18
    mov rax, 1
    syscall

    mov rax, 60
    mov rdi, 0
    push 'ddccbbaa'
    syscall
