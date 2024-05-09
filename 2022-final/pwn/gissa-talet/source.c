#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

int main() {
    char number[8];
    char flag[48];
    char inp[64];

    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    srand(time(NULL));

    memset(number, 0, sizeof(number));

    FILE *flag_file = fopen("flag.txt", "r");
    fread(flag, 1, sizeof(flag), flag_file);
    fclose(flag_file);

    read_num:
    printf("Hur många siffror vill du gissa? ");
    int num_len;

    scanf("%i", &num_len);
    if (num_len < 0 || num_len > 8) {
        printf("Max 8 siffror!\n");
        goto read_num;
    }

    for (int i = 0; i < num_len; i++) {
        number[i] = '0' + rand() % 10;
    }

    while (1) {
        memset(inp, 0, sizeof(inp));

        printf("Du gissar: ");
        scanf("%64s", inp);

        int diff = strcmp(number, inp);
        if (diff == 0) {
            puts("Du vann!");
            break;
        } else if (diff < 0) {
            puts("För stort!");
        } else {
            puts("För litet!");
        }
    }
}
