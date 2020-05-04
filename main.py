import os
from flask import Flask, flash, request, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'json'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.config['DEBUG'] = False

user = 0
task = 0
bar = 50


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/')
def hello_world():
    return 'Gesture Collect Server'


@app.route('/get_user')
def get_user():
    global user
    return str(user)


@app.route('/get_task')
def get_task():
    global task
    return str(task)


@app.route('/get_bar')
def get_bar():
    global bar
    return str(bar)


@app.route('/get_status')
def get_status():
    global user, task
    return '当前用户为 '+str(user)+' 任务为 '+str(task)+' 要求次数为 '+str(bar)


@app.route('/set_user', methods=['GET'])
def set_user():
    global user
    try:
        user = int(request.args.get('user'))
        return 'Succeed'
    except Exception as e:
        return 'Failed\n'+str(e)


@app.route('/set_task', methods=['GET'])
def set_task():
    global task
    try:
        task = int(request.args.get('task'))
        return 'Succeed'
    except Exception as e:
        return 'Failed\n' + str(e)


@app.route('/set_bar', methods=['GET'])
def set_bar():
    global bar
    try:
        bar = int(request.args.get('bar'))
        return 'Succeed'
    except Exception as e:
        return 'Failed\n' + str(e)


@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if filename == str(user)+"-"+str(task)+".json":
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return 'Succeed'
            else:
                return 'Failed\n'+get_status()

    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''


if __name__ == '__main__':
    app.run(port=8888, host='0.0.0.0')
