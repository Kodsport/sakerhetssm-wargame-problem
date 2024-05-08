#include <stdint.h>
#include <stddef.h>

int finish(void *prev, size_t prevlen, uint64_t prevkey);

void crypt_node(void *target, size_t len, uint64_t key);

void checkpoint(uint64_t value);
