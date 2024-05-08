// The Swedish Post and Telecom Authority's dynamic information communication system.

#include <stdio.h>
#include <stdlib.h>

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

	char *line = NULL;
	size_t _;

	for (;;) {
		getline(&line, &_, stdin);
		printf(line);
	}
}
