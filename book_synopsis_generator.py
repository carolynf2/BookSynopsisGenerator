#!/usr/bin/env python3
"""
Book Synopsis Generator using Markov Chains

This program generates book summaries using a Markov chain model based on bigrams.
It analyzes training data to learn word transition probabilities and generates
new text that resembles the training data.
"""

import random
import re
from collections import defaultdict
from typing import Dict, List, Optional


class BookSynopsisGenerator:
    """A Markov chain-based text generator for book synopses."""
    
    def __init__(self):
        """Initialize the generator with empty bigram dictionary."""
        self.bigrams: Dict[str, List[str]] = defaultdict(list)
        self.sentence_starters: List[str] = []
        self.sentence_enders: set = {'.', '!', '?'}
        
    def load_training_data(self, text: str) -> None:
        """
        Load training data and build bigram dictionary.
        
        Args:
            text: Training text to analyze
        """
        # Clean and tokenize the text
        words = self._tokenize_text(text)
        
        # Build bigram dictionary
        for i in range(len(words) - 1):
            current_word = words[i]
            next_word = words[i + 1]
            self.bigrams[current_word].append(next_word)
            
            # Collect sentence starters (words that follow sentence endings)
            if i > 0 and any(words[i-1].endswith(end) for end in self.sentence_enders):
                if current_word[0].isupper():
                    self.sentence_starters.append(current_word)
        
        # Add the first word as a potential starter
        if words and words[0][0].isupper():
            self.sentence_starters.append(words[0])
    
    def _tokenize_text(self, text: str) -> List[str]:
        """
        Tokenize text into words while preserving punctuation.
        
        Args:
            text: Text to tokenize
            
        Returns:
            List of tokens
        """
        # Replace multiple spaces with single space and split
        text = re.sub(r'\s+', ' ', text.strip())
        # Split on spaces but keep punctuation attached to words
        words = text.split()
        return words
    
    def generate_synopsis(self, max_length: int = 100, min_length: int = 20) -> str:
        """
        Generate a book synopsis using the Markov chain.
        
        Args:
            max_length: Maximum number of words to generate
            min_length: Minimum number of words before allowing natural endings
            
        Returns:
            Generated synopsis text
        """
        if not self.bigrams:
            return "No training data available."
        
        # Start with a good sentence starter
        current_word = self._choose_starting_word()
        synopsis = [current_word]
        
        for i in range(max_length - 1):
            # Get possible next words
            next_words = self.bigrams.get(current_word, [])
            
            if not next_words:
                # No more transitions possible
                break
            
            # Choose next word based on probability (frequency)
            next_word = random.choice(next_words)
            synopsis.append(next_word)
            
            # Check for natural ending after minimum length
            if (i >= min_length - 1 and 
                any(word.endswith(end) for end in self.sentence_enders for word in [next_word])):
                break
            
            current_word = next_word
        
        # Post-process the text
        result = ' '.join(synopsis)
        return self._post_process_text(result)
    
    def _choose_starting_word(self) -> str:
        """
        Choose a good starting word for the synopsis.
        
        Returns:
            Starting word
        """
        if self.sentence_starters:
            return random.choice(self.sentence_starters)
        elif self.bigrams:
            # Fallback to any word that starts with capital letter
            capitalized_words = [word for word in self.bigrams.keys() 
                               if word and word[0].isupper()]
            if capitalized_words:
                return random.choice(capitalized_words)
            else:
                return random.choice(list(self.bigrams.keys()))
        else:
            return "The"
    
    def _post_process_text(self, text: str) -> str:
        """
        Post-process generated text to improve quality.
        
        Args:
            text: Raw generated text
            
        Returns:
            Improved text
        """
        # Ensure proper sentence ending if not present
        if text and not any(text.endswith(end) for end in self.sentence_enders):
            text += "."
        
        # Fix spacing around punctuation
        text = re.sub(r'\s+([.!?,:;])', r'\1', text)
        text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)
        
        # Ensure first word is capitalized
        if text:
            text = text[0].upper() + text[1:] if len(text) > 1 else text.upper()
        
        return text
    
    def print_bigram_sample(self, sample_size: int = 10) -> None:
        """
        Print a sample of the bigram dictionary for inspection.
        
        Args:
            sample_size: Number of bigrams to display
        """
        print("Sample of bigrams dictionary:")
        items = list(self.bigrams.items())[:sample_size]
        for word, next_words in items:
            print(f'"{word}": {next_words[:10]}{"..." if len(next_words) > 10 else ""}')
        print()
    
    def generate_multiple_synopses(self, count: int = 5, max_length: int = 100) -> List[str]:
        """
        Generate multiple synopses and return the best one based on simple heuristics.
        
        Args:
            count: Number of synopses to generate
            max_length: Maximum length for each synopsis
            
        Returns:
            List of generated synopses
        """
        synopses = []
        for _ in range(count):
            synopsis = self.generate_synopsis(max_length)
            synopses.append(synopsis)
        return synopses
    
    def get_stats(self) -> Dict[str, int]:
        """
        Get statistics about the training data.
        
        Returns:
            Dictionary with statistics
        """
        total_words = len(self.bigrams)
        total_transitions = sum(len(transitions) for transitions in self.bigrams.values())
        
        return {
            'unique_words': total_words,
            'total_transitions': total_transitions,
            'sentence_starters': len(set(self.sentence_starters))
        }


