Server Select (homepage)

Lista de servidores guardados em cards (nome, IP, utilizador, status online/offline)
Botão para adicionar novo servidor (formulário com host, porta, utilizador, password ou chave SSH)
Editar e remover servidores existentes
Persistência dos servidores num ficheiro local (JSON)
Último servidor usado destacado


Dashboard

3 gauges circulares animados — CPU, RAM, Storage (tal como no protótipo)
Temperatura do Raspberry Pi
Uptime do servidor
Cards de serviços a correr (WireGuard, Samba, etc.) com status ativo/inativo
Gráfico de histórico de CPU e RAM dos últimos minutos
Atualização automática em tempo real (polling via SSH a cada X segundos)


Logs

Visualizador de logs em tempo real (journalctl, syslog, ou ficheiros custom)
Filtro por serviço ou palavra-chave
Botão para limpar a vista e para exportar os logs para ficheiro
Highlight de erros a vermelho e warnings a amarelo
Auto-scroll com opção de pausar


Devices / File Manager

Navegador de ficheiros estilo explorador (painel esquerdo: árvore de diretórios, painel direito: conteúdo)
Upload de ficheiros (arrastar e largar ou seleção)
Download de ficheiros para o PC local
Criar pastas, renomear e apagar ficheiros
Barra de caminho clicável (breadcrumb)
Indicador de progresso nas transferências


Settings

Gerir as ligações SSH guardadas (editar credenciais, trocar chave)
Intervalo de atualização do Dashboard (ex: 2s, 5s, 10s)
Tema (escuro por defeito, talvez um modo com mais contraste)
Porta SSH default
Opção para ligar automaticamente ao último servidor