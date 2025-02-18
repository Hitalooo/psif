from datetime import datetime
from flask import Flask, session, request, render_template, url_for, redirect, flash
from math import ceil
from database.db import obter_conexao
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models.usuario import User
from models.lancamentos import Lancamento
from models.participantes import Participante
from models.planilhas import Planilha
from simulacoes import SimulacaoJurosCompostos, SimulacaoSemRendimento
from util import datas

app = Flask(__name__)
app.secret_key = 'chave_secreta'

#  Chave para criptografia de cookies na sessão
app.config['SECRET_KEY'] = 'superdificil'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

########################################################################

@app.route('/planilhas/<id>', methods=['GET', 'POST'])
@login_required
def planilha(id):
    p = Planilha.find(id)

    if not p:
        return render_template('erro404.html')

    if p.id_usuario == current_user.id:

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
    
    else:
        return render_template('erro404.html')

########################################################################

@app.route('/planilhas', methods=['GET', 'POST'])
@login_required
def planilhas():
    if request.method == 'POST':
        id_usuario = current_user.id
        objetivo = request.form.get('objetivo')
        descricao = request.form.get('descricao')
        data_ini = request.form.get('data_ini')
        data_fim = request.form.get('data_fim')
        p = Planilha(id_usuario, descricao, objetivo, data_ini, data_fim)
        p.salvar()
        
    
    planilhas = Planilha.consultar('SELECT * FROM planilhas WHERE id_usuario=?', (current_user.id,))  # TODO: Filtrar pelo usuário logado
    return render_template('planilhas.html', planilhas=planilhas)

########################################################################

@app.route('/planilhas/<int:id_planilha>/participantes', methods=['GET', 'POST'])
@login_required 
def participantes(id_planilha):
    if request.method == 'POST':
        # TODO: tratar dados ausentes
        nome = request.form.get('nome_participante')
        contato = request.form.get('contato_participante')
        p = Participante(id_planilha=id_planilha, contato=contato, nome=nome)
        p.salvar()

    return redirect(url_for('planilha', id=id_planilha))


###############################################################

@app.route('/planilhas/<int:id_planilha>/excluir', methods=['POST'])
def excluir_planilha(id_planilha):
    p = Planilha.encontrar(id_planilha)
    p.excluir()
    return redirect(url_for('planilhas'))

@app.route('/planilhas/<int:id_planilha>/editar', methods=['GET', 'POST'])
def editar_planilha(id_planilha):
    # Recupera a planilha com o id especificado
    planilha = Planilha.encontrar(id_planilha)
    if planilha is None:
        return render_template('erro404.html')
    
    if request.method == 'POST':
        # Obtém os dados enviados pelo formulário
        descricao = request.form['descricao']
        objetivo = request.form['objetivo']
        data_ini = request.form['data_ini']
        data_fim = request.form['data_fim']

        planilha.descricao = descricao
        planilha.objetivo = objetivo
        planilha.data_ini = data_ini
        planilha.data_fim = data_fim

        planilha.alterar()
        
        # Após a atualização, redireciona para a página da planilha editada
        return redirect(url_for('planilhas'))  # ou redireciona para qualquer outra página de sua escolha

    # Se o método for GET, apenas renderiza o formulário para editar a planilha
    return render_template('editar_planilha.html', planilha=planilha)

###############################################################

@app.route('/planilhas/<int:id_planilha>/lancamentos', methods=['GET', 'POST'])
@login_required
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
@login_required
def excluir_lancamento(id_planilha, id_lancamento):
    l = Lancamento.encontrar(id_lancamento)
    l.excluir()
    return redirect(url_for('planilha', id=id_planilha))

#################################################################

@app.route('/planilhas/<int:id_planilha>/tabela', methods=['GET'])
@login_required
def tabela(id_planilha):
    # TODO: Criar função para não repetir esse código da rota Planilhas.

    p = Planilha.find(id_planilha)

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

    return render_template('tabela.html', planilha=p, meses=meses)

