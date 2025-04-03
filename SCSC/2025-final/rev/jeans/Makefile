
jeans: challenge.c elk.o scripts.c scripts.h
	gcc -O2 -s -o $@ -Wall -Wpedantic $^ -lm

jeans-dbg: challenge.c elk.o scripts.c scripts.h
	gcc -o $@ -Wall -Wpedantic $^ -DDEBUG -lm

elk.o: elk.c
	gcc -c -O2 -o $@ $^

elk.c elk.h: elk
	cp elk/elk.c elk/elk.h .

elk:
	git clone https://github.com/cesanta/elk.git

scripts.h scripts.c: generate.py
	python3 generate.py 'SNHT{js_c_js_c_js_c_js_c_js_dot_dot_dot}'

clean:
	rm -f jeans jeans-dbg elk.o scripts.c scripts.h

.PHONY: clean
