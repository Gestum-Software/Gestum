# Gestum — Sistema de Chamados e Gestão de Recursos

Sistema web para **gerenciamento de chamados, equipamentos e reservas de recursos**, desenvolvido como parte do Projeto Integrador do curso Técnico em Informática para Internet.

## 📋 Sobre o projeto

O **Gestum** tem como objetivo centralizar e organizar solicitações relacionadas a problemas técnicos, manutenção de equipamentos e utilização de recursos compartilhados de uma instituição.

Atualmente, esse tipo de solicitação pode ocorrer por meios informais, como conversas presenciais, mensagens ou aplicativos de comunicação, dificultando o acompanhamento das solicitações, o controle de responsabilidades e a manutenção de um histórico das ocorrências.

O sistema busca solucionar esse problema por meio de uma plataforma centralizada, permitindo registrar, acompanhar e gerenciar essas demandas.

O projeto também busca integrar conhecimentos de **desenvolvimento web, banco de dados, programação, interfaces, testes, documentação e gestão de projetos**, conforme a proposta do Projeto Integrador.

## 🚀 Principais funcionalidades

### 🎫 Sistema de chamados

* Abertura de chamados por usuários;
* Descrição do problema;
* Classificação por categoria;
* Definição de prioridade;
* Associação do chamado a um equipamento ou local;
* Acompanhamento do status;
* Atribuição a um responsável;
* Registro de comentários e atualizações;
* Histórico de alterações;
* Encerramento de chamados.

### 🖥️ Gestão de equipamentos e recursos

* Cadastro de equipamentos e recursos;
* Registro de identificação, localização e situação;
* Histórico de manutenções;
* Associação de equipamentos a chamados;
* Indicação de equipamentos indisponíveis ou em manutenção.

### 📅 Sistema de reservas

* Reserva de salas, projetores, laboratórios e outros recursos;
* Definição de data e horário;
* Verificação de disponibilidade;
* Impedimento de reservas conflitantes;
* Cancelamento de reservas;
* Visualização das reservas em calendário;
* Possibilidade de aprovação de reservas, quando necessário.

# ⚙️ Instalação e configuração

## 1. Pré-requisitos

Antes de começar, certifique-se de possuir instalado:

* **Python 3**
* **pip**
* **Git**

Verifique as instalações:

```bash
python --version
pip --version
git --version
```

Em alguns sistemas, principalmente Linux, o comando do Python pode ser:

```bash
python3 --version
```

---

## 2. Clonar o repositório

Clone o projeto utilizando o Git:

```bash
git clone https://github.com/Gestum-Software/Gestum.git
```

Entre na pasta do projeto:

```bash
cd gestum
```

---

## 3. Criar o ambiente virtual

É recomendado utilizar um ambiente virtual para manter as dependências do projeto isoladas.

### Windows

```bash
python -m venv venv
```

Ative o ambiente:

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv
```

Ative o ambiente:

```bash
source venv/bin/activate
```

Após a ativação, o terminal deverá indicar que o ambiente virtual está ativo.

---

## 4. Atualizar o pip

Com o ambiente virtual ativado:

```bash
python -m pip install --upgrade pip
```

---

## 5. Instalar as dependências

Caso o projeto possua um arquivo `requirements.txt`, instale todas as dependências com:

```bash
pip install -r requirements.txt
```

### Gerando o `requirements.txt`

Depois de instalar as dependências, é possível registrar as versões utilizadas:

```bash
pip freeze > requirements.txt
```

Isso permite que outros integrantes da equipe instalem as mesmas dependências posteriormente.

# 🗄️ Banco de dados e migrações

O Django utiliza **migrações** para transformar as alterações realizadas nos modelos (`models.py`) em alterações na estrutura do banco de dados.

## 6. Criar as migrações

Após configurar os modelos do projeto, execute:

```bash
python manage.py makemigrations
```

Esse comando identifica alterações nos modelos e cria os arquivos de migração correspondentes.

---

## 7. Aplicar as migrações

Para aplicar as migrações ao banco de dados:

```bash
python manage.py migrate
```

O Django criará e configurará as tabelas necessárias para o funcionamento do sistema.

> Sempre que houver alterações nos modelos do sistema, normalmente será necessário executar novamente `makemigrations` e depois `migrate`.

---

## 8. Criar um superusuário

Para acessar o painel administrativo do Django, crie um usuário administrador:

```bash
python manage.py createsuperuser
```

Informe:

* Nome de usuário;
* E-mail;
* Senha.

Esse usuário poderá acessar o Django Admin após iniciar o servidor.

# ▶️ Executando o projeto

Com o ambiente virtual ativado, execute:

```bash
python manage.py runserver
```

O servidor de desenvolvimento será iniciado.

Por padrão, o sistema poderá ser acessado em:

```text
http://127.0.0.1:8000/
```

O painel administrativo do Django fica disponível em:

```text
http://127.0.0.1:8000/admin/
```

# 🔄 Fluxo básico para desenvolvimento

Sempre que um integrante clonar o projeto ou começar uma nova sessão de desenvolvimento, o fluxo recomendado é:

```bash
# 1. Entrar na pasta
cd gestum

# 2. Criar o ambiente virtual (primeira vez)
python -m venv venv

# 3. Ativar o ambiente virtual
venv\Scripts\activate

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Aplicar migrações
python manage.py migrate

# 6. Executar o servidor
python manage.py runserver
```

Caso novos modelos ou alterações nos modelos sejam desenvolvidos:

```bash
python manage.py makemigrations
python manage.py migrate
```
