from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'chave_super_secreta_qualquer'  # para sessões

ADMIN_PASSWORD = "*J21072022w"
OPINIONS_FILE = "opinions.txt"

# Carrega opiniões salvas, se houver
def load_opinions():
    if os.path.exists(OPINIONS_FILE):
        with open(OPINIONS_FILE, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines()]
    return []

# Salva uma nova opinião no arquivo
def save_opinion(opinion):
    with open(OPINIONS_FILE, 'a', encoding='utf-8') as f:
        f.write(opinion.strip() + '\n')

opinions = load_opinions()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        opinion = request.form.get('opinion')
        if opinion:
            opinions.append(opinion)
            save_opinion(opinion)
            return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('admin'))
        else:
            return "Senha incorreta.", 401
    return render_template('login.html')

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
