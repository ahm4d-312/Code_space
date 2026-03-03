global _start

section .data
  r dd 0

section .text
  _start:
    mov rax, 89
    add al, '0'
    push rax
    xor rax, rax
    mov rax, 1
    mov rdi, 1
    pop [r]
    mov rsi, r
    mov rdx, 20
    syscall

    xor rax, rax
    mov rax, 60
    xor rdi, rdi 
    syscall

