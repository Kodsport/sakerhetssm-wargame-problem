
flag.enc: challenge flag.txt
	./challenge < flag.txt > flag.enc

challenge: challenge.cpp parameters.cpp
	clang++ -march=native -s -O3 -Wall -Wpedantic -o $@ $^

challenge-dbg: challenge.cpp parameters.cpp
	clang++ -march=native -g -DDEBUG -Wall -Wpedantic -o $@ $^

parameters.cpp: generate.py
	python3 $< 5934237f5fa068b1353fff0149ba2b2f > $@

test: challenge
	echo "AAAA" | ./challenge | xxd
	echo "BBBB" | ./challenge | xxd

debug: challenge-dbg
	echo -n "AAAAAAAAAAAAAAAA" | ./challenge-dbg | xxd

clean:
	rm -f challenge

.PHONY: test clean debug
