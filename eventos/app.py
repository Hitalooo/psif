from flask import Flask, render_template, request, make_response

app = Flask(__name__)

@app.route('/')
def index():
        return render_template('index.html')

@app.route('/submit', methods=['GET'])
def submit():
        opcao = request.args.get('opcao')
        return f'A opção escolhida foi : {opcao}'


#     if'color' in request.cookies:
#          return render_template('index.html', cor=request.cookies['color'])
#     return render_template('index.html', cor='white')

# @app.route('/evento')
# def evento():
#     evento = request.args.get('evento')
    

#             template = render_template('evento.html')
#             response = make_response(template)
#             response.delete_cookie('evento')
#             response.set_cookie('evento',value= string )
#             return response
        
#         else:
#              return render_template('evento.html', string=request.cookies['evento'])
        
#     else:
#             template = render_template('evento.html')
#             response = make_response(template)
#             response.delete_cookie('evento')
#             response.set_cookie('evento', string)
#             return response