global _start


section .text
_start:
  mov al, 0
  mov bl, 1
  inc bl
  
  add al,bl
  
  mov al, 0
  mov bl, 1
  inc bl 
  
  sub al,bl 
  
  mov al, 0
  mov bl, 1
  inc bl

  imul ax, bx

  mov al, 0
  mov bl, 1
  inc bl
  not al

  mov al, 0
  mov bl, 1
  inc bl
  and al,bl 

  mov al, 0
  mov bl, 1
  inc bl
  or al,bl  

  mov al, 0
  mov bl, 1
  inc bl
  xor al,bl 



