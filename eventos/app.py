from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['GET'])
def submit():
    opcao = request.args.get('opcao')
    
    if opcao == 'Piscina':
        return redirect(url_for('piscina'))
    elif opcao == 'Churras':
        return redirect(url_for('churras'))
    elif opcao == 'Quer dar a bunda mesmo?':
        return redirect(url_for('darabunda'))
    else:
        return 'Opção inválida'

@app.route('/piscina')
def piscina():
    return render_template('piscina.html')

@app.route('/churras')
def churras():
    return render_template('churras.html')

@app.route('/dara')
def darabunda():
    return render_template('darabunda.html')

