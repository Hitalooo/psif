from database.db import obter_conexao

class Lancamento:
    def __init__(self, id_planilha, participante, descricao, data, valor):
        self.id_planilha = id_planilha
        self.participante = participante
        self.descricao = descricao
        self.data = data
        self.valor = valor
        # self.planilha = planilha  # TODO: Deixar a opção de carregar a planilha junto
    
    def salvar(self):
        '''Salva no banco.'''
        conn = obter_conexao()
        conn.execute('INSERT INTO lancamentos (id_planilha, id_participante, descricao, data, valor) VALUES (?, ?, ?, ?, ?)',
                     (self.id_planilha, self.participante, self.descricao, self.data, self.valor))
        conn.commit()
        conn.close()

    @staticmethod
    def consultar(sqlquery: str, parametros: tuple) -> list['Lancamento']:
        '''Executa uma consulta SQL e retorna os lancamentos.
        
        Parâmetros:
            - sqlquery: A consulta SQL a executar.
            - parametros: Os parâmetros para o método execute da conexão com o banco de dados.
        
        Retorna:
            A lista de Lancamentos encontrados.'''
        conn = obter_conexao()
        dados = conn.execute(sqlquery, parametros).fetchall()
        lancamentos = []
        for linha in dados:
            id = linha[0]
            id_planilha = linha[1]
            participante = linha[2]
            descricao = linha[3]
            data = linha[4]
            valor = linha[5]
            l = Lancamento(id_planilha, participante, descricao, data, valor)
            l.id = id
            lancamentos += [l]
        return lancamentos