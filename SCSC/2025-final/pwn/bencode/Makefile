CC=aarch64-linux-gnu-gcc

build:
	@echo "Building..."
	@cd web && go build -o ../web_serve ./cmd
	$(CC) -O0 -ggdb -fno-stack-protector -no-pie -o parse bin/main.c bin/bencode.c

build-web:
	@cd web && go build -o ../container/web_serve ./cmd

build-bin:
	@echo "Building..."
	$(CC) -O0 -ggdb -fno-stack-protector -no-pie -o parse bin/main.c bin/bencode.c

debug:
	rm -f solve/.gdb_history
	make build-bin
	cp -f parse solve/
	bash -c "docker run --rm -v ./solve:/solve -p8000:8000 -it $$(docker build -q .)"

run:
	@echo "Running..."
	@./web_serve
