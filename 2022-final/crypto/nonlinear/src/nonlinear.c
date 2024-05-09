#include <stdio.h>
#include <stdlib.h>

size_t *seed = 0;

__attribute__((constructor))
static void seed_randomness() {
    seed = malloc(8);
    *seed = 0xdeadbeefcafebabe;
}

size_t generate_random() {
    *seed = *seed ** seed + (size_t) seed;
    return *seed;
}

void input_error() {
    puts("Error while reading input.");
    exit(1);
}

size_t *xor_encrypt(size_t *data, size_t key) {
    *data ^= key;
    return data;
}

void print_encrypted(size_t *data) {
    printf("Encrypted data: ");
    for (size_t i = 0; i < 8; i++) {
        printf("%lx", *xor_encrypt(&data[i], generate_random()));
    }
    puts("");
}

void encrypt() {
    char buf[128] = {0};
    printf("Data to encrypt: ");
    if (scanf("%65s", buf) != 1)
        input_error();
    
    print_encrypted((size_t *) buf);
}

void print_encrypted_flag() {
    char flag[128] = {0};
    FILE *fp = fopen("/home/ctf/flag.txt", "r");
    fread(flag, 1, 64, fp);
    fclose(fp);

    print_encrypted((size_t *) flag);
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    
    print_encrypted_flag();
    encrypt();
}