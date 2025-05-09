#include <string.h>
#include <stdio.h>

char FLAG[] = {121, 121, 103, 81, 76, 88, 27, 25, 78, 7, 68, 26, 94, 7, 76, 88, 26, 72, 68, 27, 73, 30, 94, 25, 78, 87, 42};

int main() {
    memfrob(FLAG, sizeof(FLAG));
    strfry(FLAG, sizeof(FLAG));
    printf("onej jag råkade tappa flaggan och nu ligger den helt huller om buller: %s\n", FLAG);
}
