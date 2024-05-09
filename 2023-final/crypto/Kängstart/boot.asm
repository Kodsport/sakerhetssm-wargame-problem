; nasm -f bin boot.asm -o boot.bin
; objdump -b binary -m i386:x86-64 -M intel,addr16,data16 -D boot.bin
; xxd boot.bin
; qemu-system-x86_64 boot.bin -cpu qemu64,+aes

[bits 16] ; 16-bit RealMode
[org 0x7c00] ; start address

init:
    ; mov ax, 0x07c0
    xor ax, ax
    mov ds, ax
    mov ss, ax
    mov sp, 0x9c00 ; 8KiB past code start

enable_SSE:
    ; enable SSE
    mov eax, cr0
    and al, 0xFB
    or al, 0x2
    mov cr0, eax
    mov eax, cr4
    or ah, 6 ; or ax, 3 << 9
    mov cr4, eax
    ; done enabling SSE

PLEN equ 3*16 ; passphrase length

main:
    ; print "Enter passphrase: " using interrupt with nullterminated string
    mov cx, len_password_message
    mov bp, password_message
    call print_str

    call read_password
    call print_newline

    ; load XMMs from RAM
    movdqu xmm0, [LUT2 + 0*16]
    movdqu xmm1, [LUT2 + 1*16]
    movdqu xmm2, [LUT2 + 2*16]

    call ENC

    ; store XMMs to RAM
    movdqu [LUT2 + 0*16], xmm0
    movdqu [LUT2 + 1*16], xmm1
    movdqu [LUT2 + 2*16], xmm2

    call check_password_correct

    inf_loop:
    jmp inf_loop


ENC:
    ; idea: instead of having extra instructions for rotating the registers. use self modifying code to change operands
    mov cl, PLEN
enc_loop:
    movaps xmm3, xmm1 ; F
    xorps xmm3, xmm2
    aesenc xmm3, xmm0 ; for easier debugging replace this instruction with xorps
    ; rotate regs
    movaps xmm0, xmm1
    movaps xmm1, xmm2
    movaps xmm2, xmm3
    dec cl
    jnz enc_loop

    ; swap regs
    movaps xmm3, xmm0
    movaps xmm0, xmm2
    movaps xmm2, xmm3
    ret


check_password_correct:
    mov bp, deny_message
    mov cx, len_deny_message
    xor si, si
start_check_loop:
    mov bx, [LUT2 + si]
    mov dx, [LUT1 + si]
    cmp bx, dx
    jne WRONG_PASS
    add si, 2
    cmp si, PLEN
    jne start_check_loop
CORRECT_PASS:
    mov bp, accept_message
    mov cx, len_accept_message
WRONG_PASS:
    call print_str
    call print_newline
    ret

print_str: ; paramters cx=number of bytes bp=address of string
    ; get cursor position
    push cx
    mov ah, 0x03
    mov bh, 0
    int 0x10

    ; print string at cursor position
    pop cx
    mov bl, 0b0000_0111
    mov ah, 0x13
    mov al, 0
    int 0x10

    ; move cursor at end of string
    add dx, cx
    mov ah, 0x02
    mov bh, 0
    int 0x10
    ret

read_password:
    ;interrupts and save to mem and read into xmm regs afterwards
    mov di, PLEN
    xor bx, bx
    start_scanf:
    ; read keystroke into al
    xor ah, ah ; mov ah, 0x00
    int 0x16
    cmp al, 0x0d
    je end_scanf
    ; write char to screen
    mov ah, 0x0E
    int 0x10
    dec di
    mov [LUT2 + di], al
    jnz start_scanf
    end_scanf:
    ret

print_newline:
    push ax
    mov ax, 0x0E0A ; carrige return
    int 0x10
    mov al, 0x0D ; new-line
    int 0x10
    pop ax
    ret

; encrypted flag, generated from gen_enc_data.cpp
LUT1:
    db 0x6e
    db 0x1d
    db 0x71
    db 0x30
    db 0xaf
    db 0x40
    db 0x3a
    db 0xac
    db 0xb4
    db 0x9a
    db 0xed
    db 0x58
    db 0xe4
    db 0x63
    db 0x29
    db 0x94
    db 0xa4
    db 0xed
    db 0xb6
    db 0x6c
    db 0x74
    db 0xf6
    db 0x9b
    db 0x01
    db 0xae
    db 0x91
    db 0xa4
    db 0x86
    db 0x02
    db 0x04
    db 0x32
    db 0xcd
    db 0xaf
    db 0xe1
    db 0x63
    db 0x1d
    db 0x45
    db 0x9b
    db 0xe1
    db 0xbd
    db 0x87
    db 0x14
    db 0xe3
    db 0x52
    db 0x60
    db 0xf7
    db 0xed
    db 0x9d

password_message:
    db "Enter passphrase: "
    len_password_message equ $ - password_message

deny_message:
    db "DENIED!"
    len_deny_message equ $ - deny_message

accept_message:
    db "ACCEPTED!"
    len_accept_message equ $ - accept_message

    times 510-($-$$) db 0
    db 0x55
    db 0xAA

; input from user stored here, outside of the MBR bootsector
LUT2:
    ; times 64 db 0

