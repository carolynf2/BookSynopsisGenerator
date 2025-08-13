# Book Synopsis Generator

A Python application that generates book summaries using Markov chains and bigram analysis.

## Overview

This project implements a Markov chain-based text generator that creates book synopses by analyzing training data and learning word transition probabilities. The generator uses bigrams (sequences of two consecutive words) to predict what word comes next in a sequence.

## Features

### Core Functionality
- **Bigram Analysis**: Analyzes training text to build a dictionary of word transitions
- **Markov Chain Generation**: Uses probability-based word selection to generate new text
- **Training Data Statistics**: Provides insights into the analyzed text

### Improvements Over Basic Implementation

#### Text Start/End Improvements
- **Smart Starting Words**: Automatically identifies and uses sentence starters (capitalized words that follow punctuation)
- **Natural Endings**: Ensures generated text ends at natural sentence boundaries
- **Minimum Length Control**: Prevents premature ending before minimum word count is reached

#### Text Quality Improvements
- **Punctuation Handling**: Properly manages spacing around punctuation marks
- **Capitalization**: Ensures proper sentence capitalization
- **Multiple Generation**: Can generate multiple synopses for comparison
- **Length Control**: Configurable minimum and maximum synopsis lengths

## Usage

### Basic Usage

```python
from book_synopsis_generator import BookSynopsisGenerator

# Create generator
generator = BookSynopsisGenerator()

# Load training data
training_text = "Your book summaries here..."
generator.load_training_data(training_text)

# Generate a synopsis
synopsis = generator.generate_synopsis(max_length=50)
print(synopsis)
```

### Running the Demo

```bash
# Run the main interactive demo
python book_synopsis_generator.py

# Run the test script (non-interactive)
python test_book_synopsis.py
```

## Files

- `book_synopsis_generator.py` - Main implementation with interactive demo
- `test_book_synopsis.py` - Non-interactive test script
- `README.md` - This documentation file

## Example Output

```
Training Data Statistics:
Unique words: 143
Total word transitions: 203
Sentence starters: 11

Generated Book Synopses:
The brave young warrior embarked on a perilous journey through dangerous forests and treacherous mountains.

A tale of love and adventure unfolds in the mystical realm where magic is forbidden.

The last surviving member of an ancient order seeks revenge against those who betrayed her people.
```

## How It Works

1. **Training Phase**: 
   - Tokenizes input text into words
   - Creates bigram dictionary mapping each word to possible next words
   - Identifies sentence starters and common patterns

2. **Generation Phase**:
   - Starts with a smart sentence starter
   - Uses weighted random selection based on bigram frequencies
   - Continues until natural ending point or maximum length reached

3. **Post-Processing**:
   - Fixes punctuation and spacing
   - Ensures proper capitalization
   - Adds sentence ending if needed

## Customization

The generator can be customized by:
- Adjusting `max_length` and `min_length` parameters
- Modifying the training data
- Extending the post-processing rules
- Adding custom sentence starter/ender detection

## Educational Purpose

This project demonstrates:
- Markov chain probability models
- Natural language processing basics
- Python text processing techniques
- Probability-based text generation

While simpler than modern LLMs, it provides insights into how probability-based text generation works at a fundamental level.