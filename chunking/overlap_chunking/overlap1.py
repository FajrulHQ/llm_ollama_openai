import os
import fitz
import nltk
import re
import textwrap
from langchain.text_splitter import RecursiveCharacterTextSplitter

nltk.download('punkt')
from nltk.tokenize import sent_tokenize

class PDFChunker:
    def __init__(self, chunk_size=1000, chunk_overlap=200, line_width=80):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.line_width = line_width
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file with better formatting."""
        try:
            doc = fitz.open(pdf_path)
            text_blocks = []
            
            for page in doc:
                blocks = page.get_text("blocks")
                for block in blocks:
                    clean_text = block[4].strip()
                    if clean_text:
                        text_blocks.append(clean_text)
            
            text = " ".join(text_blocks)
            return self.clean_text(text)
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return None
        finally:
            if 'doc' in locals():
                doc.close()

    def clean_text(self, text):
        """Clean and normalize text while preserving structure."""
        if not text:
            return ""
        
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'([.!?])\s*', r'\1 ', text)
        text = re.sub(r'\s+([.!?])', r'\1', text)
        text = re.sub(r'\n\s*\n', '\n', text)
        
        return text.strip()

    def create_improved_chunks(self, text):
        """Create chunks with improved sentence handling."""
        if not text:
            return []

        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence = sentence.strip()
            sentence_length = len(sentence)

            if not current_chunk:
                current_chunk.append(sentence)
                current_length = sentence_length
                continue

            if current_length + len(" ") + sentence_length <= self.chunk_size:
                current_chunk.append(sentence)
                current_length += len(" ") + sentence_length
            else:
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentence]
                current_length = sentence_length

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        final_chunks = []
        for i in range(len(chunks)):
            if i > 0:
                prev_chunk_sentences = sent_tokenize(chunks[i-1])
                overlap_sentences = prev_chunk_sentences[-2:] if len(prev_chunk_sentences) > 2 else prev_chunk_sentences
                current_chunk = " ".join(overlap_sentences) + " " + chunks[i]
                final_chunks.append(current_chunk)
            else:
                final_chunks.append(chunks[i])

        return final_chunks

    def wrap_text(self, text):
        """Wrap text to specified line width while preserving paragraphs."""
        # Split text into paragraphs
        paragraphs = text.split('\n\n')
        
        # Wrap each paragraph
        wrapped_paragraphs = []
        for paragraph in paragraphs:
            # Wrap the paragraph text
            wrapped = textwrap.fill(paragraph.strip(), width=self.line_width)
            wrapped_paragraphs.append(wrapped)
        
        # Join paragraphs with double newlines
        return '\n\n'.join(wrapped_paragraphs)

    def save_chunks_to_file(self, chunks, output_folder="chunks_output"):
        """Save chunks to a single file with proper text wrapping."""
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        output_file = os.path.join(output_folder, "chunks.txt")
        
        try:
            with open(output_file, "w", encoding="utf-8") as file:
                for i, chunk in enumerate(chunks, 1):
                    # Write chunk header
                    header = f"Chunk {i}"
                    file.write(f"{header}\n")
                    file.write("="* len(header) + "\n\n")
                    
                    # Write wrapped chunk content
                    wrapped_content = self.wrap_text(chunk)
                    file.write(wrapped_content)
                    file.write("\n\n\n")  # Add extra spacing between chunks

            print(f"✅ {len(chunks)} chunks successfully saved to '{output_file}'")
        except Exception as e:
            print(f"Error saving chunks: {e}")

    def process_pdf(self, pdf_path):
        """Process PDF and create better chunks."""
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            return []
        
        return self.create_improved_chunks(text)

    def analyze_chunks(self, chunks):
        """Analyze chunks with improved metrics."""
        if not chunks:
            return {
                "total_chunks": 0,
                "average_size": 0,
                "size_stats": {},
                "sentence_stats": {}
            }

        chunk_sizes = [len(chunk) for chunk in chunks]
        sentences_per_chunk = [len(sent_tokenize(chunk)) for chunk in chunks]

        analysis = {
            "total_chunks": len(chunks),
            "average_size": sum(chunk_sizes) / len(chunks),
            "size_stats": {
                "min": min(chunk_sizes),
                "max": max(chunk_sizes),
                "avg": sum(chunk_sizes) / len(chunks)
            },
            "sentence_stats": {
                "min_sentences": min(sentences_per_chunk),
                "max_sentences": max(sentences_per_chunk),
                "avg_sentences": sum(sentences_per_chunk) / len(sentences_per_chunk)
            }
        }
        return analysis

def main():
    # Initialize chunker with line width for text wrapping
    chunker = PDFChunker(chunk_size=1000, chunk_overlap=200, line_width=80)
    
    # Configuration
    pdf_path = "tko.pdf"
    output_folder = "overlapfix"
    
    # Process PDF
    chunks = chunker.process_pdf(pdf_path)
    
    if chunks:
        # Save results
        chunker.save_chunks_to_file(chunks, output_folder)
        
        # Analyze and display results
        analysis = chunker.analyze_chunks(chunks)
        print("\nChunking Analysis:")
        print(f"Total chunks: {analysis['total_chunks']}")
        print(f"Average chunk size: {analysis['size_stats']['avg']:.0f} characters")
        print(f"Min/Max chunk size: {analysis['size_stats']['min']}/{analysis['size_stats']['max']} characters")
        print(f"\nSentences per chunk:")
        print(f"Min: {analysis['sentence_stats']['min_sentences']:.0f}")
        print(f"Max: {analysis['sentence_stats']['max_sentences']:.0f}")
        print(f"Average: {analysis['sentence_stats']['avg_sentences']:.1f}")

if __name__ == "__main__":
    main()