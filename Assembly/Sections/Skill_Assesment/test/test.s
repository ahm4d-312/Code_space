global _start
extern printf

section .data:
  output_format db "%x", 0x0a,0x00
section .text
_start:
  mov rdi, output_format
  mov rsi, 1000000
  call printf 

  mov rdi, output_format
  mov rsi, 1000000
  call printf 
  mov rax, 60
  mov rdi, 0
  syscall
