global _start

section .text
_start:
  xor rax,rax
  xor rbx,rbx
  inc rbx
  loopfib:
    add rax, rbx
    xchg rax, rbx
    cmp rbx, 10
    js loopfib

