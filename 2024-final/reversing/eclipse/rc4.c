#include "rc4.h"

static void swap(uint8_t *a, uint8_t *b) {
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

int rc4_init(uint8_t *rc4_state, uint8_t *key, size_t keylen) {
    int j = 0;
    for(int i = 0; i < RC4_N; i++) {
        rc4_state[i] = i;
    }

    for(int i = 0; i < RC4_N; i++) {
        j = (j + rc4_state[i] + key[i % keylen]) % RC4_N;

        swap(&rc4_state[i], &rc4_state[j]);
    }

    return 0;
}

int rc4_crypt(uint8_t *rc4_state, uint8_t *inbuf, uint8_t *outbuf, size_t len) {

    int i = 0;
    int j = 0;

    for(size_t n = 0; n < len; n++) {
        i = (i + 1) % RC4_N;
        j = (j + rc4_state[i]) % RC4_N;

        swap(&rc4_state[i], &rc4_state[j]);
        int rnd = rc4_state[(rc4_state[i] + rc4_state[j]) % RC4_N];

        outbuf[n] = rnd ^ inbuf[n];
    }

    return 0;
}
