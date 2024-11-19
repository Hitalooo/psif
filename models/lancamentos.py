from database.db import obter_conexao

class Lancamento:
    def __init__(self, participante, descricao, data, valor):
        self.participante = participante
        self.descricao = descricao
        self.data = data
        self.valor = valor
    
    def salvar(self):
        conn = obter_conexao()
        conn.execute('INSERT INTO lancamentos (id_participante, descricao, data, valor) VALUES (?, ?, ?, ?)',
                     (self.participante, self.descricao, self.data, self.valor))
        conn.commit()
        conn.close()

    @staticmethod
    def todos():
        conn = obter_conexao()
        dados = conn.execute('SELECT * FROM lancamentos').fetchall()
        lancamentos = []
        for linha in dados:
            participante = linha[1]
            descricao = linha[2]
            data = linha[3]
            valor = linha[4]
            l = Lancamento(participante, descricao, data, valor)
            lancamentos += [l]
        return lancamentos