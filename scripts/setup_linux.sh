#!/bin/bash

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

echo ""
echo -e "${CYAN}"
echo " ██████╗ ██╗      █████╗  ██████╗██╗  ██╗██╗    ██╗██╗██████╗ ███████╗"
echo " ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝██║    ██║██║██╔══██╗██╔════╝"
echo " ██████╔╝██║     ███████║██║     █████╔╝ ██║ █╗ ██║██║██████╔╝█████╗  "
echo " ██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██║███╗██║██║██╔══██╗██╔══╝  "
echo " ██████╔╝███████╗██║  ██║╚██████╗██║  ██╗╚███╔███╔╝██║██║  ██║███████╗"
echo " ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝╚═╝  ╚═╝╚══════╝"
echo -e "${NC}"
echo -e "${BOLD} Setup do ambiente de desenvolvimento${NC}"
echo " -----------------------------------------------"
echo ""

# Navegar para a raiz do projeto (pasta pai de scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT" || exit 1

echo -e " ${CYAN}[INFO]${NC} A trabalhar em: $PROJECT_ROOT"
echo ""

# Caminho do requirements.txt
REQUIREMENTS_FILE="$PROJECT_ROOT/requirements.txt"

# -----------------------------------------------
# 1. Verificar Python
# -----------------------------------------------
echo -e "${BOLD}[1/3] A verificar Python...${NC}"

if command -v python3 &>/dev/null; then
    PYVER=$(python3 --version)
    echo -e " ${GREEN}[OK]${NC} $PYVER encontrado."
else
    echo -e " ${RED}[ERRO]${NC} Python3 não encontrado!"
    echo " Instala com: sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

echo ""

# -----------------------------------------------
# 2. Criar/reutilizar ambiente virtual
# -----------------------------------------------
echo -e "${BOLD}[2/3] A verificar ambiente virtual (venv)...${NC}"

if ! python3 -m venv --help &>/dev/null; then
    echo " python3-venv não encontrado. A instalar..."
    sudo apt update -qq
    sudo apt install -y python3-venv python3-pip
fi

# Dependências Qt6 para Linux
echo " A verificar dependências Qt6 para Linux..."

MISSING_DEPS=()

for pkg in libxcb-xinerama0 libxcb-cursor0 libgl1; do
    if ! dpkg -s "$pkg" &>/dev/null; then
        MISSING_DEPS+=("$pkg")
    fi
done

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo " A instalar dependências do sistema: ${MISSING_DEPS[*]}"
    sudo apt update -qq
    sudo apt install -y "${MISSING_DEPS[@]}" -qq
fi

if [ -d "venv" ]; then
    echo -e " ${YELLOW}[SKIP]${NC} venv já existe, a reutilizar."
else
    echo " A criar venv..."
    python3 -m venv venv

    if [ $? -ne 0 ]; then
        echo -e " ${RED}[ERRO]${NC} Falha ao criar venv."
        exit 1
    fi

    echo -e " ${GREEN}[OK]${NC} venv criado."
fi

source venv/bin/activate

pip install --upgrade pip --quiet

echo -e " ${GREEN}[OK]${NC} pip atualizado."
echo ""

# -----------------------------------------------
# 3. Instalar dependências Python
# -----------------------------------------------
echo -e "${BOLD}[3/3] A instalar dependências Python...${NC}"
echo ""

if [ ! -f "$REQUIREMENTS_FILE" ]; then
    echo -e " ${RED}[ERRO]${NC} requirements.txt não encontrado!"
    echo " Caminho esperado: $REQUIREMENTS_FILE"
    exit 1
fi

echo " A instalar dependências de:"
echo " $REQUIREMENTS_FILE"
echo ""

pip install -r "$REQUIREMENTS_FILE"

if [ $? -ne 0 ]; then
    echo -e " ${RED}[ERRO]${NC} Falha ao instalar dependências."
    exit 1
fi

echo ""
echo -e " ${GREEN}[OK]${NC} Todas as dependências instaladas."
echo ""

# -----------------------------------------------
# Concluído
# -----------------------------------------------
echo " -----------------------------------------------"
echo -e "${GREEN}${BOLD} Setup concluído com sucesso!${NC}"
echo ""
echo " Para começar a desenvolver:"
echo "   1. Ativa o venv:   source venv/bin/activate"
echo "   2. Corre a app:    python main.py"
echo " -----------------------------------------------"
echo ""