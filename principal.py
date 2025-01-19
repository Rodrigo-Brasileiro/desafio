
# Comando para utilizar:

# Registrar entrada
# curl -X POST -H "Content-Type: application/json" -d '{"plate": "FAA-1234"}' http://127.0.0.1:5000/parking

# Pagar estacionamento
# curl -X PUT http://127.0.0.1:5000/parking/1/pay

# Registrar saída
# curl -X PUT http://127.0.0.1:5000/parking/1/out

# Consultar histórico
# curl -X GET http://127.0.0.1:5000/parking/FAA-1234

from flask import Flask, request, jsonify   # a biblioteca flask é utilizada para criação de API, a biblioteca request serve para trefegar as requisições  
                                            # ao utilizar a api, já a jsonify é utilizada para entregar a mensagem em formato JSON
from datetime import datetime # Biblioteca para pega a hora atual do computador
import json # Biblioteca responsável pela comunicação com arquivos JSON
import os # Biblioteca responsável pela verificação da existência de um arquivo JSON, caso não exista, será criado um arquivo JSON

app = Flask(__name__) # Aqui está sendo criado uma aplicação flask 

# Nome do arquivo JSON
ARQUIVO_ESTACIONAMENTO = "estacionamento.json"
TARIFA_POR_HORA = 15  # Valor do estacionamento por hora (fictício)

# Inicializa o arquivo JSON
def inicializar_json():
    if not os.path.exists(ARQUIVO_ESTACIONAMENTO):
        with open(ARQUIVO_ESTACIONAMENTO, 'w', encoding='utf-8') as arquivo: # With open é usado para abrir o arquivo JSON, 
            json.dump({"contador": 0, "veiculos": []}, arquivo, indent=4)

inicializar_json()
                                            #app.route é usado para criar a rota utilizada para chegar até essa função na URL. Essa função apresenta o método POST do protocolo HTTP,
@app.route('/parking', methods=['POST'])    # esse método é responsável por enviar informações, as quais serão processadas na função, para acessar a função basta colocar:          
def registrar_entrada():                    # /parking/placa do carro no final do link. Ex:
    """Essa função é resposável por receber (POST), no qual recebe uma placa de carro e possui duas funcionalidades, são elas: 
        1° - Registrar a entrada de um novo veículo.
        2° - Avisar se um veículo já estáa no estacionamento
        3° - Avisar se o modo de escrita da placa é inválida
    """
    dados = request.get_json()
    placa = dados.get("plate")

    if not placa or not validar_placa(placa):
        return jsonify({"error": "Placa invalida"}), 400 # "400" é o erro do protocolo HTTP que indica que a solicitação é inválida 

    with open(ARQUIVO_ESTACIONAMENTO, 'r+', encoding='utf-8') as arquivo: # With open é usado para abrir o arquivo JSON, 'r+' é para o arquivo ser aberto em modo de leitura e escrita, ou seja, pode-se fazer alterações nele
        dados = json.load(arquivo) # A varíavel dados recebe o conteúdo do arquivo JSON em formato de um dicionário python

        registros_veiculo = [veiculo for veiculo in dados["veiculos"] if veiculo["Placa"] == placa]
        veiculo_existente = (
            max(registros_veiculo, key=lambda x: datetime.strptime(x["Horario_de_Entrada"], '%Y-%m-%d %H:%M:%S')) # Em caso de um mesmo carro ter entrado no estacionamento, ele pega o último registro dele
            if registros_veiculo
            else None
        )

        if veiculo_existente and not veiculo_existente["Saiu"]:
            return jsonify({"error": "Veiculo ainda no estacionamento"}), 400

        dados["contador"] += 1 # Adiciona uma chave chamada "contador" no dicionário dados para ser utilizado como id dos veículos
        novo_carro = { # Em caso positivo de novo carro no estacionamento, é criado o dicionário novo_carro para adiocioná-lo no dicionário dados
            "id": dados["contador"],
            "Horario_de_Entrada": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "Placa": placa,
            "Pago": False,
            "Saiu": False
        }
        dados["veiculos"].append(novo_carro) # Adiciona o novo carro em veículos do dicionário 

        arquivo.seek(0) # Esse seek é responsável para mover o cursor para a posição 0 no arquivo 
        json.dump(dados, arquivo, indent=4, ensure_ascii=False) #json.dumps converte o dicionário dados para a String no formato JSON, salvando os dados do novo carro, Indent quer dizer que o arquivo será salvo em 4 linhas 
                                                                #Ensure_ascii Permite que caracteres não ASCII (como acentos ou caracteres especiais) sejam gravados corretamente no arquivo JSON.
        arquivo.truncate() # Remove qualquer conteúdo restante no arquivo após a posição atual do cursor.

    return jsonify({"message": "Veiculo registrado", "id": novo_carro["id"]}), 201 #"201" indica que a solicitação do protocolo HTTP foi processada com sucesso

