
<h1>Drive Monitor</h1>

<p>O projeto <strong>Drive Monitor</strong> foi desenvolvido para automatizar a tarefa de monitoramento e manipulação de arquivos de áudio armazenados no Google Drive. O programa também interage com um banco de dados MySQL para recuperar informações relevantes.</p>

<h2>Funcionalidades</h2>

<ol>
    <li><strong>Automação do Google Drive:</strong> O script simula ações humanas para navegar pelo Google Drive, buscando diretórios e arquivos específicos e obtendo links para os arquivos de áudio.</li>
    <li><strong>Manipulação de Arquivos:</strong> O programa é capaz de mover arquivos de áudio entre diretórios no sistema local.</li>
    <li><strong>Registro de Logs:</strong> Todas as ações importantes e erros são registrados em um arquivo de log para referência futura.</li>
    <li><strong>Interação com Banco de Dados:</strong> O script se conecta a um banco de dados MySQL para recuperar informações relacionadas aos arquivos de áudio.</li>
</ol>

<h2>Requisitos</h2>

<p><strong>Arquivo <code>.env</code>:</strong> O programa requer um arquivo <code>.env</code> na raiz do projeto que contém várias variáveis de ambiente usadas pelo script. Estas variáveis incluem informações de autenticação do banco de dados, caminhos de arquivo e coordenadas de tela para simulação de cliques.</p>

<h3>Exemplo de conteúdo do arquivo <code>.env</code>:</h3>

<div style="background-color: #2C2C2C; color: #A9B7C6; padding: 10px; border-radius: 5px; font-family: monospace; white-space: pre-wrap;">
  
    usuario = 'Admin'                                                          ##Nome do usuário da máquina 
    profile_ = 'Profile 1'                                                     ##Endereço do navegagor onde o drive que deseja acessar já está logado. Acesse `Chrome://version` para descobrir
    host = 'localhost'                                                         ##Nome host ou IP do banco de dados
    data_base = 'banco'                                                        ##Nome do banco de dados
    User= 'root'                                                               ##Nome do usuário de acesso ao banco de dados
    Password= 'senha'                                                          ##Senha de acesso do usuário
    Query_banco = 'select * from banco.tabela;'                                ##Query de seleção da tabela desejada
    Query_banco_id = 'SELECT coluna FROM banco.tabela2 where coluna2='         ##Parte da query para fornecer a sigla do aeroporto, de acordo com o seu id que será processada no código

    link_x = 1116                                                              ##Coordenada x do botão 'Copiar link'
    link_y = 761                                                               ##Coordenada y do botão 'Copiar link'

    concluido_x = 1459                                                         ##Coordenada x do botão 'Concluído'
    concluido_y = 761                                                          ##Coordenada y do botão 'Concluído'

    planilha = 'C:/Users/Admin/Documents/planilha_de_registros.xlsx'           ##Planilha na qual deseja registrar os links copiados
    sheet_name= 'Planilha1'                                                    ##Nome da pasta de trabalho
    origem_audio = 'C:/Users/Admin/Documents/Áudios1/'                         ##Pasta de origem do arquivo de áudio
    destino_audio = 'C:/Users/Admin/Documents/Áudios2/'                        ##Pasta de destino do arquivo de áudio, onde será feita uma cópiaa
</div>

<p><em>Nota:</em> Preencha os valores de cada variável conforme suas configurações.</p>

<h2>Como Usar</h2>

<ol>
    <li>Clone o repositório ou faça o download do código fonte.</li>
    <li>Certifique-se de ter todas as bibliotecas necessárias instaladas.</li>
    <li>Crie e configure o arquivo <code>.env</code> conforme mencionado acima.</li>
    <li>Execute o script principal para iniciar o monitoramento e a manipulação dos arquivos.</li>
</ol>


