from models.base import Base


class Lancamento(Base):
    '''Um lançamento de uma planilha.

    Subclasse de models.base.Modelo.

    Atributos:
            - id_planilha: o ID da planilha correspondente. TODO: Receber objeto Planilha no lugar do id.
            - participante: o participante. TODO: Receber objeto Participante no lugar do id.
            - descricao: Uma descrição breve.
            - data: A data em que ocorreu o lançamento.
            - valor: O valor do lançamento. Pode assumir valores negativos para indicar saques, por exemplo.
    '''
    def __init__(self, id_planilha, participante, descricao, data, valor):
        super().__init__(tabela='lancamentos')
        self.id_planilha = id_planilha
        self.participante = participante
        self.descricao = descricao
        self.data = data
        self.valor = valor

    def _atributos(self) -> dict:
        '''Retorna o dicionário de atributos na mesma ordem da tabela `lancamentos`.
        É usado na classe models.base.Modelo para salvar as entidades no banco.
        '''
        d = {
            'id_planilha': self.id_planilha,
            'id_participante': self.participante,
            'descricao': self.descricao,
            'data': self.data,
            'valor': self.valor,
        }
        return d

    @classmethod
    def _carregar_registro(cls, registro: list) -> 'Lancamento':
        '''Carrega um objeto a partir do `registro` que veio de uma consulta no banco.
        É usado na classe models.base.Modelo para carregar as entidades nas consultas.
        '''
        id = registro[0]
        id_planilha = registro[1]
        participante = registro[2]
        descricao = registro[3]
        data = registro[4]
        valor = registro[5]
        l = cls(id_planilha, participante, descricao, data, valor)
        l.id = id
        return l

    @staticmethod
    def excluir(id_lancamento: int):
        '''Exclui um lançamento do banco com base no ID.'''
        conn = Base._obter_conexao()
        conn.execute('DELETE FROM lancamentos WHERE id = ?', (id_lancamento,))
        conn.commit()
        conn.close()