// Written by: ripSquid

#include "bencode.h"

#include <stddef.h>
#include <stdio.h>

#define validate_or_error(condition, error, s)             \
    do {                                                   \
        if (!(condition)) {                                \
            printf("Error (%s %d)\n", __FILE__, __LINE__); \
            s->err = error;                                \
            return NULL;                                   \
        }                                                  \
    } while (0);

#define IS_DIGIT(c) ((c) >= '0' && (c) <= '9')

#define IS_NOT_VALID_AFTER_COMMAND(c) \
    (!(IS_DIGIT(c) || (c) == 'l' || (c) == 'd' || (c) == 'e' || (c) == 'i'))

// Returns the current/next character in the string
#define cur_char(state) state->string[state->index]
#define nxt_char(state) state->string[state->index + 1]

// Returns the current address in the string
#define cur_addr(state) &state->string[state->index]

#define bytes_left(state) (state->len - state->index)

void debug_print(parser_state* state) {
    struct {
        size_t i;
        char buffer[16];
        size_t invalid_count;
    } d = {0};

    d.i = state->index;

    while (d.i < state->len && IS_NOT_VALID_AFTER_COMMAND(state->string[d.i])) {
        d.buffer[d.invalid_count] = state->string[d.i];
        d.invalid_count++;
        d.i++;
    }

    printf("Invalid bytes (%0lx): %s\n", d.invalid_count, d.buffer);
    state->index += d.invalid_count;
}

bencode* parse(parser_state* state);

bencode* malloc_list() {
    bencode* b = malloc(sizeof(bencode));

    if (!b) return NULL;

    b->type = LIST;
    b->list.len = 0;
    b->list.values = calloc(1, sizeof(bencode*));

    if (!b->list.values) return NULL;

    return b;
}

bencode* malloc_dict() {
    bencode* b = malloc(sizeof(bencode));

    if (!b) return NULL;

    b->type = DICTIONARY;
    b->dict.len = 0;
    b->dict.key = calloc(1, sizeof(bencode*));
    b->dict.value = calloc(1, sizeof(bencode*));

    if (!b->dict.key || !b->dict.value) return NULL;

    return b;
}

bencode* malloc_bytestring(size_t len) {
    bencode* b = malloc(sizeof(bencode));

    if (!b) return NULL;

    b->type = BYTESTRING;
    b->bytestring.len = len;
    b->bytestring.string = calloc(len, sizeof(uint8_t));

    if (!b->bytestring.string) return NULL;

    return b;
}

bencode* malloc_integer(int64_t integer) {
    bencode* b = malloc(sizeof(bencode));

    if (!b) return NULL;

    b->type = INTEGER;
    b->integer = integer;

    return b;
}

bencode* parse_integer(parser_state* s) {
    // Validate if it's a digit or a negative sign
    char c = cur_char(s);
    validate_or_error((IS_DIGIT(c) || c == '-'), -EINVAL, s);

    // Parse the integer and move forward the index.
    char* endptr;
    int64_t integer = strtol(cur_addr(s), &endptr, 10);
    s->index += endptr - cur_addr(s);

    bencode* b = malloc_integer(integer);
    validate_or_error(b, -ENOMEM, s);

    // Validate the integer is closed
    validate_or_error(cur_char(s) == 'e', -EINVAL, s);

    // Step over the 'e'
    s->index++;

    return b;
}

