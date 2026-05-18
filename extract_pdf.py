import pypdf
import sys

def extract_text(pdf_path, out_path):
    with open(pdf_path, 'rb') as file:
        reader = pypdf.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(text)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please provide paths: input.pdf output.txt")
        sys.exit(1)
    extract_text(sys.argv[1], sys.argv[2])
