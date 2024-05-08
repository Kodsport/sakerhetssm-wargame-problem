elf: main.c Dockerfile
	docker build -t build .
	CONTAINER=$$(docker create build) && \
	docker cp $$CONTAINER:/build/elf . && \
	docker rm -v $$CONTAINER

clean:
	rm -f elf

.PHONY: clean
