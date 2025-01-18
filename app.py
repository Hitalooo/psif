from datetime import datetime

from flask import Flask, session, request, render_template, url_for, redirect, flash
from database.db import obter_conexao
from werkzeug.security import generate_password_hash, check_password_hash

from models.lancamentos import Lancamento
from models.participantes import Participante
from models.planilhas import Planilha
from util import datas


app = Flask(__name__)
app.secret_key = 'chave_secreta'

#  Chave para criptografia de cookies na sessão
app.config['SECRET_KEY'] = 'superdificil'

@app.route('/')
def index():
    return render_template('index.html')

########################################################################

@app.route('/planilhas/<id>', methods=['GET', 'POST'])
def planilha(id):
    p = Planilha.find(id)

    if not p:
        return render_template('erro404.html')
    
    datetime_ini = datetime.strptime(p.data_ini, '%Y-%m-%d')
    datetime_fim = datetime.strptime(p.data_fim, '%Y-%m-%d')
    # O +1 é pra contar pelo menos 1 mês
    diferenca = datas.diferenca_meses(datetime_ini, datetime_fim) + 1
    # Gera o nome dos meses
    meses = []
    for i in range(diferenca):
        m = (i + datetime_ini.month) % 12
        # TODO: Gambiarra. Resolver de outra forma depois.
        if m == 0:
            m = 12
        meses += [datas.mes(m)]
    return render_template('planilha.html', planilha=p, meses=meses)

########################################################################

@app.route('/planilhas', methods=['GET', 'POST'])
def planilhas():
    if request.method == 'POST':
        objetivo = request.form.get('objetivo')
        descricao = request.form.get('descricao')
        data_ini = request.form.get('data_ini')
        data_fim = request.form.get('data_fim')
        p = Planilha(descricao, objetivo, data_ini, data_fim)
        p.salvar()
    
    planilhas = Planilha.consultar('SELECT * FROM planilhas')  # TODO: Filtrar pelo usuário logado
    return render_template('planilhas.html', planilhas=planilhas)

########################################################################

@app.route('/planilhas/<int:id_planilha>/participantes', methods=['GET', 'POST'])
def participantes(id_planilha):
    if request.method == 'POST':
        # TODO: tratar dados ausentes
        nome = request.form.get('nome_participante')
        contato = request.form.get('contato_participante')
        p = Participante(id_planilha=id_planilha, contato=contato, nome=nome)
        p.salvar()

    return redirect(url_for('planilha', id=id_planilha))


###############################################################

@app.route('/planilhas/excluir/<int:id_planilha>', methods=['POST'])  # TODO: trocar rota para /planilhas/<int:id_planilha>/excluir
def excluir_planilha(id_planilha):
    p = Planilha.encontrar(id_planilha)
    p.excluir()
    return redirect(url_for('planilhas'))

###############################################################

@app.route('/planilhas/<int:id_planilha>/lancamentos', methods=['GET', 'POST'])
def lancamentos(id_planilha):
    if request.method == 'POST':
        participante = request.form.get('participante')
        descricao = request.form.get('descricao')
        data = request.form.get('data')
        valor = request.form.get('valor')
        if not participante:
            flash('Por favor, selecione um participante.', 'error')
            return redirect(url_for('planilha', id=id_planilha))
        l = Lancamento(id_planilha, participante, descricao, data, valor)
        l.salvar()
    return redirect(url_for('planilha', id=id_planilha))

###############################################################

@app.route('/planilhas/<int:id_planilha>/lancamentos/<int:id_lancamento>/excluir', methods=['POST'])
def excluir_lancamento(id_planilha, id_lancamento):
    l = Lancamento.encontrar(id_lancamento)
    l.excluir()
    return redirect(url_for('planilha', id=id_planilha))

#################################################################

@app.route('/planilhas/<int:id_planilha>/grafico', methods=['GET'])
def grafico(id_planilha):
    p = Planilha.encontrar(id_planilha)

    return render_template('grafico.html', planilha=p)

