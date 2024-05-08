#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <string.h>

struct condement {
    char *name;
    int amount;
};

struct hummus {
    float volume;
    struct condement *condements;
    _Bool is_bitter;
};

void welcome() {
    setvbuf(stdout, NULL, _IONBF, 0); // Disable output buffering
    setvbuf(stdin, NULL, _IONBF, 0); // Disable input buffering

    puts("Oh no my hummus turned bitter!");
    puts("Please help me make it un-bitter, i'll let you flip the bit of the bitterness of the hummus");
}

void print_hummus(struct hummus mummus) {
    puts("Hummus:");
    printf("\t%foz hummus\n", mummus.volume);
    struct condement *p = mummus.condements;

    while (p->name) {
        printf("\tCondement %s\n", p->name);
        printf("\t\tAmount: %d pieces\n", p->amount);
        p++;
    }

    printf("\thummus is %sbitter\n", mummus.is_bitter ? "" : "not ");
}

void flip_hummus(struct hummus *mummus) {
    int pos = 0;
    printf("position to flip: ");
    scanf("%d", &pos);

    *(((char *)mummus) + pos / CHAR_BIT) ^= (1 << (pos % CHAR_BIT));
}

int main() {
    welcome();

    struct condement condements[4] = {
        {.name = strdup("apple sauce"), .amount = 3},
        {.name = strdup("beef jerky"), .amount = 6},
        {.name = strdup("ketchup"), .amount = 2},
    };

    char mummus[] = "echo Thank you for making my hummus mummus again!";

    struct hummus my_bitter_hummus = {
        .volume = 4,
        .condements = condements,
        .is_bitter = 1,
    };

    while (my_bitter_hummus.is_bitter) {
        print_hummus(my_bitter_hummus);
        flip_hummus(&my_bitter_hummus);
    }

    system(mummus);
}
