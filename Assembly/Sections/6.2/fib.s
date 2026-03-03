global _start

section .data
  msg db "Fibonacci Sequence:", 0x0a
  msg_length equ $-msg


section .text
  _start:
    mov rax, 1
    mov rdi, 1
    mov rsi, msg
    mov rdx, msg_length
    syscall
    xor rax,rax
    xor rbx,rbx
    inc rbx
    loobfib:
      add rax,rbx
      xchg rax,rbx
      push rax
      push rbx
      mov rax, 1
      mov rdi, 1
      mov rsi, [rsp]
      mov rdx, 2
      syscall
      xor rax, rax
      xor rbx, rbx
      pop rbx
      pop rax
      cmp rbx, 10
      js loobfib
    mov rax, 60
    mov rdi, 0
    syscall
    
