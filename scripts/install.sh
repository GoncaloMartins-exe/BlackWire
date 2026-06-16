#!/bin/bash

set -e

APP_NAME="BlackWire"
INSTALL_DIR="$HOME/.local/share/$APP_NAME"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Installing $APP_NAME..."

# Criar pastas
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$DESKTOP_DIR"
mkdir -p "$ICON_DIR"

# Copiar app
cp -r "$PROJECT_DIR/dist" "$INSTALL_DIR/"
cp -r "$PROJECT_DIR/assets" "$INSTALL_DIR/"

# Criar executável global
cp "$INSTALL_DIR/dist/BlackWire" "$BIN_DIR/blackwire"
chmod +x "$BIN_DIR/blackwire"

# Ícone do sistema
cp "$PROJECT_DIR/assets/icons/LogoBlackWire.png" "$ICON_DIR/blackwire.png"

# Desktop entry
cat > "$DESKTOP_DIR/blackwire.desktop" << EOF
[Desktop Entry]
Name=BlackWire
Exec=blackwire
Icon=blackwire
Type=Application
Terminal=false
Categories=Utility;
StartupNotify=true
EOF

# Atualizar cache
update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
gtk-update-icon-cache "$ICON_DIR" 2>/dev/null || true

echo "Installation complete!"
echo "You can now search for BlackWire in your applications."