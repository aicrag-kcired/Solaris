# backend/app.py
from flask import Flask, jsonify

app = Flask(__name__)

# Primeira rota (GET) que aponta para a página inicial do projeto Solaris
@app.route('/', methods=['GET'])
def pagina_inicial():
    return jsonify({
        "status": "sucesso",
        "projeto": "Solaris",
        "descricao": "Energia solar mais barata e acessível",
        "versao": "1.0.0",
        "mensagem": "Backend Solaris inicializado com sucesso. Pronto para integrar o chatbot e o dashboard!"
    }), 200

if __name__ == '__main__':
    # Roda o servidor local na porta 5000
    app.run(debug=True, port=5000)
