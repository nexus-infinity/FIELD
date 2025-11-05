"""
CQHI (Classical-Quantum-Harmonic Integration) Physics Framework

This module implements physically testable equations bridging:
- Classical string resonance (with real physical units)
- Quantum ground state energy and operators
- Neural observable spectral analysis

Unlike symbolic harmonic metaphors, this uses measurable quantities,
standard physics units, and produces testable predictions.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json
from datetime import datetime

# Physical constants (SI units)
PLANCK_CONSTANT = 6.62607015e-34  # J·s
BOLTZMANN_CONSTANT = 1.380649e-23  # J/K
SPEED_OF_LIGHT = 299792458  # m/s
ELECTRON_MASS = 9.1093837015e-31  # kg


@dataclass
class PhysicalParameters:
    """Real physical parameters with units"""
    string_length: float  # meters
    string_tension: float  # Newtons
    linear_density: float  # kg/m
    temperature: float  # Kelvin
    quantum_number: int  # dimensionless
    neural_sample_rate: float  # Hz
    neural_duration: float  # seconds


@dataclass
class ResonanceResult:
    """Physical resonance analysis result"""
    classical_frequencies: np.ndarray  # Hz
    quantum_energies: np.ndarray  # Joules
    spectral_power: np.ndarray  # dimensionless
    coherence_index: float  # 0-1
    timestamp: str
    validation_passed: bool


class CQHIPhysics:
    """Classical-Quantum-Harmonic Integration Physics Engine"""
    
    def __init__(self, params: PhysicalParameters):
        self.params = params
        self.validation_log: List[str] = []
        
    def classical_string_frequency(self, mode: int) -> float:
        """
        Classical wave equation for string vibration
        
        f_n = (n / 2L) * sqrt(T / μ)
        
        where:
        - n: harmonic mode number
        - L: string length (m)
        - T: tension (N)
        - μ: linear mass density (kg/m)
        
        Returns: frequency in Hz
        """
        L = self.params.string_length
        T = self.params.string_tension
        mu = self.params.linear_density
        
        # Validate physical constraints
        if L <= 0 or T <= 0 or mu <= 0:
            raise ValueError("Physical parameters must be positive")
            
        wave_speed = np.sqrt(T / mu)
        frequency = (mode / (2 * L)) * wave_speed
        
        self.validation_log.append(
            f"Classical: mode={mode}, f={frequency:.2f} Hz, v={wave_speed:.2f} m/s"
        )
        
        return frequency
    
    def quantum_energy_level(self, n: int) -> float:
        """
        Quantum harmonic oscillator energy
        
        E_n = ℏω(n + 1/2)
        
        where:
        - ℏ: reduced Planck constant (J·s)
        - ω: angular frequency (rad/s)
        - n: quantum number
        
        Returns: energy in Joules
        """
        h_bar = PLANCK_CONSTANT / (2 * np.pi)
        
        # Use fundamental classical frequency as base
        f_classical = self.classical_string_frequency(mode=1)
        omega = 2 * np.pi * f_classical
        
        # Quantum energy levels
        energy = h_bar * omega * (n + 0.5)
        
        self.validation_log.append(
            f"Quantum: n={n}, E={energy:.6e} J, ℏω={h_bar * omega:.6e} J"
        )
        
        return energy
    
    def thermal_occupation(self, frequency: float) -> float:
        """
        Bose-Einstein thermal occupation number
        
        n_BE = 1 / (exp(ℏω/k_B T) - 1)
        
        Accounts for temperature effects on quantum state population
        """
        h_bar = PLANCK_CONSTANT / (2 * np.pi)
        omega = 2 * np.pi * frequency
        
        exp_arg = (h_bar * omega) / (BOLTZMANN_CONSTANT * self.params.temperature)
        
        # Avoid numerical overflow
        if exp_arg > 100:
            return 0.0
        
        n_thermal = 1.0 / (np.exp(exp_arg) - 1)
        
        return n_thermal
    
    def neural_spectral_analysis(self, signal: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        FFT-based spectral analysis of neural/observable signal
        
        Args:
            signal: time-domain signal (arbitrary units)
            
        Returns:
            frequencies (Hz), power spectral density (normalized)
        """
        # FFT with proper normalization
        N = len(signal)
        fft_result = np.fft.rfft(signal)
        power = np.abs(fft_result) ** 2 / N
        
        # Frequency bins
        frequencies = np.fft.rfftfreq(N, d=1.0/self.params.neural_sample_rate)
        
        self.validation_log.append(
            f"Neural: N={N}, f_max={frequencies[-1]:.2f} Hz, P_total={np.sum(power):.2e}"
        )
        
        return frequencies, power
    
    def coherence_metric(
        self, 
        classical_freqs: np.ndarray,
        neural_freqs: np.ndarray,
        neural_power: np.ndarray,
        tolerance_hz: float = 2.0
    ) -> float:
        """
        Compute coherence between classical predictions and neural observations
        
        Coherence = (sum of neural power near classical frequencies) / total power
        
        Args:
            classical_freqs: predicted frequencies from physics
            neural_freqs: measured frequency bins
            neural_power: measured power spectrum
            tolerance_hz: matching tolerance
            
        Returns:
            coherence index (0-1)
        """
        coherent_power = 0.0
        
        for f_classical in classical_freqs:
            # Find neural power within tolerance
            mask = np.abs(neural_freqs - f_classical) <= tolerance_hz
            coherent_power += np.sum(neural_power[mask])
        
        total_power = np.sum(neural_power)
        
        if total_power == 0:
            return 0.0
        
        coherence = coherent_power / total_power
        
        self.validation_log.append(
            f"Coherence: {coherence:.4f} (coherent={coherent_power:.2e}, total={total_power:.2e})"
        )
        
        return coherence
    
    def full_analysis(
        self,
        neural_signal: Optional[np.ndarray] = None,
        n_harmonics: int = 8
    ) -> ResonanceResult:
        """
        Complete CQHI analysis: classical + quantum + neural coherence
        
        Args:
            neural_signal: observed time-domain signal (if None, generates test signal)
            n_harmonics: number of harmonic modes to compute
            
        Returns:
            ResonanceResult with all physical quantities
        """
        self.validation_log.clear()
        
        # Classical harmonic series
        classical_frequencies = np.array([
            self.classical_string_frequency(mode=n) for n in range(1, n_harmonics + 1)
        ])
        
        # Quantum energy levels
        quantum_energies = np.array([
            self.quantum_energy_level(n=n) for n in range(n_harmonics)
        ])
        
        # Neural spectral analysis
        if neural_signal is None:
            # Generate synthetic test signal with harmonics
            t = np.linspace(0, self.params.neural_duration, 
                          int(self.params.neural_sample_rate * self.params.neural_duration))
            neural_signal = np.zeros_like(t)
            for f in classical_frequencies[:3]:  # Add first 3 harmonics
                neural_signal += np.sin(2 * np.pi * f * t)
            # Add noise
            neural_signal += 0.1 * np.random.randn(len(t))
        
        neural_freqs, neural_power = self.neural_spectral_analysis(neural_signal)
        
        # Coherence validation
        coherence = self.coherence_metric(classical_frequencies, neural_freqs, neural_power)
        
        # Validation: coherence > 0.3 for physical significance
        validation_passed = coherence > 0.3
        
        result = ResonanceResult(
            classical_frequencies=classical_frequencies,
            quantum_energies=quantum_energies,
            spectral_power=neural_power,
            coherence_index=coherence,
            timestamp=datetime.utcnow().isoformat(),
            validation_passed=validation_passed
        )
        
        return result
    
    def export_results(self, result: ResonanceResult, filepath: str):
        """Export results to JSON with full traceability"""
        export_data = {
            "timestamp": result.timestamp,
            "parameters": {
                "string_length_m": self.params.string_length,
                "string_tension_N": self.params.string_tension,
                "linear_density_kg_per_m": self.params.linear_density,
                "temperature_K": self.params.temperature,
                "sample_rate_Hz": self.params.neural_sample_rate,
            },
            "classical_frequencies_Hz": result.classical_frequencies.tolist(),
            "quantum_energies_J": result.quantum_energies.tolist(),
            "coherence_index": result.coherence_index,
            "validation_passed": bool(result.validation_passed),
            "validation_log": self.validation_log
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"Results exported to {filepath}")


