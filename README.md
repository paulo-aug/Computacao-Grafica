# Introdução à Computação Gráfica

Repositório criado para organizar meus estudos/atividades da disciplina **"Introdução à Computação Gráfica"**.

## Estrutura do projeto

```text
Aula01/
Aula02/
Aula03/
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
python Aula01/QuadradoV1.py
```

Para rodar qualquer outro arquivo, basta informar o caminho correspondente:

```bash
python Aula02/nome_do_arquivo.py
python Aula03/nome_do_arquivo.py
```

## Dependências utilizadas

- glfw
- PyOpenGL
- PyOpenGL_accelerate
- pywavefront