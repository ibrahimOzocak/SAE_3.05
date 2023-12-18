import pdfplumber

def extract_text_and_style_from_pdf(pdf_path):
    text_with_style = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            for text_line in page.extract_text().split('\n'):
                if text_line == "PERSONNEL TECHNIQUE À PRÉVOIR PAR L’ORGANISATEUR :": 
                    pass
                elif text_line == "INFOS ARTISTE :":
                    pass
                elif text_line == "RIDER :":
                    if text_line == "ACCÈS ET FEUILLE DE ROUTE :":
                        pass
                    elif text_line == "TRANSPORTS :":
                        pass
                    elif text_line == "HÉBERGEMENT :":
                        pass
                    elif text_line == "LOGES :":
                        pass
                    elif text_line == "CATERING :":
                        pass
                    elif text_line == "INVITATIONS :":
                        pass
    return text_with_style
    
print(extract_text_and_style_from_pdf("./doc/Fiche_technique_luf_-_Astro-Symphonie_v1.1.pdf"))
