from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            valor_principal = float(request.form['valor'])
            taxa_juros = float(request.form['taxa'])
            periodo_anos = float(request.form['periodo'])
            num_pessoas = request.form.get('pessoas', 1)
            valor_mensal = float(request.form.get('valor_mensal', 0))
            
            # Verifique se o campo 'pessoas' não está vazio e é um número inteiro válido
            num_pessoas = int(num_pessoas) if num_pessoas else 1  # Definindo um valor padrão para evitar divisão por zero
            
            # Cálculo de juros simples
            juros_simples = valor_principal * taxa_juros * periodo_anos / 100
            valor_total_simples = valor_principal + juros_simples
            
            # Cálculo da mensalidade para juros simples
            periodo_meses = periodo_anos * 12
            mensalidade_simples = valor_principal / periodo_meses
            
            # Dividindo a mensalidade pelo número de pessoas
            mensalidade_por_pessoa_simples = mensalidade_simples / num_pessoas if num_pessoas > 0 else None

            # Cálculo de juros compostos
            taxa_juros_decimal = taxa_juros / 100
            numero_compostos = 12  # Supondo que os juros são compostos mensalmente
            montante_composto = valor_principal * (1 + taxa_juros_decimal / numero_compostos) ** (numero_compostos * periodo_anos)
            juros_compostos = montante_composto - valor_principal
            
            # Cálculo da mensalidade para juros compostos
            mensalidade_composta = montante_composto / periodo_meses
            
            # Dividindo a mensalidade pelo número de pessoas
            mensalidade_por_pessoa_composta = mensalidade_composta / num_pessoas if num_pessoas > 0 else None

            # Cálculo do montante total baseado no valor mensal para juros compostos
            if valor_mensal > 0:
                montante_total_mensal = valor_mensal * periodo_meses
                valor_total_composto_mensal = montante_total_mensal * (1 + taxa_juros_decimal / numero_compostos) ** (numero_compostos * periodo_anos)
                juros_compostos_mensal = valor_total_composto_mensal - montante_total_mensal
            else:
                valor_total_composto_mensal = None
                juros_compostos_mensal = None

# Arredondando os valores para duas casas decimais
            valor_principal = round(valor_principal, 2)
            taxa_juros = round(taxa_juros, 2)
            periodo_anos = round(periodo_anos, 2)
            valor_total_simples = round(valor_total_simples, 2)
            mensalidade_simples = round(mensalidade_simples, 2)
            mensalidade_por_pessoa_simples = round(mensalidade_por_pessoa_simples, 2) if mensalidade_por_pessoa_simples is not None else None
            
            montante_composto = round(montante_composto, 2)
            juros_compostos = round(juros_compostos, 2)
            mensalidade_composta = round(mensalidade_composta, 2)
            mensalidade_por_pessoa_composta = round(mensalidade_por_pessoa_composta, 2) if mensalidade_por_pessoa_composta is not None else None
            
            if valor_total_composto_mensal is not None:
                valor_total_composto_mensal = round(valor_total_composto_mensal, 2)
                juros_compostos_mensal = round(juros_compostos_mensal, 2)

            return render_template('index.html', 
                                   valor_principal=valor_principal, 
                                   taxa_juros=taxa_juros, 
                                   periodo_anos=periodo_anos,
                                   valor_total_simples=valor_total_simples,
                                   montante_composto=montante_composto,
                                   periodo_meses=periodo_meses,
                                   mensalidade_simples=mensalidade_simples,
                                   mensalidade_composta=mensalidade_composta,
                                   num_pessoas=num_pessoas,
                                   mensalidade_por_pessoa_simples=mensalidade_por_pessoa_simples,
                                   mensalidade_por_pessoa_composta=mensalidade_por_pessoa_composta,
                                   juros_compostos=juros_compostos,
                                   valor_mensal=valor_mensal,
                                   valor_total_composto_mensal=valor_total_composto_mensal,
                                   juros_compostos_mensal=juros_compostos_mensal)
        except ValueError:
            return render_template('index.html', error="Por favor, insira valores numéricos válidos.")
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
