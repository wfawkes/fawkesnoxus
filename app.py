from flask import Flask, render_template, request

app = Flask(__name__)

opinions = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        opinion = request.form.get('opinion')
        if opinion:
            opinions.append(opinion)
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html', opinions=opinions)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
