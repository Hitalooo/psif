from flask import Flask, request, render_template

app = Flask(__name__)
app.secret_key = 'supersecretkey'  

@app.route('/', methods=['GET', 'POST'])
def index():
    total = 0
    checked_items = {}
    total_por_pessoa = {}
    if request.method == 'POST':
        for key, value in request.form.items():
            try:
                # O id tem o formato mes_nome. O mês tem sempre 3 letras, então
                # o nome vem sempre do caractere 4 pra frente.
                nome = key[4:]
                # Cria o total da pessoa zerado se ainda não existir
                if nome not in total_por_pessoa:
                    total_por_pessoa[nome] = 0
                # valor é a parcela
                valor = float(value)
                # Soma a parcela ao total por pessoa e ao total geral
                total_por_pessoa[nome] += valor
                total += valor
                checked_items[key] = True
            except ValueError:
                continue
    return render_template('index.html', total=total, checked_items=checked_items, total_por_pessoa=total_por_pessoa)

if __name__ == '__main__':
    app.run(debug=True)
