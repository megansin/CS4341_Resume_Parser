from flask import Flask, request, render_template, jsonify, url_for
from KeywordFinder import get_keywords
from ResumeParser import resume_parser

app = Flask(__name__)


def do_something(jobDes, resume):
    jobDes = jobDes
    resume = resume
    test1 = 1
    test2 = 2
    combine = test1 + test2
    return combine


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    # if request.method == 'POST':
    resume_file = request.files['filename']
    job_text = request.form.get('text1')
    # parsed_resume = resume_parser(resume_file)
    keywords = get_keywords(job_text)
    # result = {
    #     "output": combine
    # }
    # result = {str(key): value for key, value in result.items()}
    # return jsonify(result=result)
    return render_template('result.html', keywords=keywords)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
