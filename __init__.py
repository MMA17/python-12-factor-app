import os
from flask.helpers import make_response
from prometheus_client import metrics
from werkzeug.utils import secure_filename
from flask import Flask,flash,request,redirect,send_file,render_template,session,Response
from prometheus_flask_exporter import PrometheusMetrics
import pymysql.cursors
import socket

from connector import con
UPLOAD_FOLDER = 'uploads/'
#app = Flask(__name__)
app = Flask(__name__, template_folder='templates')
hostname = thisdict = {
  "host": socket.gethostname()
}
metrics = PrometheusMetrics(app, default_labels=hostname)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

by_path_counter = metrics.counter(
    'by_path_counter', 'Request count by request paths',
    labels={'path': lambda: request.path}
)

# Upload API
@app.route('/uploadfile', methods=['GET', 'POST'])
@by_path_counter
def upload_file():
    # print ("User_id: " + request.cookies.get('user_id')) 
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("saved file successfully")
            try:
                with con:
                    with con.cursor() as cursor:
                    # Create a new record
                        sql = "INSERT INTO files (filename, size) VALUES ('" + filename +"','" + str(os.path.getsize('./uploads/'+ filename)) +"')"
                        cursor.execute(sql)
                        con.commit()
            except print(0):
                pass
            
      #send file name as parameter to downlad
            return redirect('/downloadfile/'+ filename)
    return render_template('upload_file.html')

# Download API
@app.route("/downloadfile/<filename>", methods = ['GET'])
@by_path_counter
def download_file(filename):
    return render_template('download.html',value=filename)

@app.route('/return-files/<filename>')
@by_path_counter
def return_files_tut(filename):
    file_path = UPLOAD_FOLDER + filename
    return send_file(file_path, as_attachment=True, attachment_filename=filename)

user_ID = ''
@app.route('/login', methods=['GET', 'POST'])
@by_path_counter
def login():
    if request.method == 'POST':
        if 'username' == '' or 'pass' == '':
            print ("chua nhap day du thong tin")
            return redirect(request.url)
        else:
            
            username = request.form['username']
            passwd = request.form['pass']
            with con:
                with con.cursor() as cursor:
                    sql = "SELECT * FROM users WHERE username = %s AND pass = %s"
                    cursor.execute(sql, (username, passwd))
                    result = cursor.fetchall()
                    if len(result) > 0:
                        print("Dang nhap thanh cong")
                    for row in result:
                        user_ID = row["user_id"]
            return redirect('/setcookie')
    return render_template('login.html')

@app.route('/setcookie', methods=['GET', 'POST'])
@by_path_counter
def setcookie():
    resp = make_response(redirect('/uploadfile'))
    resp.set_cookie('user_id', user_ID)
    return resp

@app.route('/', methods=['GET', 'POST'])
@by_path_counter
def index():
    return redirect('/uploadfile')
    
if __name__ == "__main__":
    app.run(host='0.0.0.0')