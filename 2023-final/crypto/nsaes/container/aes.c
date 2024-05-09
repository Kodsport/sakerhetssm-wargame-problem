/*
 * Source originally from https://github.com/SmarterDM/micro-aes
 *
 * Included copyright notice:
 * MIT License
 *
 * Copyright (c) 2016 Andrew Carter
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
*/

#include <stdint.h>
#include <string.h>
#include <stdio.h>

#define AES_256_ROUNDS 14
#define AES_192_ROUNDS 12
#define AES_128_ROUNDS 10

// Uncomment this (or compile with -DOPT_8_BIT) to optimise for an 8 bit architecture
// #define AES_OPT_8_BIT

#ifdef AES_OPT_8_BIT
  typedef uint8_t counter;
#else
  typedef unsigned int counter;
#endif

// AES-256

typedef struct aes_256_context_t_ {
  uint8_t round_key[(AES_256_ROUNDS + 1) * 16];
} aes_256_context_t;

void aes_256_init    (aes_256_context_t *context, uint8_t key[32]);
void aes_256_encrypt (aes_256_context_t *context, uint8_t block[16]);
void aes_256_decrypt (aes_256_context_t *context, uint8_t block[16]);

// AES-192

typedef struct aes_192_context_t_ {
  uint8_t round_key[(AES_192_ROUNDS + 1) * 16];
} aes_192_context_t;

void aes_192_init    (aes_192_context_t *context, uint8_t key[24]);
void aes_192_encrypt (aes_192_context_t *context, uint8_t block[16]);
void aes_192_decrypt (aes_192_context_t *context, uint8_t block[16]);

// AES-128

typedef struct aes_128_context_t_ {
  uint8_t round_key[(AES_128_ROUNDS + 1) * 16];
} aes_128_context_t;

void aes_128_init    (aes_128_context_t *context, uint8_t key[16]);
void aes_128_encrypt (aes_128_context_t *context, uint8_t block[16]);
void aes_128_decrypt (aes_128_context_t *context, uint8_t block[16]);

// Preprocessor Definitions

#define MAP(i,j) (((j) << 2) + (i))
#define MUL(x,y) aes_GaloisFieldMultiply((x),(y))
#define MUL2(x)  (((x) << 1) ^ (0x1B & (((x) >> 7) * 0xFF))) & 0xFF
#define MUL3(x)  ((x) ^ MUL2(x))
#define SUB4(x)  ((s_box[((x) & 0xFF000000) >> 24] << 24) | (s_box[((x) & 0xFF0000) >> 16] << 16) | (s_box[((x) & 0xFF00) >> 8] << 8) | s_box[((x) & 0xFF)])

// AES Tables

uint8_t s_box[256] = {
    0xe6, 0xe7, 0xe4, 0xe5, 0xe2, 0xe3, 0xe0, 0xe1, 0xee, 0xef, 0xec, 0xed, 0xea, 0xeb, 0xe8, 0xe9,
    0xf6, 0xf7, 0xf4, 0xf5, 0xf2, 0xf3, 0xf0, 0xf1, 0xfe, 0xff, 0xfc, 0xfd, 0xfa, 0xfb, 0xf8, 0xf9,
    0xc6, 0xc7, 0xc4, 0xc5, 0xc2, 0xc3, 0xc0, 0xc1, 0xce, 0xcf, 0xcc, 0xcd, 0xca, 0xcb, 0xc8, 0xc9,
    0xd6, 0xd7, 0xd4, 0xd5, 0xd2, 0xd3, 0xd0, 0xd1, 0xde, 0xdf, 0xdc, 0xdd, 0xda, 0xdb, 0xd8, 0xd9,
    0xa6, 0xa7, 0xa4, 0xa5, 0xa2, 0xa3, 0xa0, 0xa1, 0xae, 0xaf, 0xac, 0xad, 0xaa, 0xab, 0xa8, 0xa9,
    0xb6, 0xb7, 0xb4, 0xb5, 0xb2, 0xb3, 0xb0, 0xb1, 0xbe, 0xbf, 0xbc, 0xbd, 0xba, 0xbb, 0xb8, 0xb9,
    0x86, 0x87, 0x84, 0x85, 0x82, 0x83, 0x80, 0x81, 0x8e, 0x8f, 0x8c, 0x8d, 0x8a, 0x8b, 0x88, 0x89,
    0x96, 0x97, 0x94, 0x95, 0x92, 0x93, 0x90, 0x91, 0x9e, 0x9f, 0x9c, 0x9d, 0x9a, 0x9b, 0x98, 0x99,
    0x66, 0x67, 0x64, 0x65, 0x62, 0x63, 0x60, 0x61, 0x6e, 0x6f, 0x6c, 0x6d, 0x6a, 0x6b, 0x68, 0x69,
    0x76, 0x77, 0x74, 0x75, 0x72, 0x73, 0x70, 0x71, 0x7e, 0x7f, 0x7c, 0x7d, 0x7a, 0x7b, 0x78, 0x79,
    0x46, 0x47, 0x44, 0x45, 0x42, 0x43, 0x40, 0x41, 0x4e, 0x4f, 0x4c, 0x4d, 0x4a, 0x4b, 0x48, 0x49,
    0x56, 0x57, 0x54, 0x55, 0x52, 0x53, 0x50, 0x51, 0x5e, 0x5f, 0x5c, 0x5d, 0x5a, 0x5b, 0x58, 0x59,
    0x26, 0x27, 0x24, 0x25, 0x22, 0x23, 0x20, 0x21, 0x2e, 0x2f, 0x2c, 0x2d, 0x2a, 0x2b, 0x28, 0x29,
    0x36, 0x37, 0x34, 0x35, 0x32, 0x33, 0x30, 0x31, 0x3e, 0x3f, 0x3c, 0x3d, 0x3a, 0x3b, 0x38, 0x39,
    0x06, 0x07, 0x04, 0x05, 0x02, 0x03, 0x00, 0x01, 0x0e, 0x0f, 0x0c, 0x0d, 0x0a, 0x0b, 0x08, 0x09,
    0x16, 0x17, 0x14, 0x15, 0x12, 0x13, 0x10, 0x11, 0x1e, 0x1f, 0x1c, 0x1d, 0x1a, 0x1b, 0x18, 0x19,
};

