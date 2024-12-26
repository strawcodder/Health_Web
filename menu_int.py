from PyPDF2 import PdfReader
import re

def extract_pdf_text(pdf_path):
    """Extract text from PDF and return as string."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def process_text(text):
    """Process extracted text - customize this function based on your needs."""
    # Example processing:
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Split into sentences
    sentences = re.split('[.!?]', text)
    
    # Remove empty strings
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return sentences

def pdf_pipeline(pdf_path):
    """Main function to extract and process PDF text."""
    try:
        # Extract text
        raw_text = extract_pdf_text(pdf_path)
        
        # Process text
        processed_text = process_text(raw_text)
        
        return processed_text
        
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None

# Usage example
if __name__ == "__main__":
    pdf_path = "your_pdf_file.pdf"
    results = pdf_pipeline(pdf_path)
    
    if results:
        for idx, sentence in enumerate(results, 1):
            print(f"{idx}. {sentence}")