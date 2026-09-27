import os
import re
import io
import time
import base64
import requests
from typing import Dict, Any, Tuple, List
import pdfplumber
import pypdf
import docx
from backend.config import get_settings

settings = get_settings()

GEMINI_MODELS_FALLBACK = [
    "gemini-flash-lite-latest",
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash",
    "gemini-2.5-pro",
    "gemini-2.5-flash"
]

def extract_text_via_gemini_ocr(file_bytes: bytes) -> str:
    """
    Uses Google Gemini multimodal vision across active model endpoints with automatic fallback.
    """
    if not settings.GEMINI_API_KEY:
        return ""
    
    b64_data = base64.b64encode(file_bytes).decode("utf-8")
    payload = {
        "contents": [
            {
                "parts": [
                    {"inline_data": {"mime_type": "application/pdf", "data": b64_data}},
                    {"text": "Extract and return the entire plain text content of this resume verbatim. Preserve all section headings, candidate name, email, phone number, location, LinkedIn, GitHub, skills, experience, education, and projects without omitting any details."}
                ]
            }
        ]
    }

    for model in GEMINI_MODELS_FALLBACK:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={settings.GEMINI_API_KEY}"
        for attempt in range(2):
            try:
                res = requests.post(url, json=payload, verify=False, timeout=25)
                if res.status_code == 200:
                    data = res.json()
                    extracted = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                    if len(extracted) > 50:
                        return extracted
                elif res.status_code == 429:
                    time.sleep(1.5)
                    continue
                else:
                    break
            except Exception as e:
                print(f"Gemini OCR model {model} attempt {attempt+1} notice: {e}")
                time.sleep(1)

    return ""

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts text from PDF bytes using pdfplumber, pypdf, and multi-model Gemini Vision OCR fallback.
    """
    text_chunks = []
    
    # 1. pdfplumber extraction
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text(layout=True) or page.extract_text() or ""
                if page_text.strip():
                    text_chunks.append(page_text.strip())
    except Exception as e:
        print(f"pdfplumber extraction warning: {e}")
    
    # 2. pypdf fallback
    if not text_chunks:
        try:
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            for page in reader.pages:
                page_text = page.extract_text() or ""
                if page_text.strip():
                    text_chunks.append(page_text.strip())
        except Exception as e:
            print(f"pypdf extraction error: {e}")

    extracted = "\n\n".join(text_chunks)
    
    # 3. If extracted text is empty or too short (scanned/graphic PDF), use Multi-Model Gemini Vision OCR
    if len(extracted.strip().split()) < 25:
        print("Standard PDF text extraction below threshold. Triggering Multi-Model Gemini OCR...")
        ocr_text = extract_text_via_gemini_ocr(file_bytes)
        if len(ocr_text.strip().split()) >= 20:
            extracted = ocr_text

    return clean_extracted_text(extracted)

def extract_text_from_docx(file_bytes: bytes) -> str:
    """
    Extracts text from DOCX bytes including paragraphs and table contents.
    """
    text_chunks = []
    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        for para in doc.paragraphs:
            if para.text.strip():
                text_chunks.append(para.text.strip())
        
        for table in doc.tables:
            for row in table.rows:
                row_text = " | ".join([cell.text.strip() for cell in row.cells if cell.text.strip()])
                if row_text:
                    text_chunks.append(row_text)
    except Exception as e:
        print(f"DOCX extraction error: {e}")

    extracted = "\n".join(text_chunks)
    return clean_extracted_text(extracted)

def clean_extracted_text(text: str) -> str:
    """
    Normalizes whitespace, bullet characters, and non-printable characters.
    """
    if not text:
        return ""

    bullet_chars = ["•", "●", "▪", "◆", "▶", "►", "–", "—", "★", "✔", "✓"]
    for b in bullet_chars:
        text = text.replace(b, "- ")

    text = re.sub(r"\r\n|\r", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()

def parse_document(file_bytes: bytes, file_type: str) -> str:
    """
    Main entrypoint for document text extraction based on file extension.
    """
    file_type = file_type.lower().replace(".", "")
    if file_type == "pdf":
        return extract_text_from_pdf(file_bytes)
    elif file_type in ["docx", "doc"]:
        return extract_text_from_docx(file_bytes)
    elif file_type == "txt":
        return file_bytes.decode("utf-8", errors="ignore")
    else:
        raise ValueError(f"Unsupported file format '{file_type}'.")
