from flask import Flask, session, request, render_template, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

bancodados = {}

#  Chave para criptografia de cookies na sessão
app.config['SECRET_KEY'] = 'superdificil'

@app.route('/')
def index():
    return render_template('index.html')

########################################################################

@app.route('/planilha', methods=['GET', 'POST'])
def planilha():
    total = 0
    checked_items = {}
    totais = {}
    
    if request.method == 'POST':
      
        for key, value in request.form.items():
            try:
                nome = key[4:]
                if nome not in totais:
                    totais[nome] = 0
                valor = float(value)
                totais[nome] += valor
                total += valor
                checked_items[key] = True
                print (key, value)
            except ValueError:
               
                continue
    
    return render_template('planilha.html', total=total, checked_items=checked_items, total_por_pessoa=totais)

###############################################################

@app.route('/evento')
def evento():
    return render_template('escolha_evento.html')

@app.route('/submit', methods=['GET'])
def submit():
    opcao = request.args.get('opcao')
    
    if opcao == 'Piscina':
        return redirect(url_for('evento_detalhe', nome_evento='Piscina'))
    elif opcao == 'Churrasco':
        return redirect(url_for('evento_detalhe', nome_evento='Churrasco'))
    else:
        return 'Opção inválida'

@app.route('/evento/<nome_evento>')
def evento_detalhe(nome_evento):
    return render_template('evento_detalhe.html', nome_evento=nome_evento)


####################################################################

@app.route('/juros', methods=['GET', 'POST'])
def juros():
    if request.method == 'POST':
        try:
            objetivo = float(request.form['valor'])
            taxa_juros = float(request.form['taxa'])
            periodo_meses = float(request.form['periodo'])
            num_pessoas = request.form.get('pessoas', 1)

            num_pessoas = int(num_pessoas) if num_pessoas else 1  # Definindo um valor padrão para evitar divisão por zero
            
            # Cálculo de juros simples
            juros_simples = objetivo * taxa_juros * (periodo_meses / 12) / 100
            valor_total_simples = objetivo + juros_simples
            
            # Cálculo da mensalidade para juros simples
            mensalidade_simples = objetivo / periodo_meses
            
            # Dividindo a mensalidade pelo número de pessoas
            mensalidade_por_pessoa_simples = mensalidade_simples / num_pessoas if num_pessoas > 0 else None

            objetivo = round(objetivo, 2)
            taxa_juros = round(taxa_juros, 2)
            periodo_meses = round(periodo_meses, 2)
            valor_total_simples = round(valor_total_simples, 2)
            mensalidade_simples = round(mensalidade_simples, 2)
            mensalidade_por_pessoa_simples = round(mensalidade_por_pessoa_simples, 2) if mensalidade_por_pessoa_simples is not None else None
            

            return render_template('juros.html', 
                                   objetivo=objetivo, 
                                   taxa_juros=taxa_juros, 
                                   valor_total_simples=valor_total_simples,
                                   periodo_meses=periodo_meses,
                                   mensalidade_simples=mensalidade_simples,
                                   num_pessoas=num_pessoas,
                                   mensalidade_por_pessoa_simples=mensalidade_por_pessoa_simples,
                                )
        except ValueError:
            return render_template('juros.html', error="Por favor, insira valores numéricos válidos.")
    
    return render_template('juros.html')

#################################################################################

usuarios_db = {
    "nilso" : {
        "senha": generate_password_hash("admin123"),
        "eh_admin": True
    },
    
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome_usuario = request.form['nome_usuario']
        senha = request.form['senha']

        usuario = usuarios_db.get(nome_usuario)

        if usuario and check_password_hash(usuario['senha'], senha):
            session['nome_usuario'] = nome_usuario
            session['eh_admin'] = usuario.get('eh_admin', False)
            return redirect(url_for('painel'))
        else:
            return "Credenciais inválidas", 401

    return render_template('login.html')

@app.route('/painel')
def painel():
    if 'nome_usuario' not in session:
        return redirect(url_for('login'))

    if session.get('eh_admin'):
        return render_template('painel.html', usuarios=usuarios_db)
    return "Acesso negado", 403

@app.route('/adicionar_usuario', methods=['GET', 'POST'])
def adicionar_usuario():
    if 'nome_usuario' not in session or not session.get('eh_admin'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        nome_usuario = request.form['nome_usuario']
        senha = request.form['senha']
        eh_admin = 'eh_admin' in request.form

        if nome_usuario in usuarios_db:
            return "Usuário já existe", 400

        usuarios_db[nome_usuario] = {
            "senha": generate_password_hash(senha),
            "eh_admin": eh_admin
        }
        return redirect(url_for('painel'))

    return render_template('adicionar_usuario.html')

@app.route('/logout')
def logout():
    session.pop('nome_usuario', None)
    session.pop('eh_admin', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)