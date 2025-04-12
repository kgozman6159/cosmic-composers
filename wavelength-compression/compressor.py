import numpy as np
# Optional: Import for type hinting if desired
# from lime import Cube

def compress(cube, x_coord: int, y_coord: int) -> np.ndarray:
    """
    Compresses the wavelength dimension of a FITS data cube at a specific 
    spatial coordinate by summing flux within predefined wavelength ranges.

    Args:
        cube: The input data cube (e.g., a lime.Cube object). 
              It must have wave_rest.data and flux.data attributes.
        x_coord: The x-coordinate of the pixel.
        y_coord: The y-coordinate of the pixel.

    Returns:
        A NumPy array containing the summed flux for each defined wavelength 
        range at the specified coordinate.
    """
    
    # Define the wavelength ranges (as used in the notebook)
    wavelength_ranges = {
        'h_alpha': (6540, 6580),
        'h_beta': (4040, 4080), 
        'h_gamma': (4340, 4380),
        'h_delta': (4860, 4900),
        'h_epsilon': (5000, 5040),
        'h_zeta': (5870, 5910),
        'h_eta': (6640, 6680),
        'zero_three': (4850, 5020), # Often referred to as [O III]
        's_two': (6700, 6750)      # Often referred to as [S II]
    }

    try:
        wavelength_array = cube.wave_rest.data
        flux_cube_array = cube.flux.data # Assumes shape (wavelength, y, x)
    except AttributeError as e:
        raise ValueError("Input 'cube' object must have 'wave_rest.data' and 'flux.data' attributes.") from e

    compressed_flux = []
    
    # Store range names in a fixed order to ensure consistent output array ordering
    # Using the order defined in the dictionary initially
    range_names_ordered = list(wavelength_ranges.keys()) 

    for name in range_names_ordered:
        wavelength = wavelength_ranges[name]
        start, end = wavelength
        
        # Find indices corresponding to the wavelength range
        idx1, idx2 = np.searchsorted(wavelength_array, [start, end])

        if idx1 >= idx2:
            # Handle cases where the range is empty or invalid in the data's wavelength array
            flux_sum_in_range = 0.0 
        else:
            # Extract the spectrum slice *at the specific coordinate* for this range
            # IMPORTANT: Cube data is often (wavelength, y, x)
            spectrum_slice_at_coord = flux_cube_array[idx1:idx2, y_coord, x_coord]
            
            # Sum the linear flux values within this slice
            flux_sum_in_range = np.sum(spectrum_slice_at_coord)
            
            # Handle potential NaN results if any flux values were NaN
            if np.isnan(flux_sum_in_range):
                flux_sum_in_range = 0.0 # Or choose another appropriate fill value

        compressed_flux.append(flux_sum_in_range)

    return np.array(compressed_flux)

# Example Usage (requires you to have loaded a 'cube' object first)
# if __name__ == '__main__':
#     # This part would typically be in another script or notebook
#     # where you load the cube
#     try:
#         import lime 
#         # Replace with your actual FITS file path
#         example_cube = lime.Cube.from_file('manga-8626-12704-LOGCUBE.fits', instrument='manga') 
        
#         # Choose coordinates
#         example_x = 37
#         example_y = 37
        
#         compressed_spectrum = compress(example_cube, example_x, example_y)
        
#         print(f"Compressed spectrum at ({example_x}, {example_y}):")
#         print(compressed_spectrum)
        
#         # Verify the length
#         print(f"Length of compressed spectrum: {len(compressed_spectrum)}") 
#         print(f"Expected length: {len(wavelength_ranges)}")

#         # You could plot this compressed spectrum if desired
#         # import matplotlib.pyplot as plt
#         # range_names = list(wavelength_ranges.keys()) # Get names in the same order
#         # plt.figure()
#         # plt.bar(range_names, compressed_spectrum)
#         # plt.title(f"Compressed Spectrum at ({example_x}, {example_y})")
#         # plt.ylabel("Summed Flux (Linear)")
#         # plt.xticks(rotation=45, ha='right')
#         # plt.tight_layout()
#         # plt.show()
        
#     except ImportError:
#         print("Skipping example usage: 'lime' library not found.")
#     except FileNotFoundError:
#         print("Skipping example usage: Example FITS file not found.")
#     except Exception as e:
#         print(f"An error occurred during example usage: {e}") 