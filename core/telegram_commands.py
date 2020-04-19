from core.constants import TOKEN_TELEGRAM, MY_CHAT_ID
import requests
import json


def send_message(text: str, chat_id) -> requests:
    '''
    Função responsável pelo envio da mensagem
    :param text: Mensagem a ser enviada
    :param chat_id: ID do chat de destino
    :return:
    '''
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(TOKEN_TELEGRAM)
    data = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=data)
    return response


def send_message_me(text: str) -> requests:
    '''
    Função responsável pelo envio de mensagem específico a um chat_id
    :param text: Mensagem a ser enviada
    :return:
    '''
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(TOKEN_TELEGRAM)
    data = {'chat_id': MY_CHAT_ID, 'text': text}
    response = requests.post(url, data=data)
    return response


def get_me() -> requests:
    '''
    Função que retorna a informações do bot no telegram
    :return:
    '''
    print('metodo getme:')
    url = 'https://api.telegram.org/bot{}/getME'.format(TOKEN_TELEGRAM)
    response = requests.get(url)
    print(response.text)
    return response


def set_webhook(url_https: str = "https://igormoreiraalves.pythonanywhere.com/event/") -> requests:
    '''
    Função para setar o endereço onde o telegram ira mandar as mensagens recebidas pelo bot
    :param url_https: Endereço para o webhook
    :return:
    '''
    print(f'metodo setwebhook')
    url = 'https://api.telegram.org/bot{}/setWebhook'.format(TOKEN_TELEGRAM)
    # data = {'url': 'https://igormoreiraalves.pythonanywhere.com/event/'}
    data = {'url': url_https}
    response = requests.post(url, data=data)
    print(response.text)
    return response


def delete_webhook() -> requests:
    '''
    Função que deleta a configuração do webhook no telegram
    :return:
    '''
    print('metodo deletewebhook')
    url = 'https://api.telegram.org/bot{}/deleteWebhook'.format(TOKEN_TELEGRAM)
    response = requests.post(url)
    print(response.text)
    return response


def get_webhook_info() -> requests:
    '''
    Função que retorna as informações do webhook
    :return:
    '''
    print('metodo getwebhookinfo')
    url = 'https://api.telegram.org/bot{}/getWebhookinfo'.format(TOKEN_TELEGRAM)
    response = requests.post(url)
    print(response.text)
    return response


def get_updates() -> requests:
    '''
    Função que retorna as atualizações do bot, deve ser usada somente se o webhook não estiver configurado
    :return: Retorna um json com as novas mensagens
    '''
    print('metodo getupdates:')
    url = 'https://api.telegram.org/bot{}/getUpdates'.format(TOKEN_TELEGRAM)
    response = requests.get(url)
    print(response.text)
    return response


def tratar_mensagem(requests_telegram) -> dict:
    '''
    Pega as informações necessarias da requisição e retorna em um dict
    :param requests_telegram: Request recebido
    :return: Retorna um dicionario {'chat_id': chat_id, 'first_name': first_name, 'mensagem': texto_mensagem}
    '''
    try:
        json_list = json.loads(requests_telegram.body)
        chat_id = json_list['message']['from']['id']
        first_name = json_list['message']['from']['first_name']
        last_name = json_list['message']['from']['last_name']
        texto_mensagem = json_list['message']['text']
    except Exception as ex:
        print(f'erro: {ex}')
    return {'chat_id': chat_id, 'first_name': first_name, 'last_name': last_name, 'mensagem': texto_mensagem}
