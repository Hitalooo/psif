from datetime import datetime

from models.base import Base

from models.lancamentos import Lancamento
from models.participantes import Participante
from util.datas import diferenca_meses

class Planilha(Base):
    '''Uma planilha.

    Subclasse de models.base.Base.

    Atributos:
        - descricao: Uma descrição breve.
        - objetivo: Valor em reais a ser atingido no final do investimento.
        - data_ini: Data de início do investimento.
        - data_fim: Data de fim do investimento.
        - lancamentos: A lista de lançamentos ocorridos até o momento.
        - participantes: A lista de participantes.
    '''
    def __init__(self, descricao, objetivo, data_ini, data_fim, lancamentos=[], participantes=[]):
        super().__init__(tabela='planilhas')
        self.descricao = descricao
        self.objetivo = objetivo
        self.data_ini = data_ini
        self.data_fim = data_fim
        self.lancamentos = lancamentos
        self.participantes = participantes

    @classmethod
    def find(cls, id: int, carregar_lancamentos: bool = True,
                carregar_participantes: bool = True) -> 'Planilha | None':
        '''Retorna a Planilha com o `id` informado ou None, caso não encontre.'''
        res = cls.consultar('SELECT * FROM planilhas WHERE id = ?', (id))
        if len(res) == 0:
            return None
        if len(res) > 1:
            raise Exception(f'find({id}) retornou {len(res)} resultados.')
        p = res[0]
        if carregar_lancamentos:
            p.lancamentos = Lancamento.consultar('SELECT * FROM lancamentos WHERE id_planilha = ?', (p.id,))
        if carregar_participantes:
            p.participantes = Participante.consultar('SELECT * FROM participantes WHERE id_planilha = ?', (p.id,))
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

    @classmethod
    def encontrar(cls, id: int) -> 'Planilha | None':
        '''Encontra uma planilha no banco.
        
        Lança Exception caso haja mais de uma Planilha com o mesmo `id`.

        Parâmetros:
            - id: O id da planilha.

        Retorna:
            O objeto Planilha ou None, caso não encontre.
        
        TODO: Ver uma forma de não repetir esse código em todos os modelos.
        '''
        planilhas = cls.consultar(f'SELECT * FROM planilhas WHERE id = ?', (id,))
        if len(planilhas) == 1:
            return planilhas[0]
        if len(planilhas) == 0:
            return None
        # Erro
        raise Exception(f'Há mais de uma planilha com id={id}.')

    def dados_grafico(self) -> list[list]:
        '''Retorna os dados necessários para desenhar o gráfico da planilha.'''
        datetime_ini = datetime.strptime(self.data_ini, '%Y-%m-%d')
        datetime_fim = datetime.strptime(self.data_fim, '%Y-%m-%d')
        # O +1 é pra contar pelo menos 1 mês
        diferenca = diferenca_meses(datetime_ini, datetime_fim) + 1

        # Associa cada participante a uma linha na matriz
        id_indice = {}
        indice = 0
        for p in self.participantes:
            id_indice[p.id] = indice
            indice += 1
        
        # Cria colunas zeradas para cada mês e cada participante
        dados = []
        for p in self.participantes:
            colunas = [p]
            for _ in range(diferenca):
                colunas += [0]
            dados += [colunas]
        
        # Soma os lançamentos ao mês correspondente
        for l in self.lancamentos:
            data_lancamento = datetime.strptime(l.data, "%Y-%m-%d")
            # Esse +1 compensa o participante
            mes = diferenca_meses(datetime_ini, data_lancamento) + 1
            linha = id_indice[l.participante]
            dados[linha][mes] += l.valor

        return dados
