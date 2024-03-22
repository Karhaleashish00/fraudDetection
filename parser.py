import os
import re
import PyPDF2
import spacy
from flask import jsonify
from spacy.matcher import Matcher
import clgparser


# Load English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load('en_core_web_sm')

# Initialize matcher with a vocab
matcher = Matcher(nlp.vocab)


# Define a custom pattern for name extraction
def extract_name(resume_text):
    nlp_text = nlp(resume_text)
    nameofperson = [entity.text for entity in nlp_text.ents if (entity.label_ == 'PERSON')]
    try:
        return str(nameofperson[0])
    except Exception as e:
        pass
    # past code 1


def extract_email(resume_text):
    # Use regex pattern to extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(email_pattern, resume_text)
    if matches:
        return str(matches[0])


def extract_phone_numbers(resume_text):
    # Use regex pattern to extract phone numbers
    nlp_text = nlp(resume_text)
    phone_pattern = r'\b\d{10}\b|\d{10}'
    # phone_pattern = r'\+?\d{1,2}[\s|-]?\(?\d{3}\)?[\s|-]?\d{3}[\s|-]?\d{4}|\+?\d{1,2}[\s|-]?\d{10}'
    matches = re.findall(phone_pattern, str(nlp_text))
    if len(matches) == 0:
        phone_pattern = r'\(\d{3}\) \d{3}-\d{4}'
        matches2 = re.findall(phone_pattern, str(nlp_text))
        return matches2
    else:
        return matches


def get_resume_list():
    folder_path = 'D:/New folder/Resume/Resume'
    resume_list1 = []
    count = 0

    # Iterate through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            resume_list1.append(file_path)
            count = count + 1
            if count == 10:
                break
    print(" count  = ", count)
    return resume_list1

def get_parsed_data():
    data = []
    resume_list = get_resume_list()
    for file in resume_list:
        try:
            with open(file, "rb") as pdf_file:
                # Create a PDF reader object
                pdf_reader = PyPDF2.PdfReader(pdf_file)

                # Get the first page
                first_page = pdf_reader.pages[0]

                # Extract text from the page
                text = first_page.extract_text().strip()

                # Extract name from the text
                name = extract_name(text)
                email = extract_email(text)
                mobile_number = extract_phone_numbers(text)
                clg = clgparser.extactcollegs(file)

                eachdatadict = {}
                index = file.find('/')

                # Get the substring starting from the character after '/'
                trimmed_filename = file[index + 1:]

                eachdatadict.update({'filename': trimmed_filename})
                eachdatadict.update({'name': name})
                eachdatadict.update({'email': email})
                eachdatadict.update({'mobile_number': mobile_number})
                eachdatadict.update({'college': clg})
        except KeyError:
            continue
        except PyPDF2.errors.PdfReadError:
            continue

        data.append(eachdatadict)
    return data

