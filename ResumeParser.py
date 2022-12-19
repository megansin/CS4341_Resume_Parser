from pyresparser import ResumeParser
from docx import Document
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
