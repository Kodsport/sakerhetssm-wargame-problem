#include <stdio.h>
#include <unistd.h>

int main(int argc, char** argv) {
    setuid(geteuid());
    setgid(getegid());
    execve(argv[1], argv + 1, NULL);
}
