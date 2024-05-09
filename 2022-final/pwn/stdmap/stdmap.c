#include <sys/syscall.h>
#include <sys/mman.h>
#include <stdio.h>

#define do_syscall(nr, a, b, c, d, e, f, ...) ({\
    register long rax asm("rax") = (nr);\
    register long rdx asm("rdx") = (c);\
    register long r10 asm("r10") = (d);\
    register long r8 asm("r8") = (e);\
    register long r9 asm("r9") = (f);\
    asm volatile ("syscall\n\t": "=r" (rax):"r" (rdx), "r" (r10), "r" (r8), "r" (r9), "r" (rax), "D" (a), "S" (b):);\
    rax;\
})

#define SYSCALL(nr, ...) do_syscall(nr, __VA_ARGS__, 0, 0, 0, 0, 0, 0)

// every pwn ought to have a warm welcome!
void welcome() {
    puts("Welcome to std::map, we will map your input straight in to memory!");
    puts("No questions asked AND money back guarantee! Buy now for FREE!");
}

struct {} glob;

/* clang -no-pie -fno-stack-protector -O1 stdmap.c -o stdmap */


int main() {
    volatile size_t length = 0x1000;
    volatile size_t prot = PROT_READ | PROT_WRITE;
    volatile size_t syscall = SYS_mmap;

    struct {} stack;

    welcome();
    SYSCALL(syscall, (size_t)&glob &~ (length - 1), length, prot, MAP_FIXED | MAP_PRIVATE, 0);
    SYSCALL(syscall, (size_t)&stack &~ (0x1000 - 1), length, prot, MAP_FIXED | MAP_PRIVATE, 0);
}
