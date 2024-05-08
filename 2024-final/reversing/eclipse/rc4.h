#include <stdint.h>
#include <stddef.h>

#define RC4_N 256 // 2^8

int rc4_init(uint8_t *rc4_state, uint8_t *key, size_t keylen);
int rc4_crypt(uint8_t *rc4_state, uint8_t *inbuf, uint8_t *outbuf, size_t len);
