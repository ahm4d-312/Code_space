section .data
    result db 0

section .text
    global _start

_start:
    ; store values in registers
    mov rax, 3
    mov rbx, 4

    ; add them
    add rax, rbx          ; rax = 7

    ; convert to ASCII (single digit)
    add al, '0'
    mov byte [rel result], al

    ; write to stdout
    mov rax, 1            ; syscall: write
    mov rdi, 1            ; fd = stdout
    mov rsi, result       ; buffer
    mov rdx, 1            ; length
    syscall

    ; exit
    mov rax, 60
    xor rdi, rdi
    syscall

