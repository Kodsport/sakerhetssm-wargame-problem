#include <stdio.h>
#include <float.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>

typedef struct {
    float normal[3];
    float v1[3];
    float v2[3];
    float v3[3];
    uint16_t attr;
} STL_Vertex;

void binary_to_ascii(char *buf) {
    puts("solid ");

    while (strncmp(buf, "solid", 5) == 0) {
        buf += 5;
    }

    buf += 80;

    uint32_t nverts;
    memcpy(&nverts, buf, sizeof(nverts));
    buf += sizeof(nverts);
    if (nverts > 10000) {
        puts("Too many verts!");
        fflush(stdout);
        return;
    }

    for (int i = 0; i < nverts; i++) {
        STL_Vertex v;
        memcpy(&v, buf, 50);
        buf += 50;
        printf("facet normal %.*e %.*e %.*e\n", DECIMAL_DIG, v.normal[0], DECIMAL_DIG, v.normal[1], DECIMAL_DIG, v.normal[2]);
        printf("outer loop\n");
        printf("vertex %.*e %.*e %.*e\n", DECIMAL_DIG, v.v1[0], DECIMAL_DIG, v.v1[1], DECIMAL_DIG, v.v1[2]);
        printf("vertex %.*e %.*e %.*e\n", DECIMAL_DIG, v.v2[0], DECIMAL_DIG, v.v2[1], DECIMAL_DIG, v.v2[2]);
        printf("vertex %.*e %.*e %.*e\n", DECIMAL_DIG, v.v3[0], DECIMAL_DIG, v.v3[1], DECIMAL_DIG, v.v3[2]);
        printf("endloop\n");
        printf("endfacet\n");
    }
    puts("endsolid");
    fflush(stdout);

    return;
}

int main() {
    char flag[100] = {0};
    char buf[0x1000] = {0};

    puts("Welcome to the STL converter!");
    puts("Please paste a binary STL file, and we will convert it to a plain ASCII STL for you");
    puts("What is the length of your file in bytes?");
    fflush(stdout);

    char length_buf[10];
    fgets(length_buf, 10, stdin);
    int length = atoi(length_buf);
    if (length > 0x1000) {
        puts("Input too large");
    }

    FILE *flagf = fopen("flag.txt", "r");
    if (flagf != NULL) {
        fread(&flag, 52, 1, flagf);
        fclose(flagf);
    } else {
        puts("[warning] file not found");
        fflush(stdout);
    }

    fgets(buf, length, stdin);

    binary_to_ascii(buf);
}
