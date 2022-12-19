import os
import pip
from flask import Flask, request, render_template, flash, redirect
from werkzeug.utils import secure_filename
from KeywordFinder import get_keywords
from ResumeParser import resume_parser
from fuzzywuzzy import fuzz


app = Flask(__name__)
app.secret_key = "something"
app.config['UPLOAD_EXTENSIONS'] = ['.docx', '.pdf', '.txt']
app.config['UPLOAD_PATH'] = '.'


def intersect_keywords(resume, keywords):
    skills = list(filter(lambda item: item is not None, resume['skills']))
    degree = list(filter(lambda item: item is not None, resume['degree']))
    experience = list(filter(lambda item: item is not None, resume['experience']))
    resume_vals = []
    for s in skills:
        resume_vals.extend(s.lower().split())
    for d in degree:
        resume_vals.extend(d.lower().split())
    for e in experience:
        resume_vals.extend(e.lower().split())

    found = set(keywords).intersection(set(resume_vals))
    missing = set(keywords) - found
    found = list(found)
    missing = list(missing)

    ratio = fuzz.token_set_ratio(keywords, resume_vals)

    return missing, found, ratio


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    # if request.method == 'POST':
    job_text = request.form.get('text1')
    if len(job_text) < 1:
        flash('Empty job description, please enter text and try again', category='error')
        return render_template("home.html")

    keywords = get_keywords(job_text)

    resume_file = request.files['filename']
    filename = secure_filename(resume_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            flash('Must be a .docx, .txt, or .pdf file', category='error')
            return render_template("home.html")
        path = os.path.join(app.config['UPLOAD_PATH'], filename)
        resume_file.save(path)
        parsed_resume = resume_parser(path)
        missing, found, ratio = intersect_keywords(parsed_resume, keywords)
    else:
        flash('No file uploaded', category='error')
        return render_template("home.html")

    return render_template('result.html', keywords=keywords, parsed_resume=parsed_resume, missing=missing, found=found,
                           ratio=ratio)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
