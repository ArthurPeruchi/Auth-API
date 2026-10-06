# 🔐 API de Cadastro e Autenticação

API REST desenvolvida em **Python + FastAPI** para cadastro de usuários e autenticação utilizando **JWT (JSON Web Token)**.

O projeto foi desenvolvido como parte da atividade de desenvolvimento de um sistema funcional de **cadastro de usuários e login**, contemplando validação de dados, persistência em banco de dados, proteção de senhas e autenticação de rotas.

Além de atender aos requisitos funcionais da atividade, a aplicação foi estruturada seguindo princípios de **Clean Architecture**, buscando separar responsabilidades e facilitar a manutenção, os testes e a evolução do código.

---

## 📋 Requisitos da atividade

O sistema implementa os seguintes requisitos:

### 👤 Cadastro de usuário

- Cadastro de **nome, e-mail e senha**;
- Validação dos dados recebidos;
- Verificação de e-mail já cadastrado;
- Persistência dos dados em banco de dados;
- Armazenamento seguro da senha através de **hash**.

### 🔑 Login

- Autenticação utilizando e-mail e senha;
- Validação das credenciais;
- Tratamento de credenciais inválidas;
- Geração de **token JWT** após autenticação.

### 🛡️ Segurança

- Senhas não são armazenadas em texto puro;
- Utilização do **Argon2** para hash de senhas;
- Validação dos dados através do **Pydantic**;
- Rotas protegidas através de autenticação JWT.

### 🎫 Após o login

O usuário autenticado recebe um token JWT.

Esse token é utilizado para:

- Identificar o usuário autenticado;
- Validar a autenticidade das requisições;
- Permitir acesso a rotas protegidas;
- Impedir o acesso de usuários não autenticados.

---

## 💻 Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/ArthurPeruchi/Auth-API
```

Entre na pasta do projeto:

```bash
cd "Auth-API"
```

### 2. Criar e ativar o ambiente virtual

O ambiente virtual (`venv`) cria um ambiente isolado para o projeto, permitindo instalar as dependências do Python sem interferir nas bibliotecas instaladas globalmente no computador.

Primeiro, crie o ambiente virtual:

```bash
python -m venv .venv
```

Após a criação, é necessário **ativar o ambiente virtual** antes de instalar as dependências do projeto.

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux/macOS

```bash
source .venv/bin/activate
```

Após a ativação, o terminal normalmente exibirá `(.venv)` no início da linha de comando, indicando que o ambiente virtual está ativo. Você pode sair do ambiente virtual utilizando o comando `deactivate`.

### 3. Instalar as dependências

Com o ambiente virtual ativado:

```bash
python -m pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente

Copie o arquivo `.env.example` para `.env`, da seguinte forma:

#### Windows

```bash
copy .env.example .env
```

#### Linux/macOS

```bash
cp .env.example .env
```

Depois, configure as informações necessárias, como a conexão com o PostgreSQL e a chave utilizada para os tokens.

### 5. Configurar o PostgreSQL

Crie um banco de dados PostgreSQL e configure as informações de conexão no arquivo `.env`.

Exemplo:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/authentication
SECRET_KEY=sua_chave_secreta
```

### 6. Executar a aplicação

Com o ambiente virtual ativado:

```bash
uvicorn app.main:app --reload
```

Com a aplicação em execução, o **FastAPI** disponibiliza a documentação automática da API.

### 📚 Swagger UI

```text
http://127.0.0.1:8000/docs
```

### 📖 ReDoc

```text
http://127.0.0.1:8000/redoc
```

Através do **Swagger UI**, é possível visualizar e testar os endpoints diretamente pelo navegador.

---

## 🚀 Tecnologias utilizadas

| Tecnologia | Utilização |
|---|---|
| 🐍 **Python** | Linguagem de programação |
| ⚡ **FastAPI** | Framework para desenvolvimento da API REST |
| 🚀 **Uvicorn** | Servidor ASGI |
| 🗃️ **SQLAlchemy** | ORM para comunicação com o banco de dados |
| 🐘 **PostgreSQL** | Banco de dados relacional |
| ✅ **Pydantic** | Validação e serialização dos dados |
| 🎫 **PyJWT** | Criação e validação dos tokens JWT |
| 🔐 **Argon2** | Hash seguro das senhas |
| ⚙️ **python-decouple** | Gerenciamento de configurações e variáveis de ambiente |
| 🌱 **python-dotenv** | Carregamento de variáveis de ambiente |

---

# 🏗️ Arquitetura

A aplicação utiliza uma estrutura inspirada em **Clean Architecture**, separando as responsabilidades da aplicação em diferentes camadas.

```text
app/
├── controllers/
│   ├── auth_controller.py
│   └── user_controller.py
│
├── infrastructure/
│   ├── database/
│   ├── exceptions/
│   └── security/
│       ├── argon2_password_hasher.py
│       ├── auth.py
│       ├── jwt.py
│       └── password_hasher.py
│
├── models/
│   └── user.py
│
├── repositories/
│   └── user_repository.py
│
├── schemas/
│   ├── auth_schema.py
│   └── user_schema.py
│
└── usecases/
    ├── auth_usecase.py
    └── user_usecase.py
