
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
Query yang digunakan
```
Apa faktor utama yang mempengaruhi kesehatan mental?
```
Hasil output yang diberikan
```
🔎 Dokumen yang digunakan untuk ringkasan:
- 📄 data\ifransiska,+716-1511-1-PB.pdf - Page 2 (Score: 0.59)
- 📄 data\Kesehatan_Mental_Masyarakat_Indonesia_Pe.pdf - Page 4 (Score: 0.59)
- 📄 data\Kesehatan_Mental_Masyarakat_Indonesia_Pe.pdf - Page 4 (Score: 0.59)
- 📄 data\Kesehatan_Mental_Sumber_Daya_Manusia_Ind.pdf - Page 7 (Score: 0.59)
- 📄 data\Kesehatan_Mental_Sumber_Daya_Manusia_Ind.pdf - Page 0 (Score: 0.58)

Faktor utama yang mempengaruhi kesehatan mental menurut teks tersebut adalah:

1. Dukungan masyarakat: Masyarakat sulit menerima kondisi para penderita gangguan kesehatan mental dan menganggap mereka sebagai orang berbahaya, pasien yang tidak dapat pulih kesehatan mentalnya.
2. Stigma negatif masyarakat: Kuatnya stigma negatif masyarakat pada penderita gangguan kesehatan mental menjadikan penderita tidak mendapatkan perawatan yang sesuai.
3. Wilayah: Peneliti menduga terdapat hubungan antara kondisi wilayah terhadap jumlah penderita kesehatan mental, yaitu wilayah dengan kepadatan penduduk akan menghasilkan jumlah cacat mental yang lebih tinggi.

Namun, teks tersebut tidak menyebutkan secara spesifik faktor utama yang mempengaruhi kesehatan mental.
```

## Contoh Output 2
Response promt yang digunakan
```
Anda adalah asisten yang membantu menjawab pertanyaan berdasarkan dokumen.
Tugas Anda adalah memberikan jawaban yang akurat dan terperinci. Jika perlu, gunakan analisis atau pemahaman tambahan.
Berdasarkan teks berikut, jawab pertanyaan dengan akurat. Jika jawaban tidak lengkap, beri penjelasan lebih lanjut.
```
Query yang digunakan
```
Apa faktor utama yang mempengaruhi kesehatan mental?
```
Hasil output yang diberikan
```
🔎 Dokumen yang digunakan untuk ringkasan:
- 📄 data\ifransiska,+716-1511-1-PB.pdf - Page 2 (Score: 0.59)
- 📄 data\Kesehatan_Mental_Masyarakat_Indonesia_Pe.pdf - Page 4 (Score: 0.59)
- 📄 data\Kesehatan_Mental_Masyarakat_Indonesia_Pe.pdf - Page 4 (Score: 0.59)
- 📄 data\Kesehatan_Mental_Sumber_Daya_Manusia_Ind.pdf - Page 7 (Score: 0.59)
- 📄 data\Kesehatan_Mental_Sumber_Daya_Manusia_Ind.pdf - Page 0 (Score: 0.58)

Berdasarkan teks tersebut, faktor utama yang mempengaruhi kesehatan mental adalah stigma negatif masyarakat terhadap penderita gangguan kesehatan mental. Menurut peneliti, kekuatan stigma ini menyebabkan penderita tidak mendapatkan perawatan yang sesuai dan dianggap sebagai sebuah aib oleh keluarga mereka.

Selain itu, teks juga menyebutkan bahwa dukungan masyarakat menjadi aspek penting dalam berkembangnya seseorang menjadi hal yang sangat sulit diraih oleh penderita gangguan kesehatan mental. Masyarakat sulit menerima kondisi para penderita dan menganggap mereka sebagai orang berbahaya atau pasien yang tidak dapat pulih.

Namun, peneliti juga menekankan pentingnya memberikan edukasi mengenai kesehatan mental, gangguan kesehatan mental, dan penanganannya bagi masyarakat pada umumnya. Dengan demikian, diharapkan masyarakat dapat memiliki pemahaman yang lebih baik tentang kesehatan mental dan dapat memberikan dukungan yang tepat kepada penderita.

Dalam penelitian empiris yang dilakukan oleh peneliti menggunakan data dari Podes 2018 oleh BPS, penemuan menunjukkan bahwa wilayah dengan kepadatan penduduk yang tinggi memiliki jumlah cacat mental yang lebih tinggi. Hal ini menunjukkan bahwa faktor demografi juga dapat mempengaruhi kesehatan mental.

Dalam keseluruhan, teks tersebut menyebutkan bahwa faktor utama yang mempengaruhi kesehatan mental adalah stigma negatif masyarakat, dukungan masyarakat, serta faktor demografi.
```

## Catatan
- Jika Anda ingin menghapus database ChromaDB yang ada, jalankan fungsi `clear_database()`.
- Pastikan model bahasa yang digunakan (`OLLAMA_MODEL`) telah diunduh dan siap digunakan.
