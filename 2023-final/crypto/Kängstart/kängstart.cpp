#include <bits/stdc++.h>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <wmmintrin.h>

#define PLEN 3*16

using u8x16 = uint8_t  __attribute__((vector_size(16)));
using u32x4 = uint32_t __attribute__((vector_size(16)));
using u64x2 = uint64_t __attribute__((vector_size(16)));

using v128 = union {
    __m128i mm;
    u8x16   u8;
    u32x4   u32;
    u64x2   u64;
};

void print_v128(v128 v) {
    for (int i = 0; i < 16; ++i) {
        printf("%02x", v.u8[i]);
    }
    puts("");
}
void print_v128x3(v128 v[3]) {
    for (int i = 0; i < 3; ++i) {
    //     for (int j = 0; j < 16; ++j) {
        for (int j = 15; j >= 0; --j) {
            printf("%02x", v[i].u8[j]);
        }
        puts("");
    }
    // puts("");
}

inline
v128 F(v128 k, v128 s) {
    v128 o;
    // o.u32 = k.u32 ^ s.u32; // easier debugging
    o.mm = _mm_aesenc_si128(k.mm, s.mm);
    return o;
}

void enc(v128 s[3]) {
    v128 t;
    for (int i = 0; i < PLEN; ++i) {
        t.u32 = s[1].u32 ^ s[2].u32;
        t = F(t, s[0]);
        s[0] = s[1];
        s[1] = s[2];
        s[2] = t;
    }
    t = s[0];
    s[0] = s[2];
    s[2] = t;
}

int main() {
    uint8_t flag[PLEN+1] = {0};
    const char* x = "SSM{fiestel_ciphers_are_their_own_inverse}";
    memcpy(flag, x, strlen(x) + 1);

    v128 a = {0}, b = {0}, c = {0};
    v128 s[3] = {a, b, c};
    uint8_t t[PLEN+1];
    for (int i = 0; i < PLEN; ++i) t[PLEN-1-i] = flag[i];
    memcpy(s, t, PLEN);

    std::cout << "input" << std::endl;
    print_v128x3(s);

    enc(s);

    std::cout << "output1" << std::endl;
    uint8_t encf[PLEN+1];
    memcpy(encf, s, PLEN);

    // copy into boot.asm
    for (int i = 0; i < PLEN; ++i) {
        printf("\tdb 0x%02x\n", encf[i]);
    }

    print_v128x3(s);

    enc(s);
    std::cout << "output2" << std::endl;
    print_v128x3(s);

}
