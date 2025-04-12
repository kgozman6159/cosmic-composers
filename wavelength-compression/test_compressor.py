import numpy as np
import lime
from compressor import compress
import os
# Define the path to the FITS file relative to this test script
# Assumes the FITS file is in the same directory as the test script, 
# or adjust the path accordingly.
fits_file_path = 'manga-8626-12704-LOGCUBE.fits' 

def test_compression():
    """Tests the compress function.
    """
    print(f"--- Testing Wavelength Compression ---")
    
    if not os.path.exists(fits_file_path):
        print(f"Error: FITS file not found at {fits_file_path}")
        print("Please ensure the file exists and the path is correct.")
        return

    try:
        print(f"Loading cube from: {fits_file_path}...")
        # Load the cube
        # Note: Using instrument='manga' as in the original notebook
        cube = lime.Cube.from_file(fits_file_path, instrument='manga') 
        print("Cube loaded successfully.")
        print(f"Cube flux shape: {cube.flux.data.shape}")
        print(f"Cube wavelength shape: {cube.wave_rest.data.shape}")

        # Define test coordinates (ensure they are within the cube dimensions)
        # From the notebook, cube shape is likely (wavelength, 74, 74)
        # So valid y indices are 0-73, valid x indices are 0-73
        test_x = 30
        test_y = 25 
        print(f"\nTesting compression at coordinates (x={test_x}, y={test_y})...")

        # Call the compression function
        compressed_spectrum = compress(cube, test_x, test_y)
        
        print(f"\nCompressed spectrum at (x={test_x}, y={test_y}):")
        print(compressed_spectrum)
        
        # --- Basic Assertions/Checks ---
        expected_length = 9 # Based on the number of ranges in wavelength_ranges
        assert len(compressed_spectrum) == expected_length, \
            f"Expected output array length {expected_length}, but got {len(compressed_spectrum)}"
        print(f"\nCheck PASSED: Output array has the expected length ({expected_length}).")

        assert isinstance(compressed_spectrum, np.ndarray), \
            f"Expected output type numpy.ndarray, but got {type(compressed_spectrum)}"
        print(f"Check PASSED: Output type is numpy.ndarray.")
        
        # Check if all values are numeric (not NaN, though compress handles this)
        assert np.all(np.isfinite(compressed_spectrum)), \
            "Output array contains non-finite values (NaN or Inf)."
        print(f"Check PASSED: Output array contains only finite numeric values.")

    except FileNotFoundError:
        print(f"Error: FITS file not found during cube loading at {fits_file_path}")
    except ImportError:
        print("Error: 'lime' library not found. Please install it (pip install lime-astro)")
    except ValueError as ve:
        print(f"ValueError during compression: {ve}")
    except IndexError as ie:
         print(f"IndexError: Coordinates (x={test_x}, y={test_y}) might be out of bounds for cube shape {cube.flux.data.shape[1:]}. Error: {ie}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_compression() 