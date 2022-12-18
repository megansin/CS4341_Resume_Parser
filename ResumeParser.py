import io

import pip
from pyresparser import ResumeParser
from docx import Document
from nltk.corpus import stopwords
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import docx2txt
import spacy
import pandas as pd
from spacy.matcher import Matcher
import re


# TODO: UNCOMMENT LINES BELOW TO DOWNLOAD NECESSARY PACKAGES BEFORE RUNNING:
# nltk.download('stopwords')
# pip.main(['install', 'spacy==2.3.5'])
# pip.main(['install', 'https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz'])
# pip.main(['install', 'python-docx'])
# pip.main(['install', 'pyresparser'])
# pip.main(['install', 'pdfminer.six'])
# pip.main(['install', 'doc2text'])

STOPWORDS = set(stopwords.words('english'))
nlp = spacy.load('en_core_web_sm')

# matcher = Matcher(nlp.vocab)
# noun_chunks = nlp.noun_chunks()
# EDUCATION = [
#             'BE','B.E.', 'B.E', 'BS', 'B.S',
#             'ME', 'M.E', 'M.E.', 'MS', 'M.S',
#             'BTECH', 'B.TECH', 'M.TECH', 'MTECH',
#             'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII', 'PhD', 'Bachelor\'s'
#         ]


# def extract_text_from_pdf(pdf_path):
#     with open(pdf_path, 'rb') as fh:
#         # iterate over all pages of PDF document
#         for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
#             # creating a resoure manager
#             resource_manager = PDFResourceManager()
#
#             # create a file handle
#             fake_file_handle = io.StringIO()
#
#             # creating a text converter object
#             converter = TextConverter(
#                 resource_manager,
#                 fake_file_handle,
#                 codec='utf-8',
#                 laparams=LAParams()
#             )
#
#             # creating a page interpreter
#             page_interpreter = PDFPageInterpreter(
#                 resource_manager,
#                 converter
#             )
#
#             # process current page
#             page_interpreter.process_page(page)
#
#             # extract text
#             text = fake_file_handle.getvalue()
#             yield text
#
#             # close open handles
#             converter.close()
#             fake_file_handle.close()
#
#
# def extract_text_from_doc(doc_path):
#     temp = docx2txt.process(doc_path)
#     text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
#     return ' '.join(text)
#
#
# def extract_name(resume_text):
#     nlp_text = nlp(resume_text)
#
#     # First name and Last name are always Proper Nouns
#     pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
#
#     matcher.add('NAME', None, *pattern)
#
#     matches = matcher(nlp_text)
#
#     for match_id, start, end in matches:
#         span = nlp_text[start:end]
#         return span.text
#
#
# def extract_mobile_number(text):
#     phone = re.findall(re.compile(
#         r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'),
#                        text)
#
#     if phone:
#         number = ''.join(phone[0])
#         if len(number) > 10:
#             return '+' + number
#         else:
#             return number
#
#
# def extract_email(email):
#     email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", email)
#     if email:
#         try:
#             return email[0].split()[0].strip(';')
#         except IndexError:
#             return None
#
#
# def extract_skills(resume_text):
#     nlp_text = nlp(resume_text)
#
#     # removing stop words and implementing word tokenization
#     tokens = [token.text for token in nlp_text if not token.is_stop]
#
#     # reading the csv file
#     data = pd.read_csv("skills.csv")
#
#     # extract values
#     skills = list(data.columns.values)
#
#     skillset = []
#
#     # check for one-grams (example: python)
#     for token in tokens:
#         if token.lower() in skills:
#             skillset.append(token)
#
#     # check for bi-grams and tri-grams (example: machine learning)
#     for token in noun_chunks:
#         token = token.text.lower().strip()
#         if token in skills:
#             skillset.append(token)
#
#     return [i.capitalize() for i in set([i.lower() for i in skillset])]
#
#
# def extract_education(resume_text):
#     nlp_text = nlp(resume_text)
#
#     # Sentence Tokenizer
#     nlp_text = [sent.string.strip() for sent in nlp_text.sents]
#
#     edu = {}
#     # Extract education degree
#     for index, text in enumerate(nlp_text):
#         for tex in text.split():
#             # Replace all special symbols
#             tex = re.sub(r'[?|$|.|!|,]', r'', tex)
#             if tex.upper() in EDUCATION and tex not in STOPWORDS:
#                 edu[tex] = text + nlp_text[index + 1]
#
#     # Extract year
#     education = []
#     for key in edu.keys():
#         year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
#         if year:
#             education.append((key, ''.join(year[0])))
#         else:
#             education.append(key)
#     return education


def resume_parser(file_path):
    # Enter the path of the resume file
    # File should be .txt, .docx, .pdf

    # Parse the resume file
    if file_path.contains(".txt"):
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