uint8_t s_box_inverse[256] = {
  0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
  0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
  0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
  0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
  0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
  0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
  0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
  0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
  0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
  0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
  0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
  0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
  0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
  0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
  0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
  0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D
};

uint8_t rcon[10] = { 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36 };

// AES Operation Definitions

void aes_Rotate        (uint8_t block[4]);
void aes_SubBytes      (uint8_t state[16]);
void aes_InvSubBytes   (uint8_t state[16]);
void aes_ShiftRows     (uint8_t state[16]);
void aes_InvShiftRows  (uint8_t state[16]);
void aes_MixColumns    (uint8_t state[16]);
void aes_InvMixColumns (uint8_t state[16]);
void aes_AddRoundKey   (uint8_t state[16], uint8_t sub_key[16]);

// Maths Operation Definitions

uint8_t aes_GaloisFieldMultiply (uint8_t fixed, uint8_t variable);

// AES Core Procedures

void aes_init(uint32_t *round_key, counter b, uint32_t *key, counter n)
{
  uint32_t t;
  counter i, position, cycle;

  memcpy(round_key, key, n * sizeof(uint32_t));

  for (position = n, cycle = n, t = round_key[n - 1], i = 0; position < b; position++, cycle++) {
    if (cycle == n) {
      cycle = 0;

      aes_Rotate((uint8_t *) &t);
      t = SUB4(t);
      ((uint8_t *) &t)[0] ^= rcon[i++];
    } else if (cycle == 4 && n == 8) {
      t = SUB4(t);
    }

    t ^= round_key[position - n];
    round_key[position] = t;
  }
}

void aes_encrypt(uint8_t *round_key, uint8_t block[16], counter rounds)
{
  counter i;

  aes_AddRoundKey(block, round_key);

  for (i = 1; i < rounds; i++) {
    aes_SubBytes(block);
    aes_ShiftRows(block);
    aes_MixColumns(block);
    aes_AddRoundKey(block, round_key + (i << 4));
  }

  aes_SubBytes(block);
  aes_ShiftRows(block);
  aes_AddRoundKey(block, round_key + (i << 4));
}

void aes_decrypt(uint8_t *round_key, uint8_t block[16], counter rounds)
{
  counter i;

  aes_AddRoundKey(block, round_key + (rounds << 4));

  for (i = 1; i < rounds; i++) {
    aes_InvShiftRows(block);
    aes_InvSubBytes(block);
    aes_AddRoundKey(block, round_key + ((rounds - i) << 4));
    aes_InvMixColumns(block);
  }

  aes_InvShiftRows(block);
  aes_InvSubBytes(block);
  aes_AddRoundKey(block, round_key);
}

// AES Key Specific API

void aes_256_init(aes_256_context_t *context, uint8_t key[32])
{
  aes_init((uint32_t *) context->round_key, sizeof(context->round_key) / sizeof(uint32_t), (uint32_t *) key, 8);
}

void aes_256_encrypt(aes_256_context_t *context, uint8_t block[16])
{
  aes_encrypt(context->round_key, block, AES_256_ROUNDS);
}

