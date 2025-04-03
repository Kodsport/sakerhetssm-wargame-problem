#include "fib-ref.h"

uint64_t fib_ref(uint64_t n) {
    uint64_t prev = 1;
    uint64_t res = 0;

    while(n-- > 0) {
        uint64_t tmp = res;
        res = prev + res;
        prev = tmp;
    }
    return res;
}
