;
; rm solver ; nasm/nasm-2.15.05/nasm -f macho64 solver.asm && ld -e start -no_pie -segprot __TEXT rwx rwx -static -o solver solver.o;
;


    global    start
    section   .text

C_HEADER        equ     0x0000000100000000

g_flag:
    ;db      "nc3{arm_er_c00l_men_x64_styrer_vildt_i_2o21}", 0
    ; Flag + extra bytes that are present in target binary:
    db  0x6e,0x63,0x33,0x7b,0x61,0x72,0x6d,0x5f,0x65,0x72,0x5f,0x63,0x30,0x30,0x6c,0x5f,0x6d,0x65,0x6e,0x5f,0x78,0x36,0x34,0x5f,0x73,0x74,0x79,0x72,0x65,0x72,0x5f,0x76
    db  0x69,0x6c,0x64,0x74,0x5f,0x69,0x5f,0x32,0x6f,0x32,0x31,0x7d,0x0a,0x45,0x5a,0x45,0x52,0x4f,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00

l_rick_roll_bytes:
    db  0x6e,0x65,0x76,0x65,0x72,0x5f,0x67,0x6f,0x6e,0x6e,0x61,0x5f,0x67,0x69,0x76,0x65,0x5f,0x79,0x6f,0x75,0x5f,0x75,0x70,0x21,0x45,0x80,0x04,0x17,0x01,0x43,0x80,0x34

; Taken from memory:
l_program_checksum:
    db  0xca,0x98,0x95,0x36,0xb8,0xf1,0xa7,0xa8,0xca,0x98,0x95,0x36,0xb8,0xf1,0xa7,0xa8,0xca,0x98,0x95,0x36,0xb8,0xf1,0xa7,0xa8,0xca,0x98,0x95,0x36,0xb8,0xf1,0xa7,0xa8


l_correctly_encrypted_flag:
    db  0x0f,0x68,0xc0,0x74,0x01,0x1b,0xca,0xaf,0x35,0xb4,0xcd,0x67,0x08,0x14,0x8a,0xc1,0xab,0xcd,0xa8,0xbc,0x36,0x0a,0x42,0x08,0x62,0x5f,0x8e,0xb8,0x16,0x02,0xcc,0x95
    db  0x28,0x7b,0xae,0x5a,0x0b,0xda,0x9c,0xc9,0x33,0xa9,0xbf,0x3b,0x05,0x1e,0xba,0xbc,0x48,0x5e,0x4a,0x46,0xc5,0x96,0xc8,0x96,0xea,0x29,0x5a,0x57,0xfd,0xec,0x5b,0x38



start:

    ;mov     rax, 0x200001A
    ;mov     rdi, 31      ; req = PT_DENY_ATTACH
    ;mov     rsi, 0      ; pid = 0
    ;mov     rdx, 0      ; addr = 0
    ;mov     rcx, 0      ; addr = 0
    ;mov     r10, 0      ; data = 0
    ;syscall


    call    l_encrypt
    ;call    l_decrypt


    mov     rax, 0x02000001          ; 0x02000001 (EXIT)
    xor     rdi, rdi
    syscall



l_decrypt:
    mov             rsi, l_correctly_encrypted_flag

    VMOVDQU         ymm0, [rsi]           ; Load 256 bit - 32 bytes - First half of Flag
    VMOVDQU         ymm1, [rsi + 32]      ; Load 256 bit - 32 bytes - Second half of flag


    ; Calculate CORRECT FLAG BYTES for storage in binary:
    mov             rcx, 0x0000000002000001
    ; Generate 1
    vpcmpeqw ymm8,ymm8
    vpabsb ymm8,ymm8
l_unpack_final_code_loop1:
    ; CORRECT FLAG
    vpaddD          ymm0, ymm0, ymm8
    vpaddD          ymm1, ymm1, ymm8

    dec             rcx
    jnz             l_unpack_final_code_loop1



    ; PERMUTE
    vpermilps       ymm2, ymm0, 27
    vpermilps       ymm3, ymm1, 27


    ; ADD using very large loop
    mov             rcx, 0x0000000002000001
    vpcmpeqw ymm8,ymm8
    vpsrlq ymm8,62
