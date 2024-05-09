all: clean nonlinear dist

nonlinear:
	gcc -g -o docker/files/nonlinear src/nonlinear.c

dist: nonlinear
	-cp docker/files/nonlinear dist/nonlinear
	-cp -r src dist/
	-cd dist && tar cfJ nonlinear.tar.xz * && rm -r src nonlinear

clean:
	-rm -f docker/files/nonlinear
	-rm -f dist/*