```

## 📁 Responsabilidade das camadas

- **Controllers** → recebem as requisições HTTP e retornam as respostas;
- **Use Cases** → concentram as regras de negócio;
- **Repositories** → responsáveis pelo acesso e persistência dos dados;
- **Models** → representam as entidades utilizadas pela aplicação;
- **Schemas** → validam e estruturam os dados de entrada e saída;
- **Infrastructure** → concentra recursos externos, banco de dados, segurança e exceções.

---

# 🔄 Fluxo do cadastro

O cadastro segue aproximadamente o seguinte fluxo:

```text
Cliente
   │
   ▼
User Controller
   │
   ▼
User Use Case
   │
   ├── Verifica se o e-mail já existe
   │
   ├── Realiza o hash da senha
   │
   ▼
User Repository
   │
   ▼
PostgreSQL
```

## 1. Cliente envia os dados

O cliente envia uma requisição contendo:

```json
{
  "name": "Usuário",
  "email": "usuario@email.com",
  "password": "senha123"
}
```

## 2. Validação

O **FastAPI**, juntamente com os schemas **Pydantic**, realiza a validação dos dados recebidos.

Entre as validações estão:

- Formato do e-mail;
- Campos obrigatórios;
- Tipos dos dados;
- Regras definidas nos schemas.

## 3. Verificação do e-mail

Antes de criar o usuário, o sistema verifica se já existe um usuário utilizando o e-mail informado.

Caso o e-mail já esteja cadastrado, uma exceção de negócio é gerada e o usuário não é criado novamente.

## 4. Hash da senha

A senha recebida **não é armazenada diretamente**.

Ela passa pelo `Argon2PasswordHasher`, que utiliza o algoritmo **Argon2** para gerar um hash seguro.

```text
Senha original
      │
      ▼
    Argon2
      │
      ▼
Hash da senha
      │
      ▼
 PostgreSQL
```

## 5. Persistência

Após a validação e o processamento da senha, o usuário é enviado para o **Repository**, que realiza a persistência através do **SQLAlchemy**.

## 🔑 Fluxo do login

O processo de autenticação segue:

```text
Cliente
   │
   ▼
Auth Controller
   │
   ▼
Auth Use Case
   │
   ├── Busca usuário
   │
   ├── Verifica senha
   │
   ▼
  JWT
   │
   ▼
Token de acesso
```

O usuário envia:

```json
{
  "email": "usuario@email.com",
  "password": "senha123"
}
```

O sistema busca o usuário pelo e-mail e compara a senha informada com o hash armazenado. Caso as credenciais estejam corretas, um **JWT** é criado.

---

# 🧪 Testando o fluxo

Uma forma de demonstrar o funcionamento da aplicação é seguir esta sequência:

## 1. Cadastro

Criar um novo usuário informando:

```json
{
  "name": "Usuário",
  "email": "usuario@email.com",
  "password": "senha123"
}
```

## 2. Verificar o banco

O usuário deve estar persistido no **PostgreSQL**.

A senha armazenada deve ser um **hash Argon2**, e não `senha123`.

## 3. Login

Enviar o mesmo e-mail e senha para o endpoint de autenticação.

## 4. Receber o JWT

A API deve retornar um **token de acesso JWT**.

## 5. Acessar rota protegida

Enviar o token através do header:

```http
Authorization: Bearer <token>
```

A requisição deve ser autorizada caso o token seja válido.

## 6. Testar sem autenticação

Os recursos protegidos da aplicação podem ser acessados após o fornecimento de um token JWT válido.

Atualmente, os endpoints protegidos incluem:

- `PATCH /users/me` → permite atualizar parcialmente os dados do usuário autenticado;
- `PUT /users/me` → permite atualizar todos os dados do usuário autenticado.

Para acessar esses recursos, é necessário enviar o token no header. Caso a requisição seja realizada sem um token válido, o acesso ao recurso deve ser **negado**.