l_modify_in_long_loop_decrypt:
    vpsubq          ymm2, ymm2, ymm8
    vpsubq          ymm3, ymm3, ymm8
    dec             rcx
    jnz             l_modify_in_long_loop_decrypt


    vpcmpeqw        ymm4,ymm4           ; 0xFF
    vpabsb          ymm4, ymm4          ; 0x01
    vpxor           ymm6, ymm2, ymm4
    vpxor           ymm7, ymm3, ymm4

    mov             rbx, l_program_checksum
    VLDDQU          ymm5, [rbx]
    VPADDQ          ymm8, ymm6, ymm5    ; FLAGA - CODE HASH using 64 bit
    VPADDQ          ymm9, ymm7, ymm5    ; FLAGB - CODE HASH using 64 bit


    mov             rbx, l_rick_roll_bytes
    VLDDQU          ymm2, [rbx]         ; Load byte to modify with - OPCODES
    VPADDB          ymm10, ymm8, ymm2    ; FLAGA - OPCODES using BYTE
    VPADDB          ymm11, ymm9, ymm2    ; FLAGB - OPCODES using BYTE


    ret


l_encrypt:
    mov             rsi, g_flag

    ; 6E 63 33 7B 61 72 6D 5F 65 72 5F 63 30 30 6C 5F 6D 65 6E 5F 78 36 34 5F 73 74 79 72 65 72 5F 76
    VMOVDQU         ymm0, [rsi]           ; Load 256 bit - 32 bytes - First half of Flag
    ; 69 6C 64 74 5F 69 5F 32 6F 32 31 7D 47 45 5A 45 52 4F 00 00 00 00 00 00 00 00 00 00 00 00 00 00
    VMOVDQU         ymm1, [rsi + 32]      ; Load 256 bit - 32 bytes - Second half of flag


    ; VPSUBB med Rick Roll tekst
    mov             rbx, l_rick_roll_bytes
    ; 6E 65 76 65 72 5F 67 6F 6E 6E 61 5F 67 69 76 65 5F 79 6F 75 5F 75 70 21 45 80 04 17 01 43 80 34
    VLDDQU          ymm2, [rbx]         ; Load byte to modify with - OPCODES
    ; 00 FE BD 16 EF 13 06 F0 F7 04 FE 04 C9 C7 F6 FA 0E EC FF EA 19 C1 C4 3E 2E F4 75 5B 64 2F DF 42
    VPSUBB          ymm3, ymm0, ymm2    ; FLAGA - OPCODES using BYTE
    ; FB 07 EE 0F ED 0A F8 C3 01 C4 D0 1E E0 DC E4 E0 F3 D6 91 8B A1 8B 90 DF BB 80 FC E9 FF BD 80 CC
    VPSUBB          ymm4, ymm1, ymm2    ; FLAGB - OPCODES using BYTE


    ; VPSUBQ med PROGRAM CHECKSUM (First BYTE is affected by the INPUT LENGTH (44))
    mov             rbx, l_program_checksum
    VLDDQU          ymm5, [rbx]
    VPSUBQ          ymm6, ymm3, ymm5    ; FLAGA - CODE HASH using 64 bit
    VPSUBQ          ymm7, ymm4, ymm5    ; FLAGB - CODE HASH using 64 bit


    ; XOR 1
    vpcmpeqw        ymm4,ymm4           ; 0xFF
    vpabsb          ymm4, ymm4          ; 0x01
    vpxor           ymm6, ymm6, ymm4
    vpxor           ymm7, ymm7, ymm4


    ; ADD using very large loop
    mov             rcx, 0x0000000002000001
    vpcmpeqw        ymm8, ymm8
    vpsrlq          ymm8, 62
l_modify_in_long_loop:
    vpaddq          ymm6, ymm6, ymm8
    vpaddq          ymm7, ymm7, ymm8
    dec             rcx
    jnz             l_modify_in_long_loop


    ; PERMUTE
    vpermilps       ymm12, ymm6, 27
    vpermilps       ymm13, ymm7, 27

    ; Now the correct flag bytes are in ymm12 & ymm13.



    ; Next we store the correct flag bytes as encrypted using a long loop as well:

    ; Calculate CORRECT FLAG BYTES for storage in binary:
    mov             rcx, 0x0000000002000001
    ; Generate 1
    vpcmpeqw ymm8,ymm8
    vpabsb ymm8,ymm8
l_unpack_final_code_loop2:
    vpsubD          ymm12, ymm12, ymm8
    vpsubD          ymm13, ymm13, ymm8

    dec             rcx
    jnz             l_unpack_final_code_loop2


    ; The final bytes to store in the binary is in ymm12 and ymm13


    ret
