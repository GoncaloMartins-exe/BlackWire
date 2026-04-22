# BlackWire

**BlackWire** é uma ferramenta que visa simplificar e modernizar a interação com dispositivos remotos através de `SSH`, combinando a robustez do terminal com uma interface gráfica intuitiva.

O projeto foca-se em tornar operações comuns como a `transferência de ficheiros`, `execução de comandos remotos` e `visualização de dados`. Operações que serão mais rápidas, organizadas e acessíveis, reduzindo a dependência de comandos repetitivos e configurações manuais.

Pensado para ambientes técnicos e educacionais, o BlackWire permite ao utilizador manter o controlo e a transparência do SSH, enquanto beneficia de uma experiência visual clara e eficiente. **O objetivo não é esconder o terminal, mas sim descomplicá-lo**.

## Pré-requisitos
 
- **Python 3.12+**

## Como Configurar o Ambiente
 
O projeto inclui scripts de setup que instalam todas as dependências automaticamente.
 
### Windows
 
```powershell
scripts\setup_windows.bat
```
 
### Linux
 
```bash
chmod +x scripts/setup_linux.sh
./scripts/setup.sh
```
 
Os scripts tratam de:
- Criar e ativar o ambiente virtual (`venv`)
- Instalar todas as dependências Python
- Atualizar o `requirements.txt` com as versões exatas instaladas

## Como Correr
 
Após o setup, ativa o ambiente virtual e corre a aplicação:
 
### Windows
 
```powershell
venv\Scripts\activate
python main.py
```
 
### Linux
 
```bash
source venv/bin/activate
python main.py
```
 
## Desenvolvimento Diário (Workflow)
 
Depois de ter o ambiente configurado pela primeira vez, só é necessário:
 
```powershell
# Windows
venv\Scripts\activate
python main.py
```
 
```bash
# Ubuntu
source venv/bin/activate
python main.py
```
 
## Dependências
 
| Pacote | Versão | Utilização |
|---|---|---|
| PySide6 | 6.x | Interface gráfica (Qt6) |
| paramiko | 3.x | Ligação SSH / SFTP |
| pyqtgraph | 0.13.x | Gráficos de monitorização |
| cryptography | latest | Dependência do paramiko |
| pyinstaller | 6.x | Empacotamento em executável |
 
As versões exatas encontram-se no ficheiro `requirements.txt`.