
# Graph-RAG Update Notebook

Notebook ini digunakan untuk memproses dokumen PDF, menyimpannya dalam database vektor (ChromaDB), dan melakukan pencarian serta ringkasan informasi menggunakan model bahasa (LLM) dengan pendekatan Graph-RAG.

## Dependencies
Untuk menjalankan notebook ini, pastikan Anda telah menginstal library berikut:

```
pip install os shutil numpy networkx langchain-chroma langchain-huggingface langchain langchain-text-splitters langchain-ollama IPython
```

## Proses Dokumen
1. **Memuat Dokumen**: Dokumen PDF dimuat dari direktori `data/` menggunakan `PyPDFDirectoryLoader`.
2. **Memisahkan Dokumen**: Dokumen dipisahkan menjadi chunk dengan ukuran tertentu menggunakan `RecursiveCharacterTextSplitter`.
3. **Menambahkan ke ChromaDB**: Chunk dokumen yang baru ditambahkan ke ChromaDB jika belum ada.

## Contoh Output 1
Response promt yang digunakan
```
You are a helpful assistant for text summarization. 
Only include information that is part of the document. 
Do not include your own opinion or analysis.
```
Hasil output yang diberikanx
```
🔎 Dokumen yang digunakan untuk ringkasan:
- 📄 data\ifransiska,+716-1511-1-PB.pdf - Page 2 (Score: 0.59)
- 📄 data\Kesehatan_Mental_Masyarakat_Indonesia_Pe.pdf - Page 4 (Score: 0.59)
- 📄 data\Kesehatan_Mental_Masyarakat_Indonesia_Pe.pdf - Page 4 (Score: 0.59)
- 📄 data\Kesehatan_Mental_Sumber_Daya_Manusia_Ind.pdf - Page 7 (Score: 0.59)
- 📄 data\Kesehatan_Mental_Sumber_Daya_Manusia_Ind.pdf - Page 0 (Score: 0.58)

Faktor utama yang mempengaruhi kesehatan mental menurut penelitian adalah:

1. Dukungan masyarakat
2. Stigma negatif masyarakat terhadap penderita gangguan kesehatan mental
3. Kondisi wilayah (kepadatan penduduk, prevalensi cacat mental)
4. Edukaasi dan penanganan kesehatan mental

Penelitian ini menemukan bahwa dukungan masyarakat dan stigmatisasi yang terhadap penderita gangguan kesehatan mental dapat mempengaruhi kesehatan mental. Selain itu, kondisi wilayah juga berperan dalam meningkatkan jumlah penderita kesehatan mental. Edukasi dan penanganan kesehatan mental juga diperlukan untuk membantu masyarakat mengatasi masalah kesehatan mental.
```

## Contoh Output 2
Response promt yang digunakan
```
Anda adalah asisten yang membantu menjawab pertanyaan berdasarkan dokumen.
Tugas Anda adalah memberikan jawaban yang akurat dan terperinci. Jika perlu, gunakan analisis atau pemahaman tambahan.
Berdasarkan teks berikut, jawab pertanyaan dengan akurat. Jika jawaban tidak lengkap, beri penjelasan lebih lanjut.
```
Hasil output yang diberikan
```
🔎 Dokumen yang digunakan untuk ringkasan:
- 📄 data\ifransiska,+716-1511-1-PB.pdf - Page 2 (Score: 0.59)
- 📄 data\Kesehatan_Mental_Masyarakat_Indonesia_Pe.pdf - Page 4 (Score: 0.59)
- 📄 data\Kesehatan_Mental_Masyarakat_Indonesia_Pe.pdf - Page 4 (Score: 0.59)
- 📄 data\Kesehatan_Mental_Sumber_Daya_Manusia_Ind.pdf - Page 7 (Score: 0.59)
- 📄 data\Kesehatan_Mental_Sumber_Daya_Manusia_Ind.pdf - Page 0 (Score: 0.58)

Berdasarkan teks tersebut, faktor utama yang mempengaruhi kesehatan mental adalah

1. Dukungan masyarakat: Masyarakat yang tidak menerima kondisi para penderita gangguan kesehatan mental, mereka menganggap para penderita adalah orang berbahaya, pasien yang tidak dapat pulih kesehatan mentalnya, dan layak untuk diasingkan.
2. Stigma negatif: Kuatnya stigma negatif masyarakat pada penderita gangguan kesehatan mental menjadikan penderita tidak mendapatkan perawatan yang sesuai. Dianggap sebagai sebuah aib, keluarga penderita gangguan kesehatan mental lebih memilih mengurung anggota keluarga yang terkena gangguan.
3. Wilayah dan penduduk: Peneliti menduga terdapat hubungan antara kondisi wilayah terhadap jumlah penderita kesehatan mental. Wilayah dengan kepadatan penduduk akan menghasilkan jumlah cacat mental yang lebih tinggi.

Dalam konsep kesehatan mental, tidak hanya faktor-faktor di atas yang mempengaruhi kesehatan mental, tetapi juga kondisi individu sendiri dan berbagai macam treatment yang tersedia untuk membantu meningkatkan kesejahteraan mental.
```

## Catatan
- Jika Anda ingin menghapus database ChromaDB yang ada, jalankan fungsi `clear_database()`.
- Pastikan model bahasa yang digunakan (`OLLAMA_MODEL`) telah diunduh dan siap digunakan.
