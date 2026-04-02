global _start
extern printf

section .data
  message db "Fib Sequence", 0x0a
  message_len equ $-message
  output_format db "%d", 0x0a, 0x00

section .text
  _start:
    call printMessage
    call init_fib
    call loop_fib
    call exit

  printMessage:
    mov rax, 1
    mov rdi, 1
    mov rsi, message
    mov rdx,message_len
    syscall
    ret

  init_fib:
    xor rax, rax
    xor rbx, rbx
    inc rbx
    ret

  print_fib:
    push rax
    push rbx
    mov rdi, output_format
    mov rsi, rbx
    call printf
    pop rbx
    pop rax
    ret

  loop_fib:
    call print_fib
    add rax, rbx
    xchg rax, rbx
    cmp rbx, 10
    js loop_fib
    ret

  exit:
    mov rax, 60
    mov rdi, 0
    syscall 

