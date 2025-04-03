#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

const char whitelist[][16] = {"arch", "date", "id", "ls", "pwd", "true", "uname", "whoami"};

int main() {
    struct {
        char path[256];
        char command[256];
    } action;

    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    puts("Vad vill du köra?");
    gets(action.command);

    bool allowed = false;
    for (int i = 0; i < sizeof(whitelist) / sizeof(whitelist[0]); i++) {
        if (strcmp(action.command, whitelist[i]) == 0) {
            allowed = true;
        }
    }

    if (!allowed) {
        puts("Prank! du får inte köra det där");
        return 0;
    }

    puts("Vart vill du köra det?");
    gets(action.path);

    if (chdir(action.path) != 0) {
        puts("Onej det verkar inte gå");
        return 0;
    }

    system(action.command);

    return 0;
}