#################################################################

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
            objetivo = float(request.form['objetivo'])  # Valor total que se quer juntar
            taxa_juros = float(request.form['taxa']) / 100 / 12  # Convertendo para taxa mensal
            periodo_meses = int(request.form['periodo'])  # Período em meses
            num_pessoas = int(request.form['pessoas'])  # Número de pessoas
            
            # Cálculo da mensalidade total
            mensalidade_total = objetivo / periodo_meses
            
            # Cálculo da mensalidade por pessoa
            mensalidade_por_pessoa = mensalidade_total / num_pessoas
            
            # Cálculo do montante acumulado usando a fórmula M = C x (1 + i)^t
            if taxa_juros > 0:
                montante_acumulado = mensalidade_total * (((1 + taxa_juros) ** periodo_meses - 1) / taxa_juros)
            else:
                montante_acumulado = mensalidade_total * periodo_meses  # Sem juros, apenas somando

            # Arredondar valores para exibição
            objetivo = round(objetivo, 2)
            taxa_juros = round(taxa_juros * 100 * 12, 2)  # Convertendo de volta para percentual anual
            periodo_meses = round(periodo_meses, 2)
            mensalidade_por_pessoa = round(mensalidade_por_pessoa, 2)
            mensalidade_total = round(mensalidade_total, 2)
            montante_acumulado = round(montante_acumulado, 2)

            return render_template('juros.html', 
                                   objetivo=objetivo, 
                                   taxa_juros=taxa_juros, 
                                   periodo_meses=periodo_meses,
                                   mensalidade_por_pessoa=mensalidade_por_pessoa,
                                   mensalidade_total=mensalidade_total,
                                   montante_acumulado=montante_acumulado
                                  )
        except ValueError:
            return render_template('juros.html', error="Por favor, insira valores numéricos válidos.")

    return render_template('juros.html')



#################################################################################

@app.route('/cadastro', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nome_usuario = request.form['nome_usuario']
        senha = request.form['senha']
        eh_admin = 'eh_admin' in request.form  # Define se o usuário será admin

        # Verificar se o usuário já existe no banco de dados
        conn = obter_conexao()
        usuario_existente = conn.execute('SELECT * FROM Usuarios WHERE nome_usuario = ?', (nome_usuario,)).fetchone()

        if usuario_existente:
            conn.close()
            return "Usuário já existe", 400

        # Inserir novo usuário no banco de dados
        senha_hash = generate_password_hash(senha)
        conn.execute('INSERT INTO Usuarios (nome_usuario, senha_hash, eh_admin) VALUES (?, ?, ?)',
                     (nome_usuario, senha_hash, eh_admin))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('cadastro.html')

#################################################################################

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome_usuario = request.form['nome_usuario']
        senha = request.form['senha']

        # Conectar ao banco e buscar o usuário
        conn = obter_conexao()
        usuario = conn.execute('SELECT * FROM Usuarios WHERE nome_usuario = ?', (nome_usuario,)).fetchone()
        conn.close()

        if usuario and check_password_hash(usuario['senha_hash'], senha):
            session['nome_usuario'] = nome_usuario
            session['eh_admin'] = usuario['eh_admin']
            return redirect(url_for('painel'))
        else:
            return "Credenciais inválidas", 401

    return render_template('login.html')

#################################################################################

@app.route('/painel')
def painel():
    # Verificar se o usuário está logado
    if 'nome_usuario' not in session:
        return redirect(url_for('login'))

    # Conectar ao banco para buscar a lista de usuários
    conn = obter_conexao()
    usuarios = conn.execute('SELECT * FROM Usuarios').fetchall()
    conn.close()

    # Renderizar o painel, passando se o usuário é admin ou não
    return render_template('painel.html', usuarios=usuarios, eh_admin=session.get('eh_admin'))



#################################################################################

@app.route('/adicionar_usuario', methods=['GET', 'POST'])
def adicionar_usuario():
    if 'nome_usuario' not in session or not session.get('eh_admin'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        nome_usuario = request.form['nome_usuario']
        senha = request.form['senha']
        eh_admin = 'eh_admin' in request.form  # Define se o usuário é admin

        # Verificar se o usuário já existe no banco de dados
        conn = obter_conexao()
        usuario_existente = conn.execute('SELECT * FROM Usuarios WHERE nome_usuario = ?', (nome_usuario,)).fetchone()

        if usuario_existente:
            conn.close()
            return "Usuário já existe", 400

        # Inserir novo usuário no banco de dados
        senha_hash = generate_password_hash(senha)
        conn.execute('INSERT INTO Usuarios (nome_usuario, senha_hash, eh_admin) VALUES (?, ?, ?)',
                     (nome_usuario, senha_hash, eh_admin))
        conn.commit()
        conn.close()

        return redirect(url_for('painel'))

    return render_template('adicionar_usuario.html')

######## SENHA ADMIN:admin OUTROS USUARIOS: 123

#################################################################################

@app.route('/logout')
def logout():
    session.pop('nome_usuario', None)
    session.pop('eh_admin', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True) 