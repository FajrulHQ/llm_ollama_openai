from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import re

def clean_text(text):
    """
    Clean and format extracted text.
    """
    # Remove multiple whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove hyphenation at line ends
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
    # Remove unnecessary line breaks
    text = re.sub(r'\n+', ' ', text)
    return text.strip()

def split_into_sentences(text):
    """
    Split text into complete sentences, keeping the period with the sentence.
    """
    # Pattern matches end of sentence followed by space and capital letter
    sentences = re.split(r'(?<=\.)\s+(?=[A-Z])', text)
    return sentences

def load_and_split_pdf(pdf_path, chunk_size=1000):
    """
    Load PDF and split text into optimized chunks with improved sentence handling.
    """
    try:
        # Load PDF
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()

        # Combine pages and clean text
        full_text = ""
        for page in pages:
            page_text = clean_text(page.page_content)
            full_text += page_text + " "
        
        full_text = clean_text(full_text)
        
        # First split into complete sentences
        sentences = split_into_sentences(full_text)
        
        # Then use RecursiveCharacterTextSplitter on sentence boundaries
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            length_function=len,
            separators=["\n\n", "\n", "."]  # Don't split on periods anymore
        )
        
        # Join sentences with proper spacing and split into chunks
        processed_text = " ".join(sentences)
        chunks = text_splitter.create_documents([processed_text])
        
        return chunks

    except Exception as e:
        print(f"Error occurred: {e}")
        return []

def save_chunks_to_file(chunks, output_folder):
    """
    Save chunks to text files with improved formatting.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for idx, chunk in enumerate(chunks):
        file_path = f"{output_folder}/chunk_{idx + 1:03d}.txt"  # Zero-padded numbering
        # Ensure chunk ends with proper punctuation
        content = chunk.page_content.strip()
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

def check_chunks(output_folder):
    """
    Check chunks with detailed information.
    """
    chunk_files = sorted([f for f in os.listdir(output_folder) if f.endswith(".txt")])
    chunk_data = {}

    for chunk_file in chunk_files:
        file_path = os.path.join(output_folder, chunk_file)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Count complete sentences (including their periods)
            sentences = split_into_sentences(content)
            num_sentences = len(sentences)
            
            chunk_data[chunk_file] = {
                "length": len(content),
                "num_sentences": num_sentences,
                "content_preview": content[:200],
                "words": len(content.split())
            }

    return chunk_data

def main():
    # Configuration
    pdf_path = "C:/Users/User/pdf_chunking_project/Dokumen.pdf"
    output_folder = "output_chunks_langchainbaru"
    chunk_size = 1000

    # Load and split PDF
    print("Extracting and splitting text from PDF...")
    chunks = load_and_split_pdf(
        pdf_path,
        chunk_size=chunk_size
    )

    if not chunks:
        print("No text could be extracted. Program terminated.")
        return

    # Save chunks
    print(f"Saving {len(chunks)} chunks to folder {output_folder}...")
    save_chunks_to_file(chunks, output_folder)
    print("Finished saving chunks!")

    # Check chunking results
    print("\nChecking chunking results:")
    chunk_info = check_chunks(output_folder)

    for chunk_file, info in chunk_info.items():
        print(f"\nFile: {chunk_file}")
        print(f"  Length: {info['length']} characters")
        print(f"  Word count: {info['words']}")
        print(f"  Sentence count: {info['num_sentences']}")
        print(f"  Preview: {info['content_preview'][:100]}...")

if __name__ == "__main__":
    main()