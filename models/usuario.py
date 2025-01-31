from models.base import Base
from flask_login import UserMixin   
import sqlite3


class User(UserMixin, Base):
    '''Um usuario de uma planilha.

    Subclasse de models.base.Base.

    Atributos:
        - id: o ID do usuario correspondente. TODO: Receber objeto Usuario no lugar do id.
        - nome: O nome do participante.
        - email: e-mail.
        - senha: senha.
    '''

    @staticmethod
    def _obter_conexao():
        '''Obtém uma conexão com o banco de dados.'''
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        return conn

    def __init__(self, id: int, nome: str, email: str, senha:str):
        super().__init__(tabela='usuarios')
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha

    def _atributos(self) -> dict:
        '''Retorna o dicionário de atributos na mesma ordem da tabela `usuarios`.'''
        d = {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'senha': self.senha,
        }
        return d

    @classmethod
    def _carregar_registro(cls, registro: list) -> 'User':
        '''Carrega um objeto a partir do `registro` que veio de uma consulta no banco.'''
        id = registro[0]
        nome = registro[1]
        email = registro[2]
        senha = registro[3]
        u = cls(id, nome, email, senha)
        u.id = id
        return u
    
    
    @classmethod
    def encontrar(cls, email: str) -> 'User | None':
        '''Encontra um usuario no banco.
        
        Lança Exception caso haja mais de um User com o mesmo `id`.

        Parâmetros:
            - id: O id do usuario.

        Retorna:
            O objeto User ou None, caso não encontre.
        
        TODO: Ver uma forma de não repetir esse código em todos os modelos.
        '''
        usuarios = cls.consultar(f'SELECT * FROM usuarios WHERE email = ?', (email,))
        if len(usuarios) == 1:
            return usuarios[0]
        if len(usuarios) == 0:
            return None

    @classmethod
    def get(cls, id: int) -> 'User | None':
        '''Encontra um usuario no banco.
        
        Lança Exception caso haja mais de um User com o mesmo `id`.

        Parâmetros:
            - id: O id do usuario.

        Retorna:
            O objeto User ou None, caso não encontre.
        
        TODO: Ver uma forma de não repetir esse código em todos os modelos.
        '''
        usuarios = cls.consultar(f'SELECT * FROM usuarios WHERE id = ?', (id,))
        if len(usuarios) == 1:
            return usuarios[0]
        if len(usuarios) == 0:
            return None
