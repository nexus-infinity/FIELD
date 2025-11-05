#!/usr/bin/env python3
"""
🧠 NLP Installation Test & Demo
Verifies installation and demonstrates capabilities
"""

import sys
import importlib
from typing import Dict, List

def check_package(package_name: str, import_name: str = None) -> bool:
    """Check if a package is installed"""
    try:
        if import_name:
            importlib.import_module(import_name)
        else:
            importlib.import_module(package_name)
        return True
    except ImportError:
        return False

def test_installations():
    """Test all NLP package installations"""
    
    print("╔════════════════════════════════════════════╗")
    print("║    🧠 NLP INSTALLATION VERIFICATION 🧠      ║")
    print("╚════════════════════════════════════════════╝")
    print()
    
    packages = [
        ("nltk", None, "Natural Language Toolkit"),
        ("spacy", None, "Industrial-strength NLP"),
        ("textblob", None, "Simple text processing"),
        ("gensim", None, "Topic modeling"),
        ("transformers", None, "Hugging Face transformers"),
        ("sentence_transformers", "sentence_transformers", "Sentence embeddings"),
        ("langchain", None, "LLM framework"),
        ("textstat", None, "Text statistics"),
        ("wordcloud", None, "Word cloud generation"),
        ("langdetect", None, "Language detection"),
        ("ftfy", None, "Text encoding fixes"),
        ("fuzzywuzzy", "fuzzywuzzy", "Fuzzy string matching"),
    ]
    
    installed = []
    missing = []
    
    print("📦 Checking Core NLP Packages:")
    print("━" * 40)
    
    for package, import_name, description in packages:
        if check_package(package, import_name):
            print(f"✅ {package:20} - {description}")
            installed.append(package)
        else:
            print(f"❌ {package:20} - {description}")
            missing.append(package)
    
    print()
    print(f"Summary: {len(installed)}/{len(packages)} packages installed")
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Run: bash install_nlp_tools.sh")
        return False
    
    return True

def demo_nlp_capabilities():
    """Demonstrate NLP capabilities with examples"""
    
    print("\n" + "═" * 48)
    print("\n🎯 NLP CAPABILITIES DEMONSTRATION\n")
    print("═" * 48)
    
    sample_text = """
    The FIELD system harmonizes natural language processing with sacred geometry.
    This creates a resonant interface between human consciousness and machine intelligence.
    The sailing tools navigate through waves of meaning with 85% efficiency.
    """
    
    # 1. NLTK Demo
    try:
        import nltk
        from nltk.tokenize import word_tokenize, sent_tokenize
        from nltk.corpus import stopwords
        from nltk.sentiment.vader import SentimentIntensityAnalyzer
        
        print("\n1️⃣ NLTK Analysis:")
        print("─" * 40)
        
        # Tokenization
        sentences = sent_tokenize(sample_text)
        words = word_tokenize(sample_text)
        
        print(f"📝 Sentences: {len(sentences)}")
        print(f"📝 Words: {len(words)}")
        
        # Sentiment
        try:
            sia = SentimentIntensityAnalyzer()
            sentiment = sia.polarity_scores(sample_text)
            print(f"😊 Sentiment: {sentiment}")
        except:
            print("⚠️  Sentiment analyzer needs NLTK data")
        
    except ImportError:
        print("❌ NLTK not available")
    
    # 2. TextBlob Demo
    try:
        from textblob import TextBlob
        
        print("\n2️⃣ TextBlob Analysis:")
        print("─" * 40)
        
        blob = TextBlob(sample_text)
        print(f"🏷️  Noun phrases: {blob.noun_phrases[:5]}")
        print(f"😊 Polarity: {blob.sentiment.polarity:.2f}")
        print(f"📊 Subjectivity: {blob.sentiment.subjectivity:.2f}")
        
    except ImportError:
        print("❌ TextBlob not available")
    
    # 3. Language Detection
    try:
        from langdetect import detect, detect_langs
        
        print("\n3️⃣ Language Detection:")
        print("─" * 40)
        
        lang = detect(sample_text)
        lang_probs = detect_langs(sample_text)
        print(f"🌐 Detected language: {lang}")
        print(f"🎯 Confidence: {lang_probs}")
        
    except ImportError:
        print("❌ langdetect not available")
    
    # 4. Text Statistics
    try:
        import textstat
        
        print("\n4️⃣ Text Complexity Analysis:")
        print("─" * 40)
        
        print(f"📚 Flesch Reading Ease: {textstat.flesch_reading_ease(sample_text):.1f}")
        print(f"📊 Grade Level: {textstat.flesch_kincaid_grade(sample_text):.1f}")
        print(f"⏱️  Reading Time: {textstat.reading_time(sample_text, ms_per_char=14.69):.1f} seconds")
        
    except ImportError:
        print("❌ textstat not available")
    
    # 5. Fuzzy String Matching
    try:
        from fuzzywuzzy import fuzz, process
        
        print("\n5️⃣ Fuzzy String Matching:")
        print("─" * 40)
        
        choices = ["FIELD system", "sacred geometry", "sailing tools", "machine learning"]
        query = "FEILD systm"  # Intentional typos
        
        best_match = process.extractOne(query, choices)
        print(f"🔍 Query: '{query}'")
        print(f"✨ Best match: '{best_match[0]}' (confidence: {best_match[1]}%)")
        
    except ImportError:
        print("❌ fuzzywuzzy not available")
    
    # 6. Keyword Extraction
    try:
        from rake_nltk import Rake
        
        print("\n6️⃣ Keyword Extraction (RAKE):")
        print("─" * 40)
        
        rake = Rake()
        rake.extract_keywords_from_text(sample_text)
        keywords = rake.get_ranked_phrases()[:5]
        
        print("🔑 Top Keywords:")
        for i, keyword in enumerate(keywords, 1):
            print(f"   {i}. {keyword}")
            
    except ImportError:
        print("❌ rake-nltk not available")

