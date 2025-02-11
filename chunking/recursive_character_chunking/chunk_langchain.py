from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def load_and_split_pdf(pdf_path, chunk_size=1000):
    """
    Load PDF and split text into optimized chunks.
    """
    try:
        # Load PDF
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()

        # Combine pages and clean up
        text = " ".join(page.page_content.strip() for page in pages if page.page_content)

        # Split text using advanced separators
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            length_function=len,
            separators=["."]  # Optimized separators
        )

        # Generate chunks with natural breaks
        chunks = text_splitter.create_documents([text])
        return chunks

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return []

def save_chunks_to_file(chunks, output_folder):
    """
    Save chunks to text files in the specified folder.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for idx, chunk in enumerate(chunks):
        file_path = f"{output_folder}/chunk_{idx + 1}.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(chunk.page_content.strip())

def check_chunks(output_folder):
    """
    Check all chunk files and display their information.
    """
    chunk_files = [f for f in os.listdir(output_folder) if f.endswith(".txt")]
    chunk_data = {}

    for chunk_file in chunk_files:
        file_path = os.path.join(output_folder, chunk_file)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            chunk_data[chunk_file] = {
                "length": len(content),
                "content_preview": content[:200]
            }

    return chunk_data

def main():
    # Configurations
    pdf_path = "C:/Users/User/pdf_chunking_project/Dokumen.pdf"
    output_folder = "output_chunks_langchain"
    chunk_size = 1000

    # Load and split PDF
    print("Mengekstrak dan memecah teks dari PDF...")
    chunks = load_and_split_pdf(
        pdf_path,
        chunk_size=chunk_size
    )

    if not chunks:
        print("Tidak ada teks yang bisa diekstrak. Program dihentikan.")
        return

    # Save chunks
    print(f"Menyimpan {len(chunks)} chunk ke folder {output_folder}...")
    save_chunks_to_file(chunks, output_folder)
    print("Selesai menyimpan chunks!")

    # Check chunk results
    print("\nMengecek hasil chunking:")
    chunk_info = check_chunks(output_folder)

    for chunk_file, info in chunk_info.items():
        print(f"\nFile: {chunk_file}")
        print(f"  Panjang: {info['length']} karakter")
        print(f"  Preview: {info['content_preview']}...")

if __name__ == "__main__":
    main()