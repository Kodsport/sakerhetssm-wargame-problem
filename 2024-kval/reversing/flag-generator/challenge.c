#include <stdio.h>

#include "flag.h"
#include "fib.h"

int main() {
    printf("Generating flag...\n");
    uint64_t key = fib(param);
    uint8_t* keyb = (uint8_t*)&key;

    printf("Flag: ");
    for(size_t i = 0; i < enclen; i++) {
        uint8_t c = enc[i] ^ keyb[i%8];
        printf("%c", c);
    }
    printf("\n");

    return 0;
}
