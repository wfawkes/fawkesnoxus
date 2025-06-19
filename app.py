from flask import Flask, render_template, request, redirect, url_for, session
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)
app.secret_key = 'chave_super_secreta_qualquer'

ADMIN_PASSWORD = "*J21072022w"

opinions = []

# Configuração do e-mail
EMAIL_REMETENTE = "josewellisondossantos3@gmail.com"
EMAIL_SENHA = "wcrpzusakbordqgf"
EMAIL_DESTINO = "josewellisondossantos3@gmail.com"

def enviar_email(opiniao):
    try:
        msg = MIMEText(f"Nova opinião recebida:\n\n{opiniao}")
        msg['Subject'] = 'Nova opinião enviada pelo site'
        msg['From'] = EMAIL_REMETENTE
        msg['To'] = EMAIL_DESTINO

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_REMETENTE, EMAIL_SENHA)
            server.send_message(msg)

        print("E-mail enviado com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        opinion = request.form.get('opinion')
        if opinion:
            opinions.append(opinion)
            enviar_email(opinion)
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