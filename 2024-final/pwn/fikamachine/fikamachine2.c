#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

struct item { int cost; char *name; int inuse; } *slot;
struct machine { struct item * items; int money; } machine;

int money = 10; // you're poor due to too much fika
int sold = 0;
int USER_MODE = 1;

char *get_str() {
    char buf[1024];
    fgets(buf, 1024, stdin);
    return strdup(buf);
}

int get_int() {
    return atoi(get_str());
}

struct item *get_item(char col, char row) {
    return &machine.items[(col - 'A') * 4 + row - '0'];
}

void machine_look() {
    _Bool something_on_line = 0;

    for (int i = 0, p = 0; i < 100; i++) {

        if (!machine.items[i].inuse) { p++; continue; }
        something_on_line = 1;
        printf("%*s%s: %d ", p * 10, "", machine.items[i].name, machine.items[i].cost);
        p = 0;
        if ((i + 1) % 4 == 0 && something_on_line) { puts(""); something_on_line = 0; }
    }

    puts("");
}

_Bool can_slot() { return !slot; }

void slot_put(struct item *i) {
    slot = i;
    slot->inuse = 0;
}

void slot_remove() {
    memset(slot, 0, sizeof(struct item));
    slot = NULL;
}

void buy(struct item *i) {
    if (!can_slot()) {
        puts("The slot is full!");
        return;
    }

    printf("You bought: Fika!\n");
    printf("You now have: %dSEK left\n", money -= i->cost);

    sold += i->cost;

    slot_put(i);
}

void poor(struct item *i) {
    printf("You do not have enough money for a %s, you need to take your fika consumption addiction seriously, you can't keep fikaing this much, it's not good for your health, man.\n", i->name);
}

void machine_enter() {
    printf("Option: ");
    char *s = get_str();
    struct item* i = get_item(s[0], s[1]);

    if (i->cost <= money)
        buy(i);
    else
        poor(i);
}

void machine_hit() {
    srand(time(NULL) + rand());
    if (rand() % rand() == 0) {
        puts("*KLONK*");
        slot_put(get_item('A' + rand() % 28, rand() % 28));
    }
}

void machine_get() {
    if (can_slot()) {
        puts("No item in slot");
        return;
    }
    printf("Nom nom eat eat nom fika so good\n");

    slot_remove();
}

void machine_put() {
    printf("Item name: ");
    char *name = get_str();
    
    printf("Item cost: ");
    int cost = get_int();

    for (int i = 0; i < 100; i++) {
        if (machine.items[i].name) continue;
        
        machine.items[i].name = name;
        machine.items[i].cost = cost;
        return;
    }
}

void machine_take() {
    money += sold;
    sold = 0;
}

void machine_shell() {
    system("/bin/sh");
}

int menu() {
    puts("USER MODE");
    puts("0. EXIT");
    puts("1. Look at machine");
    puts("2. Enter option on machine padkey");
    puts("3. Hit the stupid machine");
    puts("4. Get your hard earned fika");
    
    if (!USER_MODE) {
        puts("OPERATOR MODE");
        puts("5. Put item in machine");
        puts("6. Take money from machine");
        puts("7. Enter fika shell");
    }

    return get_int();
}

__attribute__((constructor)) void setflush() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
}

__attribute__((constructor)) void initmachine() {
    static struct item m[100];
    
    for (int i = 0; i < 4*6; i++)
        m[i] = (struct item) {.name = strdup("giffel"), .cost = 1, .inuse = 1};

    machine.items = m;
}

int main() {
    int option;
    while ((option = menu()) != 0) switch (option) {
        default: break;
        case 1: machine_look();  break;
        case 2: machine_enter(); break;
        case 3: machine_hit();   break;
        case 4: machine_get();   break;
        case 5: if(!USER_MODE) machine_put();   break;
        case 6: if(!USER_MODE) machine_take();  break;
        case 7: if(!USER_MODE) machine_shell(); break;
    }
}
