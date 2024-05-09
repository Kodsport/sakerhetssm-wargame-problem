#!/usr/bin/env python3
import random
import maidenhead as mh
font = {
    "A": (""" .. 
.  .
.  .
....
.  .""", 4),
    "E": (""" ...
.   
... 
.   
 ...""", 4),
    "S": (""" ...
.   
 .. 
   .
... """, 4),
    "M": (""" . . 
. . .
. . .
.   .
.   .""", 5),
    "{": ("""  .
 . 
.. 
 . 
  .""", 3),
    "Q": (""" ..  
.  . 
.  . 
.  . 
 .. .""", 5),
    "C": (""" .. 
.  .
.   
.  .
 .. """, 4),
    "?": ("""...
  .
 . 
   
 . """, 3),
    "_": ("""   
   

   
...""", 3),
    "N": (""".  .
.  .
.. .
. ..
.  .""", 4),
    "O": (""" .. 
.  .
.  .
.  .
 .. """, 4),
    "I": ("""...
 . 
 . 
 . 
...""", 3),
    "T": ("""...
 . 
 . 
 . 
 . """, 3),
    "P": (""" .. 
.  .
... 
.   
.   """, 4),
    "}": (""".  
 . 
 ..
 . 
.  """, 3)
}

#print("name,latitude,longitude")
start_lat  = 55.45852159039501 # y
start_long = 15.38706895099124 # x
pix_size = 0.1

flag = "SSM{QSC?_NO_I_AM_TEAPOT}"
output = []
for (i, c) in enumerate(flag):
    dots, w = font[c]
    dots = dots.split("\n")
    for (y, row) in enumerate(dots):
        for (x, pix) in enumerate(row):
            if pix == ".":
                name = "%d_%d_%d" % (i, y, x)
                lat = start_lat + x*pix_size
                lon = start_long + y*pix_size
                #print("%s,%f,%f" % (name, lat, lon))
                output.append(mh.to_maiden(lat=lat, lon=lon, precision=4))
    start_lat += (w + 1)*pix_size

random.seed(1337)
random.shuffle(output)
print("\n".join(output))
