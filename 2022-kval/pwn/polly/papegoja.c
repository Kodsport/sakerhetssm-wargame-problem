#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>

#include "flag.h"

#define PASSWORD_LEN 20

const char alphabet[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
char input[1000];

void polly() {
    puts("Tell Polly something");
    printf("> ");
    fflush(stdout);
    fgets(input, 1000, stdin);

    printf("                       \\\\   Polly says: ");
    printf(input);
    puts("  \\\\    \\\\    \\\\  bok  (o> /");
    puts("  (o>   (o>   (o> /    //\\");
    puts("__(()___(()___(()______V_/_____");
    puts("  ||    ||    ||       ||");
    puts("                       ||");
    fflush(stdout);
}

void unlock(char *real_password) {
    puts("Enter super secret password to unlock vault!");
    printf("> ");
    fflush(stdout);
    fgets(input, 1000, stdin);
    if (memcmp(real_password, input, PASSWORD_LEN) == 0) {
        printf("Correct! %s", FLAG);
        fflush(stdout);
        exit(0);
    } else {
        puts("Incorrect!");
        fflush(stdout);
    }
}

void generate_password(char *password) {
    int len = strlen(alphabet);
    for(int i = 0; i < PASSWORD_LEN; i++) {
        password[i] = alphabet[rand() % len];
    }
}

void secure_seeding() {
    // This is actually secure
    unsigned int seed;
    FILE *f = fopen("/dev/urandom", "r");
    fread(&seed, sizeof(unsigned int), 1, f);
    fclose(f);
    srand(seed);
}

void signal_handler(int signum) {
    puts("");
    puts("                       \\\\   Polly says: Too slow!");
    puts("  \\\\    \\\\    \\\\  bok  (o> /");
    puts("  (o>   (o>   (o> /    //\\");
    puts("__(()___(()___(()______V_/_____");
    puts("  ||    ||    ||       ||");
    puts("                       ||");
    exit(1);
}

int main() {
    char password[PASSWORD_LEN];
    secure_seeding();
    generate_password(password);

    alarm(5); // Gotta go fast!
    signal(SIGALRM, signal_handler);
    while(1) {
        puts("1. Speak to polly.");
        puts("2. Unlock.");
        puts("3. Exit.");
        printf("> ");
        fflush(stdout);

        fgets(input, 1000, stdin);
        int choice = atoi(input);
        if (choice == 1) {
            polly();
        } else if (choice == 2) {
            unlock(password);
        } else if (choice == 3) {
            return 0;
        } else {
            puts("Bad option!");
            fflush(stdout);
        }
    }
}