void aes_256_decrypt(aes_256_context_t *context, uint8_t block[16])
{
  aes_decrypt(context->round_key, block, AES_256_ROUNDS);
}

void aes_192_init(aes_192_context_t *context, uint8_t key[24])
{
  aes_init((uint32_t *) context->round_key, sizeof(context->round_key) / sizeof(uint32_t), (uint32_t *) key, 6);
}

void aes_192_encrypt(aes_192_context_t *context, uint8_t block[16])
{
  aes_encrypt(context->round_key, block, AES_192_ROUNDS);
}

void aes_192_decrypt(aes_192_context_t *context, uint8_t block[16])
{
  aes_decrypt(context->round_key, block, AES_192_ROUNDS);
}

void aes_128_init(aes_128_context_t *context, uint8_t key[16])
{
  aes_init((uint32_t *) context->round_key, sizeof(context->round_key) / sizeof(uint32_t), (uint32_t *) key, 4);
}

void aes_128_encrypt(aes_128_context_t *context, uint8_t block[16])
{
  aes_encrypt(context->round_key, block, AES_128_ROUNDS);
}

void aes_128_decrypt(aes_128_context_t *context, uint8_t block[16])
{
  aes_decrypt(context->round_key, block, AES_128_ROUNDS);
}

// AES Operation Implementations

void aes_Rotate(uint8_t block[4])
{
  uint8_t tmp;

  tmp = block[0];
  block[0] = block[1];
  block[1] = block[2];
  block[2] = block[3];
  block[3] = tmp;
}

void aes_SubBytes(uint8_t state[16])
{
  counter i = 16;

  while (i--) {
    state[i] = s_box[state[i]];
  }
}

void aes_InvSubBytes(uint8_t state[16])
{
  counter i = 16;

  while (i--) {
    state[i] = s_box_inverse[state[i]];
  }
}

void aes_ShiftRows(uint8_t state[16])
{
  uint8_t tmp;

  tmp = state[MAP(1,0)];
  state[MAP(1,0)] = state[MAP(1,1)];
  state[MAP(1,1)] = state[MAP(1,2)];
  state[MAP(1,2)] = state[MAP(1,3)];
  state[MAP(1,3)] = tmp;

  tmp = state[MAP(2,0)];
  state[MAP(2,0)] = state[MAP(2,2)];
  state[MAP(2,2)] = tmp;

  tmp = state[MAP(2,1)];
  state[MAP(2,1)] = state[MAP(2,3)];
  state[MAP(2,3)] = tmp;

  tmp = state[MAP(3,0)];
  state[MAP(3,0)] = state[MAP(3,3)];
  state[MAP(3,3)] = state[MAP(3,2)];
  state[MAP(3,2)] = state[MAP(3,1)];
  state[MAP(3,1)] = tmp;
}

void aes_InvShiftRows(uint8_t state[16])
{
  uint8_t tmp;

  tmp = state[MAP(3,0)];
  state[MAP(3,0)] = state[MAP(3,1)];
  state[MAP(3,1)] = state[MAP(3,2)];
  state[MAP(3,2)] = state[MAP(3,3)];
  state[MAP(3,3)] = tmp;

  tmp = state[MAP(2,0)];
  state[MAP(2,0)] = state[MAP(2,2)];
  state[MAP(2,2)] = tmp;

  tmp = state[MAP(2,1)];
  state[MAP(2,1)] = state[MAP(2,3)];
  state[MAP(2,3)] = tmp;

  tmp = state[MAP(1,0)];
  state[MAP(1,0)] = state[MAP(1,3)];
  state[MAP(1,3)] = state[MAP(1,2)];
  state[MAP(1,2)] = state[MAP(1,1)];
  state[MAP(1,1)] = tmp;
}

void aes_MixColumns(uint8_t state[16])
{
  counter i = 4;
  uint8_t new_state[4];

  while (i--) {
    new_state[0] = MUL2(state[MAP(0,i)]) ^ MUL3(state[MAP(1,i)]) ^      state[MAP(2,i)]  ^      state[MAP(3,i)] ;
    new_state[1] =      state[MAP(0,i)]  ^ MUL2(state[MAP(1,i)]) ^ MUL3(state[MAP(2,i)]) ^      state[MAP(3,i)] ;
    new_state[2] =      state[MAP(0,i)]  ^      state[MAP(1,i)]  ^ MUL2(state[MAP(2,i)]) ^ MUL3(state[MAP(3,i)]);
    new_state[3] = MUL3(state[MAP(0,i)]) ^      state[MAP(1,i)]  ^      state[MAP(2,i)]  ^ MUL2(state[MAP(3,i)]);

    state[MAP(0,i)] = new_state[0];
    state[MAP(1,i)] = new_state[1];
    state[MAP(2,i)] = new_state[2];
    state[MAP(3,i)] = new_state[3];
  }
}

