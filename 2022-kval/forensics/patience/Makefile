

patience.gif: frames.gif
	python3 adjust-timings.py frames.gif patience.gif 6

frames.gif: frames/*.png
	convert -delay 14099 -loop 0 frames/*.png frames/f1.png frames.gif

clean:
	rm -f frames.gif

.PHONY: clean
