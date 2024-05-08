#include <dlfcn.h>
#include <stdio.h>

int main() {
    printf("Hello from main()");

    void* krb5 = dlopen("./libkrb5support-injected.so.0", RTLD_LAZY);
    dlclose(krb5);

    return 0;
}
