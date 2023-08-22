from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def render_html():
    return render_template('index2.html')

@app.route('/home')
def home():
    return render_template('index2.html')

@app.route('/upload')
def upload():
    return render_template('upload.html' , message = "Welcome!")

@app.route('/download')
def download():
    return render_template('download.html' , message = "Welcome!")

@app.route('/connect')
def connect_blockchain():
    return render_template('connect.html', chain =0, nodes =0)

if __name__ == '__main__':
    app.run(debug=True)