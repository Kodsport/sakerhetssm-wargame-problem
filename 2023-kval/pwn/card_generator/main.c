#include <stdio.h>
#include <string.h>

int main() {
    char name[64];
    char template_path[] = "./card_template.txt";
    char card[2048];

    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    puts("Skriv in ditt namn:");
    fgets(name, sizeof name, stdin);
    name[strlen(name) - 1] = 0;

    FILE *template = fopen(template_path, "r");
    fread(card, sizeof card, 1, template);
    memcpy(&card[1265], name, strlen(name));

    puts(card);

    return 0;
}
