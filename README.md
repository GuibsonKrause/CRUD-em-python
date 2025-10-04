teste
# Agenda CRUD em Python

Aplicacao simples para gerenciar contatos usando armazenamento em arquivo texto. O projeto oferece duas formas de uso:

- Interface de linha de comando interativa para cadastros rapidos.
- Aplicacao web com Flask para operacoes CRUD diretamente no navegador.

## Requisitos

- Python 3.10 ou superior (testado com 3.13.7)
- Pip para instalar dependencias opcionais (Flask)

## Instalar dependencias

```
python -m pip install --upgrade pip
python -m pip install flask
```

Se preferir isolar o ambiente:

```
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install flask
```

## Estrutura do projeto

```
CRUD/
+-- crud_app/
�   +-- cli.py          # Menu interativo no terminal
�   +-- storage.py      # Persistencia em data.txt
�   +-- templates/      # Paginas HTML da versao web
+-- data.txt            # Base de dados simples (mantida no repositorio)
+-- main.py             # Entrada para o modo CLI
+-- web_app.py          # Servidor Flask
+-- .gitignore
```

## Executar no terminal (CLI)

```
python main.py
```

O menu permite listar, criar, editar e excluir contatos. Os registros ficam salvos em `data.txt`.

## Executar como aplicacao web

Modo direto:

```
python web_app.py
```

Modo Flask recomendado para desenvolvimento:

```
set FLASK_APP=web_app
set FLASK_ENV=development
python -m flask run
```

Acesse http://127.0.0.1:5000 no navegador. O arquivo `data.txt` continua sendo usado como base de dados compartilhada entre o CLI e a interface web.

## Dados e persistencia

- Cada contato recebe um ID numerico incremental.
- Campos gravados: nome, email e telefone, separados por "|".
- Registros corrompidos sao ignorados na leitura para evitar falhas totais.

## Personalizacoes

- Atualize `SECRET_KEY` em `web_app.py` antes de usar em producao.
- Ajuste layout alterando os templates em `crud_app/templates/`.
- Substitua `TxtStorage` por outro backend (por exemplo SQLite) sem mudar o restante do app.

## Contribuindo

1. Crie um branch.
2. Aplique as mudancas e adicione testes se necessario.
3. Rode `python -m compileall .` ou outros testes relevantes.
4. Abra um pull request descrevendo as alteracoes.

## Licenca

Projeto disponibilizado para uso educacional. Adapte conforme a necessidade.
