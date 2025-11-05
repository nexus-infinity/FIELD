#!/usr/bin/env python3
"""
Harmonic Transaction Data Model
Resonance-Based Fraud Detection System

This module implements the mathematical foundation for converting financial
transactions into harmonic frequencies, geometric patterns, and chakra resonances
for intuitive fraud detection.
"""

import json
import math
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

# Sacred Geometry Constants
PHI = (1 + math.sqrt(5)) / 2  # Golden Ratio
SACRED_FREQUENCIES = {
    'root': 174,      # Root Chakra - Foundation/Security
    'sacral': 285,    # Sacral Chakra - Creativity/Relationships
    'solar': 396,     # Solar Plexus - Personal Power
    'heart': 528,     # Heart Chakra - Love/Healing (DNA repair)
    'throat': 741,    # Throat Chakra - Expression/Truth
    'third_eye': 852, # Third Eye - Intuition/Insight  
    'crown': 963      # Crown Chakra - Spiritual Connection
}

class TransactionType(Enum):
    TRUST_DISTRIBUTION = "trust_distribution"
    SHARE_TRANSFER = "share_transfer" 
    LOAN_FACILITY = "loan_facility"
    DIVIDEND_PAYMENT = "dividend_payment"
    CAPITAL_INJECTION = "capital_injection"
    NOMINEE_TRANSFER = "nominee_transfer"
    SYNTHETIC_TRANSACTION = "synthetic_transaction"

class ResonanceStatus(Enum):
    HARMONIC = "harmonic"        # Clean, legitimate transaction
    DISSONANT = "dissonant"      # Requires review
    MICROTONAL = "microtonal"    # Fraud detected
    SILENT = "silent"            # Missing/blocked transaction

@dataclass
class GeometricSignature:
    """Sacred geometry pattern completion metrics"""
    shape_type: str              # triangle, hexagon, octagon, etc.
    completion_ratio: float      # 0.0 to 1.0 (1.0 = complete pattern)
    missing_vertices: List[int]  # Which connection points are broken
    symmetry_score: float        # Bilateral symmetry measure
    golden_ratio_alignment: float # Phi alignment score

@dataclass
class HarmonicTransaction:
    """Core transaction with harmonic analysis"""
    # Basic Transaction Data
    transaction_id: str
    timestamp: datetime
    from_entity: str
    to_entity: str
    amount: float
    transaction_type: TransactionType
    
    # Harmonic Analysis
    base_frequency: float        # Primary harmonic frequency
    harmonic_series: List[float] # Overtones and undertones
    resonance_status: ResonanceStatus
    dissonance_score: float      # 0.0 = perfect, 1.0 = maximum discord
    
    # Geometric Analysis  
    geometric_signature: GeometricSignature
    chakra_impact: Dict[str, float]  # Impact on each chakra frequency
    
    # Fraud Detection
    fraud_probability: float     # 0.0 to 1.0
    anomaly_flags: List[str]     # Specific red flags detected
    vault_anchor_distance: float # Distance from verified baseline

