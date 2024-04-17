# myapp/summary_generator.py

import PyPDF2
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import nltk
import time

# Download NLTK punkt tokenizer data
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    words = nltk.word_tokenize(text.lower())
    return ' '.join([word for word in words if word.isalnum() and word not in stop_words])

def generate_summary(text, num_sentences=3):
    sentences = sent_tokenize(text)
    return ' '.join(sentences[:num_sentences])

def generate_pdf_summary(pdf_file_path, output_pdf_path):
    with open(pdf_file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        full_text = ""
        for page in pdf_reader.pages:
            full_text += page.extract_text()

    print("Chunking PDF...\n")
    chunks = sent_tokenize(full_text)
    preprocessed_chunks = [preprocess_text(chunk) for chunk in chunks]

    # Combine all chunks to create a single document for analysis
    all_text = ' '.join(preprocessed_chunks)

    # Generate summary for the entire document
    summary = generate_summary(all_text, num_sentences=5)

    if summary:
        print("\n\nPDF Summary:\n" + summary + "\n")

        with open(output_pdf_path, "a", encoding="utf-8") as pdf_file:
            pdf_file.write(f"Summary:\n{summary}\n\n")

        # Add a delay before exiting
        time.sleep(2)
        return summary
    else:
        print("\n\nGPT: I'm sorry, but I can't find that information\n")
        return None
