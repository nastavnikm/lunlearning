import pdfplumber


# Funkcija za čitanje PDF-a i pretragu u njemu
def search_pdf(query):
    try:
        # Otvoriti PDF koristeći pdfplumber
        with pdfplumber.open('chatbot/cnc_manual.pdf') as pdf:
            text = ""
            # Prolazimo kroz sve stranice PDF-a
            for page in pdf.pages:
                # Dobijamo tekst sa strane
                page_text = page.extract_text()
                if page_text:
                    text += page_text

                # Takođe pokušavamo da uhvatimo tabele ako postoje
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        text += " ".join(row) + "\n"

        # Ako je query u tekstu, vratiti deo teksta kao odgovor
        if query.lower() in text.lower():
            start_index = text.lower().find(query.lower())
            end_index = start_index + 500  # Povećaj broj karaktera ako je potrebno
            snippet = text[start_index:end_index]
            return snippet
        else:
            return None  # Ako nije pronađeno ništa, vrati None
    except FileNotFoundError:
        return None  # Ako PDF fajl nije pronađen