class HarmonicTransactionAnalyzer:
    """Converts financial transactions into harmonic and geometric patterns"""
    
    def __init__(self):
        self.vault_baselines = {}  # Verified ground truth patterns
        self.entity_signatures = {}  # Known harmonic signatures per entity
        
    def analyze_transaction(self, transaction_data: Dict) -> HarmonicTransaction:
        """Convert raw transaction into harmonic analysis"""
        
        # Extract basic transaction info
        tx_id = transaction_data.get('id', 'unknown')
        timestamp = datetime.fromisoformat(transaction_data.get('timestamp', '1970-01-01'))
        from_entity = transaction_data.get('from_entity', 'unknown')
        to_entity = transaction_data.get('to_entity', 'unknown')
        amount = float(transaction_data.get('amount', 0))
        tx_type = TransactionType(transaction_data.get('type', 'synthetic_transaction'))
        
        # Calculate base frequency using sacred geometry principles
        base_freq = self._calculate_base_frequency(amount, tx_type, timestamp)
        
        # Generate harmonic series
        harmonic_series = self._generate_harmonic_series(base_freq)
        
        # Analyze geometric patterns
        geometric_sig = self._analyze_geometric_pattern(
            from_entity, to_entity, amount, tx_type
        )
        
        # Calculate chakra impact
        chakra_impact = self._calculate_chakra_impact(
            base_freq, harmonic_series, geometric_sig
        )
        
        # Determine resonance status and fraud probability
        resonance_status, dissonance_score = self._analyze_resonance(
            base_freq, harmonic_series, geometric_sig
        )
        
        fraud_prob, anomaly_flags = self._detect_fraud_patterns(
            from_entity, to_entity, amount, base_freq, geometric_sig
        )
        
        vault_distance = self._calculate_vault_distance(
            from_entity, to_entity, tx_type, base_freq
        )
        
        return HarmonicTransaction(
            transaction_id=tx_id,
            timestamp=timestamp,
            from_entity=from_entity,
            to_entity=to_entity,
            amount=amount,
            transaction_type=tx_type,
            base_frequency=base_freq,
            harmonic_series=harmonic_series,
            resonance_status=resonance_status,
            dissonance_score=dissonance_score,
            geometric_signature=geometric_sig,
            chakra_impact=chakra_impact,
            fraud_probability=fraud_prob,
            anomaly_flags=anomaly_flags,
            vault_anchor_distance=vault_distance
        )
    
    def _calculate_base_frequency(self, amount: float, tx_type: TransactionType, 
                                 timestamp: datetime) -> float:
        """Calculate primary harmonic frequency for transaction"""
        
        # Base frequency mapping using logarithmic scaling
        # Large amounts = lower frequencies (bass foundation)
        # Small amounts = higher frequencies (treble details)
        
        if amount <= 0:
            return 1.0  # Anomalous frequency for zero/negative amounts
            
        # Logarithmic scaling to map dollar amounts to musical frequencies
        log_amount = math.log10(amount)
        
        # Map to musical range (20Hz to 20kHz, focused on 80Hz to 4kHz)
        base_freq = 80 + (log_amount * 100)
        
        # Adjust for transaction type (different instruments)
        type_modifiers = {
            TransactionType.TRUST_DISTRIBUTION: 1.0,    # Pure tone
            TransactionType.SHARE_TRANSFER: 1.125,      # Perfect fourth up
            TransactionType.LOAN_FACILITY: 0.75,        # Perfect fourth down  
            TransactionType.DIVIDEND_PAYMENT: 1.5,      # Perfect fifth up
            TransactionType.CAPITAL_INJECTION: 2.0,     # Octave up
            TransactionType.NOMINEE_TRANSFER: 1.618,    # Golden ratio (suspicious)
            TransactionType.SYNTHETIC_TRANSACTION: 1.414 # Square root of 2 (dissonant)
        }
        
        base_freq *= type_modifiers.get(tx_type, 1.0)
        
        # Time-based modulation (business hours vs after hours)
        hour = timestamp.hour
        if hour < 9 or hour > 17:  # After business hours
            base_freq *= 0.9  # Slightly lower (more suspicious)
            
        return round(base_freq, 2)
    
    def _generate_harmonic_series(self, base_freq: float) -> List[float]:
        """Generate overtones and undertones for harmonic analysis"""
        
        harmonics = [base_freq]  # Fundamental
        
        # Add overtones (2x, 3x, 4x, 5x the base frequency)
        for multiplier in [2, 3, 4, 5]:
            harmonics.append(round(base_freq * multiplier, 2))
            
        # Add undertones (1/2x, 1/3x, 1/4x, 1/5x the base frequency)  
        for divisor in [2, 3, 4, 5]:
            harmonics.append(round(base_freq / divisor, 2))
            
        return sorted(harmonics)
    
    def _analyze_geometric_pattern(self, from_entity: str, to_entity: str, 
                                  amount: float, tx_type: TransactionType) -> GeometricSignature:
        """Analyze sacred geometry completion patterns"""
        
        # Determine expected geometric shape based on transaction type
        shape_mappings = {
            TransactionType.TRUST_DISTRIBUTION: "triangle",    # 3 points (trustee, beneficiary, asset)
            TransactionType.SHARE_TRANSFER: "hexagon",         # 6 points (complex ownership)
            TransactionType.LOAN_FACILITY: "square",           # 4 points (lender, borrower, collateral, terms)
            TransactionType.DIVIDEND_PAYMENT: "pentagon",      # 5 points (company, shareholders, earnings, distribution, tax)
            TransactionType.CAPITAL_INJECTION: "octagon",      # 8 points (complex capital structure)
            TransactionType.NOMINEE_TRANSFER: "triangle",      # Should be simple, fraud if complex
            TransactionType.SYNTHETIC_TRANSACTION: "irregular" # No expected pattern
        }
        
        expected_shape = shape_mappings.get(tx_type, "irregular")
        
        # Calculate completion ratio based on entity verification
        known_entities = self._get_known_entities()
        from_verified = from_entity in known_entities
        to_verified = to_entity in known_entities
        
        if expected_shape == "triangle":
            completion_ratio = 0.33 + (0.33 if from_verified else 0) + (0.33 if to_verified else 0)
            missing_vertices = []
            if not from_verified:
                missing_vertices.append(0)
            if not to_verified:
                missing_vertices.append(1)
                
        elif expected_shape == "hexagon":
            # More complex verification needed for hexagonal patterns
            completion_ratio = 0.5 if (from_verified and to_verified) else 0.2
            missing_vertices = [i for i in range(6) if not (from_verified and to_verified)]
            
        else:
            completion_ratio = 0.1  # Default low completion for irregular patterns
            missing_vertices = list(range(6))  # Assume broken pattern
        
        # Calculate symmetry score based on amount patterns
        symmetry_score = self._calculate_symmetry_score(amount)
        
        # Golden ratio alignment check
        phi_alignment = self._calculate_phi_alignment(amount)
        
        return GeometricSignature(
            shape_type=expected_shape,
            completion_ratio=completion_ratio,
            missing_vertices=missing_vertices,
            symmetry_score=symmetry_score,
            golden_ratio_alignment=phi_alignment
        )
    
    def _calculate_chakra_impact(self, base_freq: float, harmonics: List[float], 
                                geometric_sig: GeometricSignature) -> Dict[str, float]:
        """Calculate impact on each chakra frequency"""
        
        chakra_impact = {}
        
        for chakra_name, chakra_freq in SACRED_FREQUENCIES.items():
            # Find closest harmonic to this chakra frequency
            closest_harmonic = min(harmonics, key=lambda x: abs(x - chakra_freq))
            frequency_distance = abs(closest_harmonic - chakra_freq)
            
            # Calculate resonance strength (closer = stronger impact)
            max_distance = chakra_freq * 0.5  # 50% frequency tolerance
            if frequency_distance <= max_distance:
                impact = 1.0 - (frequency_distance / max_distance)
            else:
                impact = 0.0
                
            # Modulate by geometric completion (broken geometry weakens chakras)
            impact *= geometric_sig.completion_ratio
            
            chakra_impact[chakra_name] = round(impact, 3)
            
        return chakra_impact
    
    def _analyze_resonance(self, base_freq: float, harmonics: List[float], 
                          geometric_sig: GeometricSignature) -> Tuple[ResonanceStatus, float]:
        """Determine overall resonance status and dissonance score"""
        
        # Check for harmonic relationships with sacred frequencies
        harmonic_matches = 0
        total_checked = 0
        
        for sacred_freq in SACRED_FREQUENCIES.values():
            total_checked += 1
            for harmonic in harmonics:
                # Check for perfect ratios (octaves, fifths, fourths)
                ratio = max(harmonic, sacred_freq) / min(harmonic, sacred_freq)
                if self._is_harmonic_ratio(ratio):
                    harmonic_matches += 1
                    break
        
        harmonic_score = harmonic_matches / total_checked if total_checked > 0 else 0
        
        # Factor in geometric completion
        overall_score = (harmonic_score + geometric_sig.completion_ratio) / 2
        
        # Calculate dissonance score (inverse of harmonic score)
        dissonance_score = 1.0 - overall_score
        
        # Determine status
        if dissonance_score < 0.3:
            status = ResonanceStatus.HARMONIC
        elif dissonance_score < 0.7:
            status = ResonanceStatus.DISSONANT
        else:
            status = ResonanceStatus.MICROTONAL
            
        return status, round(dissonance_score, 3)
    
    def _is_harmonic_ratio(self, ratio: float, tolerance: float = 0.05) -> bool:
        """Check if frequency ratio represents a harmonic interval"""
        
        # Common harmonic ratios in music
        harmonic_ratios = [
            1.0,    # Unison
            2.0,    # Octave
            1.5,    # Perfect Fifth
            1.333,  # Perfect Fourth  
            1.25,   # Major Third
            1.2,    # Minor Third
            1.125,  # Major Second
            PHI     # Golden Ratio (divine proportion)
        ]
        
        for target_ratio in harmonic_ratios:
            if abs(ratio - target_ratio) <= tolerance:
                return True
                
        return False
    
    def _detect_fraud_patterns(self, from_entity: str, to_entity: str, amount: float,
                              base_freq: float, geometric_sig: GeometricSignature) -> Tuple[float, List[str]]:
        """Detect specific fraud patterns and calculate fraud probability"""
        
        anomaly_flags = []
        fraud_score = 0.0
        
        # Pattern 1: Unknown entities (not in vault baselines)
        known_entities = self._get_known_entities()
        if from_entity not in known_entities:
            anomaly_flags.append("unknown_source_entity")
            fraud_score += 0.3
        if to_entity not in known_entities:
            anomaly_flags.append("unknown_destination_entity")
            fraud_score += 0.3
            
        # Pattern 2: Broken geometric patterns
        if geometric_sig.completion_ratio < 0.5:
            anomaly_flags.append("incomplete_geometric_pattern")
            fraud_score += 0.2
            
        # Pattern 3: Microtonal frequencies (not harmonic)
        if not any(self._is_harmonic_ratio(base_freq / sacred) for sacred in SACRED_FREQUENCIES.values()):
            anomaly_flags.append("microtonal_dissonance")
            fraud_score += 0.4
            
        # Pattern 4: Round number bias (suspicious clean amounts)
        if amount % 1000000 == 0:  # Exactly 1M, 2M, etc.
            anomaly_flags.append("round_number_bias")
            fraud_score += 0.1
            
        # Pattern 5: Self-referential transactions
        if from_entity == to_entity:
            anomaly_flags.append("self_referential_transaction") 
            fraud_score += 0.5
            
        # Pattern 6: Phi-ratio amounts (golden ratio manipulation)
        phi_ratios = [PHI, PHI**2, 1/PHI, 1/(PHI**2)]
        for phi_ratio in phi_ratios:
            if abs(amount - round(amount * phi_ratio)) < 1000:  # Within $1000 of phi ratio
                anomaly_flags.append("golden_ratio_manipulation")
                fraud_score += 0.3
                break
        
        fraud_probability = min(fraud_score, 1.0)  # Cap at 100%
        
        return round(fraud_probability, 3), anomaly_flags
    
    def _calculate_vault_distance(self, from_entity: str, to_entity: str, 
                                 tx_type: TransactionType, base_freq: float) -> float:
        """Calculate distance from verified vault baselines"""
        
        # This would integrate with your TATA vault system
        # For now, simulate with basic entity verification
        
        vault_key = f"{from_entity}:{to_entity}:{tx_type.value}"
        
        if vault_key in self.vault_baselines:
            expected_freq = self.vault_baselines[vault_key]
            distance = abs(base_freq - expected_freq) / expected_freq
        else:
            # No baseline = maximum distance
            distance = 1.0
            
        return round(distance, 3)
    
    def _get_known_entities(self) -> set:
        """Get set of known/verified entities from vault"""
        # This would integrate with your entity validation system
        return {
            "Ansevata Nominees Pty Ltd",
            "Ansevata Trust No 2", 
            "Centosa S.A",
            "Berjak Nominees (Vic) Pty Ltd",
            "J Rich and Partners",
            "J Rich Family Trust No 3",
            "Mount Eliza Trust No.2"
        }
    
    def _calculate_symmetry_score(self, amount: float) -> float:
        """Calculate bilateral symmetry in amount patterns"""
        
        amount_str = str(int(amount))
        length = len(amount_str)
        
        if length == 1:
            return 1.0
            
        # Check palindromic symmetry
        reversed_str = amount_str[::-1]
        matches = sum(1 for i, (a, b) in enumerate(zip(amount_str, reversed_str)) if a == b)
        
        symmetry_score = matches / length
        return round(symmetry_score, 3)
    
    def _calculate_phi_alignment(self, amount: float) -> float:
        """Calculate alignment with golden ratio"""
        
        # Check if amount aligns with phi proportions
        phi_multiples = [amount * PHI, amount / PHI, amount * (PHI ** 2), amount / (PHI ** 2)]
        
        best_alignment = 0.0
        for phi_multiple in phi_multiples:
            # Check alignment with round numbers
            for round_number in [1000000, 100000, 10000, 1000]:
                if round_number > 0:
                    ratio = phi_multiple / round_number
                    if 0.9 <= ratio <= 1.1:  # Within 10% of round number
                        alignment = 1.0 - abs(1.0 - ratio)
                        best_alignment = max(best_alignment, alignment)
        
        return round(best_alignment, 3)

