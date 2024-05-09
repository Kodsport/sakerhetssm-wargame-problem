
all: docker

run: docker
	docker run --rm -it -p8080:80 ssm_congratulations:latest

build: build/index.html build/congratulations.js build/999999th-visitor-you-won.gif

build/index.html: src/index.html
	mkdir -p build
	cp src/index.html build/index.html

build/999999th-visitor-you-won.gif: src/999999th-visitor-you-won.gif
	mkdir -p build
	cp src/999999th-visitor-you-won.gif build/999999th-visitor-you-won.gif

build/congratulations.js: src/congratulations.js
	mkdir -p build
	python3 src/generate.py src/congratulations.js build/congratulations.js

docker: build
	docker build -t ssm_congratulations .

.PHONY: docker run all
