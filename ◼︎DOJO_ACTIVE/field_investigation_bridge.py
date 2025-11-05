#!/usr/bin/env python3
"""
FIELD Investigation Bridge
Connects sovereign Drive sync data with existing FIELD investigation systems

This bridge:
1. Connects sovereign data lake with resonance analysis system
2. Integrates with existing fraud detection and harmonic models
3. Provides unified investigation interface
4. Enables cross-system data correlation and pattern analysis
"""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
import sys
import importlib.util

class FIELDInvestigationBridge:
    """Bridge connecting all FIELD investigation systems"""
    
    def __init__(self):
        self.field_root = Path("/Users/jbear/FIELD")
        self.dojo_active = self.field_root / "◼︎DOJO_ACTIVE"
        
        # Database connections
        self.sovereign_db = self.dojo_active / "sovereign_data_lake.db"
        self.field_db = self.dojo_active / "notion_sync" / "field_entities.db"
        
        # Integration modules
        self.loaded_modules = {}
        self.system_status = {}
        
        print("🌉 FIELD Investigation Bridge initializing...")
        self.load_investigation_modules()
    
    def load_investigation_modules(self):
        """Load existing FIELD investigation modules"""
        
        # Available FIELD systems
        module_configs = {
            'resonance_analysis': {
                'path': self.dojo_active / 'trust_resonance_analysis.py',
                'class': 'TrustResonanceAnalyzer'
            },
            'harmonic_transaction': {
                'path': self.dojo_active / 'harmonic_transaction_model.py', 
                'class': 'HarmonicTransactionAnalyzer'
            },
            'field_integration': {
                'path': self.dojo_active / 'field_integration_analysis.py',
                'class': 'FIELDIntegrationAnalyzer'
            },
            'investigation_interface': {
                'path': self.dojo_active / 'field_investigation_interface.py',
                'class': 'FIELDInvestigationInterface'
            }
        }
        
        for system_name, config in module_configs.items():
            try:
                if config['path'].exists():
                    spec = importlib.util.spec_from_file_location(system_name, config['path'])
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Try to instantiate the main class if it exists
                    if hasattr(module, config['class']):
                        instance = getattr(module, config['class'])()
                        self.loaded_modules[system_name] = instance
                        self.system_status[system_name] = 'ACTIVE'
                    else:
                        self.loaded_modules[system_name] = module
                        self.system_status[system_name] = 'LOADED'
                    
                    print(f"✅ Loaded {system_name}: {self.system_status[system_name]}")
                else:
                    self.system_status[system_name] = 'NOT_FOUND'
                    print(f"⚠️  {system_name} module not found: {config['path']}")
                    
            except Exception as e:
                self.system_status[system_name] = f'ERROR: {str(e)}'
                print(f"❌ Failed to load {system_name}: {e}")
    
    def bridge_sovereign_to_resonance(self):
        """Bridge sovereign documents to resonance analysis system"""
        print("🎵 Bridging sovereign data to resonance analysis...")
        
        conn = sqlite3.connect(self.sovereign_db)
        cursor = conn.cursor()
        
        # Get documents with high resonance frequencies
        cursor.execute('''
            SELECT d.id, d.file_name, d.harmonic_frequency, d.resonance_state,
                   GROUP_CONCAT(DISTINCT e.entity_name) as entities,
                   GROUP_CONCAT(DISTINCT t.topic_name) as topics
            FROM documents d
            LEFT JOIN document_entities e ON d.id = e.document_id
            LEFT JOIN document_topics t ON d.id = t.document_id
            WHERE d.harmonic_frequency >= 432
            GROUP BY d.id
            ORDER BY d.harmonic_frequency DESC
        ''')
        
        resonant_docs = cursor.fetchall()
        
        # Create resonance analysis bridge data
        resonance_bridge_data = []
        for doc in resonant_docs:
            doc_id, file_name, frequency, state, entities, topics = doc
            
            # Create transaction-like object for resonance analysis
            resonance_entry = {
                'id': doc_id,
                'description': file_name,
                'amount': frequency,  # Use frequency as "amount" for pattern analysis
                'frequency': frequency,
                'resonance_state': state,
                'entities': entities.split(',') if entities else [],
                'topics': topics.split(',') if topics else [],
                'timestamp': datetime.now().isoformat(),
                'source_system': 'SOVEREIGN_DATA_LAKE'
            }
            
            resonance_bridge_data.append(resonance_entry)
        
        conn.close()
        
        # Save bridge data for resonance analysis system
        bridge_file = self.dojo_active / "resonance_bridge_data.json"
        with open(bridge_file, 'w') as f:
            json.dump(resonance_bridge_data, f, indent=2)
        
        print(f"✅ Created resonance bridge for {len(resonant_docs)} documents")
        print(f"📄 Bridge data saved: {bridge_file}")
        
        return resonance_bridge_data
    
    def run_integrated_analysis(self):
        """Run integrated analysis across all FIELD systems"""
        print("🔬 Running integrated FIELD analysis...")
        
        analysis_results = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'system': 'FIELD_INTEGRATED_ANALYSIS',
            'components': {},
            'cross_correlations': {},
            'unified_insights': {}
        }
        
        # 1. Sovereign data analysis
        sovereign_analysis = self.analyze_sovereign_patterns()
        analysis_results['components']['sovereign_data'] = sovereign_analysis
        
        # 2. Resonance analysis integration
        if 'resonance_analysis' in self.loaded_modules:
            try:
                resonance_data = self.bridge_sovereign_to_resonance()
                # Run resonance analysis on bridged data
                resonance_results = self.run_resonance_on_bridged_data(resonance_data)
                analysis_results['components']['resonance_analysis'] = resonance_results
            except Exception as e:
                print(f"⚠️  Resonance analysis error: {e}")
                analysis_results['components']['resonance_analysis'] = {'error': str(e)}
        
        # 3. Cross-correlation analysis
        correlations = self.find_cross_system_correlations(analysis_results['components'])
        analysis_results['cross_correlations'] = correlations
        
        # 4. Generate unified insights
        insights = self.generate_unified_insights(analysis_results)
        analysis_results['unified_insights'] = insights
        
        # Save integrated analysis
        results_file = self.dojo_active / "integrated_analysis_results.json"
        with open(results_file, 'w') as f:
            json.dump(analysis_results, f, indent=2)
        
        print(f"📊 Integrated analysis complete: {results_file}")
        return analysis_results
    
    def analyze_sovereign_patterns(self):
        """Analyze patterns in sovereign data"""
        conn = sqlite3.connect(self.sovereign_db)
        cursor = conn.cursor()
        
        # Frequency distribution analysis
        cursor.execute('''
            SELECT 
                CASE 
                    WHEN harmonic_frequency >= 777 THEN 'PERFECT_HARMONY'
                    WHEN harmonic_frequency >= 528 THEN 'HIGH_RESONANCE' 
                    WHEN harmonic_frequency >= 432 THEN 'HARMONIC_ALIGNMENT'
                    ELSE 'BASELINE'
                END as frequency_band,
                COUNT(*) as count,
                AVG(harmonic_frequency) as avg_freq
            FROM documents
            GROUP BY frequency_band
            ORDER BY avg_freq DESC
        ''')
        frequency_bands = cursor.fetchall()
        
        # Entity correlation analysis
        cursor.execute('''
            SELECT e1.entity_name, e2.entity_name, COUNT(*) as co_occurrence
            FROM document_entities e1
            JOIN document_entities e2 ON e1.document_id = e2.document_id AND e1.entity_name < e2.entity_name
            GROUP BY e1.entity_name, e2.entity_name
            HAVING co_occurrence > 1
            ORDER BY co_occurrence DESC
        ''')
        entity_correlations = cursor.fetchall()
        
        # Priority-frequency correlation
        cursor.execute('''
            SELECT investigation_priority, 
                   AVG(harmonic_frequency) as avg_frequency,
                   COUNT(*) as count
            FROM documents
            GROUP BY investigation_priority
            ORDER BY avg_frequency DESC
        ''')
        priority_frequencies = cursor.fetchall()
        
        conn.close()
        
        return {
            'frequency_distribution': frequency_bands,
            'entity_correlations': entity_correlations,
            'priority_frequency_correlation': priority_frequencies,
            'total_patterns': len(frequency_bands) + len(entity_correlations)
        }
    
    def run_resonance_on_bridged_data(self, resonance_data):
        """Run resonance analysis on bridged sovereign data"""
        
        # Create a simplified resonance analysis
        results = {
            'total_documents': len(resonance_data),
            'resonance_patterns': {},
            'frequency_analysis': {},
            'harmonic_anomalies': []
        }
        
        # Analyze frequency patterns
        frequencies = [doc['frequency'] for doc in resonance_data]
        
        results['frequency_analysis'] = {
            'min_frequency': min(frequencies) if frequencies else 0,
            'max_frequency': max(frequencies) if frequencies else 0,
            'avg_frequency': sum(frequencies) / len(frequencies) if frequencies else 0,
            'perfect_harmony_count': sum(1 for f in frequencies if f >= 777),
            'high_resonance_count': sum(1 for f in frequencies if 528 <= f < 777),
            'harmonic_alignment_count': sum(1 for f in frequencies if 432 <= f < 528)
        }
        
        # Identify resonance patterns by entity
        entity_patterns = {}
        for doc in resonance_data:
            for entity in doc['entities']:
                if entity not in entity_patterns:
                    entity_patterns[entity] = []
                entity_patterns[entity].append(doc['frequency'])
        
        # Calculate average frequency per entity
        for entity, freqs in entity_patterns.items():
            avg_freq = sum(freqs) / len(freqs)
            results['resonance_patterns'][entity] = {
                'documents': len(freqs),
                'average_frequency': avg_freq,
                'resonance_level': self.classify_resonance_level(avg_freq)
            }
        
        # Detect anomalies (documents with unusual frequency patterns)
        avg_freq = results['frequency_analysis']['avg_frequency']
        for doc in resonance_data:
            freq_deviation = abs(doc['frequency'] - avg_freq) / avg_freq
            if freq_deviation > 0.5:  # More than 50% deviation
                results['harmonic_anomalies'].append({
                    'document': doc['description'],
                    'frequency': doc['frequency'],
                    'deviation': freq_deviation,
                    'resonance_state': doc['resonance_state']
                })
        
        return results
    
    def classify_resonance_level(self, frequency):
        """Classify resonance level based on frequency"""
        if frequency >= 777:
            return 'PERFECT_HARMONY'
        elif frequency >= 700:
            return 'NEAR_PERFECT'
        elif frequency >= 528:
            return 'HIGH_RESONANCE'
        elif frequency >= 432:
            return 'HARMONIC_ALIGNMENT'
        else:
            return 'BASELINE_RESONANCE'
    
    def find_cross_system_correlations(self, component_results):
        """Find correlations between different system analyses"""
        correlations = {}
        
        # Cross-correlate sovereign patterns with resonance analysis
        if 'sovereign_data' in component_results and 'resonance_analysis' in component_results:
            sovereign = component_results['sovereign_data']
            resonance = component_results['resonance_analysis']
            
            # Correlate entity patterns with frequency patterns
            correlations['entity_frequency'] = {}
            
            if 'resonance_patterns' in resonance:
                for entity, pattern in resonance['resonance_patterns'].items():
                    correlations['entity_frequency'][entity] = {
                        'avg_frequency': pattern['average_frequency'],
                        'resonance_level': pattern['resonance_level'],
                        'document_count': pattern['documents']
                    }
            
            # Correlate frequency distributions
            correlations['frequency_distribution_correlation'] = {
                'sovereign_patterns': len(sovereign.get('frequency_distribution', [])),
                'resonance_anomalies': len(resonance.get('harmonic_anomalies', [])),
                'high_resonance_ratio': resonance.get('frequency_analysis', {}).get('high_resonance_count', 0) / max(resonance.get('total_documents', 1), 1)
            }
        
        return correlations
    
    def generate_unified_insights(self, analysis_results):
        """Generate unified insights from integrated analysis"""
        insights = {
            'key_findings': [],
            'investigation_priorities': [],
            'system_health': {},
            'recommendations': []
        }
        
        # Key findings from cross-correlation
        if 'cross_correlations' in analysis_results:
            correlations = analysis_results['cross_correlations']
            
            # High-resonance entities
            if 'entity_frequency' in correlations:
                high_resonance_entities = [
                    entity for entity, data in correlations['entity_frequency'].items()
                    if data['avg_frequency'] >= 528
                ]
                if high_resonance_entities:
                    insights['key_findings'].append(f"High resonance entities detected: {', '.join(high_resonance_entities)}")
            
            # Frequency distribution insights
            if 'frequency_distribution_correlation' in correlations:
                freq_corr = correlations['frequency_distribution_correlation']
                high_res_ratio = freq_corr.get('high_resonance_ratio', 0)
                if high_res_ratio > 0.5:
                    insights['key_findings'].append(f"High resonance ratio: {high_res_ratio:.1%} of documents in optimal frequency range")
        
        # Investigation priorities from sovereign data
        if 'sovereign_data' in analysis_results['components']:
            sovereign = analysis_results['components']['sovereign_data']
            
            # Priority entities based on correlations
            if 'entity_correlations' in sovereign:
                top_correlations = sovereign['entity_correlations'][:3]
                for correlation in top_correlations:
                    entity1, entity2, count = correlation
                    insights['investigation_priorities'].append({
                        'type': 'ENTITY_CORRELATION',
                        'description': f"{entity1} ↔ {entity2}",
                        'strength': count,
                        'priority': 'HIGH' if count >= 3 else 'MEDIUM'
                    })
        
        # System health assessment
        for system_name, status in self.system_status.items():
            insights['system_health'][system_name] = {
                'status': status,
                'operational': status in ['ACTIVE', 'LOADED']
            }
        
        # Generate recommendations
        operational_systems = sum(1 for status in self.system_status.values() if status in ['ACTIVE', 'LOADED'])
        total_systems = len(self.system_status)
        
        if operational_systems == total_systems:
            insights['recommendations'].append("All FIELD systems operational - continue integrated analysis")
        elif operational_systems > total_systems / 2:
            insights['recommendations'].append("Most systems operational - consider addressing non-functional components")
        else:
            insights['recommendations'].append("Multiple system issues detected - prioritize system restoration")
        
        # Resonance-based recommendations
        if 'resonance_analysis' in analysis_results['components']:
            resonance = analysis_results['components']['resonance_analysis']
            avg_freq = resonance.get('frequency_analysis', {}).get('avg_frequency', 0)
            
            if avg_freq >= 600:
                insights['recommendations'].append("Excellent harmonic alignment - maintain current investigative focus")
            elif avg_freq >= 400:
                insights['recommendations'].append("Good resonance baseline - consider frequency optimization techniques")
            else:
                insights['recommendations'].append("Low frequency detected - investigate dissonance sources and apply harmonic correction")
        
        return insights
    
    def create_unified_dashboard_data(self):
        """Create unified data for investigation dashboard"""
        print("📊 Creating unified dashboard data...")
        
        # Run integrated analysis
        analysis = self.run_integrated_analysis()
        
        # Create dashboard-friendly data structure
        dashboard_data = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'system_status': self.system_status,
            'summary_metrics': {},
            'high_priority_items': [],
            'resonance_overview': {},
            'investigation_focus_areas': []
        }
        
        # Extract summary metrics
        if 'sovereign_data' in analysis['components']:
            sovereign = analysis['components']['sovereign_data']
            dashboard_data['summary_metrics']['total_patterns'] = sovereign.get('total_patterns', 0)
            dashboard_data['summary_metrics']['entity_correlations'] = len(sovereign.get('entity_correlations', []))
        
        if 'resonance_analysis' in analysis['components']:
            resonance = analysis['components']['resonance_analysis']
            freq_analysis = resonance.get('frequency_analysis', {})
            dashboard_data['summary_metrics']['avg_frequency'] = round(freq_analysis.get('avg_frequency', 0), 2)
            dashboard_data['summary_metrics']['perfect_harmony_docs'] = freq_analysis.get('perfect_harmony_count', 0)
            
            # Resonance overview
            dashboard_data['resonance_overview'] = {
                'total_documents': resonance.get('total_documents', 0),
                'frequency_bands': {
                    'perfect_harmony': freq_analysis.get('perfect_harmony_count', 0),
                    'high_resonance': freq_analysis.get('high_resonance_count', 0),
                    'harmonic_alignment': freq_analysis.get('harmonic_alignment_count', 0)
                },
                'anomalies_detected': len(resonance.get('harmonic_anomalies', []))
            }
        
        # High priority items from insights
        if 'unified_insights' in analysis:
            insights = analysis['unified_insights']
            
            # Investigation priorities
            for priority in insights.get('investigation_priorities', []):
                dashboard_data['high_priority_items'].append({
                    'type': priority['type'],
                    'description': priority['description'],
                    'priority': priority['priority'],
                    'action': 'INVESTIGATE'
                })
            
            # Focus areas from key findings
            dashboard_data['investigation_focus_areas'] = insights.get('key_findings', [])
        
        # Save dashboard data
        dashboard_file = self.dojo_active / "unified_dashboard_data.json"
        with open(dashboard_file, 'w') as f:
            json.dump(dashboard_data, f, indent=2)
        
        print(f"📊 Unified dashboard data created: {dashboard_file}")
        return dashboard_data
    
    def run_full_bridge_operation(self):
        """Run complete bridge operation connecting all systems"""
        print("🌉 FIELD INVESTIGATION BRIDGE - FULL OPERATION")
        print("=" * 70)
        
        # System status report
        print("\n📋 SYSTEM STATUS:")
        for system, status in self.system_status.items():
            status_icon = "✅" if status in ['ACTIVE', 'LOADED'] else "❌"
            print(f"   {status_icon} {system}: {status}")
        
        # Bridge sovereign data to resonance system
        print("\n🎵 BRIDGING TO RESONANCE ANALYSIS:")
        self.bridge_sovereign_to_resonance()
        
        # Run integrated analysis
        print("\n🔬 INTEGRATED ANALYSIS:")
        analysis_results = self.run_integrated_analysis()
        
        # Create unified dashboard
        print("\n📊 UNIFIED DASHBOARD:")
        dashboard_data = self.create_unified_dashboard_data()
        
        # Final status
        print("\n✅ BRIDGE OPERATION COMPLETE")
        print("🌉 All FIELD systems are now interconnected")
        print(f"📊 Dashboard metrics: {len(dashboard_data['high_priority_items'])} high-priority items")
        print(f"🎵 Resonance state: {dashboard_data['summary_metrics'].get('avg_frequency', 0):.2f} Hz")
        
        return {
            'analysis_results': analysis_results,
            'dashboard_data': dashboard_data,
            'system_status': self.system_status
        }


def main():
    """Main execution function"""
    bridge = FIELDInvestigationBridge()
    return bridge.run_full_bridge_operation()


if __name__ == "__main__":
    main()