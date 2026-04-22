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
cd "$PROJECT_ROOT"
echo -e " ${CYAN}[INFO]${NC} A trabalhar em: $PROJECT_ROOT"
echo ""

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

# Garantir que python3-venv está disponível
if ! python3 -m venv --help &>/dev/null; then
    echo " python3-venv não encontrado. A instalar..."
    sudo apt update -qq && sudo apt install -y python3-venv python3-pip
fi

# Dependências Qt6 no Linux necessárias para PySide6
echo " A verificar dependências Qt6 para Linux..."
MISSING_DEPS=()
for pkg in libxcb-xinerama0 libxcb-cursor0 libgl1; do
    if ! dpkg -l "$pkg" &>/dev/null; then
        MISSING_DEPS+=("$pkg")
    fi
done
if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo " A instalar dependências do sistema: ${MISSING_DEPS[*]}"
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

install_pkg() {
    echo -e "  - ${1} (${2})..."
    pip install "$1" --quiet
    if [ $? -ne 0 ]; then
        echo -e "  ${RED}[ERRO]${NC} Falha ao instalar $1."
        exit 1
    fi
}

install_pkg "PySide6"      "interface gráfica Qt6"
install_pkg "paramiko"     "SSH / SFTP"
install_pkg "pyqtgraph"    "gráficos de monitorização"
install_pkg "cryptography" "dependência do paramiko"
install_pkg "pyinstaller"  "empacotar app mais tarde"

# Guardar versões exatas no requirements.txt
pip freeze > requirements.txt

echo ""
echo -e " ${GREEN}[OK]${NC} Todas as dependências instaladas."
echo -e " ${GREEN}[OK]${NC} requirements.txt atualizado com versões exatas."
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