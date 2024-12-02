from models.base import Base

from models.lancamentos import Lancamento

class Planilha(Base):
    def __init__(self, descricao, objetivo, data_ini, data_fim, lancamentos=[]):
        super().__init__(tabela='planilhas')
        self.descricao = descricao
        self.objetivo = objetivo
        self.data_ini = data_ini
        self.data_fim = data_fim
        self.lancamentos = lancamentos

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

    def _atributos(self) -> dict:
        '''Retorna o dicionário dos atributos na mesma ordem da tabela `planilha`.
        É usado na classe models.base.Modelo para salvar as entidades no banco.
        '''
        p = {
            'descricao': self.descricao,
            'objetivo': self.objetivo,
            'data_ini': self.data_ini,
            'data_fim': self.data_fim,
        }
        return p

    @classmethod
    def _carregar_registro(cls, registro: list) -> 'Planilha':
        '''Carrega um objeto a partir do `registro` que veio de uma consulta no banco.
        É usado na classe models.base.Modelo para carregar as entidades nas consultas.
        '''
        id = registro[0]
        descricao = registro[1]
        objetivo = registro[2]
        data_ini = registro[3]
        data_fim = registro[4]
        p = cls(descricao, objetivo, data_ini, data_fim)
        p.id = id
        return p

    @staticmethod
    def excluir(id_planilha: int):
        '''Exclui uma planilha do banco com base no ID.'''
        conn = Base._obter_conexao()
        conn.execute('DELETE FROM planilhas WHERE id = ?', (id_planilha,))
        conn.commit()
        conn.close()