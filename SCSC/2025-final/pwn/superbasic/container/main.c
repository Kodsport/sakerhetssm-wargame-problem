#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <assert.h>
#include "my_basic.h"

int basic_syscall(struct mb_interpreter_t *s, void **l) {
	int result = MB_FUNC_OK;

	mb_assert(s && l);

	mb_value_t nr = {.value = {.string = 0}};
	mb_value_t arg1 = {.value = {.string = 0}};
	mb_value_t arg2 = {.value = {.string = 0}};
	mb_value_t arg3 = {.value = {.string = 0}};

	mb_check(mb_attempt_open_bracket(s, l));

	mb_check(mb_pop_value(s, l, &nr));
	mb_check(mb_pop_value(s, l, &arg1));
	mb_check(mb_pop_value(s, l, &arg2));
	mb_check(mb_pop_value(s, l, &arg3));

	mb_check(mb_attempt_close_bracket(s, l));

	mb_check(mb_push_int(s, l, syscall((long long)nr.value.string, (long long)arg1.value.string, (long long)arg2.value.string, (long long)arg3.value.string)));
	
	return result;
}

int main() {
	char buf[1024] = {0};
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	
	puts(" -- SuperBASIC 2025 -- ");
	fgets(buf, sizeof buf, stdin);
	
	mb_init();
	struct mb_interpreter_t *bas = 0;
	mb_open(&bas);
	mb_register_func(bas, "syscall", basic_syscall);
	mb_load_string(bas, buf, true);
	mb_run(bas, true);
	mb_close(&bas);
	mb_dispose();
}
