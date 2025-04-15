#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vietnamese Corpus Filter
------------------------
A tool to filter Vietnamese text by removing sentences containing abbreviations or English words.
"""

import argparse
import re
import os
import logging
import string

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def is_abbreviation(word):
    """
    Check if a word is an abbreviation.
    
    Rules:
    1. All uppercase words with 2+ characters (e.g., NBA, FLC)
    2. Words with periods between letters (e.g., U.S.A)
    3. Mixed case words where uppercase letters aren't just at the beginning (e.g., iPhone, MacBook)
    """
    # Rule 1: All uppercase with 2+ characters
    if len(word) >= 2 and word.isupper():
        return True
    
    # Rule 2: Contains periods between letters
    if "." in word and not word.endswith("."):
        # Check if it's a pattern like U.S.A or etc.
        if re.match(r'[A-Za-z](\.[A-Za-z])+\.?', word):
            return True
    
    # Rule 3: Mixed case (camelCase or PascalCase)
    if len(word) >= 2 and not word.islower() and not word.isupper():
        # If there's an uppercase letter not at the start, it's likely an abbreviation
        # or proper noun with special formatting
        if any(c.isupper() for c in word[1:]):
            return True
    
    return False

def is_english_word(word):
    """
    Check if a word is likely English rather than Vietnamese.
    
    This is a simple heuristic based on character patterns:
    - Vietnamese uses special diacritics
    - English only uses ASCII letters
    
    We count a word as English if it uses only English letters (a-z)
    and doesn't contain Vietnamese diacritics.
    """
    # Strip punctuation
    word = re.sub(r'[^\w\s]', '', word)
    
    # Skip empty strings or single letters
    if len(word) <= 1:
        return False
        
    # Skip numbers
    if word.isdigit():
        return False
    
    # Vietnamese diacritics and special characters
    vietnamese_chars = 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ'
    vietnamese_chars += vietnamese_chars.upper()
    
    # Check if the word contains only ASCII letters (a-z, A-Z)
    if word.isalpha() and all(c.lower() in string.ascii_lowercase for c in word):
        # Check if it doesn't contain any Vietnamese characters
        if not any(c in vietnamese_chars for c in word):
            # Words of length 2-3 are often abbreviations in Vietnamese context
            # rather than English words, so we're more strict with them
            if len(word) <= 3:
                # Common Vietnamese short words that might be mistaken as English
                vietnamese_short_words = ['xe', 'me', 'be', 'to', 'va', 'la', 'do', 'ba', 'an', 'bo', 'ca', 'he']
                if word.lower() in vietnamese_short_words:
                    return False
                    
            return True
    
    return False

def segment_sentences(text):
    """
    Simple Vietnamese sentence segmentation.
    Split text into sentences based on punctuation marks followed by spaces or newlines.
    """
    # Pattern: One or more sentence-ending punctuation followed by whitespace or end of string
    pattern = r'([.!?;…][\s\n]+|[.!?;…]$)'
    sentences = re.split(pattern, text)
    
    # Combine sentences with their punctuation
    result = []
    for i in range(0, len(sentences), 2):
        if i+1 < len(sentences):
            result.append(sentences[i] + sentences[i+1])
        else:
            result.append(sentences[i])
    
    # Filter out empty strings
    return [s.strip() for s in result if s.strip()]

def contains_abbreviation_or_english(sentence):
    """
    Check if a sentence contains abbreviations or English words.
    """
    # Split into words, handling punctuation
    words = re.findall(r'\b\w+[\.\w]*\b', sentence)
    
    for word in words:
        if is_abbreviation(word):
            logger.debug(f"Abbreviation found: {word}")
            return True
        
        if is_english_word(word):
            logger.debug(f"English word found: {word}")
            return True
    
    return False

def filter_corpus(input_file, output_file):
    """
    Filter the corpus by removing sentences with abbreviations or English words.
    """
    try:
        # Read the input file with UTF-8 encoding
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split content into paragraphs (preserving structure)
        paragraphs = content.split('\n\n')
        filtered_paragraphs = []
        
        total_sentences = 0
        removed_sentences = 0
        
        for paragraph in paragraphs:
            if not paragraph.strip():
                filtered_paragraphs.append(paragraph)
                continue
                
            sentences = segment_sentences(paragraph)
            total_sentences += len(sentences)
            
            # Filter sentences
            filtered_sentences = []
            for sentence in sentences:
                if not sentence.strip():
                    continue
                    
                if contains_abbreviation_or_english(sentence):
                    removed_sentences += 1
                    logger.debug(f"Removing: {sentence}")
                else:
                    filtered_sentences.append(sentence)
            
            # Reconstruct the paragraph
            if filtered_sentences:
                filtered_paragraph = ' '.join(filtered_sentences)
                filtered_paragraphs.append(filtered_paragraph)
            
        # Join paragraphs with double newlines to preserve structure
        filtered_content = '\n\n'.join(filtered_paragraphs)
        
        # Write the filtered content to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(filtered_content)
        
        logger.info(f"Filtering complete. Processed {total_sentences} sentences, removed {removed_sentences} sentences.")
        logger.info(f"Filtered content written to: {output_file}")
        
    except Exception as e:
        logger.error(f"Error filtering corpus: {str(e)}")
        raise

def main():
    """
    Main function to parse arguments and run the filter.
    """
    parser = argparse.ArgumentParser(description='Filter Vietnamese corpus by removing sentences with abbreviations or English words.')
    parser.add_argument('input_file', help='Path to the input text file (UTF-8 encoded)')
    parser.add_argument('-o', '--output', help='Path to the output file (default: input_file_filtered.txt)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Determine output file name
    if args.output:
        output_file = args.output
    else:
        base_name, ext = os.path.splitext(args.input_file)
        output_file = f"{base_name}_filtered{ext}"
    
    # Check if input file exists
    if not os.path.exists(args.input_file):
        logger.error(f"Input file does not exist: {args.input_file}")
        return 1
    
    logger.info(f"Starting to filter: {args.input_file}")
    filter_corpus(args.input_file, output_file)
    
    return 0

if __name__ == "__main__":
    exit(main())
