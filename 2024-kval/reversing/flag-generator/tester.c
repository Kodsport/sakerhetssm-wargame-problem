#include <stdio.h>

#include "fib.h"
#include "fib-ref.h"

#define NUM_TESTS 30

int main() {
    for(size_t i = 0; i < NUM_TESTS; i++) {
        printf("N=%ld: ", i);
        uint64_t res_a = fib(i);
        uint64_t res_b = fib_ref(i);
        if(res_a != res_b) {
            printf("fail, %ld!=%ld\n", res_a, res_b);
            return 1;
        }
        printf("ok, res=%ld\n", res_a);
        
    }

    return 0;
}
