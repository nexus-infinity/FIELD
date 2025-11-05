#!/bin/bash

echo "╔════════════════════════════════════════════╗"
echo "║   🧠 INSTALLING NLP TOOLS FOR FIELD 🧠     ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install with pip3
install_package() {
    local package=$1
    local description=$2
    echo -e "${BLUE}Installing ${package}...${NC} ${description}"
    pip3 install --upgrade "$package" --quiet
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ ${package} installed successfully${NC}"
    else
        echo -e "${RED}✗ Failed to install ${package}${NC}"
    fi
}

# Check for Python 3
if ! command_exists python3; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3 first.${NC}"
    exit 1
fi

# Check for pip3
if ! command_exists pip3; then
    echo -e "${YELLOW}pip3 not found. Installing pip...${NC}"
    python3 -m ensurepip --default-pip
fi

echo ""
echo "🔧 Upgrading pip first..."
pip3 install --upgrade pip --quiet

echo ""
echo "📦 Installing Core NLP Libraries..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Core NLP Libraries
install_package "nltk" "Natural Language Toolkit - comprehensive NLP library"
install_package "spacy" "Industrial-strength NLP with neural models"
install_package "textblob" "Simple API for common NLP tasks"
install_package "gensim" "Topic modeling and document similarity"

echo ""
echo "🧠 Installing Advanced NLP Tools..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Advanced NLP
install_package "transformers" "Hugging Face transformers for BERT, GPT, etc."
install_package "sentence-transformers" "Sentence embeddings and semantic search"
install_package "langchain" "Framework for LLM applications"
install_package "langchain-community" "Community integrations for LangChain"

echo ""
echo "📊 Installing Text Analysis Tools..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Text Analysis
install_package "textstat" "Text readability and complexity metrics"
install_package "wordcloud" "Generate word clouds from text"
install_package "pyLDAvis" "Interactive topic model visualization"
install_package "sumy" "Automatic text summarization"
install_package "rake-nltk" "Keyword extraction using RAKE algorithm"
install_package "yake" "Yet Another Keyword Extractor"

echo ""
echo "🌐 Installing Language Detection & Translation..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Language Tools
install_package "langdetect" "Language detection library"
install_package "googletrans==4.0.0rc1" "Google Translate API"
install_package "polyglot" "Multilingual NLP toolkit"

echo ""
echo "🔍 Installing Text Processing Utilities..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Text Processing
install_package "ftfy" "Fixes text encoding issues"
install_package "unidecode" "ASCII transliterations of Unicode"
install_package "python-Levenshtein" "Fast string matching"
install_package "fuzzywuzzy" "Fuzzy string matching"
install_package "jellyfish" "Phonetic encoding and string comparison"

echo ""
echo "🎯 Installing Named Entity Recognition..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# NER and Information Extraction
install_package "flashtext" "Fast keyword extraction and replacement"
install_package "dateparser" "Parse dates in any string format"
install_package "numerizer" "Convert natural language numbers to digits"

echo ""
echo "📈 Installing Sentiment Analysis..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Sentiment Analysis
install_package "vaderSentiment" "Sentiment analysis for social media"
install_package "afinn" "Simple sentiment analysis"

echo ""
echo "🔬 Installing Scientific NLP Tools..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Scientific NLP
install_package "scispacy" "SpaCy models for scientific text"
install_package "stanza" "Stanford NLP toolkit"

echo ""
echo "📚 Downloading NLTK Data..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Download essential NLTK data
python3 -c "
import nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download essential datasets
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('maxent_ne_chunker', quiet=True)
nltk.download('words', quiet=True)
nltk.download('vader_lexicon', quiet=True)
print('✓ NLTK data downloaded')
"

echo ""
echo "🤖 Downloading SpaCy Language Models..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Download SpaCy models
python3 -m spacy download en_core_web_sm --quiet 2>/dev/null && echo -e "${GREEN}✓ Small English model${NC}"
python3 -m spacy download en_core_web_md --quiet 2>/dev/null && echo -e "${GREEN}✓ Medium English model${NC}"

echo ""
echo "═══════════════════════════════════════════════"
echo ""
echo -e "${GREEN}✨ NLP Tools Installation Complete!${NC}"
echo ""
echo "Installed packages include:"
echo "  • NLTK - Natural Language Toolkit"
echo "  • SpaCy - Industrial NLP"
echo "  • Transformers - State-of-the-art models"
echo "  • LangChain - LLM application framework"
echo "  • TextBlob - Simple text processing"
echo "  • Gensim - Topic modeling"
echo "  • And many more specialized tools!"
echo ""
echo "To verify installation, run:"
echo "  python3 test_nlp_installation.py"
echo ""
