import numpy as np
import matplotlib.pyplot as plt
import lime
from sonify import sonify_spectrum_to_wav, remove_trailing_silence_from_wav
import numpy as np


def get_spaxel_spectra(filename, x, y, plot=True):
    
    cube = lime.Cube.from_file(filename, instrument='manga')
    
    rest_wav = cube.wave_rest.data

    spec = cube.get_spectrum(x, y)
    spec.infer.components()

    # Define classification indices
    continuum_inds = np.array([0, 1, 2, 10])
    emission_inds = np.array([3, 6, 7, 8])
    absorption_inds = np.array([9, 11])
    cosmic_ray_inds = np.array([4, 5])

    # Get indices for each type
    cont = np.where(np.isin(spec.infer.pred_arr, continuum_inds))
    em = np.where(np.isin(spec.infer.pred_arr, emission_inds))
    absr = np.where(np.isin(spec.infer.pred_arr, absorption_inds))
    cr = np.where(np.isin(spec.infer.pred_arr, cosmic_ray_inds))

    # Full flux array
    flux = spec.flux.data

    # Initialize all component arrays with zeros
    continuum = np.zeros_like(flux)
    emission = np.zeros_like(flux)
    absorption = np.zeros_like(flux)
    cosmic_ray = np.zeros_like(flux)

    # Fill values at matched indices
    continuum[cont] = flux[cont]
    emission[em] = flux[em]
    absorption[absr] = flux[absr]
    cosmic_ray[cr] = flux[cr]

    # Get wavelengths for dot plotting
    cont_wav = rest_wav[cont]
    em_wav = rest_wav[em]
    absr_wav = rest_wav[absr]
    cr_wav = rest_wav[cr]

    # print(f"Length of rest_wav: {len(rest_wav)}")
    # print(f"Length of flux: {len(flux)}")
    # print(f"Length of continuum: {len(continuum)}")
    # print(f"Length of emission: {len(emission)}")
    # print(f"Length of absorption: {len(absorption)}")
    # print(f"Length of cosmic_ray: {len(cosmic_ray)}")
    # print(f"Length of cont_wav (nonzero): {len(cont_wav)}")
    # print(f"Length of em_wav (nonzero): {len(em_wav)}")
    # print(f"Length of absr_wav (nonzero): {len(absr_wav)}")
    # print(f"Length of cr_wav (nonzero): {len(cr_wav)}")
    # print()
    # print("First 10 values:")
    # print("rest_wav     :", rest_wav[:10])
    # print("flux         :", flux[:10])
    # print("continuum    :", continuum[:10])
    # print("emission     :", emission[:10])
    # print("absorption   :", absorption[:10])
    # print("cosmic_ray   :", cosmic_ray[:10])
    # print("cont wav     :", cont_wav[:10])
    # print("emi wav      :", em_wav[:10])
    # print("abs wav      :", absr_wav[:10])
    # print("cr wav       :", cr_wav[:10])

    if plot:
        plt.figure(figsize=(12, 8))
        plt.plot(rest_wav, flux, color='black', label='Observed')
        plt.plot(cont_wav, continuum[cont], ".", color='blue', label='Continuum')
        plt.plot(em_wav, emission[em], ".", color='red', label='Emission')
        plt.plot(absr_wav, absorption[absr], ".", color='green', label='Absorption')
        plt.plot(cr_wav, cosmic_ray[cr], ".", color='orange', label='Cosmic Ray')
        plt.xlabel('Wavelength (Angstroms)')
        plt.ylabel('Flux (1e-17 FLAM)')
        plt.legend()
        plt.title(f'Spectrum at x={x}, y={y}')
        plt.show()

    return rest_wav, flux, continuum, emission, absorption, cosmic_ray


# Run the function
rest_wav, flux, continuum, emission, absorption, cosmic_rays = get_spaxel_spectra("/Users/tabby/Downloads/cubes/manga-7443-12703-LOGCUBE.fits", 40, 40)

sonify_spectrum_to_wav(rest_wav, continuum, emission, absorption, cosmic_rays, wav_path="sound.wav")
remove_trailing_silence_from_wav("sound.wav")