def main():
    """Main function to demonstrate the book synopsis generator."""
    
    # Sample training data (book summaries)
    training_data = """
    The brave young warrior embarked on a perilous journey to save the kingdom. 
    Against all odds, she fought against ancient evil forces that threatened the land.
    The magical sword glowed with power as she faced the dark sorcerer in battle.
    
    A tale of love and adventure unfolds in the mystical realm of dragons and wizards.
    The prince must rescue the princess from the tower where she has been imprisoned.
    Evil creatures lurk in the shadows, waiting to prevent the hero from succeeding.
    
    In a world where magic is forbidden, a young girl discovers her hidden powers.
    She must learn to control her abilities while avoiding the king's guards.
    The fate of the kingdom rests in her hands as she prepares for the final confrontation.
    
    Two unlikely friends join forces to defeat the tyrant who rules their homeland.
    Their adventure takes them through dangerous forests and treacherous mountains.
    Only together can they hope to restore peace to their war-torn country.
    
    The last surviving member of an ancient order seeks revenge against those who betrayed her people.
    Armed with legendary weapons and forgotten spells, she begins her quest for justice.
    Dark secrets from the past threaten to consume her as she walks the path of vengeance.
    """
    
    # Create generator and load training data
    generator = BookSynopsisGenerator()
    generator.load_training_data(training_data)
    
    # Show statistics
    stats = generator.get_stats()
    print("Training Data Statistics:")
    print(f"Unique words: {stats['unique_words']}")
    print(f"Total word transitions: {stats['total_transitions']}")
    print(f"Sentence starters: {stats['sentence_starters']}")
    print()
    
    # Print sample of bigrams
    generator.print_bigram_sample()
    
    # Generate multiple synopses
    print("Generated Book Synopses:")
    print("-" * 50)
    
    synopses = generator.generate_multiple_synopses(count=5, max_length=80)
    for i, synopsis in enumerate(synopses, 1):
        print(f"Synopsis {i}:")
        print(synopsis)
        print()
    
    # Interactive mode
    print("Interactive Mode - Press Enter to generate new synopses (type 'quit' to exit):")
    while True:
        user_input = input("\nPress Enter for new synopsis: ").strip().lower()
        if user_input in ['quit', 'exit', 'q']:
            break
        
        new_synopsis = generator.generate_synopsis(max_length=60)
        print("New synopsis:")
        print(new_synopsis)


if __name__ == "__main__":
    main()