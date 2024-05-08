#include <string.h>
#include <stdint.h>
#include <stdio.h>

#include "fib-ref.h"

int main(int argc, char** argv, char** envp) {
    // Find largest fib that fits in a 64bit number
    uint64_t max = 0;
    uint64_t max_i = 0;
    for(size_t i = 0; ; i++) {
        uint64_t res = fib_ref(i);
        if(res >= max) {
            max = res;
            max_i = i;
        } else {
            break;
        }
    }
    fprintf(stderr, "Largest fib(%ld): %#lx\n", max_i, max);

    // Uncomment to test smaller key
    //max_i = 42;

    // Encrypt flag with max fib
    uint64_t key = fib_ref(max_i);
    fprintf(stderr, "Encrypting with fib(%ld): %#lx\n", max_i, key);
    uint8_t* keyb = (uint8_t*)&key;
    char* flag = argv[1];
    size_t flaglen = strlen(flag);

    printf("#include \"flag.h\"\n");
    printf("size_t param = %ld;\n", max_i);
    printf("size_t enclen = %ld;\n", flaglen);
    printf("uint8_t enc[%ld] = {\n", flaglen);
    for(size_t i = 0; i < flaglen; i++) {
        uint8_t c = flag[i] ^ keyb[i%8];
        printf("\t%#x,\n", c);
    }
    printf("};\n");

    return 0;
}
