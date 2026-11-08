# BREAK EXECUTOR 2.0 — projeto pronto para gerar EXE Windows x64

Editor e biblioteca local de scripts Lua com interface Tkinter. A interface foi refinada sem alterar a proposta do aplicativo.

## Novidades da versão 2.0

- Cabeçalho com versão e status LOCAL.
- Atalhos `Ctrl+S`, `Ctrl+N` e `Ctrl+O`.
- Contador de linha, coluna, caracteres e linhas no editor.
- Preservação do rascunho ao trocar de seção.
- Busca instantânea na biblioteca de scripts.
- Duplo clique para abrir um script no editor.
- Mensagens de estado mais claras para novo, aberto e salvo.
- Tratamento de configurações corrompidas e erros de arquivos.
- Animação RGB corrigida ao sair da tela principal.
- Build configurado sem console e sem exigir Python no computador de destino.

## O que foi configurado para o EXE

O workflow `.github/workflows/build-windows.yml` gera um executável Windows x64 real com:

- runner `windows-latest`;
- Python 3.12 x64;
- PyInstaller em modo `--onefile`;
- modo `--windowed`, sem janela de terminal;
- validação da sintaxe antes do build;
- verificação de que `dist/BREAK_EXECUTOR.exe` foi criado;
- upload do artefato `BREAK_EXECUTOR-Windows-x64`.

O computador de destino não precisa ter Python, Tkinter ou PyInstaller instalados.

## Como obter o EXE pelo navegador

1. Crie um repositório no GitHub, preferencialmente privado.
2. Envie estes arquivos mantendo a estrutura de pastas:
   - `break_executor.py`
   - `README.md`
   - `build-windows.cmd`
   - `.github/workflows/build-windows.yml`
3. Abra a aba **Actions**.
4. Selecione **Build BREAK EXECUTOR for Windows x64**.
5. Clique em **Run workflow** e confirme em **Run workflow** novamente.
6. Aguarde o job terminar com status verde **Success**.
7. Abra a execução concluída.
8. Na seção **Artifacts**, baixe `BREAK_EXECUTOR-Windows-x64`.
9. Extraia o ZIP baixado.
10. Dê dois cliques em `BREAK_EXECUTOR.exe`.

O arquivo dentro do artefato é o aplicativo final. Não é necessário abrir `break_executor.py`, `README.md` ou `build-windows.cmd` no computador de destino.

## Login inicial

Usuário: `admin`  
Senha: `1234`

Altere as credenciais em **Configurações** após entrar.

## Build local opcional

O arquivo `build-windows.cmd` também pode ser usado em um Windows 64 bits com Python instalado. Isso não é necessário quando o workflow do GitHub Actions é utilizado.

## Limites

O programa é um editor e organizador local. Ele não injeta código no Roblox, não burla anti-cheat e não concede permissões administrativas em jogos de terceiros. Integrações em experiências próprias devem ser implementadas com validação no servidor.
