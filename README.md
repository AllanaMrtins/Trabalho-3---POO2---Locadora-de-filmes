<div align="center">

# 🎬 Locadora de Filmes

Sistema para gerenciar os filmes e os aluguéis de uma locadora.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-Qt-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)

*Trabalho 03 da disciplina de Programação Orientada a Objetos II (POO2)*

</div>

---

## 📖 Sobre o projeto

A **Locadora de Filmes** é um programa com interface gráfica feito em **Python** com a biblioteca **PySide6**. Com ele, o atendente consegue cadastrar filmes, alugar para um cliente, registrar a devolução, remover filmes e buscar pelo título.

O projeto foi feito para praticar **Programação Orientada a Objetos**: cada parte do sistema (o filme, a tela principal, as janelas de formulário e o acesso ao banco) é uma classe separada, em seu próprio arquivo.

Na versão atual (3.0.0), os dados ficam em um banco **PostgreSQL** que executa em um **contêiner Docker**. O acesso ao banco acontece em uma **thread** separada, para a tela não travar.

---

##  Funcionalidades

-  **Adicionar filme:** informando título, gênero e ano.
-  **Alugar filme:** informando o nome do cliente e os dias de aluguel (de 1 a 30). Também dá para alugar com duplo clique no filme.
-  **Devolver filme:** deixa o filme disponível de novo.
-  **Remover filme:** tira o filme da lista.
-  **Buscar filme:** a lista é filtrada enquanto você digita o título.
-  **Status:** cada filme aparece como *Disponível* ou *Alugado*.
-  **Dados no banco:** os filmes ficam no PostgreSQL (volume Docker) e continuam lá quando o programa ou o contêiner são reiniciados.
-  **Banco em segundo plano:** as consultas e alterações são feitas por uma thread, sem travar a tela.
-  **Recarregar:** *Arquivo > Recarregar do banco* atualiza a lista.
-  **Avisos e confirmações:** o sistema avisa quando nenhum filme foi selecionado e pede confirmação antes de devolver, remover ou sair.

Na primeira vez que o contêiner sobe, `db/init.sql` cria a tabela e insere 4 filmes de exemplo: *Interestelar*, *Toy Story*, *O Poderoso Chefão* e *Homem-Aranha*.

---

## 🗂️ Estrutura do projeto

| Arquivo | O que faz |
| --- | --- |
| `main.py` | Inicia o programa e abre a janela principal. |
| `modelos.py` | Classe `Filme` (id, título, gênero, ano, disponibilidade, cliente e dias), com `para_dicionario` e `de_dicionario`. |
| `repositorio.py` | Classe `RepositorioFilmes`: único lugar com SQL (listar, inserir, atualizar aluguel, remover). Lê a configuração do `.env`. |
| `tarefas.py` | Classe `GerenciadorBanco`: thread com fila que executa as operações no banco e avisa a janela por `Signal`. |
| `janela_principal.py` | Classe `JanelaPrincipal`: tela principal, botões, menus e lógica da interface. |
| `dialogo_filme.py` | Classe `DialogoFilme`: janelinha para cadastrar um filme. |
| `dialogo_aluguel.py` | Classe `DialogoAluguel`: janelinha para registrar o cliente e os dias do aluguel. |
| `sobre.py` | Classe `JanelaSobre`: janela com informações sobre o sistema. |
| `docker-compose.yml` | Define o contêiner do PostgreSQL, o volume e o healthcheck. |
| `db/init.sql` | Cria a tabela `filmes` e os dados de exemplo na primeira inicialização. |
| `.env.example` | Modelo de configuração do banco (copiar para `.env`). |
| `requirements.txt` | Dependências Python. |

--- | --- |
| `main.py` | Inicia o programa e abre a janela principal. |
| `modelos.py` | Classe `Filme`, que guarda título, gênero, ano, se está disponível, o cliente e os dias de aluguel. Tem os métodos `para_dicionario` e `de_dicionario`, usados para gravar e ler o JSON. |
| `janela_principal.py` | Classe `JanelaPrincipal`: a tela principal, com a lista, os botões, os menus e a lógica de adicionar, alugar, devolver, remover e buscar. |
| `dialogo_filme.py` | Classe `DialogoFilme`: janelinha para cadastrar um filme. |
| `dialogo_aluguel.py` | Classe `DialogoAluguel`: janelinha para registrar o cliente e os dias do aluguel. |
| `sobre.py` | Classe `JanelaSobre`: janela com informações sobre o sistema. |

---

## 🧠 Como funciona

