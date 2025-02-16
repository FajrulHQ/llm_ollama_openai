import os
import re
import json
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from langchain_ollama.llms import OllamaLLM

from langchain.prompts import ChatPromptTemplate

class AdvancedChunking:
    def __init__(self, ukuran_chunk=1000, overlap=200):
        self.ukuran_chunk = ukuran_chunk
        self.overlap = overlap
        self.output_folder = 'output_chunks'
        os.makedirs(self.output_folder, exist_ok=True)
        pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
    
    def baca_pdf(self, path_file):
        pdf_reader = PdfReader(path_file)
        teks = "".join([halaman.extract_text() or "" for halaman in pdf_reader.pages])
        return teks
    
    def preprocessing_teks(self, teks):
        return re.sub(r'\s+', ' ', teks).strip()
    
    def chunk_dengan_konteks(self, teks):
        teks_bersih = self.preprocessing_teks(teks)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.ukuran_chunk, chunk_overlap=self.overlap, length_function=len,
            separators=[".", "\n\n", "\n", " ", ""])
        
        chunks = text_splitter.create_documents([teks_bersih])
        chunks_dengan_konteks = []
        
        for i, chunk in enumerate(chunks):
            konteks_sebelum = chunks[i-1].page_content if i > 0 else ""
            konteks_sesudah = chunks[i+1].page_content if i < len(chunks)-1 else ""
            
            chunk_konteks = f"{konteks_sebelum} {chunk.page_content} {konteks_sesudah}".strip()
            chunk_konteks = chunk_konteks.rstrip('.') + '.'
            
            metadata = {
                'chunk_id': i,
                'total_chunks': len(chunks),
                'panjang_chunk': len(chunk_konteks),
                'konteks_sebelum': konteks_sebelum[:50],
                'konteks_sesudah': konteks_sesudah[:50]
            }
            
            chunks_dengan_konteks.append({'konten': chunk_konteks, 'metadata': metadata})
        
        return chunks_dengan_konteks
    
    def summarize_text(self, text):
        """
        Summarize text using LLM.
        """
        OLLAMA_MODEL = "llama3"
        llm = OllamaLLM(model=OLLAMA_MODEL)
        
        template = """
        Anda adalah asisten AI yang ahli dalam menganalisis dokumen. 
        Berdasarkan dokumen berikut, identifikasi perubahan nama, restrukturisasi, dan strategi ekspansi PT Pertamina. 
        Gunakan hanya informasi yang terdapat dalam dokumen. 

        Dokumen:
        "{document}"
        Ringkasan:
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | llm
        response = chain.invoke({"document": text})
        return response
    
    def proses_folder_pdf(self, folder_path):
        hasil = {}
        total_chunk = 0
        summaries = []
        
        for filename in os.listdir(folder_path):
            if filename.endswith('.pdf'):
                file_path = os.path.join(folder_path, filename)
                print(f"\n{'='*50}")
                print(f"Memproses file: {filename}")
                print(f"{'='*50}")
                teks_pdf = self.baca_pdf(file_path)
                chunks = self.chunk_dengan_konteks(teks_pdf)
                
                total_chunk += len(chunks)
                
                for chunk in chunks:
                    summary = self.summarize_text(chunk['konten'])  # Memastikan hanya satu argumen
                    summaries.append(summary)
                    print(f"Ringkasan Chunk {chunk['metadata']['chunk_id'] + 1}:\n{summary}\n")
                
                hasil[filename] = {'chunks': chunks, 'summaries': summaries}
        
        summary_file = os.path.join(self.output_folder, "summaryTKO.txt")
        with open(summary_file, "w", encoding="utf-8") as f:
            for idx, summary in enumerate(summaries, 1):
                f.write(f"Ringkasan Chunk {idx:03d}:\n")
                f.write(summary)
                f.write("\n\n")
        
        print(f"Semua ringkasan telah disimpan ke file: {summary_file}")
        return hasil
    
if __name__ == "__main__":
    chunker = AdvancedChunking(ukuran_chunk=1000, overlap=200)
    FOLDER_PATH = "./data"
    try:
        hasil_chunking = chunker.proses_folder_pdf(FOLDER_PATH)
    except Exception as e:
        print(f"Terjadi error: {str(e)}")
