from database.db import obter_conexao
from models.base import Base


class Lancamento(Base):
    def __init__(self, id_planilha, participante, descricao, data, valor):
        '''Um lançamento de uma planilha.

        Subclasse de models.base.Modelo.

        Parâmetros:
            - id_planilha: o ID da planilha correspondente. TODO: Receber objeto Planilha no lugar do id.
            - participante: o participante. TODO: Receber objeto Participante no lugar do id.
            - descricao: Uma descrição breve.
            - data: A data em que ocorreu o lançamento.
            - valor: O valor do lançamento. Pode assumir valores negativos para indicar saques, por exemplo.
        '''
        super().__init__(
            tabela='lancamentos',
            atributos=['id_planilha', 'participante', 'descricao', 'data',
                       'valor'])
        self.id_planilha = id_planilha
        self.participante = participante
        self.descricao = descricao
        self.data = data
        self.valor = valor

    def _valores_atributos(self):
        '''Retorna a tupla do valor dos atributos na mesma ordem da tabela `lancamentos`.
        É usado na classe models.base.Modelo para salvar as entidades no banco.
        '''
        return tuple(self.id_planilha, self.participante, self.descricao,
                     self.data, self.valor)

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
        l = Lancamento(id_planilha, participante, descricao, data, valor)
        l.id = id
        return l