def create_nlp_field_integration():
    """Create example of NLP integrated with FIELD system"""
    
    print("\n" + "═" * 48)
    print("\n🌌 FIELD-NLP INTEGRATION EXAMPLE\n")
    print("═" * 48)
    
    integration_code = '''
from dataclasses import dataclass
from typing import List, Dict
import json

@dataclass
class FieldNLPProcessor:
    """NLP Processor harmonized with FIELD sacred geometry"""
    
    def __init__(self):
        self.sacred_frequencies = {
            'root': 108,   # OM frequency
            'heart': 528,  # Love frequency
            'crown': 963,  # Divine connection
        }
        
    def harmonic_tokenize(self, text: str) -> List[str]:
        """Tokenize with harmonic resonance scoring"""
        # Your FIELD-aware tokenization logic here
        pass
        
    def sacred_sentiment(self, text: str) -> Dict:
        """Analyze sentiment through sacred geometry lens"""
        # Sentiment aligned with tetrahedral nodes
        pass
        
    def extract_field_entities(self, text: str) -> List:
        """Extract entities relevant to FIELD operations"""
        # Identify OB1, TATA, ATLAS, DOJO references
        pass

# Example usage:
processor = FieldNLPProcessor()
print("✨ FIELD-NLP Processor initialized")
print(f"🎵 Sacred frequencies: {list(processor.sacred_frequencies.keys())}")
'''
    
    print(integration_code)
    
    print("\n💡 Integration Ideas:")
    print("─" * 40)
    print("• Use NLP to analyze your code comments for harmonic patterns")
    print("• Extract sailing metaphors from documentation")
    print("• Sentiment analysis on git commit messages")
    print("• Auto-generate FIELD documentation from code")
    print("• Natural language queries to navigate your codebase")
    print("• Convert natural language to FIELD commands")

def main():
    """Main test runner"""
    
    # Test installations
    all_installed = test_installations()
    
    if all_installed:
        # Demo capabilities
        demo_nlp_capabilities()
        
        # Show integration example
        create_nlp_field_integration()
        
        print("\n" + "═" * 48)
        print("\n✨ All NLP tools are ready for FIELD integration!")
        print("\nNext steps:")
        print("  1. Run specific NLP analyses on your code")
        print("  2. Build natural language interfaces")
        print("  3. Create semantic code navigation")
        print("  4. Implement harmonic text processing")
        
    else:
        print("\n⚠️  Some packages are missing.")
        print("Run: bash install_nlp_tools.sh")
        sys.exit(1)

if __name__ == "__main__":
    main()