#################################################################

@app.route('/planilhas/<int:id_planilha>/lista_participantes', methods=['GET'])
@login_required
def lista_participantes(id_planilha):
    # TODO: Criar função para não repetir esse código da rota Planilhas.

    p = Planilha.find(id_planilha)

    if not p:
        return render_template('erro404.html')
    
    return render_template('participantes.html', planilha=p)

#################################################################

@app.route('/planilhas/<int:id_planilha>/lista_lancamentos', methods=['GET'])
@login_required
def lista_lancamentos(id_planilha):
    # TODO: Criar função para não repetir esse código da rota Planilhas.

    p = Planilha.find(id_planilha)

    if not p:
        return render_template('erro404.html')
    
    return render_template('lancamentos.html', planilha=p)

#################################################################

@app.route('/eventos', methods=['GET', 'POST'])
@login_required
def eventos():
    conn = obter_conexao()
    if request.method == 'POST':
        nome = request.form['nome']
        contato = request.form['contato']
        preco = request.form['preco']
        data_horario = request.form['data_horario']
        local = request.form['local']
        
        conn.execute(
            'INSERT INTO eventos (nome, contato, preco, data_horario, local, id_usuario) VALUES (?, ?, ?, ?, ?, ?)',
            (nome, contato, preco, data_horario, local, current_user.id)
        )
        conn.commit()
    
    # Paginação
    pagina = request.args.get('pagina', 1, type=int)  # Página atual
    eventos_por_pagina = 2  # Quantidade de eventos por página
    offset = (pagina - 1) * eventos_por_pagina  # Cálculo do deslocamento
    
    eventos = conn.execute(
        'SELECT * FROM eventos WHERE id_usuario = ? LIMIT ? OFFSET ?',
        (current_user.id, eventos_por_pagina, offset)).fetchall()
    
    total_eventos = conn.execute(
        'SELECT COUNT(*) FROM eventos WHERE id_usuario = ?',
        (current_user.id,)).fetchone()[0]
    
    total_paginas = ceil(total_eventos / eventos_por_pagina)  # Total de páginas
    
    conn.close()
    return render_template('eventos.html', eventos=eventos, pagina=pagina, total_paginas=total_paginas)

@app.route('/eventos/<int:id_evento>/editar', methods=['GET', 'POST'])
@login_required
def editar_evento(id_evento):
    conn = obter_conexao()
    evento = conn.execute('SELECT * FROM eventos WHERE id = ? AND id_usuario = ?', (id_evento, current_user.id)).fetchone()
    
    if request.method == 'POST':
        nome = request.form['nome']
        contato = request.form['contato']
        preco = request.form['preco']
        data_horario = request.form['data_horario']
        local = request.form['local']
        
        conn.execute('UPDATE eventos SET nome = ?, contato = ?, preco = ?, data_horario = ?, local = ? WHERE id = ? AND id_usuario = ?',
                     (nome, contato, preco, data_horario, local, id_evento, current_user.id))
        conn.commit()
        conn.close()
        return redirect(url_for('eventos'))
    
    conn.close()
    return render_template('editar_evento.html', evento=evento)

@app.route('/eventos/<int:id_evento>/excluir', methods=['POST'])
@login_required
def excluir_evento(id_evento):
    conn = obter_conexao()
    conn.execute('DELETE FROM eventos WHERE id = ? AND id_usuario = ?', (id_evento, current_user.id))
    conn.commit()
    conn.close()
    return redirect(url_for('eventos'))


#################################################################################

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        # Verificar se o usuário já existe no banco de dados
        conn = obter_conexao()
        usuario_existente = conn.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()

        if usuario_existente:
            conn.close()
            return "Usuário já existe", 400

        # Inserir novo usuário no banco de dados
        senha_hash = generate_password_hash(senha)
        conn.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)',
                     (nome, email, senha_hash))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('cadastro.html')