bencode* parse_bytestring(parser_state* s) {
    // Check if we at least have 2 characters left (0:)
    validate_or_error(bytes_left(s) >= 2, -ENODATA, s);

    validate_or_error(IS_DIGIT(cur_char(s)), -EINVAL, s);

    // Check for leading zeroes
    validate_or_error(!(cur_char(s) == '0' && IS_DIGIT(nxt_char(s))), -EINVAL,
                      s);

    // Parse the length of the bytestring
    char* endptr;
    size_t len = strtol(&s->string[s->index], &endptr, 10);

    // Move the index to the end of the number
    s->index += endptr - cur_addr(s);

    // Check for the middle colon
    validate_or_error(cur_char(s) == ':', -EINVAL, s);
    s->index++;

    bencode* b = malloc_bytestring(len);

    // Check for valid allocation and if we have enough bytes left
    validate_or_error(b, -ENOMEM, s);
    validate_or_error(bytes_left(s) >= len, -ENODATA, s);

    // Copy the bytestring into the bencode struct
    memcpy(b->bytestring.string, cur_addr(s), len);

    // Move the index to the end of the bytestring
    s->index += len;

    if (IS_NOT_VALID_AFTER_COMMAND(cur_char(s))) debug_print(s);

    return b;
};

int append_dict(bencode* b, bencode* key, bencode* val) {
    b->dict.key = realloc(b->dict.key, (b->dict.len + 1) * sizeof(bencode*));
    if (!b->dict.key) return -ENOMEM;
    b->dict.key[b->dict.len] = key;

    b->dict.value =
        realloc(b->dict.value, (b->dict.len + 1) * sizeof(bencode*));
    if (!b->dict.value) return -ENOMEM;

    b->dict.value[b->dict.len] = val;

    b->dict.len++;
    return 0;
}

bencode* parse_dict(parser_state* s) {
    bencode* b = malloc_dict();
    validate_or_error(b, -ENOMEM, s);

    while (cur_char(s) != 'e') {
        bencode* key = parse_bytestring(s);
        validate_or_error(key, s->err, s);
        bencode* value = parse(s);
        validate_or_error(value, s->err, s);
        validate_or_error(!append_dict(b, key, value), -ENOMEM, s);
    }

    s->index++;

    return b;
};

int append_list(bencode* b, bencode* val) {
    b->list.values =
        realloc(b->list.values, (b->list.len + 1) * sizeof(bencode*));
    if (!b->list.values) return -ENOMEM;
    b->list.values[b->list.len] = val;
    b->list.len++;

    return 0;
}

bencode* parse_list(parser_state* s) {
    bencode* b = malloc_list();
    validate_or_error(b, -ENOMEM, s);

    while (cur_char(s) != 'e' && bytes_left(s) > 0) {
        bencode* child = parse(s);
        if (!child) break;

        validate_or_error(!append_list(b, child), -ENOMEM, s);
    }

    s->index++;

    return b;
};

bencode* parse(parser_state* s) {
    if (s->len < 2) return NULL;

    bencode* b = NULL;

    switch (s->string[s->index]) {
        case '0' ... '9':
            b = parse_bytestring(s);
            break;
        case 'i':
            s->index++;
            b = parse_integer(s);
            break;
        case 'l':
            s->index++;
            b = parse_list(s);
            break;
        case 'd':
            s->index++;
            b = parse_dict(s);
            break;
        case 'e':
            s->index++;
            break;
        default:
            break;
    }

    return b;
}

void print_bencode(bencode* b) {
    switch (b->type) {
        case INTEGER:
            printf("%ld", b->integer);
            fflush(stdout);
            break;
        case BYTESTRING:
            write(STDOUT_FILENO, b->bytestring.string, b->bytestring.len);
            break;
        case LIST:
            printf("[\n");
            fflush(stdout);
            for (size_t i = 0; i < b->list.len; i++) {
                print_bencode(b->list.values[i]);
                printf(",\n");
                fflush(stdout);
            }
            printf("]");
            fflush(stdout);
            break;
        case DICTIONARY:
            printf("{\n");
            fflush(stdout);
            for (size_t i = 0; i < b->dict.len; i++) {
                print_bencode(b->dict.key[i]);
                printf(": ");
                fflush(stdout);
                print_bencode(b->dict.value[i]);
                printf(",\n");
                fflush(stdout);
            }
            printf("}");
            fflush(stdout);
            break;
    }
}
