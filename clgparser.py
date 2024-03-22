import spacy
import re
import PyPDF2
import tabula

import clgparser

nlp = spacy.load('en_core_web_sm')

clg_error_count = 0


def table_data(resume):
    try:
        tables = tabula.read_pdf(resume, pages='all', multiple_tables=True)
        college_name = []

        # Convert each table into text
        for table in tables:
            # Flatten the table and concatenate values into a single text string
            table_text = ['\t'.join(map(str, row)) for row in table.values]
            for cell in table_text:
                if cell.upper().__contains__("COLLEGE") | cell.upper().__contains__(
                        "EDUCATION") | cell.upper().__contains__("INSTITUTE") | cell.upper().__contains__("UNIVERSITY") \
                        | cell.upper().__contains__("ACADEMY") | cell.upper().__contains__(
                    "SCHOOL") | cell.upper().__contains__("OF ENGINEERING"):
                    college_name.append(cell)
            clg = set()
            for row in college_name:
                fields = row.split('\t')  # Split the entry by '\t'
                cleaned_fields = [field.replace('\r', ' ') for field in
                                  fields]  # Replace '\r' with space in each field
                for field in cleaned_fields:
                    clg.add(field)
            # Now you can process the table text as needed
            return clg
    except:
        pass


def extactcollegs(resume):
    # Create a PDF reader object
    global doc
    pdf_reader = PyPDF2.PdfReader(resume)

    # Initialize a variable to store college names
    return_data = {}
    college_names = []
    pages_text = ''
    # Loop through each page in the PDF
    for page in pdf_reader.pages:
        # Extract text from the page
        text = page.extract_text().strip()
        pages_text = pages_text + ' ' + text
        lines = text.splitlines()
        # Process the text with spaCy NER
        doc = nlp(text)

        # Extract entities labeled as organizations or educational institutions
        for entity in doc.ents:
            if entity.label_ in ['ORG', 'EDU']:
                # Add the entity text to the list of college names
                college_names.append(str(entity.text))

    index = []
    for clg in college_names:
        if clg.__contains__('\n'):
            index.append(college_names.index(clg))
    for i in index:
        college_names.pop(i)
        college_names.insert(i + 1, 'x')

    selected_clg_names = []
    defaul_clgs = []

    # second layer of NER
    doc2 = nlp(str(college_names))
    for ent in doc2.ents:
        if ent.label_ == 'ORG':
            if len(ent) > 1:
                if ent.text.upper().__contains__("COLLEGE") | ent.text.upper().__contains__(
                        "EDUCATION") | ent.text.upper().__contains__("INSTITUTE") \
                        | ent.text.upper().__contains__("UNIVERSITY") | ent.text.upper().__contains__(
                    "ACADEMY") | ent.text.upper().__contains__(
                    "SCHOOL"):
                    selected_clg_names.append(str(ent))
            else:
                pass

    # extracting lines directly if line contains following keyword in case of 0 or 1 college extracted above
    if len(selected_clg_names) <= 1:
        for line in lines:
            if line.upper().__contains__("COLLEGE") | line.upper().__contains__(
                    "EDUCATION") | line.upper().__contains__("INSTITUTE") | line.upper().__contains__("UNIVERSITY") \
                    | line.upper().__contains__("ACADEMY") | line.upper().__contains__(
                "SCHOOL") | line.upper().__contains__("OF ENGINEERING"):
                defaul_clgs.append(line)

    for clg in defaul_clgs:
        selected_clg_names.append(str(clg))

    table_d = table_data(resume)
    if table_d is not None:
        for table_clg in table_d:
            print(table_clg)
            selected_clg_names.append(table_clg)

    # selected_clg_names.append(defaul_clgs)
    if len(selected_clg_names) == 0:
        clgparser.clg_error_count += 1

    return_data.update({'colleges' : selected_clg_names})
    return_data.update({'page_text' : pages_text})

    return return_data
