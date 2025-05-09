
all: flag-generator tester

tester: fib.c fib.h fib-ref.h fib-ref.c tester.c
	gcc -O1 -Wall -Wpedantic -o $@ $^

encryptor: encryptor.c fib-ref.h fib-ref.c
	gcc -O1 -Wall -Wpedantic -o $@ $^

test: tester
	./tester

flag.c: encryptor
	./encryptor "SSM{g0tt4_go_r33333l_f4zt!}" > flag.c

flag-generator: fib.c fib.h challenge.c flag.c flag.h
	gcc -O1 -Wall -Wpedantic -o $@ $^
	strip $@

clean:
	rm -f tester

.PHONY: clean test all
