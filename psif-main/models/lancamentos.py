from models.base import Base


class Lancamento(Base):
    '''Um lançamento de uma planilha.

    Subclasse de models.base.Base.

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
        data = registro[3]
        descricao = registro[4]
        valor = registro[5]
        l = cls(id_planilha, participante, descricao, data, valor)
        l.id = id
        return l

    @classmethod
    def encontrar(cls, id: int) -> 'Lancamento | None':
        '''Encontra um lançamento no banco.
        
        Lança Exception caso haja mais de um Lancamento com o mesmo `id`.

        Parâmetros:
            - id: O id do lançamento.

        Retorna:
            O objeto Lancamento ou None, caso não encontre.
        
        TODO: Ver uma forma de não repetir esse código em todos os modelos.
        '''
        lancamentos = cls.consultar(f'SELECT * FROM lancamentos WHERE id = ?', (id,))
        if len(lancamentos) == 1:
            return lancamentos[0]
        if len(lancamentos) == 0:
            return None
        # Erro
        raise Exception(f'Há mais de um lançamento com id={id}.')
