# Sistema de Gestão de Estoque de Pneus

Sistema de gerenciamento de estoque de pneus desenvolvido com Flask, MySQL, HTML, CSS e JavaScript.

## Requisitos

- Python 3.8 ou superior
- MySQL Server
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd [NOME_DO_DIRETORIO]
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o banco de dados:
- Crie um banco de dados MySQL chamado `estoque_pneus`
- Atualize o arquivo `.env` com suas credenciais do MySQL se necessário

5. Execute a aplicação:
```bash
python app.py
```

6. Acesse a aplicação no navegador:
```
http://localhost:5000
```

## Funcionalidades

- Cadastro de pneus com informações detalhadas
- Edição de pneus existentes
- Exclusão de pneus
- Listagem de todos os pneus
- Busca por dimensões, marca ou tipo
- Interface responsiva e intuitiva

## Estrutura do Projeto

- `app.py`: Arquivo principal da aplicação Flask
- `templates/`: Pasta com os templates HTML
- `static/`: Pasta com arquivos CSS e JavaScript
- `requirements.txt`: Lista de dependências do projeto
- `.env`: Configurações de ambiente

## Contribuição

Sinta-se à vontade para contribuir com o projeto através de pull requests.

## Licença

Este projeto está licenciado sob a licença MIT. 