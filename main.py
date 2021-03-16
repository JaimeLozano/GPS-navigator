import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.io.img_tiles as cimgt
from position import Position

# Initialize the class
pos = Position()
    
# Create stamen terrain background instance
request = cimgt.GoogleTiles()
fig = plt.figure()

# Create a GeoAxes in hte tile's projection
m1 = fig.add_subplot(111, projection=request.crs)

# Wait for new position
x = 0
while not x:
    x = pos.updatePosition()

# Set map extent to +- 0.01º of the received position
m1.set_extent([pos.longitude + 0.01, pos.longitude - 0.01, pos.latitude + 0.01, pos.latitude - 0.01])

# Get image at desired zoom
m1.add_image(request, 14)

while True:
    # Wait for new position
    x = 0
    while not x:
        x = pos.updatePosition()
        
    # Print data on console
    pos.printData()
    
    # Plot the new position
    m1.plot(pos.longitude, pos.latitude, '.', transform=ccrs.Geodetic())
    plt.pause(0.1)