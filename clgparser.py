import spacy
import re
import PyPDF2

import clgparser

nlp = spacy.load('en_core_web_sm')

clg_error_count = 0
def extactcollegs(resume):
    # Create a PDF reader object
    global doc
    pdf_reader = PyPDF2.PdfReader(resume)

    # Initialize a variable to store college names
    college_names = []

    # Loop through each page in the PDF
    for page in pdf_reader.pages:
        # Extract text from the page
        text = page.extract_text().strip()
        lines = text.splitlines()
        # Process the text with spaCy NER
        doc = nlp(text)

        # Extract entities labeled as organizations or educational institutions
        for entity in doc.ents:
            if entity.label_ in ['ORG', 'EDU']:
                # Add the entity text to the list of college names
                college_names.append(str(entity.text))

    # Print the extracted college names
    index = []
    for clg in college_names:
        if clg.__contains__('\n'):
            index.append(college_names.index(clg))
    for i in index:
        college_names.pop(i)
        college_names.insert(i + 1, 'x')

    selected_clg_names = []
    defaul_clgs = []
    doc2 = nlp(str(college_names))
    for ent in doc2.ents:
        if ent.label_ == 'ORG':
            if len(ent) > 1:
                if ent.text.upper().__contains__("COLLEGE") | ent.text.upper().__contains__("EDUCATION") | ent.text.upper().__contains__(
                        "college") | ent.text.upper().__contains__("INSTITUTE") \
                        | ent.text.upper().__contains__("UNIVERSITY") | ent.text.upper().__contains__(
                    "university") | ent.text.upper().__contains__(
                    "Institute"):
                    selected_clg_names.append(str(ent))
            else:
                pass
    if len(selected_clg_names) == 0:
        for line in lines:
            if str(resume).__contains__("Aditya Namdev Magdum.RESUME pdf..pdf"):
                print(line)

            if line.upper().__contains__("COLLEGE") | line.upper().__contains__("EDUCATION") | line.upper().__contains__("college") | line.upper().__contains__("INSTITUTE")| line.upper().__contains__("UNIVERSITY") | line.upper().__contains__("university") | line.upper().__contains__("Institute")|line.upper().__contains__("Academy")|line.upper().__contains__("academy")|line.upper().__contains__("School")|line.upper().__contains__("school"):
                defaul_clgs.append(line)
                # if '\n' in line:
                #     newline_index = line.find('\n')
                #     trimmed_ent = doc.char_span(line.start_char + newline_index + 1, line.end_char)
                #     defaul_clgs.append(str(trimmed_ent))
                # else:
                #     defaul_clgs.append(line)

    for clg in defaul_clgs:
        selected_clg_names.append(str(clg))
    # selected_clg_names.append(defaul_clgs)
    if len(selected_clg_names) == 0 :
        clgparser.clg_error_count += 1

    print(clgparser.clg_error_count)
    return selected_clg_names
