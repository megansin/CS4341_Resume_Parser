from pyresparser import ResumeParser
import os
from docx import Document

# pip.main(['install', 'pyresparser'])
# pip.main(['install', 'docx'])

# Enter the path of the resume file
# File should be .txt, .docx, .pdf
filed = input()

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
    print(data['skills'])

except:
    # This next line does the parsing
    data = ResumeParser(filed).get_extracted_data()
    # This next line prints the skills (aka keywords) parsed from the resume
    print(data['skills'])

# if you only want to obtain the skills (aka keywords) parsed from the resume
# print(data['skills'])

# This next line prints the dictionary containing the extracted information
# # print(data)
# Contains the following: name, email, mobile_number, skills, college_name, degree, designation, experience, company_names, no_of_pages, total_experience
