#!/usr/bin/env bash
# Sai do script se houver algum erro
set -o errexit

# Atualiza o pip e ferramentas de build
pip install --upgrade pip setuptools wheel

# Instala dependências do projeto
pip install -r requirements.txt

# Coleta os arquivos estáticos
python manage.py collectstatic --no-input

# Aplica as migrações
python manage.py migrate
