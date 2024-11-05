
# API de Predição de Doenças Respiratórias com Machine Learning - XPredict

Esta API utiliza machine learning para auxiliar profissionais médicos na classificação de imagens de raio-X do tórax em quatro categorias: **COVID-19**, **normal**, **pneumonia viral** e **pneumonia bacteriana**. O modelo de machine learning foi desenvolvido para agilizar o processo de diagnóstico e melhorar a eficiência do atendimento médico.

Além das predições, a API gerencia o controle de acesso dos usuários e fornece dados processados, permitindo que os clientes visualizem informações em uma aplicação web. Isso inclui a **gestão de usuários**, **controle de permissões** e o **upload de imagens** para análise e predição pelo modelo.

## Autor
Desenvolvido por [Diogo Brazil](https://github.com/DiogoBrazil)

---

## Índice
- [Recursos Principais](#recursos-principais)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação e Configuração](#instalação-e-configuração)
- [Uso da API](#uso-da-api)
- [Execução com Docker](#execução-com-docker)
- [Contribuição](#contribuição)

---

## Recursos Principais

- **Classificação de Imagens**: Classifica imagens de raio-X em quatro categorias.
- **Gestão de Usuários e Controle de Acesso**: Controle de permissões e autenticação para usuários.
- **Upload de Imagens**: Permite o upload de imagens para análise e predição.
- **Visualização Web**: Dados processados e informações exibidas em uma aplicação web.

---

## Tecnologias Utilizadas

- **Linguagem**: Python
- **Framework**: FastAPI
- **Machine Learning**: YOLO, ResNet (ou outra arquitetura especificada)
- **Banco de Dados**: Integração com bancos de dados externos (Postgres e SQL Server)
- **Docker**: Contêinerização para facilitar a implantação

---

## Estrutura do Projeto

```plaintext
├── config                # Configurações de ambiente e variáveis
├── controllers           # Lógica dos endpoints e controle de fluxo
├── infra                 # Infraestrutura e conectividade com banco de dados
├── interfaces            # Interfaces e contratos para a API
├── models                # Definição e carregamento do modelo de machine learning
├── repository            # Acesso ao banco de dados e operações de persistência
├── routes                # Definição das rotas da API
├── services              # Lógica de negócios e serviços auxiliares
├── utils                 # Funções utilitárias para processamento e validação
├── .env                  # Arquivo de variáveis de ambiente (não incluído no repositório)
├── .gitignore            # Arquivo de configuração para ignorar arquivos no git
├── Dockerfile            # Arquivo para criação da imagem Docker
├── docker-compose.yml    # Arquivo para orquestração dos contêineres
├── main.py               # Arquivo principal para iniciar a aplicação FastAPI
└── requirements.txt      # Dependências do projeto
```

---

## Instalação e Configuração

1. **Clone o repositório**:
    ```bash
    git clone https://github.com/DiogoBrazil/respiratory-disease-prediction-api.git
    cd respiratory-disease-prediction-api
    ```

2. **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configuração do `.env`**: Crie um arquivo `.env` na raiz com as variáveis de ambiente necessárias, como informações de banco de dados e chave secreta para autenticação.

4. **Execute a aplicação**:
    ```bash
    uvicorn main:app --reload
    ```

A API estará disponível em `http://localhost:8000`.

---

## Uso da API

### Documentação Interativa
A documentação da API, com todos os endpoints e exemplos, está disponível em:
- [Swagger UI](http://localhost:8000/docs)
- [Redoc](http://localhost:8000/redoc)

### Exemplos de Endpoints

- `POST /predict`: Retorna a predição para uma imagem enviada.
- `GET /users`: Retorna a lista de usuários (requer autenticação).

> Consulte a documentação interativa para ver todos os endpoints e detalhes.

---

## Execução com Docker

Para executar a aplicação em contêiner usando Docker e Docker Compose:

1. **Construa e inicie o contêiner**:
    ```bash
    docker compose up --build
    ```

2. **Acesse a aplicação**:
    A aplicação estará disponível em `http://localhost:8000`.

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.