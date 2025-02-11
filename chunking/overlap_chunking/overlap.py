import os
import fitz
import nltk
from langchain.text_splitter import RecursiveCharacterTextSplitter

nltk.download('punkt')
from nltk.tokenize import sent_tokenize

class PDFChunker:
    def __init__(self, chunk_size=500, chunk_overlap=100):  # ✅ Perbaikan __init__
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file."""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text("text") + " "
            return text.strip()
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return None

    def clean_text(self, text):
        """Clean text from excess spaces and special characters."""
        if not text:
            return ""
        text = " ".join(text.split())
        return text

    def get_sentence_end_position(self, text, approximate_position):
        """Find the nearest sentence end after the approximate position."""
        if approximate_position >= len(text):
            return len(text)

        # Look ahead up to overlap size to find sentence boundary
        look_ahead = min(len(text) - approximate_position, self.chunk_overlap)
        text_segment = text[approximate_position:approximate_position + look_ahead]
        sentences = sent_tokenize(text_segment)

        if len(sentences) <= 1:
            # If no sentence boundary found, return the original position
            return approximate_position
        
        # Find position of first sentence end
        first_sentence = sentences[0]
        return approximate_position + len(first_sentence)

    def create_chunks_with_overlap(self, text):
        """Create chunks with proper overlap, respecting sentence boundaries."""
        if not text:
            return []

        chunks = []
        text_length = len(text)
        start = 0

        while start < text_length:
            # Calculate the end position for this chunk
            end = min(start + self.chunk_size, text_length)
            
            # If we're not at the end of the text, find a proper sentence boundary
            if end < text_length:
                end = self.get_sentence_end_position(text, end)
            
            # Add the chunk
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Calculate next start position with overlap
            if end == text_length:
                break
                
            # Move back by overlap amount, then find the nearest sentence start
            start = max(end - self.chunk_overlap, 0)
            # Find the next sentence start after this position
            sentences_after_start = sent_tokenize(text[start:start + self.chunk_overlap])
            if len(sentences_after_start) > 1:
                # Skip the first partial sentence to start at a sentence boundary
                start += len(sentences_after_start[0])

        return chunks

    def process_pdf(self, pdf_path):
        """Process PDF and create overlapping chunks."""
        # Extract text
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            return []
        
        # Clean text
        cleaned_text = self.clean_text(text)
        
        # Create chunks with overlap
        return self.create_chunks_with_overlap(cleaned_text)

    def save_chunks_to_folder(self, chunks, output_folder="chunks_output"):
        """Save chunks to folder."""
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for i, chunk in enumerate(chunks):
            file_path = os.path.join(output_folder, f"chunk_{i+1}.txt")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(chunk)

        print(f"✅ {len(chunks)} chunks successfully saved in folder '{output_folder}'.")

    def analyze_chunks(self, chunks):
        """Analyze chunking results."""
        if not chunks:
            return {
                "total_chunks": 0,
                "chunk_sizes": [],
                "average_size": 0,
                "overlap_analysis": []
            }

        chunk_sizes = [len(chunk) for chunk in chunks]
        overlap_analysis = []
        
        # Analyze overlap between consecutive chunks
        for i in range(len(chunks) - 1):
            current_chunk = chunks[i]
            next_chunk = chunks[i + 1]
            
            # Find overlapping content
            overlap_size = 0
            for j in range(min(len(current_chunk), self.chunk_overlap)):
                if current_chunk[-j-1:] in next_chunk:
                    overlap_size = j + 1
            
            overlap_analysis.append({
                "chunks": f"{i+1}-{i+2}",
                "overlap_size": overlap_size
            })

        return {
            "total_chunks": len(chunks),
            "chunk_sizes": chunk_sizes,
            "average_size": sum(chunk_sizes) / len(chunks),
            "overlap_analysis": overlap_analysis
        }

def main():
    # Initialize chunker
    chunker = PDFChunker(chunk_size=500, chunk_overlap=100)
    
    # Configuration
    pdf_path = "tko.pdf"
    output_folder = "tko_test"
    
    # Process PDF
    chunks = chunker.process_pdf(pdf_path)
    
    # Save results
    if chunks:
        chunker.save_chunks_to_folder(chunks, output_folder)
        
        # Analyze results
        analysis = chunker.analyze_chunks(chunks)
        print("\nChunking Analysis:")
        print(f"Total chunks: {analysis['total_chunks']}")
        print(f"Average chunk size: {analysis['average_size']:.2f} characters")
        print(f"Smallest chunk: {min(analysis['chunk_sizes'])} characters")
        print(f"Largest chunk: {max(analysis['chunk_sizes'])} characters")
        print("\nOverlap Analysis:")
        for overlap in analysis['overlap_analysis']:
            print(f"Chunks {overlap['chunks']}: {overlap['overlap_size']} characters overlap")

if __name__ == "__main__":
    main()