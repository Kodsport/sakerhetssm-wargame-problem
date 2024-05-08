#include <stdio.h>
#include <string.h>

void banner() {
puts("      .-=-.");
puts("     /  .  \\");
puts("    |   |   |");
puts("    /  .-.  \\");
puts("   |  /   \\  |");
puts("   | |     | |     .-~~^^~-.");
puts("   | |     | |   .'          '.");
puts("    \\ \\   / /   /   O      O   \\");
puts("     '.___.'   |    .-~~^^~-.   |");
puts("      /   \\    |   /  C  3  D   |");
puts("     /   /     |   |    U       |");
puts("    /   /~      \\  |           |");
puts("   (~~~         |  \\         0 /");
puts("   /            |   '._     _.'");
puts("  |             |      ^^~~~");
puts("  |             |");
puts("  ---------------");
puts("                        Alien ASCII art by ChatGPT.");
puts("");
}

char password[] = "3xTr4t3rR35tr14l!!\n";

int main() {
      banner();
      puts("Human! Give us the password or prepare to be Space Invaded!");
      fflush(stdout);
      char pass[1024];
      fgets(pass, 64, stdin);
      if (strcmp(pass, password) == 0) {
            FILE *fptr = fopen("flag.txt", "r");
            char flag[64];
            fgets(flag, 64, fptr);
            puts("We will spare you! Here is our flag:");
            printf("%s", flag);
      }  else {
            puts("Zzzzzzapped!");
      }

}
