# pip install pyresparser
# pip install python-docx
import pip
from pyresparser import ResumeParser
from docx import Document
import nltk
from nltk.corpus import stopwords

# TODO: UNCOMMENT 4 LINES BELOW TO DOWNLOAD NECESSARY PACKAGES BEFORE RUNNING:
# nltk.download('stopwords')
# pip.main(['install', 'spacy==2.3.5'])
# pip.main(['install', 'https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz'])
# pip.main(['install', 'pyresparser'])

STOPWORDS = set(stopwords.words('english'))

def resume_parser(file_path):
    # Enter the path of the resume file
    # File should be .txt, .docx, .pdf
    filed = file_path

    # Parse the resume file
    try:
        # This next line converts the .txt file to .docx
        doc = Document()
        # This next line opens the .txt file
        with open(filed, 'r') as f:
            # This next line adds the .txt file to the .docx file
            doc.add_paragraph(f.read())
        # This next line saves the .docx file
        doc.save('resume.docx')
        # This next line does the parsing
        data = ResumeParser('resume.docx').get_extracted_data()
        # This next line prints the skills (aka keywords) parsed from the resume
        # print(data['skills'])
    except:
        # This next line does the parsing
        data = ResumeParser(file_path).get_extracted_data()
        # This next line prints the skills (aka keywords) parsed from the resume
        # print(data['skills'])

    # if you only want to obtain the skills (aka keywords) parsed from the resume
    # print(data['skills'])

    # This next line prints the dictionary containing the extracted information
    # # print(data)
    return data
    # Contains the following: name, email, mobile_number, skills, college_name, degree, designation, experience, company_names, no_of_pages, total_experience