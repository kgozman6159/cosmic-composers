# %%
from astropy.io import fits
import lime
from sonify import sonify_spectrum
from comp.compressor import compress
import fluidsynth
import os
import matplotlib.pyplot as plt

# %%
cube = lime.Cube.from_file('comp/manga-8626-12704-LOGCUBE.fits', instrument='manga')
# %%
while True:
    x_cord = int(input("Enter the x-coordinate: "))
    y_cord = int(input("Enter the y-coordinate: "))  
    intensities = compress(cube, x_cord, y_cord)

    plt.plot([i for i in range(len(intensities))], intensities)
    plt.show()
    
    try:
        sonify_spectrum([i for i in range(len(intensities))], intensities)
    except ValueError as e:
        print(f"Error: Invalid coordinates: {e}")
        continue

    # Play the generated sound file (macOS specific)
    os.system("afplay spectrum.wav")

# %%



