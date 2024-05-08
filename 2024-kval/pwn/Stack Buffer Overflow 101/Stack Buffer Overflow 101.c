#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

// ANSI escape codes for colors
#define ANSI_COLOR_RED     "\x1b[31m"
#define ANSI_COLOR_GREEN   "\x1b[32m"
#define ANSI_COLOR_BLUE    "\x1b[34m"
#define ANSI_COLOR_RESET   "\x1b[0m"

// Function to generate colored hexdump
void colored_hexdump(void *data, size_t size, size_t buffer_start, size_t buffer_end, size_t return_address) {
    unsigned char *p = (unsigned char *)data;
    size_t i;

    for (i = 0; i < size; i++) {
        if (i >= return_address && i < buffer_end && i < return_address + 8) {
            printf("%s%02x%s ", ANSI_COLOR_RED, p[i], ANSI_COLOR_RESET); // Colorize overwritten return address
        }
        else if (i >= return_address && i < return_address + 8) {
            printf("%s%02x%s ", ANSI_COLOR_BLUE, p[i], ANSI_COLOR_RESET); // Colorize return address
        } else {
            printf("%s%02x%s ", (i >= buffer_start && i < buffer_end) ? ANSI_COLOR_GREEN : "", p[i], ANSI_COLOR_RESET);
        }
        if ((i + 1) % 16 == 0 || i == size - 1) {
            size_t j;
            // Print ASCII values
            printf("| ");
            for (j = i - (i % 16); j <= i; j++) {
                char c = p[j];
                if (c >= 32 && c < 127)
                    printf("%c", c); // Print printable characters
                else
                    printf("."); // Print '.' for non-printable characters
            }
            printf("\n");
        }
    }

    puts("");
}

char *command = "nope";

void set_command() {
    command = "/bin/sh";
}

void win() {
    system(command);
}

unsigned long long return_address;
size_t return_address_offset;
int nread;

void vuln() {
    char buffer[24];

    register long long rbp asm("rbp");
    return_address = (unsigned long long)__builtin_return_address(0);
    return_address_offset = rbp - (size_t) buffer + 8;

    printf("%p\n", return_address_offset);

    puts("Before:");

    colored_hexdump(buffer, 0x80, 0, 0, return_address_offset);

    nread = read(0, buffer, 0x80); // reading 0x80 bytes starting at pointer decayed at array called buffer with size 16.

    puts("\nAfter:");
    
    colored_hexdump(buffer, 0x80, 0, nread, return_address_offset);

    if (return_address != (unsigned long long)__builtin_return_address(0)) {
        printf("You overwrote part of the return address.\n");
        printf("Before: %p\n", return_address);
        printf("After:  %p\n", __builtin_return_address(0));

        printf("New return address points to:\n");
    }
    else {
        // Note that if you send a newline (enter) this will also count as a character.
        printf("You wrote %d characters, you are %d characters away from changing the return address.\n", nread, return_address_offset - nread + 1);
    }

    printf("Return address: %p\n", __builtin_return_address(0));
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0); // Disable output buffering
    setvbuf(stdin, NULL, _IONBF, 0); // Disable input buffering

    printf("Address of the function win(): %p\n", win);
    vuln();
}
