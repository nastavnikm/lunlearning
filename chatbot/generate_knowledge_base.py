import pdfplumber
import re

# Kreiramo prazan rečnik za bazu znanja
knowledge_base = {}

# Otvaramo PDF
with pdfplumber.open('chatbot/cnc_manual.pdf') as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        lines = text.split('\n')
        for line in lines:
            # Tražimo linije koje sadrže G kodove ili M kodove
            match = re.match(r'([GM]\d+)\s+(.*)', line, re.IGNORECASE)
            if match:
                code = match.group(1).lower()
                description = match.group(2)
                knowledge_base[code] = description

# Štampamo šta smo dobili
for code, desc in knowledge_base.items():
    print(f"{code}: {desc}")
