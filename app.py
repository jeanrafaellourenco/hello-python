from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)
db = mysql.connector.connect(
    host= os.environ.get('MYSQL_HOST'),
    user= os.environ.get('MYSQL_USER'),
    password= os.environ.get('MYSQL_PASSWORD'),
    database= os.environ.get('MYSQL_DATABASE')
)

cursor = db.cursor()

# Rota raiz da aplicação para verificar se está funcionando
@app.route('/')
def index():
    return jsonify({'message': 'Ok'}), 200  # Status 200 - OK

# Rota para listar todos os veículos
@app.route('/veiculos', methods=['GET'])
def listar_veiculos():
    cursor.execute("SELECT * FROM veiculos")
    veiculos = cursor.fetchall()
    veiculos_list = []
    for veiculo in veiculos:
        veiculo_dict = {
            'id': veiculo[0],
            'marca': veiculo[1],
            'modelo': veiculo[2],
            'placa': veiculo[3]
        }
        veiculos_list.append(veiculo_dict)
    return jsonify(veiculos_list)

# Rota para criar um novo veículo
@app.route('/veiculos', methods=['POST'])
def criar_veiculo():
    marca = request.json['marca']
    modelo = request.json['modelo']
    placa = request.json['placa']
    
    # Verificar se a placa já está cadastrada
    query = "SELECT * FROM veiculos WHERE placa = %s"
    value = (placa,)
    cursor.execute(query, value)
    veiculo = cursor.fetchone()
    if veiculo:
        return jsonify({'message': 'Veículo com essa placa já está cadastrado'}), 409  # Status 409 - Conflito

    # Inserir o veículo no banco de dados
    query = "INSERT INTO veiculos (marca, modelo, placa) VALUES (%s, %s, %s)"
    values = (marca, modelo, placa)
    cursor.execute(query, values)
    db.commit()
    return jsonify({'message': 'Veículo criado com sucesso'}), 201  # Status 201 - Criado


# Rota para buscar um veículo por ID
@app.route('/veiculos/<int:id>', methods=['GET'])
def buscar_veiculo(id):
    query = "SELECT * FROM veiculos WHERE id = %s"
    value = (id,)
    cursor.execute(query, value)
    veiculo = cursor.fetchone()
    if veiculo:
        veiculo_dict = {
            'id': veiculo[0],
            'marca': veiculo[1],
            'modelo': veiculo[2],
            'placa': veiculo[3]
        }
        return jsonify(veiculo_dict)
    else:
        return jsonify({'message': 'Veículo não encontrado'}), 404  # Status 404 - Não encontrado

# Rota para atualizar um veículo
@app.route('/veiculos/<int:id>', methods=['PUT'])
def atualizar_veiculo(id):
    marca = request.json['marca']
    modelo = request.json['modelo']
    placa = request.json['placa']

    # Verificar se o veículo existe
    query = "SELECT * FROM veiculos WHERE id = %s"
    value = (id,)
    cursor.execute(query, value)
    veiculo = cursor.fetchone()
    if not veiculo:
        return jsonify({'message': 'Veículo não encontrado'}), 404  # Status 404 - Não encontrado

    # Atualizar o veículo no banco de dados
    query = "UPDATE veiculos SET marca = %s, modelo = %s, placa = %s WHERE id = %s"
    values = (marca, modelo, placa, id)
    cursor.execute(query, values)
    db.commit()
    return jsonify({'message': 'Veículo atualizado com sucesso'}), 200  # Status 200 - OK

# Rota para deletar um veículo
@app.route('/veiculos/<int:id>', methods=['DELETE'])
def deletar_veiculo(id):
    # Verificar se o veículo existe
    query = "SELECT * FROM veiculos WHERE id = %s"
    value = (id,)
    cursor.execute(query, value)
    veiculo = cursor.fetchone()
    if not veiculo:
        return jsonify({'message': 'Veículo não encontrado'}), 404  # Status 404 - Não encontrado

    # Excluir o veículo do banco de dados
    query = "DELETE FROM veiculos WHERE id = %s"
    cursor.execute(query, value)
    db.commit()
    return jsonify({'message': 'Veículo deletado com sucesso'}), 200  # Status 200 - OK