1. **`Filme`** representa cada filme. Começa como *disponível*; ao ser alugado guarda o cliente e os dias, e ao ser devolvido esses dados são limpos. O `id` vem do banco.
2. **`RepositorioFilmes`** executa os comandos SQL (com parâmetros, sem concatenar texto) e faz `commit` a cada alteração.
3. **`GerenciadorBanco`** roda em uma thread própria. A janela coloca pedidos (carregar, inserir, atualizar, remover ou encerrar) em uma fila e a thread os atende um de cada vez. O resultado volta por um `Signal`. A conexão é criada dentro da thread; se der erro, é feito `rollback` e a conexão é refeita no pedido seguinte.
4. **`JanelaPrincipal`** mostra a lista. Depois de cada alteração bem-sucedida, ela pede nova leitura ao banco, que é a fonte da verdade.
5. **Os diálogos** abrem para digitar informações. Se o campo obrigatório estiver vazio, a janela não fecha.

### Banco de dados

Tabela `filmes`: `id` (chave primária), `titulo`, `genero`, `ano`, `disponivel`, `cliente`, `dias`. As restrições (`CHECK`) garantem ano entre 1900 e 2100, dias entre 0 e 30 e coerência: filme disponível não tem cliente nem dias; filme alugado precisa de cliente e de pelo menos 1 dia.

**Por que banco?** Filmes e aluguéis são dados estruturados, alterados com frequência e que precisam de integridade, então ficam em um banco relacional. Já a configuração de conexão fica em arquivo (`.env`), por ser texto simples e variar por ambiente.

### Fluxo

1. Ao abrir, a janela pede à thread para carregar os filmes. Enquanto isso, as operações ficam bloqueadas (`carregamento_concluido`).
2. Quando a leitura termina, a lista é montada e as operações são liberadas.
3. Adicionar, alugar, devolver ou remover enviam o pedido à thread; ao terminar, a lista é recarregada.
4. Ao fechar, a janela manda a thread encerrar e espera ela terminar.

### Conceitos de POO usados

- **Classes e objetos:** `Filme`, `RepositorioFilmes`, `JanelaPrincipal`, `GerenciadorBanco` e os diálogos.
- **Herança:** a tela principal herda de `QMainWindow`, os diálogos herdam de `QDialog` e o gerenciador do banco herda de `QThread`.
- **Encapsulamento e organização:** cada classe cuida de uma tarefa e fica em um arquivo próprio.
- **Sobrescrita de métodos:** `__str__` na classe `Filme`, `closeEvent` na tela principal e `run` no gerenciador do banco.
- **Threads e sinais:** o acesso ao banco roda em paralelo com a interface, e a comunicação de volta é feita por `Signal`.

---

## 🚀 Como executar

Você precisa de [Python 3.10+](https://www.python.org/downloads/) e do [Docker](https://docs.docker.com/get-docker/) (com Docker Compose).

```bash
# 1. Baixe o projeto
git clone https://github.com/AllanaMrtins/Trabalho-de-POO2---Locadora-de-filmes.git
cd Trabalho-de-POO2---Locadora-de-filmes

# 2. (opcional) personalize a configuração do banco
cp .env.example .env

# 3. Suba o banco de dados em um contêiner
docker compose up -d

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Execute
python main.py
```

Comandos úteis:

```bash
docker compose ps            # ver se o banco está saudável
docker compose logs db       # ver os logs do banco
docker compose down          # parar o contêiner (os dados continuam no volume)
docker compose down -v       # parar e APAGAR os dados (recria os 4 filmes de exemplo na próxima vez)
```

> Para o banco rodar em **outra máquina**, suba o `docker compose` nela e coloque o IP em `POSTGRES_HOST` no `.env` da aplicação.

---

## 📘 Como usar

- **Adicionar:** clique em *Adicionar Filme*, preencha os dados e confirme.
- **Alugar:** selecione um filme, clique em *Alugar* (ou dê duplo clique), informe o cliente e os dias.
- **Devolver:** selecione um filme alugado, clique em *Devolver* e confirme.
- **Remover:** selecione o filme, clique em *Remover* e confirme.
- **Buscar:** digite o título no campo de busca, no topo da tela.

Tudo o que você fizer é salvo automaticamente no banco de dados.

---

## 📝 Histórico de versões

- **3.0.0 (13/11/2026):** banco PostgreSQL em contêiner Docker, `RepositorioFilmes` e `GerenciadorBanco` (parcial 1 do Trabalho 03).
- **2.1.0 (16/10/2026):** leitura e gravação do arquivo em uma thread (`tarefas.py`), com fila de operações, sinais e encerramento seguro ao fechar o programa.
- **2.0.0 (09/10/2026):** dados salvos em `filmes.json`, com `para_dicionario` e `de_dicionario` na classe `Filme`.
- **1.0.0:** interface gráfica, cadastro, busca, aluguel, devolução e remoção, com dados só na memória.

---

## 🔧 Melhorias futuras

- Mostrar o cliente e os dias de aluguel na lista.
- Cadastro de clientes e histórico de aluguéis.
- API em FastAPI entre a aplicação e o banco (parcial 2 do Trabalho 03).

---

## 👥 Equipe

- **Allana Camily de Sousa Martins**
- **Gabriel dos Santos Silva**
- **Janiele de Jesus Barbosa**

---

 
<div align="center">
Feito pelo grupo para a disciplina de POO2 · Trabalho para fins acadêmicos
</div>