def create_sample_transactions():
    """Create sample transactions for testing"""
    
    transactions = [
        {
            'id': 'TX001',
            'timestamp': '2024-03-15T14:23:15',
            'from_entity': 'Ansevata Trust No 2',
            'to_entity': 'J Rich and Partners', 
            'amount': 847000,
            'type': 'trust_distribution'
        },
        {
            'id': 'TX002', 
            'timestamp': '2024-03-15T14:23:22',
            'from_entity': 'Centosa S.A',
            'to_entity': 'Berjak Nominees (Vic) Pty Ltd',
            'amount': 2100000,
            'type': 'share_transfer'
        },
        {
            'id': 'TX003',
            'timestamp': '2024-03-15T14:23:31', 
            'from_entity': 'Unknown Entity XYZ',
            'to_entity': 'J Rich Family Trust No 7',
            'amount': 500000,
            'type': 'synthetic_transaction'
        }
    ]
    
    return transactions

if __name__ == "__main__":
    # Test the harmonic analyzer
    analyzer = HarmonicTransactionAnalyzer()
    
    print("🎵 Harmonic Transaction Analysis Test")
    print("=" * 50)
    
    sample_transactions = create_sample_transactions()
    
    for tx_data in sample_transactions:
        print(f"\n📊 Analyzing Transaction: {tx_data['id']}")
        
        harmonic_tx = analyzer.analyze_transaction(tx_data)
        
        print(f"Base Frequency: {harmonic_tx.base_frequency}Hz")
        print(f"Resonance Status: {harmonic_tx.resonance_status.value}")
        print(f"Dissonance Score: {harmonic_tx.dissonance_score}")
        print(f"Fraud Probability: {harmonic_tx.fraud_probability}")
        print(f"Geometric Completion: {harmonic_tx.geometric_signature.completion_ratio}")
        print(f"Anomaly Flags: {harmonic_tx.anomaly_flags}")
        
        # Show chakra impact
        print("Chakra Impact:")
        for chakra, impact in harmonic_tx.chakra_impact.items():
            if impact > 0.1:  # Only show significant impacts
                print(f"  {chakra}: {impact}")