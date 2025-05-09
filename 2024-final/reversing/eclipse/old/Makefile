default: challenge

%.o: %.c
	gcc -c -fPIC -o $@ $^

%.dat: %.o
	objcopy -O binary --only-section=.text $< $@

%.dat.enc: encrypt-section.py %.dat 
	python3 $^ > $@

%.enc.o: %.dat.enc %.o
	objcopy --update-section '.text=$<' $(word 2, $^) $@ 

challenge: part1.enc.o part2.enc.o challenge.c
	gcc -o challenge -Wall $^

clean:
	rm -f *.enc *.dat *.o challenge

.PHONY: clean default
