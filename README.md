# Introdução à Computação Gráfica

Repositório criado para organizar meus estudos/atividades da disciplina **"Introdução à Computação Gráfica"**.

## Estrutura do projeto

```text
Aula01/
Aula02/
Aula03/
Aula04/
Aula05/
Aula06/
Aula07/
Aula08/
Aula09/
Aula10/
Aula11/
Aula12/
Trabalho01/
Trabalho02/
venv/
requirements.txt
README.md
```

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/paulo-aug/Computacao-Grafica.git
```

### 2. Criar e ativar o ambiente virtual

#### Windows
```bash
python -m venv venv
.\venv\Scripts\activate
```

#### Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Executar um arquivo

Exemplo para rodar a primeira aula:

```bash
cd Aula01
python QuadradoV1.py
```

Para rodar qualquer outro arquivo, basta informar o caminho correspondente:

```bash
cd Aula02
python nome_do_arquivo.py
```

## Dependências utilizadas

- glfw
- PyOpenGL
- PyOpenGL_accelerate
- pywavefront