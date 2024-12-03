from models.base import Base


class Participante(Base):
    '''Um participante de uma planilha.

    Subclasse de models.base.Base.

    Atributos:
        - id_planilha: o ID da planilha correspondente. TODO: Receber objeto Planilha no lugar do id.
        - nome: O nome do participante.
        - contato: Um telefone, e-mail, etc.
    '''
    def __init__(self, id_planilha: int, nome: str, contato: str):
        super().__init__(tabela='participantes')
        self.id_planilha = id_planilha
        self.nome = nome
        self.contato = contato

    def _atributos(self) -> dict:
        '''Retorna o dicionário de atributos na mesma ordem da tabela `participantes`.'''
        d = {
            'id_planilha': self.id_planilha,
            'nome': self.nome,
            'contato': self.contato,
        }
        return d

    @classmethod
    def _carregar_registro(cls, registro: list) -> 'Participante':
        '''Carrega um objeto a partir do `registro` que veio de uma consulta no banco.'''
        id = registro[0]
        id_planilha = registro[1]
        nome = registro[2]
        contato = registro[3]
        p = cls(id_planilha, nome, contato)
        p.id = id
        return p

    @classmethod
    def encontrar(cls, id: int) -> 'Participante | None':
        '''Encontra um participante no banco.
        
        Lança Exception caso haja mais de um Participante com o mesmo `id`.

        Parâmetros:
            - id: O id do participante.

        Retorna:
            O objeto Participante ou None, caso não encontre.
        
        TODO: Ver uma forma de não repetir esse código em todos os modelos.
        '''
        participantes = cls.consultar(f'SELECT * FROM participantes WHERE id = ?', (id,))
        if len(participantes) == 1:
            return participantes[0]
        if len(participantes) == 0:
            return None
        # Erro
        raise Exception(f'Há mais de um participante com id={id}.')
