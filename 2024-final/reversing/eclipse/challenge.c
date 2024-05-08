#include <stdio.h>

#include "traversal.h"
#include "nodes/node0.h"

int main(int argc, char **argv, char **envp) {
    if(argc == 5) {
        printf("In memoriam Sophia \"quend\" d'Antoine\n");
        return 1337;
    }
    if(argc != 2) {
        printf("Usage: %s <password>\n", argv[0]);
        return 1;
    }
    node_0_pre(argv[1], NULL, 0, 0);
    return 0;
}
