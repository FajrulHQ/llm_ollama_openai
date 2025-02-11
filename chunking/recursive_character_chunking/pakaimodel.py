import fitz  # Fitz from PyMuPDF
from llama_index import GPTListIndex, LLMPredictor, ServiceContext
from llama_index.llms import OpenAI
from typing import List

# Function to read text from PDF
def extract_pdf_text(pdf_path: str) -> str:
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text")
    return text

# Recursive function to chunk text
MAX_CHUNK_SIZE = 2048

def chunk_text_recursive(text: str) -> List[str]:
    if len(text) <= MAX_CHUNK_SIZE:
        return [text]
    split_pos = text.rfind(" ", 0, MAX_CHUNK_SIZE)
    if split_pos == -1:
        split_pos = MAX_CHUNK_SIZE
    chunk = text[:split_pos].strip()
    remaining_text = text[split_pos:].strip()
    return [chunk] + chunk_text_recursive(remaining_text)

# Process text using OpenAI
def process_text_with_openai(chunks: List[str]):
    # Use OpenAI GPT-3.5 model
    llm_predictor = LLMPredictor(llm=OpenAI(model="gpt-3.5-turbo"))
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

    results = []
    for chunk in chunks:
        response = llm_predictor.predict(chunk)
        results.append(response)

    return results

if __name__ == "__main__":
    pdf_path = "C:/Users/User/pdf_chunking_project/Draft_TKO.pdf"

    # Extract text from PDF
    pdf_text = extract_pdf_text(pdf_path)
    print("PDF text extracted successfully.")

    # Chunk text recursively
    text_chunks = chunk_text_recursive(pdf_text)
    print(f"Text chunked into {len(text_chunks)} parts.")

    # Process chunks with OpenAI
    responses = process_text_with_openai(text_chunks)
    for idx, response in enumerate(responses):
        print(f"Response {idx + 1}: {response}")