void aes_InvMixColumns(uint8_t state[16])
{
  counter i = 4;
  uint8_t new_state[4];

  while (i--) {
    new_state[0] = MUL(14, state[MAP(0,i)]) ^ MUL(11, state[MAP(1,i)]) ^ MUL(13, state[MAP(2,i)]) ^ MUL( 9, state[MAP(3,i)]);
    new_state[1] = MUL( 9, state[MAP(0,i)]) ^ MUL(14, state[MAP(1,i)]) ^ MUL(11, state[MAP(2,i)]) ^ MUL(13, state[MAP(3,i)]);
    new_state[2] = MUL(13, state[MAP(0,i)]) ^ MUL( 9, state[MAP(1,i)]) ^ MUL(14, state[MAP(2,i)]) ^ MUL(11, state[MAP(3,i)]);
    new_state[3] = MUL(11, state[MAP(0,i)]) ^ MUL(13, state[MAP(1,i)]) ^ MUL( 9, state[MAP(2,i)]) ^ MUL(14, state[MAP(3,i)]);

    state[MAP(0,i)] = new_state[0];
    state[MAP(1,i)] = new_state[1];
    state[MAP(2,i)] = new_state[2];
    state[MAP(3,i)] = new_state[3];
  }
}

void aes_AddRoundKey(uint8_t state[16], uint8_t sub_key[16])
{
#ifdef OPTIMISE_8_BIT

  counter i = 16;

  while (i--) {
    state[i] ^= sub_key[i];
  }

#else

  counter i = 4;

  while (i--) {
    ((uint32_t *) state)[i] ^= ((uint32_t *) sub_key)[i];
  }

#endif
}

// Maths Operation Implementations

uint8_t aes_GaloisFieldMultiply(uint8_t fixed, uint8_t variable)
{
  uint8_t result = 0;

  while (fixed) {
    result ^= variable & ((fixed & 0x01) * 0xFF);
    variable = MUL2(variable);
    fixed >>= 1;
  }

  return result;
}

void print_hexstring(uint8_t *st) {
    for (int i = 0; i < 16; i++) {
        printf("%02x", st[i]);
    }
}

int hex2bytes(char hex[32], uint8_t out[16]) {
    for (int i = 0; i < 32; i += 2) {
        uint8_t hi = 255;
        if (hex[i] == '\n' || hex[i] == 0) {
            puts("Need a hex string of 16 bytes");
            return -1;
        }

        if (hex[i] >= '0' && hex[i] <= '9') {
            hi = hex[i] - '0';
        }
        if (hex[i] >= 'a' && hex[i] <= 'f') {
            hi = 10 + hex[i] - 'a';
        }
        if (hi == 255) {
            printf("Invalid hex character %c\n", hex[i]);
            return -1;
        }

        if (hex[i+1] == '\n' || hex[i+1] == 0) {
            puts("Need a hex string of 16 bytes");
            return -1;
        }

        uint8_t lo = 255;
        if (hex[i+1] >= '0' && hex[i+1] <= '9') {
            lo = hex[i+1] - '0';
        }
        if (hex[i+1] >= 'a' && hex[i+1] <= 'f') {
            lo = 10 + hex[i+1] - 'a';
        }
        if (lo == 255) {
            printf("Invalid hex character %c\n", hex[i+1]);
            return -1;
        }

        out[i/2] = lo + 16 * hi;
    }
    return 0;
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    uint8_t key[32];
    FILE *rand = fopen("/dev/urandom", "r");
    if (rand == NULL) {
        puts("No /dev/random");
        return 1;
    }
    fread(key, 32, 1, rand);
    fclose(rand);
    aes_256_context_t ctx;
    aes_256_init(&ctx, key);

    puts("** Welcome to NSAES, the non-backdoored© AES variant **");

    uint8_t flag[16];
    FILE *flagfd = fopen("flag.txt", "r");
    if (flagfd == NULL) {
        puts("No flag.txt");
        return 1;
    }
    fread(flag, 16, 1, flagfd);
    fclose(flagfd);
    aes_256_encrypt(&ctx, flag);
    puts("Here is the encrypted flag. Good luck decrypting it!");
    print_hexstring(flag);
    printf("\n");


    while (1) {
        puts("Please enter a string to be encrypted");

        char msg_hex[64];
        if (fgets(msg_hex, 64, stdin) == 0) {
            return 0;
        }

        uint8_t msg[16];
        if (hex2bytes(msg_hex, msg) != 0) {
            return 1;
        }
        aes_256_encrypt(&ctx, msg);
        printf("Here is your encrypted string: ");
        print_hexstring(msg);
        printf("\n");
    }
}
