# BlackWire

**BlackWire** é uma ferramenta que visa simplificar e modernizar a interação com dispositivos remotos através de `SSH`, combinando a robustez do terminal com uma interface gráfica intuitiva.

O projeto foca-se em tornar operações comuns como a `transferência de ficheiros`, `execução de comandos remotos` e `visualização de dados`. Operações que serão mais rápidas, organizadas e acessíveis, reduzindo a dependência de comandos repetitivos e configurações manuais.

Pensado para ambientes técnicos e educacionais, o BlackWire permite ao utilizador manter o controlo e a transparência do SSH, enquanto beneficia de uma experiência visual clara e eficiente. **O objetivo não é esconder o terminal, mas sim descomplicá-lo**.

## Como Compilar e Correr (Windows + MinGW)

Este projeto usa **Qt 6.10.1** e **CMake**.

### Pré-requisitos
1. **Qt 6.10.1** instalado (componente MinGW 64-bit).
2. **CMake** instalado e acessível no terminal.
3. **MinGW (g++)** instalado.

### Passo a Passo

1. **Limpar builds anteriores (em caso de erro):**
   ```powershell
   Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue

2. **Configurar o Projeto (Gerar Makefiles):** É necessário indicar onde está a instalação do Qt.
    ```powershell
    cmake -S . -B build -G "MinGW Makefiles" -DCMAKE_PREFIX_PATH="C:\Qt\6.10.1\mingw_64"

3. **Compilar:**
    ```powershell
    cmake --build build

4. **Corrigir dependências (DLLs) - Apenas na primeira vez:** O Windows precisa das DLLs do Qt junto ao executável utilizando o windeployqt:
    ```powershell
    C:\Qt\6.10.1\mingw_64\bin\windeployqt.exe build\BlackWire.exe

5. **Executar:**
    ```powershell
    .\build\BlackWire.exe


## Desenvolvimento Diário (Workflow)

Depois de ter o ambiente configurado pela primeira vez só é necessário correr os seguintes comandos:

1. **Recompilar:**
   ```powershell
   cmake --build build

2. **Executar**
    ```powershell
    .\build\BlackWire.exe