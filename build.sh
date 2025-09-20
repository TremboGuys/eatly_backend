#!/usr/bin/env bash
# Sai do script se houver algum erro
set -o errexit

curl https://sh.rustup.rs -sSf | sh -s -- -y
export PATH=$HOME/.cargo/bin:$PATH
export CARGO_HOME=$HOME/.cargo
export RUSTUP_HOME=$HOME/.rustup

# Atualiza o pip
pip install --upgrade pip

# Atualiza pip/setuptools/wheel para pegar wheels pré-compilados
pip install --upgrade pip setuptools wheel

# Instala dependências do seu projeto
pip install -r requirements.txt

# Coleta os arquivos estáticos
python manage.py collectstatic --no-input

# Aplica as migrações
python manage.py migrate