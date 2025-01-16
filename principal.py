

# ############################################################################

# from flask import Flask, request, jsonify
# from datetime import datetime
# import json
# import os

# app = Flask(__name__)

# # Nome do arquivo JSON
# ARQUIVO_ESTACIONAMENTO = "estacionamento.json"
# TARIFA_POR_HORA = 15  # Valor da tarifa por hora

# # Inicializa o arquivo JSON
# def inicializar_json():
#     if not os.path.exists(ARQUIVO_ESTACIONAMENTO):
#         with open(ARQUIVO_ESTACIONAMENTO, 'w', encoding='utf-8') as arquivo:
#             json.dump({"contador": 0, "veiculos": []}, arquivo, indent=4)

# inicializar_json()

# @app.route('/estacionamento', methods=['POST'])
# def registrar_entrada():
#     """Registra a entrada de um veículo."""
#     dados = request.get_json()
#     placa = dados.get("plate")

#     if not placa or not validar_placa(placa):
#         return jsonify({"error": "Placa inválida"}), 400

#     with open(ARQUIVO_ESTACIONAMENTO, 'r+', encoding='utf-8') as arquivo:
#         dados = json.load(arquivo)

#         registros_veiculo = [veiculo for veiculo in dados["veiculos"] if veiculo["Placa"] == placa]
#         veiculo_existente = (
#             max(registros_veiculo, key=lambda x: datetime.strptime(x["Horario_de_Entrada"], '%Y-%m-%d %H:%M:%S'))
#             if registros_veiculo
#             else None
#         )

#         if veiculo_existente and not veiculo_existente["Pago"]:
#             return jsonify({"error": "Veículo ainda no estacionamento"}), 400

#         dados["contador"] += 1
#         novo_carro = {
#             "id": dados["contador"],
#             "Horario_de_Entrada": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#             "Placa": placa,
#             "Pago": False,
#             "Saiu": False
#         }
#         dados["veiculos"].append(novo_carro)

#         arquivo.seek(0)
#         json.dump(dados, arquivo, indent=4, ensure_ascii=False)
#         arquivo.truncate()

#     return jsonify({"message": "Veículo registrado", "id": novo_carro["id"]}), 201

# @app.route('/estacionamento/<int:id>/pay', methods=['PUT'])
# def pagar_estacionamento(id):
#     """Registra o pagamento de um veículo."""
#     try:
#         with open(ARQUIVO_ESTACIONAMENTO, 'r+', encoding='utf-8') as arquivo:
#             dados = json.load(arquivo)

#             # Procura o veículo pelo ID
#             veiculo = next((v for v in dados["veiculos"] if v["id"] == id), None)

#             if not veiculo:
#                 return jsonify({"error": "Veículo não encontrado"}), 404

#             if veiculo["Pago"]:
#                 return jsonify({"error": "Pagamento já realizado"}), 400

#             # Calcula o valor devido
#             horario_entrada = datetime.strptime(veiculo["Horario_de_Entrada"], '%Y-%m-%d %H:%M:%S')
#             horario_atual = datetime.now()
#             tempo_permanencia = (horario_atual - horario_entrada).total_seconds() / 3600
#             valor_a_pagar = round(tempo_permanencia * TARIFA_POR_HORA, 2)

#             # Atualiza os campos do veículo
#             veiculo["Pago"] = True
#             veiculo["Saiu"] = True
#             veiculo["Horario_de_Saida"] = horario_atual.strftime('%Y-%m-%d %H:%M:%S')
#             veiculo["Valor_Pago"] = valor_a_pagar

#             # Salva as mudanças no JSON
#             arquivo.seek(0)
#             json.dump(dados, arquivo, indent=4, ensure_ascii=False)
#             arquivo.truncate()

#         return jsonify({
#             "message": "Pagamento realizado com sucesso",
#             "id": id,
#             "valor_pago": valor_a_pagar
#         }), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route('/estacionamento/<string:placa>', methods=['GET'])
# def historico_veiculo(placa):
#     """Obtém o histórico de um veículo por placa."""
#     with open(ARQUIVO_ESTACIONAMENTO, 'r', encoding='utf-8') as arquivo:
#         dados = json.load(arquivo)
#         historico = [v for v in dados["veiculos"] if v["Placa"] == placa]

#     if not historico:
#         return jsonify({"error": "Placa não encontrada"}), 404

#     return jsonify(historico), 200

# # Função auxiliar para validar placas
# def validar_placa(placa):
#     import re
#     return bool(re.match(r'^[A-Z]{3}-\d{4}$', placa))

# if __name__ == '__main__':
#     app.run(debug=True)

############################################################################################

from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# Nome do arquivo JSON
ARQUIVO_ESTACIONAMENTO = "estacionamento.json"
TARIFA_POR_HORA = 15  # Valor da tarifa por hora

