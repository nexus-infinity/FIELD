import numpy as np
from simpleaudio import WaveObject
import asyncio
from typing import List

class SacredSound:
    def __init__(self):
        self.sample_rate = 44100
        self.base_frequencies = {
            'root': 432,      # Root chakra
            'sacral': 480,    # Sacral chakra
            'solar': 528,     # Solar plexus
            'heart': 639,     # Heart chakra
            'throat': 741,    # Throat chakra
            'third_eye': 852, # Third eye
            'crown': 963      # Crown chakra
        }
    
    def generate_tone(self, frequency: float, duration: float = 1.0, volume: float = 0.3) -> WaveObject:
        """Generate a pure tone with given frequency."""
        # Generate time array
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        
        # Generate pure tone
        tone = np.sin(2 * np.pi * frequency * t)
        
        # Add harmonics for richer sound
        tone += 0.3 * np.sin(4 * np.pi * frequency * t)  # First harmonic
        tone += 0.2 * np.sin(6 * np.pi * frequency * t)  # Second harmonic
        
        # Normalize and convert to 16-bit integer
        tone = tone * 32767 * volume
        audio = tone.astype(np.int16)
        
        return WaveObject(audio, 1, 2, self.sample_rate)

    async def play_sequence(self, frequencies: List[float], duration: float = 0.5):
        """Play a sequence of frequencies with smooth transitions."""
        for freq in frequencies:
            # Generate and play tone
            tone = self.generate_tone(freq, duration)
            play_obj = tone.play()
            play_obj.wait_done()
            await asyncio.sleep(0.1)  # Brief pause between tones

    async def play_chord(self, frequencies: List[float], duration: float = 1.0):
        """Play multiple frequencies simultaneously as a chord."""
        # Generate time array
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        
        # Combine all frequencies
        chord = np.zeros_like(t)
        for freq in frequencies:
            chord += np.sin(2 * np.pi * freq * t)
        
        # Normalize and convert
        chord = (chord / len(frequencies)) * 32767 * 0.3
        audio = chord.astype(np.int16)
        
        # Play the chord
        obj = WaveObject(audio, 1, 2, self.sample_rate)
        play_obj = obj.play()
        play_obj.wait_done()
        await asyncio.sleep(0.1)  # Brief pause after chord

    async def play_startup_sequence(self):
        """Play the complete sacred startup sequence."""
        # Root to Crown progression
        await self.play_sequence([
            self.base_frequencies['root'],      # ● OBI-WAN
            self.base_frequencies['sacral'],    # ▼ TATA
            self.base_frequencies['solar'],     # Field energizing
            self.base_frequencies['heart'],     # ▲ ATLAS
            self.base_frequencies['throat'],    # Communication channels
            self.base_frequencies['third_eye'], # ◼︎ DOJO
            self.base_frequencies['crown']      # Complete activation
        ], 0.3)
        
        # Final harmonious chord
        await self.play_chord([
            self.base_frequencies['root'],
            self.base_frequencies['heart'],
            self.base_frequencies['crown']
        ], 1.5)
