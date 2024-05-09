#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#include "flag.h"

int main()
{
    srand(time(NULL));
    unsigned long long password = 1;
    unsigned long long input = 0;

    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    for (int i = 0; i < 5; i++)
        password *= rand();

    puts("Välkommen! Var vänlig mata in lösenordet.");

    scanf("%llu", &input);
    if (input == password)
    {
        printf("Grattis! Flaggan är: %s\n", flag);
        return 0;
    }
}
