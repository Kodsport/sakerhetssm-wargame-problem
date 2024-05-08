#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>

#define CMC_CALLBACKS

typedef struct {
    int type;
    size_t size;
    void *data;
} datapoint;

#define min(a, b) ((a)>(b)?(b):(a))

#define V datapoint
#define PFX db
#define SNAME datapoint_list
#define CMC_EXT_STR    // Enables an extra functionality (STR) of the list
#include "cmc/list.h"

#define V int
#define PFX res
#define SNAME int_list
#include "cmc/list.h"

#include "cmc/utl/futils.h"

datapoint *nil = & (datapoint) {.type = -1};

struct datapoint_list *database;
struct int_list *result;

bool print_datapoint(FILE *file, datapoint element) {
    return fprintf(file, "type: %d\tsize: %ld\tdata: %s\n", element.type, element.size, (char*)element.data) > 0;
}

void yield(bool (*query)(datapoint)) {
    res_clear(result);

    for (size_t i = 0; i < db_count(database); i++)
        if (query(db_get(database, i)))
            res_push_back(result, i);
}

int get_int(char *prompt) {
    char buf[8] = {0};
    printf("%s", prompt);
    fgets(buf, 8, stdin);
    return atoi(buf);
}

unsigned char *get_bytes(char *prompt, size_t size) {
    unsigned char *bytes = malloc(size);
    printf("%s", prompt);
    read(0, bytes, size);
    return bytes;
}

void add() {
    datapoint p = {.type = get_int("type: "), .size = get_int("size: ")};
    p.data = get_bytes("Data:", p.size);
    db_push_back(database, p);
    puts("");
}

void del() {
    size_t s = get_int("Select query size: ");
    unsigned char *b = get_bytes("Query: ", s);
    bool (*query)(datapoint) = mmap((void *)0xdead0000, s, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_SHARED | MAP_ANON, -1, 0);
    memcpy(query, b, s);
    
    yield(query);
    for (int i = 0; i < res_count(result); i++)
        db_pop_at(database, res_get(result, i));

    munmap((void *)0xdead0000, 0x1000);
}

void list() {
    db_print(database, stdout, "Elements:\n\t", "\t", "\n");
}

void search() {
    size_t s = get_int("Select query size: ");
    unsigned char *b = get_bytes("Query: ", s);
    bool (*query)(datapoint) = mmap((void *)0xdead0000, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_SHARED | MAP_ANON, -1, 0);
    memcpy(query, b, min(s, 0x1000));
    
    yield(query);
    for (int i = 0; i < res_count(result); i++)
        print_datapoint(stdout, db_get(database, res_get(result, i)));

    munmap((void *)0xdead0000, 0x1000);
}


int menu() {
    puts("1. Add item");
    puts("2. Delete item");
    puts("3. Search item");
    puts("4. List items");
    puts("5. Exit");

    return get_int("Option: ");
}

int main() {
	setvbuf(stdout, NULL, _IONBF, 0); // Disable output buffering
	setvbuf(stdin,  NULL, _IONBF, 0); // Disable input buffering

    database = db_new(100, &(struct datapoint_list_fval){.str = print_datapoint});
    result = res_new(100, &(struct int_list_fval){});

    while (1) {
        switch (menu()) {
            case 1:
                add(); break;
            case 2:
                del(); break;
            case 3:
                search(); break;
            case 4:
                list(); break;
            case 5:
                exit(0);
        }
    }
}

// _dl_start_user+60
