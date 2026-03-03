global _start


section .text
_start:
  mov al, 7
  mov bl, 9
  xchg bx,ax
