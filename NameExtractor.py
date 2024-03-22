import os
import fitz  # PyMuPDF
import re
import nltk
from nltk.corpus import stopwords

# Download NLTK stopwords if not already downloaded
nltk.download('stopwords')

def load_ignore_words(file_path):
    with open(file_path, 'r') as file:
        ignore_words = {line.strip().lower() for line in file}
    return ignore_words

def find_largest_font_line(pdf_path, ignore_words, max_lines=10):
    doc = fitz.open(pdf_path)
    largest_font_size = 0
    largest_font_line = ""

    # Regular expression pattern to match common website patterns
    website_pattern = r'\b(?:https?://|www\.)\S+\b'

    # Process only the first page
    page = doc.load_page(0)
    blocks = page.get_text("dict")["blocks"]

    line_count = 0  # Track the number of lines processed
    for b in blocks:
        for l in b.get("lines", []):
            line_text = ""
            font_sizes = []  # List to store font sizes in the line
            for s in l.get("spans", []):
                font_size = s["size"]
                text = s["text"]
                font_sizes.append(font_size)
                # Accumulate text for the line
                line_text += text
            
            # Check if any word in the line is in ignore_words or if the line contains a website pattern
            line_text = ' '.join(word for word in line_text.split() if word.lower() not in ignore_words and not re.match(website_pattern, word, re.IGNORECASE))

            # Check if line contains keywords like "Name" only in the first max_lines
            if line_count < max_lines and "name" in line_text.lower():
                return line_text.strip()  # Prioritize lines containing "Name"

            # Check if font size is bigger than the current largest
            if font_sizes and max(font_sizes) > largest_font_size and any(word.strip() for word in line_text.split()):
                largest_font_size = max(font_sizes)
                largest_font_line = line_text.strip()

            line_count += 1  # Increment line count after processing each line

    # Remove email addresses
    largest_font_line = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', largest_font_line)

    return largest_font_line



def process_pdfs_in_directory(directory_path, ignore_words):
    results = {}
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory_path, filename)
            largest_font_line = find_largest_font_line(pdf_path, ignore_words)
            # Remove everything except letters and spaces
            largest_font_line = re.sub(r'[^a-zA-Z\s]', '', largest_font_line)
            results[filename] = largest_font_line
    return results

# Example usage
directory_path = r'C:\Users\Prasen\Desktop\Internship\Project 1\Resume\Resume'  # Replace with the directory containing your PDF files
ignore_words_file_path = 'excluded_words.txt'  # Replace with the path to your ignore words file
ignore_words = load_ignore_words(ignore_words_file_path)

# Add NLTK English stopwords to ignore_words
english_stopwords = set(stopwords.words('english'))
ignore_words.update(english_stopwords)

results = process_pdfs_in_directory(directory_path, ignore_words)
for filename, largest_font_line in results.items():
    print(f"PDF: {filename}, Person Name is: {largest_font_line}")