# Inicializa o arquivo JSON
def inicializar_json():
    if not os.path.exists(ARQUIVO_ESTACIONAMENTO):
        with open(ARQUIVO_ESTACIONAMENTO, 'w', encoding='utf-8') as arquivo:
            json.dump({"contador": 0, "veiculos": []}, arquivo, indent=4)

inicializar_json()

@app.route('/parking', methods=['POST'])
def registrar_entrada():
    """Registra a entrada de um veículo."""
    dados = request.get_json()
    placa = dados.get("plate")

    if not placa or not validar_placa(placa):
        return jsonify({"error": "Placa invalida"}), 400

    with open(ARQUIVO_ESTACIONAMENTO, 'r+', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)

        registros_veiculo = [veiculo for veiculo in dados["veiculos"] if veiculo["Placa"] == placa]
        veiculo_existente = (
            max(registros_veiculo, key=lambda x: datetime.strptime(x["Horario_de_Entrada"], '%Y-%m-%d %H:%M:%S'))
            if registros_veiculo
            else None
        )

        if veiculo_existente and not veiculo_existente["Saiu"]:
            return jsonify({"error": "Veiculo ainda no estacionamento"}), 400

        dados["contador"] += 1
        novo_carro = {
            "id": dados["contador"],
            "Horario_de_Entrada": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "Placa": placa,
            "Pago": False,
            "Saiu": False
        }
        dados["veiculos"].append(novo_carro)

        arquivo.seek(0)
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)
        arquivo.truncate()

    return jsonify({"message": "Veiculo registrado", "id": novo_carro["id"]}), 201

@app.route('/parking/<int:id>/pay', methods=['PUT'])
def pagar_estacionamento(id):
    """Registra o pagamento de um veículo."""
    try:
        with open(ARQUIVO_ESTACIONAMENTO, 'r+', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)

            # Procura o veículo pelo ID
            veiculo = next((v for v in dados["veiculos"] if v["id"] == id), None)

            if not veiculo:
                return jsonify({"error": "Veiculo não encontrado"}), 404

            if veiculo["Pago"]:
                return jsonify({"error": "Pagamento ja realizado"}), 400

            # Verifica o horário de entrada e calcula o valor devido
            horario_entrada = datetime.strptime(veiculo["Horario_de_Entrada"], '%Y-%m-%d %H:%M:%S')
            horario_atual = datetime.now()
            tempo_permanencia = (horario_atual - horario_entrada).total_seconds() / 3600
            valor_a_pagar = round(tempo_permanencia * TARIFA_POR_HORA, 2)

            # Atualiza o status do veículo
            veiculo["Pago"] = True
            veiculo["Valor_Pago"] = valor_a_pagar

            # Salva as alterações no JSON
            arquivo.seek(0)
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)
            arquivo.truncate()

        return jsonify({
            "message": "Pagamento realizado com sucesso",
            "id": id,
            "valor_pago": valor_a_pagar
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/parking/<int:id>/out', methods=['PUT'])
def registrar_saida(id):
    """Registra a saída de um veículo."""
    try:
        with open(ARQUIVO_ESTACIONAMENTO, 'r+', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)

            veiculo = next((v for v in dados["veiculos"] if v["id"] == id), None)

            if not veiculo:
                return jsonify({"error": "Veiculo não encontrado"}), 404

            if not veiculo["Pago"]:
                return jsonify({"error": "Pagamento não realizado"}), 400

            if veiculo["Saiu"]:
                return jsonify({"error": "Veiculo ja saiu do estacionamento"}), 400

            veiculo["Saiu"] = True
            veiculo["Horario_de_Saida"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            arquivo.seek(0)
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)
            arquivo.truncate()

        return jsonify({"message": "Saida registrada com sucesso", "id": id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/parking/<string:placa>', methods=['GET'])
def historico_veiculo(placa):
    """Obtém o histórico de um veículo por placa."""
    with open(ARQUIVO_ESTACIONAMENTO, 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)
        historico = [
            {
                "id": v["id"],
                "Horario_de_Entrada": v["Horario_de_Entrada"],
                "Placa": v["Placa"],
                "Pago": v["Pago"],
                "Saiu": v["Saiu"],
            }
            for v in dados["veiculos"] if v["Placa"] == placa
        ]

    if not historico:
        return jsonify({"error": "Placa não encontrada"}), 404

    return jsonify(historico), 200

# Funções auxiliares
def validar_placa(placa):
    import re
    return bool(re.match(r'^[A-Z]{3}-\d{4}$', placa))

def calcular_tempo(horario_entrada, horario_saida):
    if not horario_saida:
        return "Ainda no estacionamento"
    entrada = datetime.strptime(horario_entrada, '%Y-%m-%d %H:%M:%S')
    saida = datetime.strptime(horario_saida, '%Y-%m-%d %H:%M:%S')
    diferenca = saida - entrada
    minutos = int(diferenca.total_seconds() // 60)
    return f"{minutos} minutes"

if __name__ == '__main__':
    app.run(debug=True)
    
    