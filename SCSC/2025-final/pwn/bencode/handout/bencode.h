// Written by: ripSquid

#ifndef BENCODE_H
#define BENCODE_H

#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>

typedef struct {
    char* string;
    size_t len;
    size_t index;
    int err;
} parser_state;

enum type { INTEGER, BYTESTRING, LIST, DICTIONARY };

typedef struct {
    struct bencode** key;
    struct bencode** value;
    size_t len;
} dict;

typedef struct {
    struct bencode** values;
    size_t len;
} list;

typedef struct {
    uint8_t* string;
    size_t len;
} bytestring;

typedef struct bencode {
    enum type type;
    union {
        int64_t integer;
        bytestring bytestring;
        list list;
        dict dict;
    };
} bencode;


bencode* parse(parser_state* state);
void print_bencode(bencode* b);

#endif
