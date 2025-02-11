import fitz  # PyMuPDF
import os
import re
import sys

# Increase recursion limit
sys.setrecursionlimit(10000)

def clean_text(text):
    """Clean text from unwanted characters and normalize whitespace."""
    # Remove multiple newlines while preserving paragraph structure
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Remove multiple spaces
    text = re.sub(r' +', ' ', text)
    # Clean special characters while preserving essential punctuation
    text = re.sub(r'[^\w\s.,!?;:()/-]', '', text)
    # Normalize line endings
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    return text.strip()

def find_split_position(text, target_pos):
    """Find the best position to split text with priorities."""
    # Header patterns
    header_patterns = [
        r'^[IVX]+\.',      # Roman numerals
        r'^\d+\.',         # Numbers
        r'^[A-Z]\.',       # Capital letters
        r'^\d+\.\d+',      # Sub-numbers
    ]
    
    # Look for headers near target_pos
    text_before = text[:target_pos].split('\n')
    text_after = text[target_pos:target_pos + 500].split('\n')
    
    # Check headers before target
    current_pos = 0
    for line in text_before:
        if any(re.match(pattern, line.strip()) for pattern in header_patterns):
            last_header_pos = current_pos
        current_pos += len(line) + 1
    
    # Check headers after target
    current_pos = target_pos
    for line in text_after:
        if any(re.match(pattern, line.strip()) for pattern in header_patterns):
            return current_pos
        current_pos += len(line) + 1
    
    # Look for paragraph breaks
    paragraph_end = text[:target_pos].rfind('\n\n')
    if paragraph_end != -1 and paragraph_end > target_pos - 500:
        return paragraph_end
    
    # Look for sentence endings
    sentence_matches = list(re.finditer(r'[.!?]\s+(?=[A-Z])', text[:target_pos + 500]))
    if sentence_matches:
        # Find the closest sentence end to target_pos
        closest_match = min(sentence_matches, 
                          key=lambda x: abs(x.end() - target_pos))
        return closest_match.end()
    
    return target_pos

def recursive_character_chunking(text, min_chunk_size=300, max_chunk_size=2000, depth=0):
    """Split text into chunks using optimized recursive approach."""
    if depth > 100 or len(text) <= max_chunk_size:
        return [clean_text(text)]
    
    target_pos = len(text) // 2
    split_pos = find_split_position(text, target_pos)
    
    # Ensure split position is reasonable
    if split_pos < len(text) * 0.2 or split_pos > len(text) * 0.8:
        split_pos = target_pos
    
    chunk1 = clean_text(text[:split_pos])
    chunk2 = clean_text(text[split_pos:])
    
    result = []
    
    # Process chunks
    if len(chunk1) > max_chunk_size:
        result.extend(recursive_character_chunking(chunk1, min_chunk_size, max_chunk_size, depth + 1))
    elif len(chunk1) >= min_chunk_size:
        result.append(chunk1)
    
    if len(chunk2) > max_chunk_size:
        result.extend(recursive_character_chunking(chunk2, min_chunk_size, max_chunk_size, depth + 1))
    elif len(chunk2) >= min_chunk_size:
        result.append(chunk2)
    
    return result

def load_pdf_text(pdf_path):
    """Load and extract text from PDF with improved formatting."""
    try:
        doc = fitz.open(pdf_path)
        text_blocks = []
        
        for page in doc:
            # Get text with blocks formatting
            blocks = page.get_text("blocks")
            # Sort blocks by vertical position then horizontal
            blocks.sort(key=lambda b: (b[1], b[0]))
            # Extract text from blocks
            page_text = "\n".join(block[4] for block in blocks)
            text_blocks.append(page_text)
            
        return "\n\n".join(text_blocks)
    except Exception as e:
        print(f"Error loading PDF: {e}")
        return ""

def save_chunks(chunks, output_folder):
    """Save chunks to files."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for i, chunk in enumerate(chunks, 1):
        chunk_filename = f"{output_folder}/chunk_{i:03d}.txt"
        with open(chunk_filename, 'w', encoding='utf-8') as f:
            f.write(chunk.strip() + "\n")

def save_summary(chunks, output_folder):
    """Save summary information about the chunks."""
    summary_file = os.path.join(output_folder, "summary.txt")
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"Total chunks: {len(chunks)}\n\n")
        
        for i, chunk in enumerate(chunks, 1):
            f.write(f"Chunk {i:03d}:\n")
            f.write(f"Characters: {len(chunk)}\n")
            f.write(f"Words: {len(chunk.split())}\n")
            f.write(f"Lines: {len(chunk.splitlines())}\n")
            f.write("-" * 50 + "\n")

def main():
    pdf_path = "C:/Users/User/pdf_chunking_project/Draft_TKO.pdf"
    output_folder = "output_chunks"
    
    print("Membaca PDF...")
    text = load_pdf_text(pdf_path)
    
    if not text:
        print("Tidak dapat membaca PDF!")
        return
    
    print("Membuat chunks menggunakan optimized recursive character chunking...")
    chunks = recursive_character_chunking(text)
    
    print(f"Berhasil membuat {len(chunks)} chunks")
    print("Menyimpan chunks...")
    save_chunks(chunks, output_folder)
    
    print("Membuat summary...")
    save_summary(chunks, output_folder)
    
    print(f"Chunks dan summary telah disimpan di folder: {output_folder}")

if __name__ == "__main__":
    main()