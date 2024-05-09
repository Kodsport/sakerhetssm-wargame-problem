
docker:
	docker build -t ssm_fixarfrasse .

run:
	docker run --rm -it --privileged -p5001:5000 ssm_fixarfrasse:latest

dev:
	cd src && USE_SUDO=1 FLASK_ENV=development FLASK_APP=server.py python3 -m flask run

.PHONY: docker run dev