#################################################################################

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = User.encontrar(email)
        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            return redirect(url_for('planilhas'))
        else:
            return "Credenciais inválidas", 401

    return render_template('login.html')

#################################################################################

@app.route('/simulacao', methods=['GET', 'POST'])
@login_required
def simulacao():
    tipo_simulacao = request.form.get('tipo_simulacao')
    aba_selecionada = request.form.get('aba_selecionada', 'juros')

    objetivo = request.form.get("objetivo", '')
    num_participantes = request.form.get("num_participantes", '')
    descricao = request.form.get("descricao", '')
    data_ini = request.form.get("data_ini", '')
    data_fim = request.form.get("data_fim", '')
    periodo_meses=0
    juros_compostos_taxa = request.form.get("juros_compostos_taxa", '')
    juros_taxa_exibir=0
    jc_mensalidade_por_participante=0
    jc_mensalidade_total=0
    jc_montante_acumulado=0
    sr_mensalidade_por_participante=0
    sr_mensalidade_total=0

    if request.method == 'POST':
        # Dados da planilha
        objetivo = float(request.form['objetivo'])
        num_participantes = int(num_participantes)
        
        planilha = Planilha(
            id_usuario=current_user.id,
            descricao=descricao,
            objetivo=objetivo,
            data_ini=data_ini,
            data_fim=data_fim
        )

        periodo_meses = planilha.periodo_meses()

        if tipo_simulacao == 'sem_rendimentos':
            aba_selecionada = 'sem_rendimento'
            modelo = SimulacaoSemRendimento(objetivo, planilha.periodo_meses(), num_participantes)
            sr_mensalidade_por_participante, sr_mensalidade_total, _ = modelo.simular()
            sr_mensalidade_por_participante = round(sr_mensalidade_por_participante, 2)
            sr_mensalidade_total = round(sr_mensalidade_total, 2)
        elif tipo_simulacao == 'juros_compostos':
            juros_compostos_taxa = float(juros_compostos_taxa) / 100 / 12
            # Simulação de juros
            modelo = SimulacaoJurosCompostos(objetivo, juros_compostos_taxa, periodo_meses, num_participantes)
            jc_mensalidade_por_participante, jc_mensalidade_total, jc_montante_acumulado = modelo.simular()
            jc_mensalidade_por_participante = round(jc_mensalidade_por_participante, 2)
            jc_mensalidade_total = round(jc_mensalidade_total, 2)
            jc_montante_acumulado = round(jc_montante_acumulado, 2)
            juros_taxa_exibir = (juros_compostos_taxa) * 100 * 12
        else:
            raise Exception('tipo_simulacao inválido.')

        # Criar a planilha se o botão for pressionado
        if 'criar_planilha' in request.form:
            planilha_id = planilha.salvar()  # Salva e obtém o id
            flash('Planilha criada com sucesso!', 'success')
            return redirect(url_for('planilha', id=planilha_id))  # Redireciona para a planilha criada

        # Arredondar valores para exibição
        objetivo = round(objetivo, 2)
    
    return render_template(
        'simulacao.html',
        aba_selecionada=aba_selecionada,
        objetivo=objetivo,
        num_participantes=num_participantes,
        descricao=descricao,
        juros_compostos_taxa=juros_compostos_taxa,
        juros_taxa_exibir=juros_taxa_exibir,
        data_ini=data_ini,
        data_fim=data_fim,
        jc_mensalidade_por_participante=jc_mensalidade_por_participante,
        jc_mensalidade_total=jc_mensalidade_total,
        jc_montante_acumulado=jc_montante_acumulado,
        sr_mensalidade_por_participante=sr_mensalidade_por_participante,
        sr_mensalidade_total=sr_mensalidade_total,
        num_parcelas=periodo_meses)
        


@app.route('/logout')
@login_required  # TODO: Não precisa estar logado para deslogar
def logout():
    logout_user()
    return redirect(url_for('index'))
