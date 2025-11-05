#!/usr/bin/env python3
"""
Sonic Fraud Detection Audio Engine
Real-time audio feedback for financial transaction resonance

This module converts harmonic transaction analysis into audio alerts,
making fraud audible through dissonant chords and broken harmonies.
"""

import math
import time
import threading
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum

# Audio synthesis (lightweight, cross-platform)
try:
    import numpy as np
    import sounddevice as sd
    AUDIO_AVAILABLE = True
except ImportError:
    print("🔇 Audio libraries not available. Install: pip install numpy sounddevice")
    AUDIO_AVAILABLE = False

from harmonic_transaction_model import (
    HarmonicTransaction, 
    ResonanceStatus, 
    SACRED_FREQUENCIES,
    HarmonicTransactionAnalyzer
)

class SonicAlert(Enum):
    HARMONY = "harmony"          # Clean transaction - pleasant chord
    DISSONANCE = "dissonance"    # Review needed - minor discord
    TRITONE = "tritone"          # Fraud detected - devil's interval
    SILENCE = "silence"          # Missing transaction - ominous quiet
    CHAOS = "chaos"              # System attack - cacophony

@dataclass
class AudioWave:
    """Audio wave configuration"""
    frequency: float
    amplitude: float
    duration: float
    wave_type: str = "sine"      # sine, square, sawtooth, noise

