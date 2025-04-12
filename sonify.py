import mido
from mido import Message, MidiFile, MidiTrack
import numpy as np
from midi2audio import FluidSynth
import matplotlib.pyplot as plt
# from pydub import AudioSegment

def sonify_spectrum_to_wav(
    wavelength,
    continuum,
    emission,
    absorption,
    cosmic_rays,
    midi_path="spectrum.mid",
    wav_path="spectrum.wav",
    soundfont_path="FluidR3_GM.sf2"
):
    # Normalize data
    def normalize(arr, out_min, out_max):
        arr_min, arr_max = min(arr), max(arr)
        return [int(out_min + (x - arr_min) / (arr_max - arr_min) * (out_max - out_min)) if arr_max != arr_min else out_min for x in arr]

    # Initialize MIDI
    mid = MidiFile()
    tempo = 50000  # microseconds per beat (120 BPM)

    # Continuum track (pad instrument for ambient sound)
    track_bg = MidiTrack()
    mid.tracks.append(track_bg)
    track_bg.append(mido.MetaMessage('set_tempo', tempo=tempo))
    track_bg.append(Message('program_change', program=90, channel=0))  # Pad 3 (polysynth)

    # Emission track (bright instrument with longer note durations)
    track_em = MidiTrack()
    mid.tracks.append(track_em)
    track_em.append(Message('program_change', program=73, channel=1))  # Choir (ambient-friendly)

    # Absorption track (synth pad instrument for deep, atmospheric sound)
    track_ab = MidiTrack()
    mid.tracks.append(track_ab)
    track_ab.append(Message('program_change', program=92, channel=2))  # String or Synth pad

    # Cosmic ray track (soft percussion with delayed pings)
    track_cosmic = MidiTrack()
    mid.tracks.append(track_cosmic)
    track_cosmic.append(Message('program_change', program=10, channel=3))  # Music Box

    # Normalize values to MIDI pitch (21–108)
    pitches_emission = normalize(emission, 50, 70)  # Emission (higher notes)
    pitches_absorption = normalize(absorption, 28, 50)  # Absorption (lower notes)
    velocities_bg = normalize(continuum, 40, 80)  # Background noise intensity
    velocities_cosmic = normalize(cosmic_rays, 80, 127)  # Cosmic rays (higher velocity for impact)

    # Note duration for smoother sound (longer duration for overlapping sounds)
    note_duration = 500  # 500ms (0.5 seconds)

    # Apply pitch bends for smoother transitions
    pitch_bend_range = 8191  # Maximum allowed pitch bend

    for i in range(len(wavelength)):
        time = i * 100  # milliseconds between notes

        # Background noise (if non-zero)
        if continuum[i] != 0:
            track_bg.append(Message('note_on', note=50, velocity=velocities_bg[i], time=0, channel=0))
            track_bg.append(Message('note_off', note=50, velocity=0, time=note_duration, channel=0))

        # Emission line (if non-zero)
        elif emission[i] != 0:
            track_em.append(Message('note_on', note=pitches_emission[i], velocity=70, time=0, channel=1))
            track_em.append(Message('pitchwheel', pitch=pitch_bend_range, time=0, channel=1))
            track_em.append(Message('note_off', note=pitches_emission[i], velocity=0, time=note_duration, channel=1))

        # Absorption line (if non-zero)
        elif absorption[i] != 0:
            track_ab.append(Message('note_on', note=pitches_absorption[i], velocity=100, time=0, channel=2))
            track_ab.append(Message('pitchwheel', pitch=pitch_bend_range, time=0, channel=2))
            track_ab.append(Message('note_off', note=pitches_absorption[i], velocity=0, time=note_duration, channel=2))

        # Cosmic ray spike (only if above threshold)
        elif cosmic_rays[i] != 0:
            velocity = velocities_cosmic[i] // 2
            note = 85
            delay = i * 100
            track_cosmic.append(Message('note_on', note=note, velocity=velocity, time=delay, channel=3))
            track_cosmic.append(Message('note_off', note=note, velocity=0, time=note_duration, channel=3))

    mid.save(midi_path)

    fs = FluidSynth(soundfont_path)
    fs.midi_to_audio(midi_path, wav_path)

    print(f"✅ Saved: {midi_path} and {wav_path}")



def remove_trailing_silence_from_wav(wav_path, silence_threshold=-40, chunk_size=10):
    """Remove trailing silence from a WAV file."""

    return 
    audio = AudioSegment.from_wav(wav_path)

    # Find where the sound ends by checking for silence
    start_trim = len(audio)  # Start with the entire audio
    for i in range(len(audio)-1, 0, -chunk_size):
        chunk = audio[i - chunk_size:i]
        if chunk.dBFS > silence_threshold:  # Check if the chunk is above the silence threshold
            start_trim = i
            break

    trimmed_audio = audio[:start_trim]
    trimmed_audio.export(f"{wav_path}", format="wav")
    print(f"Trimmed audio saved as '{wav_path}'")

# Example usage:
# remove_trailing_silence_from_wav("spectrum_sonification.wav")


# # test code
# n = 50
# # Simulated arrays based on more realistic patterns
# wavelength = np.linspace(400, 700, n)  # Wavelength from 400 nm to 700 nm (visible spectrum)

# # Background noise: Random fluctuation with a smooth trend
# continuum = np.random.normal(0.5, 0.1, n) + np.linspace(0.1, 0.8, n)

# # Emission lines: Sinusoidal peaks with random variability
# emission = np.zeros(n)
# emission[10:20] = np.sin(np.linspace(0, 2 * np.pi, 10)) ** 2  # Emission line in a section of the spectrum
# emission[30:40] = np.sin(np.linspace(0, 2 * np.pi, 10)) ** 2

# # Absorption lines: Cosine dips with a gradual change
# absorption = np.cos(np.linspace(0, 2 * np.pi, n)) ** 2

# # Cosmic rays: Sporadic spikes
# cosmic_rays = np.random.normal(0, 0.1, n)
# cosmic_rays[5] = 5  # Add a significant spike
# cosmic_rays[20] = 4  # Add another cosmic ray spike
# cosmic_rays[40] = 3  # Add another spike

# # Plot to visualize the arrays
# plt.figure(figsize=(10, 6))
# plt.plot(wavelength, continuum, label='Background Noise', color='gray', alpha=0.7)
# plt.plot(wavelength, emission, label='Emission Lines', color='blue', linewidth=2)
# plt.plot(wavelength, absorption, label='Absorption Lines', color='red', linewidth=2)
# plt.plot(wavelength, cosmic_rays, label='Cosmic Rays', color='green', marker='o', linestyle='--', alpha=0.8)
# plt.xlabel("Wavelength (nm)")
# plt.ylabel("Intensity")
# plt.title("Simulated Spectrum")
# plt.legend()
# plt.grid(True)
# plt.show()

# Save the sonified file
# sonify_spectrum_to_wav(wavelength, continuum, emission, absorption, cosmic_rays, wav_path="sound7.wav")
# remove_trailing_silence_from_wav("sound7.wav")
