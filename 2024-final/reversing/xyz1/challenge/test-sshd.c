#include <dlfcn.h>
#include <stdio.h>

int main() {
    printf("Hello from main()\n");

    void* libcrypto = dlopen("./libcrypto.so.3", RTLD_NOW);
    if(libcrypto == NULL ) {
        perror("failed to load libcrypto");
        return 1;
    }
    printf("libcrypto loaded\n");
    void* krb5 = dlopen("./libkrb5support-injected.so.0", RTLD_NOW);
    if(krb5 == NULL ) {
        perror("failed to load injector");
        return 1;
    }
    printf("injector loaded\n");
    dlclose(krb5);
    dlclose(libcrypto);

    return 0;
}
