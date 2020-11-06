# megadados

## Organização

A configuração está dentro da pasta "api", onde há a configuração passada e a atual "aps3". 

## Rodando

### Página de endpoints

Comando dentro da pasta raíz do repositório: uvicorn api.aps3.tasklist.tasklist.main:app --reload

Acesso: http://127.0.0.1:8000/docs


### Testes

Comando dentro da pasta "aps3": pytest