@app.route('/parking/<int:id>/pay', methods=['PUT'])
def pagar_estacionamento(id):
    """Essa função é responsável por registrar o pagamento de um veículo que está no estacionamento. Ela contém as funcionalidades:
        1° Avisar caso não encontre o veículo
        2° Avisar caso o encontre o veículo e o pagamento já foi realizado
        3° Realizar o pagamento 
    """
    with open(ARQUIVO_ESTACIONAMENTO, 'r+', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)

        # Procura o veículo pelo ID
        veiculo = None
        for v in dados["veiculos"]: #Essa for procura ver se o ID recebido no método PUT existe 
            if v["id"] == id:
                veiculo = v
                break

        if not veiculo:
            return jsonify({"error": "Veiculo não encontrado"}), 404 # "404" indica que que a solicitação do protocolo HTTP não foi encontrada 

        if veiculo["Pago"]:
            return jsonify({"error": "Pagamento ja realizado"}), 400

        # Esse trecho do código verifica o horário de entrada e calcula o valor devido
        horario_entrada = datetime.strptime(veiculo["Horario_de_Entrada"], '%Y-%m-%d %H:%M:%S') # pega o horário de entrada do carro e o converte 
        horario_atual = datetime.now() # pega o horário atual, porque a conta vai ser baseada em quanto tempo ele ficou no estacionamento
        tempo_permanencia = (horario_atual - horario_entrada).total_seconds() / 3600 # Vai converter as horas em segundos, fazer a conta e depois converter em horas novamente
        valor_a_pagar = round(tempo_permanencia * TARIFA_POR_HORA, 2) # round serve para aredondar a conta, o 2 depois da vírgula indica que são duas casas depois da vírgula

        
        veiculo["Pago"] = True # Atualiza o status do veículo no dicionário de chave "Pago" para true
        veiculo["Valor_Pago"] = valor_a_pagar # Salva o valor que ele pagou(na variável valor_a_pagar) em uma nova chave chamada "Valor_Pago"

        # Salva as alterações no JSON
        arquivo.seek(0)
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)
        arquivo.truncate()

    # A função retorna uma mensagem se tudo estiver certo, onde retorna que o pagamento foi concluído perfeitamente, o ID do bilhete do carro e o valor que foi pago
    return jsonify({ 
        "message": "Pagamento realizado com sucesso", 
        "id": id,
        "valor_pago": valor_a_pagar
    }), 200



@app.route('/parking/<int:id>/out', methods=['PUT'])
def registrar_saida(id):
    """Essa função tem como objetivo registrar a saída de um veículo. Ela contém as seguintes funcionalidades:
        1° - Avisar caso a placa do veículo não seja encontrada
        2° - Avisar caso o veículo seja encontrado, mas o pagamento não foi realizado
        3° - Avisar caso o veículo já esteve no estacionamento, entretanto ele já saiu
        4° - Registrar a saída do veículo e informar que ele saiu com sucesso
    """
    with open(ARQUIVO_ESTACIONAMENTO, 'r+', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)

        veiculo = None
        for v in dados["veiculos"]: #Essa for procura ver se o ID recebido no método PUT existe 
            if v["id"] == id:
                veiculo = v
                break

        if not veiculo:
            return jsonify({"error": "Veiculo não encontrado"}), 404

        if not veiculo["Pago"]:
            return jsonify({"error": "Pagamento não realizado"}), 400

        if veiculo["Saiu"]:
            return jsonify({"error": "Veiculo ja saiu do estacionamento"}), 400
        
        veiculo["Saiu"] = True # em caso de pagamento concluído com sucesso, muda o valor da chave saiu do veículo para TRUE
        veiculo["Horario_de_Saida"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Em caso de pagamento concluído com sucesso, adiciona o horário de saída do veículo ao dicionário(histórico do carro)

        arquivo.seek(0)
        json.dump(dados, arquivo, indent=4, ensure_ascii=False) # Salva as novas informações 
        arquivo.truncate()

    return jsonify({"message": "Saida registrada com sucesso", "id": id}), 200 # Informa o usuário que o veículo teve a saída registrada


@app.route('/parking/<string:placa>', methods=['GET'])
def historico_veiculo(placa):
    """Essa função tem como objetivo obter o histórico de um veículo por placa. Ela tem duas funcionalidades:
        1° - Mostrar o histórico do veículo no estacionamento, independente de quantas vezes ele visitou o local
        2° - Informar caso não tenha encontrado a placa
    """
    with open(ARQUIVO_ESTACIONAMENTO, 'r', encoding='utf-8') as arquivo: # With open é usado para abrir o arquivo JSON, 'r' é para o arquivo ser aberto em modo de leitura
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
        return jsonify({"error": "Placa não encontrada"}), 404 # Mensagem de retorno caso o veículo não seja encontrado no estacionamento

    return jsonify(historico), 200 # Mensagem de retorno ao usuário do histórico do veículo no estacionamento


def validar_placa(placa):
    """ 
    Função que valida a placa para verificar se está de acordo com a norma das placas, sendo essa sua única funcionalidade
    """
    import re
    return bool(re.match(r'^[A-Z]{3}-\d{4}$', placa))


if __name__ == '__main__': # Resposável por fazer a API funcionar
    app.run(debug=True)
    
    