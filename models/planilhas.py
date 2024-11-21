from database.db import obter_conexao

from models.lancamentos import Lancamento

class Planilha:
    def __init__(self, descricao, objetivo, data_ini, data_fim, lancamentos=[]):
        self.descricao = descricao
        self.objetivo = objetivo
        self.data_ini = data_ini
        self.data_fim = data_fim
        self.lancamentos = lancamentos

    def salvar(self):
        '''Salva no banco.'''
        conn = obter_conexao()
        conn.execute('INSERT INTO planilhas (descricao, objetivo, data_ini, data_fim) VALUES (?, ?, ?, ?)',
                     (self.descricao, self.objetivo, self.data_ini, self.data_fim))
        conn.commit()
        # TODO: Se o id acabou de ser criado, atribuir a self
        conn.close()
    
    @classmethod
    def consultar(cls, sqlquery: str, parametros: tuple = tuple()) -> list['Planilha']:
        '''Executa uma consulta SQL e retorna as planilhas.
        
        Parâmetros:
            - sqlquery: A consulta SQL a executar.
            - parametros: Os parâmetros para o método execute da conexão com o banco de dados.
        
        Retorna:
            A lista de Planilhas encontradas.'''
        conn = obter_conexao()
        dados = conn.execute(sqlquery, parametros).fetchall()
        planilhas = []
        for linha in dados:
            id = linha[0]
            descricao = linha[1]
            objetivo = linha[2]
            data_ini = linha[3]
            data_fim = linha[4]
            p = cls(descricao, objetivo, data_ini, data_fim)
            p.id = id
            planilhas += [p]
        return planilhas

    @classmethod
    def find(cls, id: int, carregar_lancamentos: bool = True) -> 'Planilha | None':
        '''Retorna a Planilha com o `id` informado ou None, caso não encontre.'''
        res = cls.consultar('SELECT * FROM planilhas WHERE id = ?', (id))
        if len(res) == 0:
            return None
        if len(res) > 1:
            raise Exception(f'find({id}) retornou {len(res)} resultados.')
        p = res[0]
        if carregar_lancamentos:
            p.lancamentos = Lancamento.consultar('SELECT * FROM lancamentos WHERE id_planilha = ?', (p.id,))
        return p