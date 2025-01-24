class Simulacao:
    '''Um modelo de simulação de rendimento.'''

    def simular() -> float:
        '''Simula o rendimento baseado em juros compostos.
        '''
        raise Exception('Método abstrato.')


class SimulacaoJurosSimples(Simulacao):
    '''Modelo de simulação de rendimento com juros simples.'''
    pass


class SimulacaoJurosCompostos(Simulacao):
    '''Modelo de simulação de rendimento com juros simples.

    Atributos
        - `objetivo`: O valor que se quer atingir ao final do investimento.
        - `taxa_juros`: Taxa mensal de juros.
        - `periodo_meses`: Período de rendimento em meses.
        - `num_participantes`: Quantidade de participantes do investimento.
    '''

    def __init__(self, objetivo: float, taxa_juros: float, periodo_meses: int, num_participantes: int):
        self.objetivo = objetivo
        self.taxa_juros = taxa_juros
        self.periodo_meses = periodo_meses
        self.num_participantes = num_participantes

    def simular(self) -> tuple[float, float, float]:
        '''Simula o rendimento baseado em juros compostos.

        TODO: Calcular a mensalidade para atingir o montante acumulado mais próximo possível do objetivo.
        Atualmente, estamos calculando o montante acumulado baseado na divisão simples do objetivo por participantes e meses.

        Parâmetros:
            - `objetivo`: O valor que se quer atingir ao final do investimento.
            - `taxa_juros`: Taxa mensal de juros.
            - `periodo_meses`: Período de rendimento em meses.
            - `num_participantes`: Quantidade de participantes do investimento.

        Retorna:
            - `mensalidade_por_participante`: a mensalidade paga por cada participante.
            - `mensalidade_total`: a mensalidade paga por todos os participantes somadas em um mês apenas.
            - `montante_acumulado`: montante acumulado das mensalidades + rendimento. 
        '''
        # Cálculo da mensalidade total
        mensalidade_total = self.objetivo / self.periodo_meses
        
        # Cálculo da mensalidade por participante
        mensalidade_por_participante = mensalidade_total / self.num_participantes
        
        # Cálculo do montante acumulado usando a fórmula M = C x (1 + i)^t
        if self.taxa_juros > 0:
            montante_acumulado = mensalidade_total * (((1 + self.taxa_juros) ** self.periodo_meses - 1) / self.taxa_juros)
        else:
            montante_acumulado = mensalidade_total * self.periodo_meses  # Sem juros, apenas somando

        return mensalidade_por_participante, mensalidade_total, montante_acumulado