
container: container/html/megahash.js
	docker build -t ssm_megahash container/

run: container
	docker run --rm -it -p8000:80 ssm_megahash:latest

container/html/megahash.js: *.tpl build.py *.sage
	python3 build.py

.PHONY: container run
