// Written by: ripSquid
#include <stdio.h>
#include <string.h>

#include "bencode.h"

// const char* flag =    "SNHT{kj3ll_k0d_4r_0cksa_3n_gr3j}";
/* Fake flag of the same length */
const char flag[33] = "SNHT{fake_fake_flag_really_fake}";

int main(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    parser_state state;
    state.index = 0;
    char buffer[1024];
    size_t total_size = 0;
    size_t bytes_read = 0;
    char* input = NULL;

    while ((bytes_read = fread(buffer, 1, sizeof(buffer), stdin)) > 0) {
        input = realloc(input, total_size + bytes_read + 1);
        if (input == NULL) {
            perror("Failed to allocate memory");
            return 1;
        }

        memcpy(input + total_size, buffer, bytes_read);
        total_size += bytes_read;
    }

    if (input == NULL) {
        printf("No input provided\n");
        return 1;
    }

    state.string = input;
    state.len = total_size;

    bencode* b = parse(&state);

    if (b != NULL) print_bencode(b);

    return 0;
}
