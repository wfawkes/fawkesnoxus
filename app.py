from flask import Flask, render_template, request, redirect

app = Flask(__name__)

opinions = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    opiniao = request.form['opiniao']
    if opiniao:
        opinions.append(opiniao)
    return redirect('/')

@app.route('/admin')
def admin():
    return "<br>".join(opinions)
