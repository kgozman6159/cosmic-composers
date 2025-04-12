import numpy as np
import pretty_midi
from midi2audio import FluidSynth
import os
import sys

"""
INPUTS: 
- wavelengths array
- intensities array
- desired output path for .wav file
- path for fluidsynth file (to make use of instruments)

OUTPUT:
- returns nothing
- generates .wav file (path is printed in terminal)

SETUP:
- install dependencies in requirements.txt file
- manually install fluidsynth
    brew install fluidsynth (mac)
    sudo apt-get install fluidsynth
    (download separately for windows)
- open folder to get FluidR3_GM.sf2 file
- pass path to file as input
"""

def sonify_spectrum(wavelengths, intensities, wav_output_path="spectrum.wav", soundfont_path="FluidR3_GM.sf2"):
    # Normalize intensities to [0, 1]
    intensities = intensities / np.max(intensities)

    # Map intensity to velocity (volume)
    def intensity_to_velocity(i):
        return int(np.interp(i, [0, 1], [30, 127]))  # Avoid velocity = 0

    # Create PrettyMIDI object
    pm = pretty_midi.PrettyMIDI()

    # Create instruments for different intensity levels
    instruments = {
        'bells': pretty_midi.Instrument(program=10),     # Glockenspiel for low intensities
        'flute': pretty_midi.Instrument(program=73),     # Flute for moderate intensities
        'violin': pretty_midi.Instrument(program=40),    # Violin for moderate-high intensities
        'cello': pretty_midi.Instrument(program=42),     # Cello for high intensities
        'bass': pretty_midi.Instrument(program=32),      # Bass for very high intensities
    }

    # Function to choose instrument based on intensity
    def choose_instrument(i):
        if i < 0.2:
            return instruments['bells']
        elif i < 0.4:
            return instruments['flute']
        elif i < 0.6:
            return instruments['violin']
        elif i < 0.8:
            return instruments['cello']
        else:
            return instruments['bass']

    # Time per note
    note_duration = 0.2
    current_time = 0.0

    # Create notes based on intensity and wavelength
    for w, i in zip(wavelengths, intensities):
        pitch = int(np.interp(w, [min(wavelengths), max(wavelengths)], [40, 100]))
        velocity = intensity_to_velocity(i)
        instrument = choose_instrument(i)
        note = pretty_midi.Note(
            velocity=velocity,
            pitch=pitch,
            start=current_time,
            end=current_time + note_duration
        )
        instrument.notes.append(note)
        current_time += note_duration

    # Add instruments to the MIDI object
    for inst in instruments.values():
        if inst.notes:  # only add instruments that have notes
            pm.instruments.append(inst)

    # Save MIDI file temporarily
    midi_filename = "temp_spectrum.mid"
    pm.write(midi_filename)

    # Convert MIDI to WAV using FluidSynth
    fs = FluidSynth(soundfont_path)
    fs.midi_to_audio(midi_filename, wav_output_path)

    print(f"🎶 Sonification complete. WAV saved at: {wav_output_path}")


"""
INPUTS:
- program number: number from 0-127 which maps to a MIDI instrument
- soundfont_path: path to FluidR3_GM.sf2 file
- out_dir: directory to store output

OUTPUT:
- returns nothing
- creates .wav file of simple 5-note scale played with specified instrument
- file stored in specified output directory
"""
def play_instrument(program_number, soundfont_path="FluidR3_GM.sf2", out_dir="preview"):
    os.makedirs(out_dir, exist_ok=True)

    if not (0 <= program_number <= 127):
        raise ValueError("Instrument number must be between 0 and 127.")

    # Create MIDI object
    pm = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=program_number)

    # Simple 5-note scale (C D E F G)
    start_time = 0.0
    for i in range(5):
        pitch = 60 + i  # C major scale starting at middle C
        note = pretty_midi.Note(velocity=100, pitch=pitch, start=start_time, end=start_time + 0.5)
        instrument.notes.append(note)
        start_time += 0.5

    pm.instruments.append(instrument)

    # Save MIDI
    midi_path = "temp_preview.mid"
    pm.write(midi_path)

    # WAV path
    output_wav = os.path.join(out_dir, 'instr')
    output_wav += str(program_number) + '.wav'

    # Convert to WAV
    fs = FluidSynth(soundfont_path)
    fs.midi_to_audio(midi_path, output_wav)

    print(f"✅ Instrument {program_number} preview saved to {output_wav}")


# CODE TO SONIFY SPECTRUM
# wavelengths = np.linspace(300, 900, 100)
# intensities = np.random.rand(100) * 100
# sonify_spectrum(wavelengths, intensities, "spectrum1.wav")

# CODE TO GENERATE PREVIEWS for all 0-127 instruments
# for i in range(128):
#     play_instrument(i)