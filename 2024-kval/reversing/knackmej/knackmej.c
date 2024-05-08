#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>

#define TARGET_SIZE 68
char target_result[] = "\x1d\x1b\x1d\x1b\x1c\x48\x13\x13\x1c\x12\x13\x19\x12\x4b\x12\x19\x12\x49\x1d\x4e\x1d\x4c\x13\x1a\x1d\x4e\x12\x1c\x1d\x4c\x13\x1a\x1d\x4e\x13\x1b\x1d\x4c\x1d\x4e\x1d\x4c\x13\x18\x1d\x4e\x12\x4b\x12\x1d\x13\x18\x12\x19\x1d\x4e\x12\x13\x12\x49\x1d\x4c\x12\x1b\x12\x13\x13\x48";

void add(char *buf, int n, int key) {
    for(int i = 0; i < n; i++) {
        buf[i] = (char)(((int)buf[i] + key) & 0xff);
    }
}

void unhex(char *buf, char *out) {
    for(int i = 0; i < TARGET_SIZE/2; i++) {
        int val;
        sscanf(&buf[2*i], "%02x", &val);
        out[i] = (char)val;
    }
}

void banner() {
    puts("   *    *  ()   *   *");
    puts("*        * /\\         *");
    puts("      *   /i\\\\    *  *");
    puts("    *     o/\\\\  *      *");
    puts(" *       ///\\i\\    *");
    puts("     *   /*/o\\\\  *    *");
    puts("   *    /i//\\*\\      *");
    puts("        /o/*\\\\i\\   *");
    puts("  *    //i//o\\\\\\\\     *");
    puts("    * /*////\\\\\\\\i\\*");
    puts(" *    //o//i\\\\*\\\\\\   *");
    puts("   * /i///*/\\\\\\\\\\o\\   *");
    puts("  *    *   ||     *");
    puts("");
}

int main() {
    char input[256];
    char new_target[256];

    banner();
    printf("> ");
    fgets(input, 50, stdin);

    memfrob(target_result, TARGET_SIZE);
    unhex(target_result, new_target);

    add(input, strlen(input), 30);

    if (memcmp(input, new_target, TARGET_SIZE/2) == 0) {
        puts("Yay!");
    } else {
        puts("nej.");
    }
}
