#include "traversal.h"
#include "rc4.h"
#include "flag.h"

#include <sys/mman.h>
#include <unistd.h>
#include <stdio.h>

static uint64_t state = 0x1337133713371337;

int finish(void *prev, size_t prevlen, uint64_t prevkey) {
    crypt_node(prev, prevlen, prevkey);
    //printf("State: %#lx\n", state);

    uint8_t rc4_state[RC4_N];
    rc4_init(rc4_state, (uint8_t*)&state, sizeof(state));
    uint8_t decrypted[flaglen];
    rc4_crypt(rc4_state, flag, decrypted, flaglen);
    uint64_t *marker = (uint64_t *)&decrypted[0];
    if(*marker == 0x1337133713371337) {
        printf("Great work! Flag: ");
        fwrite(&decrypted[sizeof(uint64_t)], sizeof(char), flaglen-sizeof(uint64_t), stdout);
        printf("\n");
        return 1;
    } else {
        printf("Nope!\n");
        return 0;
    }
}

void crypt_node(void *target, size_t len, uint64_t key) {
    int pagesize = sysconf (_SC_PAGE_SIZE);
    void* align = (void*)(((uintptr_t)target) & ~(pagesize-1));
    size_t prefix = target - align;
    mprotect(align, prefix+len, PROT_READ | PROT_WRITE | PROT_EXEC);
    uint64_t keydata = key;
    uint8_t *keyptr = (uint8_t*)&keydata; 
    for(size_t i = 0; i < len; i++) {
        ((uint8_t*)target)[i] ^= keyptr[i%sizeof(key)];
    }
}

void checkpoint(uint64_t value) {
    //printf("State: %#lx, Adding: %#lx\n", state, value);
    state = (state * 0x1fffffffffffffff + value) % 0xffffffffffffffc5;
}
