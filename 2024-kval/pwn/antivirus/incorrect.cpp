#include <cstdio>

int main(){
    FILE* f = fopen("/flag", "r");
    char flag[1000];
    fgets(flag, 1000, f);
    printf("%s\n", flag);
}
