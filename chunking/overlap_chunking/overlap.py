import os
import fitz
import nltk
from langchain.text_splitter import RecursiveCharacterTextSplitter

nltk.download('punkt')
from nltk.tokenize import sent_tokenize

class PDFChunker:
    def __init__(self, chunk_size=500, chunk_overlap=100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )

    def extract_text_from_pdf(self, pdf_path):
        """Ekstrak teks dari file PDF."""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text("text") + " "
            return text.strip()
        except Exception as e:
            print(f"Error saat membaca PDF: {e}")
            return None

    def recursive_character_chunking(self, text):
        """
        Memproses teks menggunakan RecursiveCharacterTextSplitter dari LangChain
        dan menerapkan chunking rekursif tambahan.
        """
        if not text:
            return []

        # Langkah 1: Bagi teks menggunakan RecursiveCharacterTextSplitter
        initial_chunks = self.text_splitter.create_documents([text])
        
        # Langkah 2: Proses setiap chunk untuk pengecekan tambahan
        final_chunks = []
        for chunk in initial_chunks:
            # Ambil konten dari Document object
            chunk_text = chunk.page_content
            
            # Terapkan chunking rekursif tambahan jika diperlukan
            if len(chunk_text) > self.chunk_size:
                sub_chunks = self._recursive_overlap_chunking(
                    chunk_text, 
                    self.chunk_size, 
                    self.chunk_overlap
                )
                final_chunks.extend(sub_chunks)
            else:
                final_chunks.append(chunk_text)

        return final_chunks

    def _recursive_overlap_chunking(self, text, chunk_size, overlap, start=0, chunks=None):
        """
        Metode helper untuk chunking rekursif tambahan.
        """
        if chunks is None:
            chunks = []

        if start >= len(text):
            return chunks

        end = min(start + chunk_size, len(text))
        
        # Cari batas kalimat terdekat untuk splitting yang lebih alami
        if end < len(text):
            sentences = sent_tokenize(text[start:end + overlap])
            if len(sentences) > 1:
                # Gunakan kalimat terakhir yang lengkap
                partial_text = " ".join(sentences[:-1])
                end = start + len(partial_text)

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        return self._recursive_overlap_chunking(
            text, 
            chunk_size, 
            overlap, 
            start + chunk_size - overlap, 
            chunks
        )

    def save_chunks_to_folder(self, chunks, output_folder="chunks_output"):
        """Menyimpan chunks ke folder."""
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for i, chunk in enumerate(chunks):
            file_path = os.path.join(output_folder, f"chunk_{i+1}.txt")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(chunk)

        print(f"✅ {len(chunks)} chunk berhasil disimpan di folder '{output_folder}'.")

    def analyze_chunks(self, chunks):
        """Menganalisis hasil chunking."""
        analysis = {
            "total_chunks": len(chunks),
            "chunk_sizes": [len(chunk) for chunk in chunks],
            "average_size": sum(len(chunk) for chunk in chunks) / len(chunks) if chunks else 0
        }
        return analysis

def main():
    # Inisialisasi chunker
    chunker = PDFChunker(chunk_size=500, chunk_overlap=100)
    
    # Konfigurasi
    pdf_path = "contoh.pdf"
    output_folder = "recursive_chunks"
    
    # Proses PDF
    text = chunker.extract_text_from_pdf(pdf_path)
    if text:
        # Terapkan chunking
        chunks = chunker.recursive_character_chunking(text)
        
        # Simpan hasil
        chunker.save_chunks_to_folder(chunks, output_folder)
        
        # Analisis hasil
        analysis = chunker.analyze_chunks(chunks)
        print("\nAnalisis Hasil Chunking:")
        print(f"Total chunks: {analysis['total_chunks']}")
        print(f"Rata-rata ukuran chunk: {analysis['average_size']:.2f} karakter")
        print(f"Ukuran chunk terkecil: {min(analysis['chunk_sizes'])} karakter")
        print(f"Ukuran chunk terbesar: {max(analysis['chunk_sizes'])} karakter")

if __name__ == "__main__":
    main()