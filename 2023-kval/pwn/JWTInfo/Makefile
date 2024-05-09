all: clean
	gcc -g -o container/JWTInfo JWTInfo.c -Wl,-L,/usr/local/lib -ldl -lssl -lcrypto

.SILENT:
clean:
	-mkdir container
	-rm container/JWTInfo
