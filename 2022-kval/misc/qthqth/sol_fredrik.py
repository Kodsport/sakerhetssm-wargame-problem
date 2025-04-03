import maidenhead as mh
import matplotlib.pyplot as plt

lats = []
lons = []
with open("kluring.txt","r") as f:
    for c in f.readlines():
        lat, lon = mh.to_location(c)
        lats.append(lat)
        lons.append(-lon)

plt.scatter(lats,lons)
plt.show()

#SSM{QSC?_NO_I_AM_TEAPOT}