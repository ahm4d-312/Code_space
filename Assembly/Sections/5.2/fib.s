global _start

section .text
_start:
  xor rax,rax
  xor rbx,rbx
  inc rbx 
  mov rcx, 10
  loopfib:
    add rax, rbx
    xor rax, rbx
    xor rbx, rax
    xor rax, rbx
    jmp loopfib
