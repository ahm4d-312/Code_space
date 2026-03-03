global _start

section .data 
  message db "Fibonacci Sequence:", 0x0a
  msg_len equ $-message

section .text
  _start:
    call printMessage
    call initfib
    call loopfib
    call Exit

  printMessage:
    mov rax, 1
    mov rdi, 1
    mov rsi, message
    mov rdx, msg_len
    syscall
    ret
  
  initfib: 
    xor rax, rax
    xor rbx, rbx
    inc rbx
    ret

  loopfib:
    add rax, rbx
    xchg rax, rbx
    cmp rbx, 10
    js loopfib
    ret

  Exit:
    mov rax, 60
    mov rdi, 0
    syscall
