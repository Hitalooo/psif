from flask import Flask, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def conectar_mysql():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='usbw',
            database='db_atividade6'
        )
        if conexao.is_connected():
            return conexao
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

@app.route('/')
def index():
    conexao = conectar_mysql()
    dados = []
    if conexao:
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT * FROM tb_alunos")  # Substitua 'sua_tabela' pelo nome da tabela
            dados = cursor.fetchall()
        finally:
            conexao.close()
    return render_template('index.html', dados=dados)

if __name__ == '__main__':
    app.run(debug=True)
