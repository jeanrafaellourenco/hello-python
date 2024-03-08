# Hello Python
API utilizando python flask com mysql em docker para gerenciamento de veículos 

![background](/imagens/background.jpeg)

## Iniciando e acessando a aplicação
```
docker-compose build && docker-compose up -d
```
Aguarde 20 segundos até que o banco de dados esteja conectado, depois acesse: http://localhost:5000/


# Testando a aplicação
## Documentação
```
http://localhost:5000/docs
```

### Listar todos os veículos (GET):
```
curl -X GET http://localhost:5000/veiculos
```

### Criar um novo veículo (POST):
```
curl -X POST -H "Content-Type: application/json" -d '{
  "marca": "Toyota",
  "modelo": "Corolla",
  "placa": "ABC1234"
}' http://localhost:5000/veiculos
```

### Buscar um veículo por ID (GET):
```
curl -X GET http://localhost:5000/veiculos/{id}
```

### Atualizar um veículo (PUT):
```
curl -X PUT -H "Content-Type: application/json" -d '{
  "marca": "Honda",
  "modelo": "Civic",
  "placa": "XYZ5678"
}' http://localhost:5000/veiculos/{id}
```

### Deletar um veículo (DELETE):
```
curl -X DELETE http://localhost:5000/veiculos/{id}
```
