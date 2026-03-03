global _start

section .text
  _start:
    xor rax,rax
    xor rbx,rbx
    inc rbx
    push rax
    push rbx 
    ; call a function
    pop rbx
    pop rax
