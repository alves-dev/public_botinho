from core.constants import MY_CHAT_ID
import core.telegram_commands as telegram
import core.watson_commands as watson
import core.lista_comandos_bot as commands
import core.conversa as conversa

# linhas abaixo para tirar a validação do ssl
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

assistant = watson.new_assistente_watson()

global intencoes, conversas
intencoes = []
conversas = []


def trata_conversa(requests):
    try:
        info_msg = telegram.tratar_mensagem(requests)
        chat_id = info_msg['chat_id']
        texto_mensagem = info_msg['mensagem']
        first_name = info_msg['first_name']
        last_name = info_msg['last_name']
        retorno_comandos = commands.is_command(texto_mensagem)

        session_id = controlar_sessoes(chat_id, first_name, origem='telegram')

        if retorno_comandos['command']:
            resposta_watson = retorno_comandos['message']
        else:
            resposta_watson = process_message_watson(texto_mensagem, session_id)
        telegram.send_message(resposta_watson, chat_id)

        if str(chat_id) != MY_CHAT_ID:
            telegram.send_message_me(f'{first_name} {last_name}: {texto_mensagem} \nResposta: {resposta_watson}')
    except Exception as ex:
        print(f'erro: {ex}')


def process_message_watson(text: str, session_id: str):
    global intencoes

    msg = watson.criar_mensagem(text, intencoes)

    my_detailed_response = watson.send_menssage(assistant, session_id, msg)

    retorno = watson.tratar_resposta(my_detailed_response)

    intencoes = retorno['intencoes']

    return retorno['resposta']


def controlar_sessoes(chat_id: str, first_name: str, origem: str) -> str:
    global conversas
    conversas = conversa.verificar_sessoes_ativas(conversas, chat_id)
    session_id = ''
    for i in conversas:
        if str(chat_id) == str(i.chat_id):
            session_id = i.session_id

    if session_id == '':
        print('nova sessao')
        session_id = watson.new_session(assistant)
        con = conversa.Conversa(session_id, chat_id, first_name, origem)
        conversas.append(con)

    return session_id
