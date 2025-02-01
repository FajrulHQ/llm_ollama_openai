
# Graph-RAG Update Notebook

Notebook ini digunakan untuk memproses dokumen PDF, menyimpannya dalam database vektor (ChromaDB), dan melakukan pencarian serta ringkasan informasi menggunakan model bahasa (LLM) dengan pendekatan Graph-RAG.

## Dependencies
Untuk menjalankan notebook ini, pastikan Anda telah menginstal library berikut:

```bash
pip install os shutil numpy networkx langchain-chroma langchain-huggingface langchain langchain-text-splitters langchain-ollama IPython
```

## Proses Dokumen
1. **Memuat Dokumen**: Dokumen PDF dimuat dari direktori `data/` menggunakan `PyPDFDirectoryLoader`.
2. **Memisahkan Dokumen**: Dokumen dipisahkan menjadi chunk dengan ukuran tertentu menggunakan `RecursiveCharacterTextSplitter`.
3. **Menambahkan ke ChromaDB**: Chunk dokumen yang baru ditambahkan ke ChromaDB jika belum ada.

### Contoh Output dari Pencarian
```plaintext
🔎 Dokumen yang digunakan untuk ringkasan:
- 📄 data\ifransiska,+716-1511-1-PB.pdf - Page 2 (Score: 0.59)
- 📄 data\Kesehatan_Mental_Masyarakat_Indonesia_Pe.pdf - Page 4 (Score: 0.59)
- 📄 data\Kesehatan_Mental_Masyarakat_Indonesia_Pe.pdf - Page 4 (Score: 0.59)
- 📄 data\Kesehatan_Mental_Sumber_Daya_Manusia_Ind.pdf - Page 7 (Score: 0.59)
- 📄 data\Kesehatan_Mental_Sumber_Daya_Manusia_Ind.pdf - Page 0 (Score: 0.58)
```

### Contoh Respons dari Model Bahasa
```markdown
Berdasarkan teks tersebut, faktor utama yang mempengaruhi kesehatan mental adalah dukungan masyarakat. Menurut teks, penderita gangguan kesehatan mental mengalami kesulitan dalam mendapatkan dukungan dari masyarakat karena mereka dianggap sebagai orang berbahaya atau pasien yang tidak dapat pulih. Oleh karena itu, memberikan edukasi tentang kesehatan mental dan gangguan kesehatan mental adalah penting untuk membantu masyarakat memahami kondisi penderita dan mengurangi stigma negatif terhadap mereka.

Selain dukungan masyarakat, teks juga menyebutkan bahwa faktor lain yang mempengaruhi kesehatan mental adalah wilayah. Penelitian empiris menunjukkan bahwa wilayah dengan kepadatan penduduk akan menghasilkan jumlah cacat mental yang lebih tinggi. Hal ini berarti bahwa faktor geografis dan demografi juga dapat mempengaruhi kesehatan mental.

Namun, perlu diingat bahwa teks tersebut tidak menyebutkan secara eksplisit tentang faktor utama yang mempengaruhi kesehatan mental secara umum. Namun, berdasarkan konteks dan isi teks, dapat disimpulkan bahwa dukungan masyarakat dan wilayah merupakan faktor-faktor yang signifikan dalam mempengaruhi kesehatan mental.

Dalam konteks ini, penelitian yang dilakukan oleh BPS tahun 2018 menunjukkan bahwa prevalensi cacat mental menyebar di seluruh wilayah Indonesia, termasuk Sulawesi. Hal ini dapat membantu memahami bahwa kesehatan mental bukan hanya dipengaruhi oleh faktor-faktor internal tetapi juga oleh faktor-faktor luar yang terkait dengan lingkungan dan masyarakat.

Dalam keseluruhan, teks tersebut menyebutkan bahwa kesehatan mental dipengaruhi oleh berbagai faktor, termasuk dukungan masyarakat, wilayah, dan lain-lain. Oleh karena itu, penting untuk memahami bahwa kesehatan mental bukan hanya dipengaruhi oleh faktor-faktor internal tetapi juga oleh faktor-faktor luar yang terkait dengan lingkungan dan masyarakat.
```

## Catatan
- Jika Anda ingin menghapus database ChromaDB yang ada, jalankan fungsi `clear_database()`.
- Pastikan model bahasa yang digunakan (`OLLAMA_MODEL`) telah diunduh dan siap digunakan.