# Rota para a documentação
@app.route('/docs', methods=['GET'])
def get_documentation():
    documentation = {
        "/veiculos": {
            "GET": {
                "description": "Retorna a lista de todos os veículos cadastrados",
                "responses": {
                    "200": {
                        "description": "OK",
                        "content": {
                            "application/json": {
                                "example": [
                                    {
                                        "id": 1,
                                        "marca": "Fiat",
                                        "modelo": "Uno",
                                        "placa": "ABC123"
                                    },
                                    {
                                        "id": 2,
                                        "marca": "Volkswagen",
                                        "modelo": "Gol",
                                        "placa": "DEF456"
                                    }
                                ]
                            }
                        }
                    }
                }
            },
            "POST": {
                "description": "Cria um novo veículo",
                "parameters": {
                    "marca": {
                        "type": "string",
                        "description": "A marca do veículo"
                    },
                    "modelo": {
                        "type": "string",
                        "description": "O modelo do veículo"
                    },
                    "placa": {
                        "type": "string",
                        "description": "A placa do veículo"
                    }
                },
                "responses": {
                    "201": {
                        "description": "Criado",
                        "content": {
                            "application/json": {
                                "example": {
                                    "message": "Veículo criado com sucesso"
                                }
                            }
                        }
                    },
                    "409": {
                        "description": "Conflito",
                        "content": {
                            "application/json": {
                                "example": {
                                    "message": "Veículo com essa placa já está cadastrado"
                                }
                            }
                        }
                    }
                }
            },
            "/<int:id>": {
                "GET": {
                    "description": "Retorna um veículo por ID",
                    "parameters": {
                        "id": {
                            "type": "integer",
                            "description": "O ID do veículo"
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "OK",
                            "content": {
                                "application/json": {
                                    "example": {
                                        "id": 1,
                                        "marca": "Fiat",
                                        "modelo": "Uno",
                                        "placa": "ABC123"
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Não encontrado",
                            "content": {
                                "application/json": {
                                    "example": {
                                        "message": "Veículo não encontrado"
                                    }
                                }
                            }
                        }
                    }
                },
                "PUT": {
                    "description": "Atualiza um veículo",
                    "parameters": {
                        "id": {
                            "type": "integer",
                            "description": "O ID do veículo"
                        },
                        "marca": {
                            "type": "string",
                            "description": "A marca do veículo"
                        },
                        "modelo": {
                            "type": "string",
                            "description": "O modelo do veículo"
                        },
                        "placa": {
                            "type": "string",
                            "description": "A placa do veículo"
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "OK",
                            "content": {
                                "application/json": {
                                    "example": {
                                        "message": "Veículo atualizado com sucesso"
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Não encontrado",
                            "content": {
                                "application/json": {
                                    "example": {
                                        "message": "Veículo não encontrado"
                                    }
                                }
                            }
                        }
                    }
                },
                "DELETE": {
                    "description": "Deleta um veículo",
                    "parameters": {
                        "id": {
                            "type": "integer",
                            "description": "O ID do veículo"
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "OK",
                            "content": {
                                "application/json": {
                                    "example": {
                                        "message": "Veículo deletado com sucesso"
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Não encontrado",
                            "content": {
                                "application/json": {
                                    "example": {
                                        "message": "Veículo não encontrado"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    return jsonify(documentation), 200 # Status 200 - OK


def run_debug():
    app.run(debug=True, host="127.0.0.1", port=3000)

def run_prod():
    from waitress import serve
    try:
        print("Status: Ok")
        serve(app, host="0.0.0.0", port=5000)
    except Exception:
        print("Erro ao subir o servidor")

if __name__ == '__main__':
    if os.getenv("AMBIENTE") == "PRODUCAO":
        run_prod()
    else:
        run_debug()


