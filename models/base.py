import sqlite3

class Base:
    def __init__(self, tabela: str):
        '''Classe base para qualquer modelo.

        Parâmetros:
          - tabela: nome da tabela no banco de dados.
          - atributos: list de atributos na ordem em que aparecem na tabela.

        Todo modelo deve ser uma subclasse desta e sobrescrever os métodos abstratos.
        '''
        self._tabela = tabela

    @staticmethod
    def _obter_conexao():
        '''Obtém uma conexão com o banco de dados.'''
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        return conn

    def salvar(self):
        '''Salva no banco.'''
        conn = self._obter_conexao()
        atributos = self._atributos()
        interrogacoes = ('?, ' * len(atributos))[:-2]
        colunas = (', '.join(list(atributos.keys())))
        valores = list(atributos.values())
        conn.execute(f'INSERT INTO {self._tabela} ({colunas}) VALUES ({interrogacoes})',
                     valores)
        conn.commit()
        conn.close()
    
    def _atributos(self) -> dict:
        '''Retorna um dicionário contendo o nome e o valor das colunas na mesma ordem da tabela.
        Método abstrato. Deve ser sobrescrito nas subclasses.
        '''
        raise MetodoAbstrato(self._atributos.__name__)

    @classmethod
    def _carregar_registro(cls, registro: list):
        '''Carrega o objeto a partir do registro que vem de uma consulta.
        Método abstrato. Deve ser sobrescrito nas subclasses.'''
        raise MetodoAbstrato(cls._carregar_registro.__name__)

    @classmethod
    def consultar(cls, sqlquery: str, parametros: tuple = tuple()) -> list['Base']:
        '''Executa uma consulta SQL e retorna os objetos.
        
        Parâmetros:
            - sqlquery: A consulta SQL a executar.
            - parametros: Os parâmetros para o método execute da conexão com o banco de dados.
        
        Retorna:
            A lista de objetos encontrados no banco.'''
        conn = cls._obter_conexao()
        dados = conn.execute(sqlquery, parametros).fetchall()
        objetos = []
        for registro in dados:
            objeto = cls._carregar_registro(registro)
            objetos += [objeto]
        return objetos

    def encontrar(cls, id: int) -> 'Base | None':
        '''Encontra um registro baseado no `id`.
        Método abstrato. Deve ser sobrescrito nas subclasses.'''
        raise MetodoAbstrato('encontrar')


class MetodoAbstrato(Exception):
    def __init__(self, nome_do_metodo: str):
        '''Exceção lançada dentro de métodos abstratos.
        
        Serve para evitar que subclasses chamem métodos abstratos sem sobrescrevê-los.
        
        Parâmetros:
          - nome_do_metodo: o nome do método abstrato para exibir em caso de erro.
        '''
        nota = f'O método abstrato {nome_do_metodo} precisa ser sobrescrito nas subclasses.'
        super().__init__(nota)
    