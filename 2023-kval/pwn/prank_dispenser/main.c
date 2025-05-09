#include <stdbool.h>
#include <stdio.h>

#include "flag.h"

int main() {
    struct {
        char password[256];
        bool is_admin;
    } user;

    user.is_admin = false;

    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    puts("Skriv in admin lösenordet:");
    gets(user.password);

    if (user.is_admin) {
        puts("Uhh, jag vet inte hur du kom in hit men här har du flaggan");
        puts(flag);
    } else {
        puts("Haha prank, det finns inget korrekt lösenord");
    }

    return 0;
}
