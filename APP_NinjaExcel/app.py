from flask import Flask, render_template, request, session, redirect, url_for, send_file
import pandas as pd
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)

DIRETORIO_UPLOADS = 'uploads'
EXTENSOES_PERMITIDAS = {'xlsx', 'xls'}

app.config['DIRETORIO_UPLOADS'] = DIRETORIO_UPLOADS
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite de 16 MB para uploads

# Certifique-se de que o direório de uploads exista
os.makedirs(DIRETORIO_UPLOADS, exist_ok=True)

# Definindo a variável global
arquivo_gerado = None

def extensoes_permitidas(arquivos):
    """Valida se as extensões dos arquivos são permitidas."""
    for arquivo in arquivos:
        if '.' not in arquivo.filename:
            return False
        extensao = arquivo.filename.rsplit('.', 1)[1].lower()
        if extensao not in EXTENSOES_PERMITIDAS:
            return False
    return True

@app.route('/', methods=['POST'])
def upload_arquivo():
    """Rota para lidar com o envio de arquivos."""
    if 'arquivos' not in request.files:
        mensagem_erro = 'Nenhum arquivo enviado.'
        return redirect(url_for('formulario_upload', erro=mensagem_erro))

    arquivos = request.files.getlist('arquivos')  # Obter a lista de arquivos enviados
  
    if not extensoes_permitidas(arquivos):
        mensagem_erro = 'Extensão inválida!'
        limpar()
        return redirect(url_for('formulario_upload', erro=mensagem_erro))

    for arquivo in arquivos:
        if arquivo.filename == '':
            mensagem_erro = 'Nenhum arquivo selecionado.'
            return redirect(url_for('formulario_upload', erro=mensagem_erro))

        nome_arquivo = arquivo.filename
        caminho_arquivo = os.path.join(app.config['DIRETORIO_UPLOADS'], nome_arquivo)
        arquivo.save(caminho_arquivo)

        arquivos_enviados = session.get('arquivos_enviados', [])
        arquivos_enviados.append(nome_arquivo)
        session['arquivos_enviados'] = arquivos_enviados      

    session['sucesso'] = "Enviado com sucesso!"
    return render_template('upload.html', arquivos_enviados=arquivos_enviados, sucesso=session['sucesso'])

@app.route('/processar')
def processar_arquivos():
    global arquivo_gerado
    """Rota para processar os arquivos enviados."""
    try:
        arquivos = os.listdir(app.config['DIRETORIO_UPLOADS'])

        dir_uploads = app.config['DIRETORIO_UPLOADS']  # Localização do diretório uploads
        arquivo_xlsx = 'planilhas.xlsx'  # nome do arquivo que será criado para gravação
        caminho_arquivo_xlsx = os.path.join(dir_uploads, arquivo_xlsx)  # Localização do arquivo

        # Criar um ExcelWriter para salvar várias planilhas em um arquivo Excel
        if arquivos:
            with pd.ExcelWriter(os.path.join(caminho_arquivo_xlsx)) as writer:

                for arquivo in arquivos:
                    caminho_arquivo = os.path.join(dir_uploads, arquivo)

                    # Verificar se o arquivo é um arquivo .xlsx
                    if arquivo.endswith('.xlsx') or arquivo.endswith('.xls'):
                        xls = pd.ExcelFile(caminho_arquivo)

                        # Iterar sobre as planilhas no arquivo .xlsx
                        for nome_planilha in xls.sheet_names:
                            tabela_enviada = pd.read_excel(xls, nome_planilha)

                            # Salvar cada planilha em uma planilha separada no arquivo Excel de saída
                            tabela_enviada.to_excel(writer, sheet_name=f'{arquivo}_{nome_planilha}', index=False)

            # Definir o caminho completo do arquivo de saída dentro do diretório de uploads
            nome_arquivo_saida = caminho_arquivo_xlsx
            arquivo_gerado = nome_arquivo_saida  # Definindo o arquivo gerado

            return redirect(url_for('formulario_upload', download_file=arquivo_gerado))

        else:
            mensagem_erro = f'Selecione os arquivos!'
            limpar()
            return redirect(url_for('formulario_upload',erro=mensagem_erro))

    except Exception as e:
        mensagem_erro = f'Erro ao processar arquivos: {str(e)}'
        limpar()
        return redirect(url_for('formulario_upload',erro=mensagem_erro))


   

def limpar():
    """Limpa a pasta de uploads e a lista de arquivos enviados."""
    for arquivo in os.listdir(app.config['DIRETORIO_UPLOADS']):
        os.remove(os.path.join(app.config['DIRETORIO_UPLOADS'], arquivo))
    session['arquivos_enviados'] = []  # Define a lista de arquivos enviados como vazia
    global arquivo_gerado
    arquivo_gerado = None

@app.route('/', methods = ['GET'])
def formulario_upload():
    global arquivo_gerado
    arquivos_enviados = session.get('arquivos_enviados')
    download_file = request.args.get('download_file')

    if download_file:
        return render_template('upload.html', sucesso="Arquivo Gerado!", arquivo_gerado=arquivo_gerado, arquivos_enviados=arquivos_enviados)
    else:
        erro = request.args.get('erro')
        return render_template('upload.html', erro=erro)

@app.route('/download')
def download_base():
    global arquivo_gerado
    if arquivo_gerado is not None:
        enviar = send_file(arquivo_gerado, as_attachment=True)
        limpar()
        return enviar
    else:
        erro = "Selecione os arquivos!"
        return render_template('upload.html', erro=erro)
    
@app.route('/restaurar')
def restaurar():
    global arquivo_gerado
    if arquivo_gerado is not None:
        limpar()
        return redirect(url_for('upload_arquivo'))
    else:
        limpar()
        return redirect(url_for('upload_arquivo'))

if __name__ == '__main__':
    app.run(debug=True)
