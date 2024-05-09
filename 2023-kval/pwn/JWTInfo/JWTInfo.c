#define __GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <dlfcn.h>

#include <openssl/evp.h>

void banner() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    puts(
        "JSON Web Tokens are an open, industry standard RFC 7519 method for representing claims securely between two parties.\n"
        "JWTInfo allows you to decode, verify and (TODO) generate JWT.\n"
        "Warning: JWTs are credentials, which can grant access to resources.\nBe careful where you paste them! We do record tokens, all validation and debugging is done on the server side.\n"
    );
}

struct JWT {
    char *head;
    char *body;
    char *sign;
    _Bool signvalid;
};

char *get_jwt() {
    char *jwt = NULL;
    size_t size = 0;

    printf("Encoded: ");

    getline(&jwt, &size, stdin);
    
    return jwt;
}

char *base64_decode(char **output, char *input) {
    if (strlen(input) % 4 != 0) {
        char *new = malloc(strlen(input) + 3);
        strcpy(new, input);

        if (strlen(input) % 4 == 2) {
            strcat(new, "==");
        }
        else {
            strcat(new, "=");
        }

        input = new;
    }

    *output = calloc(3 * strlen(input) / 4 + 1, 1);
    EVP_DecodeBlock(*output, input, strlen(input));
    return *output;
}

char *get_json_field(char *json, char *key) {
    char *new_json = strdup(json);
    char *current_key = strtok(new_json, ":");

    while (strstr(current_key, key) == NULL) {
        strtok(NULL, ",");
        current_key = strtok(NULL, ":");
    }

    if (strstr(current_key, key)) {
        char *value = strdup(strtok(NULL, "\""));
        free(new_json);
        return value;
    }

    return NULL;
}

char *get_jwt_alg(struct JWT token) {
    return get_json_field(token.head, "alg");
}

_Bool validate_jwt(struct JWT token) {
    char *alg = get_jwt_alg(token);
    _Bool (*validate)(char *head, char *body, char *signature) = dlsym(dlopen(NULL, RTLD_LAZY), alg);

    if (validate) {
        printf("[INFO] Validating token with algorithm: %s\n", alg);
        return validate(token.head, token.body, token.sign);
    }

    printf("[INFO] Invalid or unsupported algorithm: %s\n", alg);

    return 0;
}

struct JWT parse_jwt_from_string(char *jwt) {
    struct JWT token = {
        .head = base64_decode(&token.head, strtok(jwt, ".")),
        .body = base64_decode(&token.body, strtok(NULL, ".")),
        .sign = strdup(strtok(NULL, ".")),
        .signvalid = validate_jwt(token)
    };

    return token;
}

void pretty_print_jwt(struct JWT token) {
    printf("[INFO] Decoded JWT:\n\n");
    printf("Head: %s\n", token.head);
    printf("Body: %s\n", token.body);
    printf("Signature: %s\n", token.sign);
    printf("Validity: %s\n", token.signvalid ? "true" : "false");
}

int main() {
    banner();
    char *jwt = get_jwt();
    struct JWT token = parse_jwt_from_string(jwt);
    pretty_print_jwt(token);
}