# ============================================================================
# WORKED EXAMPLE: Guitar String Analysis
# ============================================================================

def example_guitar_string_analysis():
    """
    Physically realistic example: analyzing a guitar string
    
    Standard guitar string (high E):
    - Length: 0.648 m (25.5 inches scale length)
    - Tension: ~70 N
    - Linear density: ~0.0004 kg/m
    - Expected fundamental: ~329.6 Hz (E4 note)
    """
    
    print("=" * 70)
    print("CQHI Framework: Guitar String Analysis")
    print("=" * 70)
    
    # Physical parameters
    params = PhysicalParameters(
        string_length=0.648,  # m
        string_tension=70.0,  # N
        linear_density=0.0004,  # kg/m
        temperature=298.15,  # K (25°C)
        quantum_number=0,
        neural_sample_rate=8000.0,  # Hz (audio rate)
        neural_duration=2.0  # seconds
    )
    
    # Initialize physics engine
    cqhi = CQHIPhysics(params)
    
    # Run full analysis
    result = cqhi.full_analysis(n_harmonics=6)
    
    # Display results
    print("\nCLASSICAL HARMONIC SERIES:")
    for i, freq in enumerate(result.classical_frequencies, 1):
        print(f"  Mode {i}: {freq:.2f} Hz")
    
    print("\nQUANTUM ENERGY LEVELS:")
    for i, energy in enumerate(result.quantum_energies):
        print(f"  n={i}: E = {energy:.6e} J = {energy / 1.602e-19:.3e} eV")
    
    print(f"\nCOHERENCE INDEX: {result.coherence_index:.4f}")
    print(f"VALIDATION: {'PASSED' if result.validation_passed else 'FAILED'}")
    
    print("\nVALIDATION LOG:")
    for log_entry in cqhi.validation_log:
        print(f"  {log_entry}")
    
    # Export
    export_path = "/Users/jbear/FIELD/◎_source_core/cqhi_guitar_analysis.json"
    cqhi.export_results(result, export_path)
    
    return result


if __name__ == "__main__":
    example_guitar_string_analysis()
