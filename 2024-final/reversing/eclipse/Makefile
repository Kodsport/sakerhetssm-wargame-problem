
default: challenge.enc.elf

FLAG = SSM{return_from_total_darkness}

nodes/*.c graph.dot flag.h flag.c: generate-graph.py
	python3 generate-graph.py "$(FLAG)"

%.dot.svg: %.dot
	dot -O -Tsvg $<

challenge.elf: challenge.c traversal.c flag.c rc4.c nodes/*.c
	gcc -O2 -Wall -o $@ -I. $^

challenge.enc.elf: encrypt-nodes.py challenge.elf
	python3 $^ $@
	chmod +x $@
	strip $@

clean:
	rm -rf challenge.elf challenge.enc.elf nodes/ flag.h flag.c

.PHONY: default clean
