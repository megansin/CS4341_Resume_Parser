import os
import pip
from flask import Flask, request, render_template, jsonify, send_from_directory, abort
from werkzeug.utils import secure_filename
from KeywordFinder import get_keywords
from ResumeParser import resume_parser
from fuzzywuzzy import fuzz


app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.docx', '.pdf', '.txt']
app.config['UPLOAD_PATH'] = 'uploads'


def intersect_keywords(resume, keywords):
    skills = resume['skills']
    degree = resume['degree']
    experience = resume['experience']
    resume_vals = []
    for s in skills:
        resume_vals.append(s.lower())
    for d in degree:
        resume_vals.append(d.lower())
    for e in experience:
        resume_vals.append(e.lower())
    keywords_dict = {k: False for k in keywords}
    intersect = list(set(keywords) & set(resume_vals))
    for i in intersect:
        keywords_dict[i] = True
    ratio = len(intersect)/len(keywords)
    return keywords_dict, ratio


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    # if request.method == 'POST':
    job_text = request.form.get('text1')
    keywords = get_keywords(job_text)

    resume_file = request.files['filename']
    filename = secure_filename(resume_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        path = os.path.join(app.config['UPLOAD_PATH'], filename)
        resume_file.save(path)
        parsed_resume = resume_parser(path)
        keywords_dict, ratio = intersect_keywords(parsed_resume, keywords)

    return render_template('result.html', keywords=keywords, parsed_resume=parsed_resume, dict=keywords_dict, ratio=ratio)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
