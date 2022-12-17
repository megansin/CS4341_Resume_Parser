from flask import Flask, request, render_template,jsonify
from KeywordFinder import get_keywords
from ResumeParser import resume_parser

app = Flask(__name__)

def do_something(jobDes, resume):
   jobDes = jobDes
   resume = resume
   test1= 1
   test2 =2
   combine = test1 + test2
   return combine

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/join', methods=['GET','POST'])
def my_form_post():
    jobDes = 1
    resume = 2
    combine = do_something(jobDes,resume)
    result = {
        "output": combine
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)


if __name__ == '__main__':
    app.run(debug=True)