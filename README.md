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
| PySide6 | 6.11.0 | Interface gráfica (Qt6) |
| PySide6_Addons | 6.11.0 | Módulos adicionais do Qt6 |
| PySide6_Essentials | 6.11.0 | Componentes essenciais do Qt6 |
| shiboken6 | 6.11.0 | Binding generator utilizado pelo PySide6 |
| pyqtgraph | 0.14.0 | Gráficos de monitorização |
| numpy | 2.4.4 | Processamento numérico e arrays |
| keyring | 25.2.1 | Armazenamento seguro de credenciais |
| platformdirs | 4.2.2 | Gestão de diretórios específicos da plataforma |
| paramiko | 4.0.0 | Ligação SSH / SFTP |
| cryptography | 46.0.7 | Criptografia utilizada pelo Paramiko |
| bcrypt | 5.0.0 | Hashing de passwords |
| PyNaCl | 1.6.2 | Funções criptográficas adicionais |
| cffi | 2.0.0 | Interface C para bibliotecas Python |
| pycparser | 3.0 | Parser C utilizado pelo cffi |
| pyinstaller | 6.19.0 | Empacotamento em executável |
| pyinstaller-hooks-contrib | 2026.4 | Hooks adicionais para PyInstaller |
| altgraph | 0.17.5 | Análise de dependências para empacotamento |
| packaging | 26.1 | Gestão e parsing de versões/pacotes |
| colorama | 0.4.6 | Cores no terminal multiplataforma |
| invoke | 3.0.3 | Automatização de tarefas e scripts |
| pefile | 2024.8.26 | Manipulação de executáveis PE (Windows) |
| pywin32-ctypes | 0.2.3 | Integração Win32 para Python (Windows) |
| setuptools | 82.0.1 | Ferramentas de build/distribuição (Linux) |
| SecretStorage | 3.3.3 | Acesso ao armazenamento seguro no Linux |
| jeepney | 0.8.0 | Comunicação D-Bus utilizada pelo SecretStorage |
 
As versões exatas encontram-se no ficheiro `requirements.txt`.
