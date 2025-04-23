import PyPDF2
import string
import os
#from pdf_search import search_pdf  # Importujte funkciju iz pdf_search.py
from chatbot.pdf_search import search_pdf


# Funkcija za čitanje PDF-a i pretragu u njemu
def search_pdf(query):
    try:
        pdf_path = os.path.join(os.path.dirname(__file__), 'cnc_manual.pdf')
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

        text_lower = text.lower()
        query_lower = query.lower()

        if query_lower in text_lower:
            start_index = text_lower.find(query_lower)
            end_index = start_index + 500
            snippet = text[start_index:end_index]
            return snippet.strip()
        else:
            return None
    except FileNotFoundError:
        return None

# Funkcija za čišćenje teksta
def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

# Glavna funkcija za odgovor
def get_answer(user_message):
    user_message_clean = clean_text(user_message)

    # Definisani odgovori
    answers = {
        "g1": "G1 je G-kod koji označava linearno kretanje alata u CNC mašini.",
        "g1 funkcija": "G1 funkcija omogućava alatima da se pomeraju duž ravne linije, koristeći podešene brzine kretanja.",
        "sta je g1 funkcija": "G1 funkcija omogućava alatima da se pomeraju duž ravne linije, koristeći podešene brzine kretanja.",
        "objasnite g1 funkciju": "G1 funkcija omogućava alatima da se pomeraju duž ravne linije, koristeći podešene brzine kretanja.",
        "g2": "G2 je G-kod za kružno interpolaciju u smeru kazaljke na satu (CW).",
        "g3": "G3 je G-kod za kružno interpolaciju suprotno od kazaljke na satu (CCW).",
        "radni hod": "Radni hod je udaljenost koju alat pređe tokom obrade.",
        "radna brzina": "Radna brzina je brzina kretanja alata u materijalu."
    }

    # 1. Prvo pokušaj rečnik
    for key in answers.keys():
        if key in user_message_clean:
            return answers[key]

    # 2. Ako nema u rečniku, probaj PDF
    pdf_answer = search_pdf(user_message)
    if pdf_answer:
        return pdf_answer

    return "Nažalost, nemam odgovor za to pitanje."
