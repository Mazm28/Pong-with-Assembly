section .data
    wave_amplitude dd 80.0
    wave_frequency dd 0.02
    gravity dd 0.4

section .note.GNU-stack,"",@progbits  ; اضافه کردن بخش .note.GNU-stack

section .text
global calculate_wave_offset
global apply_gravity
global update_ball_x
global update_ball_y



calculate_wave_offset:
    ; float calculate_wave_offset(float x)
    ; read input from xmm0
    mulss xmm0, dword [rel wave_frequency]  ; x cross in wave frequency
    cvtss2sd xmm0, xmm0                     ; make it double to use it in fsin
    movq [rsp-8], xmm0                      ; save in memmory
    fld qword [rsp-8]                       
    fsin                                    ; calculate sin with fsin
    fstp qword [rsp-8]                      ; save in memmory
    movq xmm0, [rsp-8]                      ; load answer in xmm0
    cvtsd2ss xmm0, xmm0                     ; return it to float
    mulss xmm0, dword [rel wave_amplitude]  ; cross in wave amplitude
    ret


apply_gravity:
    ; void apply_gravity(float* ball_velocity_y)
    ; read input from rdi
    movss xmm0, dword [rdi]                  ; load ball velocity in xmm0
    addss xmm0, dword [rel gravity]          ; add to gravity
    movss dword [rdi], xmm0                  ; save in ball velocity
    ret

update_ball_x:
    ; float update_ball_x(float ball_x, float ball_velocity_x)
    ; read ball_x in xmm0 and ball_velocity_x in xmm1
    addss xmm0, xmm1  ; ball_x + ball_velocity_x
    ret

update_ball_y:
    ; float update_ball_y(float ball_y, float ball_velocity_y)
    ; read ball_y in xmm0 and ball_velocity_y in xmm1
    addss xmm0, xmm1  ; ball_y + ball_velocity_y
    ret


    ;command to make a python library from assembly file:
    ;nasm -felf64 calculations.asm -o calculations.o && gcc -shared -o libcalculations.so calculations.o