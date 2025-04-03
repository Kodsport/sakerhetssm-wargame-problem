#include <fcntl.h>
#include <sys/sendfile.h>
#include <stdio.h>

int main(int argc, char *argv[]) {
    int fd = open("/flag.txt", O_RDONLY);
    if (fd < 0) {
        printf("idk contact org?\n");
        return 1;
    }
    sendfile(1, fd, 0, 100);
}
