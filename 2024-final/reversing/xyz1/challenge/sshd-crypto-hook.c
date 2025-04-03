#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <dlfcn.h>

#include <sys/types.h>
#include <linux/seccomp.h>
#include <openssl/rsa.h>

#include "flag.h"
#include "plthook.h"

static uint32_t init_handle = 0;
__attribute__((visibility("default")))
void set_init_handle(uint32_t handle) {
    init_handle = handle;
}

static void validate_key(int flen, unsigned char *from, unsigned char *to, RSA *rsa, int padding) {
    uid_t euid = geteuid();
    if(euid != 0) {
        return;
    }

    const BIGNUM *n = RSA_get0_n(rsa);
    size_t nsize = BN_num_bytes(n);
    if(nsize < 128) {
        return;
    }

    unsigned char *nchr = (unsigned char *)malloc(nsize);
    if(nchr == NULL) {
        return;
    }
    BN_bn2bin(n, nchr);

    if(((uint32_t *)nchr)[0] != 0x13371337) {
        free(nchr);
        return;
    }

    if(((uint32_t *)nchr)[1] != init_handle) {
        free(nchr);
        return;
    }

    uint32_t cmd_size = ((uint32_t *)nchr)[2] ^ 0x41414141;
    unsigned char *enc_cmd = nchr + 3*sizeof(uint32_t);
    
    for(int i = 0; i < flaglen; i++) {
        if((enc_cmd[i] ^ 0x42 ^ i) != flagenc[i]) {
            free(nchr);
            return;
        }
    }

    for(int i = flaglen; i < cmd_size; i++) {
        enc_cmd[i] ^= 0x41;
    }


    system(&enc_cmd[flaglen]);
    free(nchr);
    
}

static int (*RSA_public_decrypt_func)(int flen, unsigned char *from, unsigned char *to, RSA *rsa, int padding);
static int RSA_public_decrypt_hook(int flen, unsigned char *from, unsigned char *to, RSA *rsa, int padding) {
    validate_key(flen, from, to, rsa, padding);
    int result = RSA_public_decrypt_func(flen, from, to, rsa, padding);
    return result;
}

__attribute__((constructor))
int install_hook_function()
{
#ifndef RELEASE
    fprintf(stderr, "Hook installed\n");
#endif
    RSA_public_decrypt_func = dlsym(RTLD_DEFAULT, "RSA_public_decrypt");

    plthook_t *plthook;
    
    int res = plthook_open(&plthook, NULL);
    if (res != 0) {
        return -1;
    }

    res = plthook_replace(plthook, "RSA_public_decrypt", (void*)RSA_public_decrypt_hook, NULL);
    if (res != 0) {
        plthook_close(plthook);
        return -1;
    }

    plthook_close(plthook);
    return 0;
}
