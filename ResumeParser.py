# TODO: UNCOMMENT LINES BELOW TO DOWNLOAD NECESSARY PACKAGES BEFORE RUNNING:
# import pip
# pip.main(['install', 'spacy==2.3.5'])
# pip.main(['install', 'https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz'])
# pip.main(['install', 'python-docx'])
# pip.main(['install', 'pyresparser'])


from pyresparser import ResumeParser
from docx import Document


import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
STOPWORDS = set(stopwords.words('english'))


def resume_parser(file_path):
    # Enter the path of the resume file
    # File should be .txt, .docx, .pdf

    # Parse the resume file
    if '.txt' in file_path:
        # This next line converts the .txt file to .docx
        doc = Document()
        # This next line opens the .txt file
        with open(file_path, 'r') as f:
            # This next line adds the .txt file to the .docx file
            doc.add_paragraph(f.read())
        # This next line saves the .docx file
        doc.save('resume.docx')
        # This next line does the parsing
        data = ResumeParser('resume.docx').get_extracted_data()

    else:
        data = ResumeParser(file_path).get_extracted_data()

    # skills (aka keywords) parsed from the resume
    # print(data['skills'])

    # dictionary containing the extracted information
    # Contains: name, email, mobile_number, skills, college_name, degree, designation, experience, company_names, no_of_pages, total_experience
    return data