class SonicFraudDetector:
    """Real-time audio feedback for transaction analysis"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.is_playing = False
        self.audio_thread = None
        self.volume = 0.3  # Safe default volume
        
        # Audio synthesis functions
        self.wave_generators = {
            'sine': self._generate_sine_wave,
            'square': self._generate_square_wave,  
            'sawtooth': self._generate_sawtooth_wave,
            'noise': self._generate_noise_wave
        }
        
    def play_transaction_audio(self, harmonic_tx: HarmonicTransaction):
        """Convert transaction into audio feedback"""
        
        if not AUDIO_AVAILABLE:
            self._print_audio_description(harmonic_tx)
            return
            
        # Determine sonic alert type
        alert_type = self._classify_sonic_alert(harmonic_tx)
        
        # Generate appropriate audio response
        audio_waves = self._create_audio_waves(harmonic_tx, alert_type)
        
        # Play the audio (non-blocking)
        self._play_waves_async(audio_waves)
        
        # Also print description for debugging
        self._print_audio_description(harmonic_tx, alert_type)
        
    def _classify_sonic_alert(self, harmonic_tx: HarmonicTransaction) -> SonicAlert:
        """Classify transaction into sonic alert category"""
        
        if harmonic_tx.fraud_probability > 0.7:
            return SonicAlert.TRITONE
        elif harmonic_tx.resonance_status == ResonanceStatus.HARMONIC:
            return SonicAlert.HARMONY
        elif harmonic_tx.resonance_status == ResonanceStatus.DISSONANT:
            return SonicAlert.DISSONANCE
        elif harmonic_tx.resonance_status == ResonanceStatus.MICROTONAL:
            return SonicAlert.TRITONE
        else:
            return SonicAlert.SILENCE
            
    def _create_audio_waves(self, harmonic_tx: HarmonicTransaction, 
                           alert_type: SonicAlert) -> List[AudioWave]:
        """Generate audio waves based on transaction and alert type"""
        
        base_freq = harmonic_tx.base_frequency
        waves = []
        
        if alert_type == SonicAlert.HARMONY:
            # Clean transaction: Pleasant major triad
            waves = [
                AudioWave(base_freq, 0.4, 1.0, "sine"),           # Root
                AudioWave(base_freq * 1.25, 0.3, 1.0, "sine"),   # Major third
                AudioWave(base_freq * 1.5, 0.2, 1.0, "sine")     # Perfect fifth
            ]
            
        elif alert_type == SonicAlert.DISSONANCE:
            # Review needed: Minor dissonance with resolution
            waves = [
                AudioWave(base_freq, 0.4, 1.5, "sine"),
                AudioWave(base_freq * 1.125, 0.3, 1.0, "sine"),  # Minor second (dissonant)
                AudioWave(base_freq * 1.5, 0.2, 1.5, "sine")     # Resolves to fifth
            ]
            
        elif alert_type == SonicAlert.TRITONE:
            # Fraud detected: Devil's interval + chaotic harmonics
            waves = [
                AudioWave(base_freq, 0.5, 2.0, "square"),        # Harsh square wave
                AudioWave(base_freq * 1.414, 0.4, 2.0, "square"), # Tritone (√2 ratio)
                AudioWave(base_freq * 0.7, 0.3, 2.0, "sawtooth"), # Destabilizing sub-bass
                AudioWave(base_freq * 2.828, 0.2, 1.0, "noise")   # High-frequency chaos
            ]
            
        elif alert_type == SonicAlert.SILENCE:
            # Missing transaction: Ominous low-frequency pulse
            waves = [
                AudioWave(base_freq * 0.25, 0.6, 0.5, "sine"),   # Sub-bass pulse
                AudioWave(0, 0, 1.0, "sine"),                    # Silence gap
                AudioWave(base_freq * 0.25, 0.6, 0.5, "sine")    # Repeat pulse
            ]
            
        elif alert_type == SonicAlert.CHAOS:
            # System attack: Complete cacophony
            waves = [
                AudioWave(base_freq * np.random.random(), 0.3, 0.1, "noise") 
                for _ in range(10)  # Random chaotic frequencies
            ]
            
        return waves
        
    def _play_waves_async(self, waves: List[AudioWave]):
        """Play audio waves asynchronously"""
        
        if self.is_playing:
            return  # Don't overlap audio
            
        self.audio_thread = threading.Thread(
            target=self._play_waves_blocking, 
            args=(waves,)
        )
        self.audio_thread.daemon = True
        self.audio_thread.start()
        
    def _play_waves_blocking(self, waves: List[AudioWave]):
        """Play audio waves (blocking call)"""
        
        if not AUDIO_AVAILABLE:
            return
            
        self.is_playing = True
        
        try:
            # Calculate total duration
            max_duration = max(wave.duration for wave in waves) if waves else 1.0
            total_samples = int(max_duration * self.sample_rate)
            
            # Create composite audio signal
            composite_signal = np.zeros(total_samples)
            
            for wave in waves:
                if wave.frequency > 0:  # Skip silent waves
                    wave_samples = int(wave.duration * self.sample_rate)
                    wave_signal = self._generate_wave_signal(wave, wave_samples)
                    
                    # Add to composite (mix the waves)
                    if wave_samples <= len(composite_signal):
                        composite_signal[:wave_samples] += wave_signal
                    else:
                        composite_signal += wave_signal[:total_samples]
            
            # Normalize to prevent clipping
            if np.max(np.abs(composite_signal)) > 0:
                composite_signal = composite_signal / np.max(np.abs(composite_signal))
                
            # Apply volume control
            composite_signal *= self.volume
            
            # Play the audio
            sd.play(composite_signal, self.sample_rate)
            sd.wait()  # Wait until playback is finished
            
        except Exception as e:
            print(f"🔇 Audio playback error: {e}")
        finally:
            self.is_playing = False
            
    def _generate_wave_signal(self, wave: AudioWave, num_samples: int) -> np.ndarray:
        """Generate wave signal for specified wave configuration"""
        
        if wave.frequency <= 0:
            return np.zeros(num_samples)
            
        generator = self.wave_generators.get(wave.wave_type, self._generate_sine_wave)
        return generator(wave.frequency, wave.amplitude, num_samples)
        
    def _generate_sine_wave(self, frequency: float, amplitude: float, num_samples: int) -> np.ndarray:
        """Generate pure sine wave"""
        t = np.linspace(0, num_samples / self.sample_rate, num_samples)
        return amplitude * np.sin(2 * np.pi * frequency * t)
        
    def _generate_square_wave(self, frequency: float, amplitude: float, num_samples: int) -> np.ndarray:
        """Generate square wave (harsh, attention-grabbing)"""
        t = np.linspace(0, num_samples / self.sample_rate, num_samples)
        return amplitude * np.sign(np.sin(2 * np.pi * frequency * t))
        
    def _generate_sawtooth_wave(self, frequency: float, amplitude: float, num_samples: int) -> np.ndarray:
        """Generate sawtooth wave (cutting, aggressive)"""
        t = np.linspace(0, num_samples / self.sample_rate, num_samples)
        return amplitude * (2 * (t * frequency - np.floor(t * frequency + 0.5)))
        
    def _generate_noise_wave(self, frequency: float, amplitude: float, num_samples: int) -> np.ndarray:
        """Generate filtered noise (chaos, system disruption)"""
        # Generate white noise then filter around target frequency
        noise = np.random.normal(0, amplitude, num_samples)
        
        # Simple low-pass filter to approximate frequency content
        if frequency > 0:
            cutoff = frequency / self.sample_rate
            noise = self._simple_lowpass_filter(noise, cutoff)
            
        return noise
        
    def _simple_lowpass_filter(self, signal: np.ndarray, cutoff: float) -> np.ndarray:
        """Simple exponential lowpass filter"""
        alpha = cutoff
        filtered = np.zeros_like(signal)
        
        if len(signal) > 0:
            filtered[0] = signal[0]
            for i in range(1, len(signal)):
                filtered[i] = alpha * signal[i] + (1 - alpha) * filtered[i-1]
                
        return filtered
        
    def _print_audio_description(self, harmonic_tx: HarmonicTransaction, 
                                alert_type: SonicAlert = None):
        """Print textual description of what should be heard"""
        
        if alert_type is None:
            alert_type = self._classify_sonic_alert(harmonic_tx)
            
        print(f"\n🎵 SONIC FEEDBACK: {harmonic_tx.transaction_id}")
        print(f"Alert Type: {alert_type.value.upper()}")
        print(f"Base Frequency: {harmonic_tx.base_frequency}Hz")
        
        if alert_type == SonicAlert.HARMONY:
            print("🎼 Playing: Pleasant major chord - transaction resonates cleanly")
            
        elif alert_type == SonicAlert.DISSONANCE:
            print("⚠️  Playing: Minor discord with resolution - requires review")
            
        elif alert_type == SonicAlert.TRITONE:
            print("🚨 Playing: Devil's interval + harsh overtones - FRAUD DETECTED")
            
        elif alert_type == SonicAlert.SILENCE:
            print("🔇 Playing: Ominous sub-bass pulse - missing transaction pattern")
            
        elif alert_type == SonicAlert.CHAOS:
            print("💥 Playing: Complete cacophony - system under attack")
            
        # Show chakra impact as audio description
        print("Chakra Frequency Impact:")
        for chakra, impact in harmonic_tx.chakra_impact.items():
            if impact > 0.2:
                freq = SACRED_FREQUENCIES[chakra]
                intensity = "HIGH" if impact > 0.7 else "MEDIUM" if impact > 0.4 else "LOW"
                print(f"  {chakra.title()}: {freq}Hz ({intensity} resonance)")
                
    def play_chakra_sequence(self, chakra_impacts: Dict[str, float]):
        """Play ascending/descending chakra sequence based on impacts"""
        
        if not AUDIO_AVAILABLE:
            print("🔇 Would play chakra frequency sequence")
            return
            
        waves = []
        for i, (chakra, impact) in enumerate(chakra_impacts.items()):
            if impact > 0.1:  # Only play significant impacts
                freq = SACRED_FREQUENCIES[chakra]
                amplitude = min(impact * 0.3, 0.4)  # Scale amplitude by impact
                duration = 0.5
                start_delay = i * 0.3  # Stagger the chakra tones
                
                waves.append(AudioWave(freq, amplitude, duration, "sine"))
                
        if waves:
            self._play_waves_async(waves)
            
    def create_fraud_symphony(self, harmonic_transactions: List[HarmonicTransaction]):
        """Create a musical composition from multiple transactions"""
        
        print("\n🎼 CREATING FRAUD DETECTION SYMPHONY")
        print("=" * 50)
        
        for i, tx in enumerate(harmonic_transactions):
            print(f"\nMovement {i+1}: {tx.transaction_id}")
            self.play_transaction_audio(tx)
            
            if AUDIO_AVAILABLE:
                time.sleep(2.5)  # Pause between movements
                
        print("\n🎭 Symphony complete. Fraudulent patterns should be audibly distinct.")

def demo_sonic_fraud_detection():
    """Demonstrate the sonic fraud detection system"""
    
    print("🎵 SONIC FRAUD DETECTION DEMO")
    print("=" * 50)
    
    # Create analyzer and sonic detector
    analyzer = HarmonicTransactionAnalyzer()
    sonic_detector = SonicFraudDetector()
    
    # Test with various transaction types
    test_transactions = [
        {
            'id': 'CLEAN_TX',
            'timestamp': '2024-03-15T14:23:15',
            'from_entity': 'Ansevata Trust No 2',
            'to_entity': 'J Rich and Partners',
            'amount': 847000,
            'type': 'trust_distribution'
        },
        {
            'id': 'SUSPICIOUS_TX',
            'timestamp': '2024-03-15T02:45:30',  # After hours
            'from_entity': 'Unknown Offshore Entity',
            'to_entity': 'J Rich Family Trust No 7',
            'amount': 1618000,  # Golden ratio manipulation
            'type': 'synthetic_transaction'
        },
        {
            'id': 'ROUND_NUMBER_TX',
            'timestamp': '2024-03-15T14:30:00',
            'from_entity': 'Centosa S.A',
            'to_entity': 'Centosa S.A',  # Self-referential
            'amount': 5000000,  # Exactly 5M (round number bias)
            'type': 'nominee_transfer'
        }
    ]
    
    harmonic_results = []
    
    for tx_data in test_transactions:
        harmonic_tx = analyzer.analyze_transaction(tx_data)
        harmonic_results.append(harmonic_tx)
        
        print(f"\n📊 Transaction Analysis: {tx_data['id']}")
        print(f"Fraud Probability: {harmonic_tx.fraud_probability}")
        print(f"Resonance: {harmonic_tx.resonance_status.value}")
        print(f"Flags: {harmonic_tx.anomaly_flags}")
        
        # Play the audio for this transaction
        sonic_detector.play_transaction_audio(harmonic_tx)
        
        if AUDIO_AVAILABLE:
            time.sleep(3)  # Pause between transactions
            
    # Create fraud symphony from all transactions
    sonic_detector.create_fraud_symphony(harmonic_results)

if __name__ == "__main__":
    demo_sonic_fraud_detection()