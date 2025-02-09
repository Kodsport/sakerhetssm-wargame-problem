FLAG = 2020ctf{ganska_enkel_att_se_va}

all:
	cp main.c tempmain.c
	sed -i 's/REPLACE_FLAG/${FLAG}/' tempmain.c
	gcc -O2 tempmain.c -o chall
	rm tempmain.c

clean:
	rm -f tempmain.c
