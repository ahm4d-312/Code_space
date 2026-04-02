global _start

section .text
  _start:
    xor rbx, rbx
    mov bx, 'y!'
    push rbx
    mov rbx, 'B Academ'
    push rbx
    mov rbx, 'Hello HT'
    push rbx
    xor rax,rax
    mov al, 1
    xor rdi, rdi
    mov dil, 1
    mov rsi, rsp
    xor rdx,rdx
    mov dl, 18
    syscall 

    xor rax, rax
    xor rdi, rdi
    mov al, 60
    syscall

