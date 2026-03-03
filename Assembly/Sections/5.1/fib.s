global _start

section .text
_start:
  xor rax,rax
  xor rbx,rbx
  inc rbx 
  mov rcx, 10
  loopfib:
    add rax, rbx
    xchg rax, rbx
    loop loopfib
