[bits 64]
file_load_va: equ 4096 * 40

db 0x7f, 'E', 'L', 'F'
db 2
db 1
db 1
db 0

code_chunk_1:
	mov rsi, rsp
	dec sp ; you actually need to do some slight reversing to figure this out for exploit to work, also we had 3 spare bytes anyway
	jmp code_chunk_3

dw 2
dw 0x3e
dd 1
dq entry_point + file_load_va
dq program_headers_start

entry_point:
; 1
code_chunk_2:
	db 0x66, 0x81, 0x2d, 0x22, 0x00, 0x00, 0x00, 0x02, 0xf0 ; sub WORD PTR [rip + 0x22], 0xf002
	jmp code_chunk_1

db 0
dw 64
dw 0x38
dw 1

program_headers_start:
dd 1
dd 7
dq 0
dq file_load_va

code_chunk_3:
	mov  sp, 0xef
	syscall
	jmp code_chunk_2

dq file_end
dq file_end

message: db "th15golf" ; needed to pad out kernel structure (introduced in later linux versions)

file_end:
