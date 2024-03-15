# data = {}
# def get_parsed_data(file):
#     with open(file, "rb") as pdf_file:
#         # Create a PDF reader object
#         pdf_reader = PyPDF2.PdfReader(pdf_file)
#
#         # Get the first page
#         first_page = pdf_reader.pages[0]
#
#         # Extract text from the page
#         text = first_page.extract_text().strip()
#
#         # Extract name from the text
#         name = extract_name(text)
#         email = extract_email(text)
#         mobile_number = extract_phone_numbers(text)
#         clg = clgparser.extactcollegs(file)
#
#         eachdatadict = {}
#         eachdatadict.update({'name': name})
#         eachdatadict.update({'email': email})
#         eachdatadict.update({'mobile_number': mobile_number})
#         eachdatadict.update({'college': clg})
#
#     data.update({file: eachdatadict})
#
#
# def process_pdfs_multithreading():
#     threads = []
#     for pdf_path in resume_list:
#         thread = threading.Thread(target=get_parsed_data(pdf_path), args=(pdf_path,))
#         thread.start()
#         threads.append(thread)
#     for thread in threads:
#         thread.join()
#     jsonobj = {'entiies': data}
#     return jsonobj