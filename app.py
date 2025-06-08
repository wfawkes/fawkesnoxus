
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'chave_super_secreta_qualquer'  # para sessões

ADMIN_PASSWORD = "*J21072022w"

opinions = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        opinion = request.form.get('opinion')
        if opinion:
            opinions.append(opinion)
            return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('admin'))
        else:
            error = "Senha incorreta."
    return render_template('login.html', error=error)

@app.route('/admin')
def admin():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    return render_template('admin.html', opinions=opinions)

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
