import fitz  # PyMuPDF
import os
import re


def clean_text(text):
    """
    Membersihkan dan merapikan teks hasil ekstraksi.
    """
    # Menghapus multiple whitespace
    text = re.sub(r'\s+', ' ', text)
    # Menghapus hyphenation di akhir baris
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
    # Menghapus line breaks yang tidak diperlukan
    text = re.sub(r'\n+', ' ', text)
    return text.strip()


def load_pdf_text(pdf_path):
    """
    Load dan ekstrak teks dari PDF.
    """
    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        
        # Ekstrak teks per halaman dengan pembersihan
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            page_text = page.get_text("text")
            # Bersihkan teks per halaman
            page_text = clean_text(page_text)
            full_text += page_text + " "
        
        return clean_text(full_text)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return ""


def recursive_chunk(text, chunk_size, separators=None):
    """
    Membagi teks secara rekursif menjadi chunk dengan panjang maksimum menggunakan separator yang ditentukan.
    """
    if not text.strip():  # Jika teks kosong, hentikan rekursi
        return []

    if separators is None:
        separators = ["."]

    for separator in separators:
        if separator in text[:chunk_size]:
            split_index = text[:chunk_size].rfind(separator) + len(separator)
            chunk = text[:split_index]
            remaining_text = text[split_index:].strip()
            return [chunk] + recursive_chunk(remaining_text, chunk_size, separators)

    # Jika tidak ada separator yang ditemukan dalam batas chunk_size
    chunk = text[:chunk_size]
    remaining_text = text[chunk_size:].strip()
    return [chunk] + recursive_chunk(remaining_text, chunk_size, separators)


def save_chunks_to_single_file(chunks, output_file):
    """
    Menyimpan semua chunks ke dalam satu file dengan pemisah yang jelas.
    """
    # Pastikan direktori output ada
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_file, "w", encoding="utf-8") as f:
        for idx, chunk in enumerate(chunks, 1):
            # Tulis header chunk
            f.write(f"\n{'='*50}\n")
            f.write(f"CHUNK {idx:03d}\n")
            f.write(f"{'='*50}\n\n")
            
            # Tulis konten chunk
            f.write(chunk)
            f.write("\n")  # Tambah baris kosong di akhir chunk

        # Tulis ringkasan di akhir file
        f.write(f"\n{'='*50}\n")
        f.write(f"RINGKASAN\n")
        f.write(f"{'='*50}\n")
        f.write(f"Total Chunks: {len(chunks)}\n")
        
        # Tambah statistik per chunk
        for idx, chunk in enumerate(chunks, 1):
            words = len(chunk.split())
            sentences = len(re.split(r'(?<=[.!?])\s+', chunk.strip()))
            f.write(f"\nChunk {idx:03d}:\n")
            f.write(f"- Jumlah kata: {words}\n")
            f.write(f"- Jumlah kalimat: {sentences}\n")


def main():
    # Konfigurasi
    pdf_path = "C:/Users/User/pdf_chunking_project/Dokumen.pdf"
    output_file = "output_chunks.txt"  # File output tunggal
    chunk_size = 1000

    # Load PDF dan ekstrak teks
    print("Mengekstrak teks dari PDF...")
    full_text = load_pdf_text(pdf_path)

    if not full_text:
        print("Tidak ada teks yang bisa diekstrak. Program dihentikan.")
        return

    # Chunk teks secara rekursif
    print("Membagi teks menjadi chunks secara rekursif...")
    chunks = recursive_chunk(full_text, chunk_size)

    print(f"Selesai membagi menjadi {len(chunks)} chunks.")

    # Simpan semua chunks ke satu file
    save_chunks_to_single_file(chunks, output_file)
    print(f"Semua chunks telah disimpan ke file: {output_file}")
    
    # Tampilkan preview struktur file
    print("\nStruktur file output:")
    print("1. Setiap chunk dipisahkan dengan garis pembatas '='")
    print("2. Setiap chunk memiliki header dengan nomor chunk")
    print("3. Di akhir file terdapat ringkasan statistik untuk semua chunks")


if __name__ == "__main__":
    main()