from core.constants import WATSON_API_KEY, WATSON_VERSION, WATSON_URL, WATSON_Assistant_ID

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.assistant_v2 import *


def new_assistente_watson():
    cliente_assistente = assistant()
    desable_ssl(cliente_assistente)
    return cliente_assistente


def authenticator() -> IAMAuthenticator:
    '''
    Função que utiliza a constante API_KEY para realizar a autenticação na API do Watson
    :return: Retorna um objeto de autenticação
    '''
    autenticado = IAMAuthenticator(WATSON_API_KEY)
    return autenticado


def assistant() -> AssistantV2:
    '''
    Função cria um novo cliente ao serviço de assistente, utiliza a constante WATSON_VERSION para definir data da api
    caso ela mude no futuro a ibm saiba sobre qual documentação ela deve prosseguir.
    Também faz set_service_url passando a constante WATSON_URL, representa o servidor da IBM onde esta hospedado o
    seu assistente.
    :return: Novo cliente do assistente
    '''
    cliente = AssistantV2(
        version=WATSON_VERSION,
        authenticator=authenticator()
    )
    cliente.set_service_url(WATSON_URL)
    return cliente


def desable_ssl(cliente: AssistantV2):
    '''
    Função desativa a verificação SSL, não recomendado!
    :param cliente: Cliente assistente a qual a verificação SSL vai ser desativado.
    '''
    cliente.set_disable_ssl_verification(True)


def new_session(cliente: AssistantV2) -> str:
    '''
    Cria uma nova sessão com o assistente
    :param cliente: Cliente já autenticado
    :return: Retorna o ID da sessão
    '''
    response = cliente.create_session(WATSON_Assistant_ID).get_result()
    session_id = response['session_id']
    return session_id


def delete_session(cliente: AssistantV2, session_id: str):
    '''
    Função deleta uma sessão com o assistente
    :param cliente: Assistente a qual a sessão esta vinculada
    :param session_id: ID da sessão
    '''
    cliente.delete_session(WATSON_Assistant_ID, session_id)


def send_menssage(cliente: AssistantV2, session_id: str, msg: MessageInput) -> DetailedResponse:
    '''
    Envia a mensagem para o assistente watson
    :param cliente: Objeto do tipo AssistantV2
    :param session_id: ID da sessão a ser enviada a mensagem
    :param msg: Objeto do tipo MessageInput
    :return: Retorna um objeto contendo as informações da resposta
    '''
    my_detailed_response = cliente.message(WATSON_Assistant_ID, session_id, input=msg)
    return my_detailed_response


def tratar_resposta(resposta: DetailedResponse) -> dict:
    '''
    Função trata o retorno, coletando apenas a resposta e as intenções
    :param resposta:
    :return:
    '''
    # parte responsável por pegar a resposta
    valores = resposta.get_result()
    valores = valores['output']
    valores = valores['generic']
    retorno = ''
    i = 0
    for val in valores:
        if i > 0:
            retorno = retorno + '\n'
        retorno = retorno + val['text']
        i = i + 1

    # parte responsável por pegar as intenções da mensagem de envio
    valores = resposta.get_result()
    valores = valores['output']
    valores = valores['intents']
    intencoes = []
    for val in valores:
        ri = RuntimeIntent(val['intent'], val['confidence'])
        intencoes.append(ri)

    return {'resposta': retorno, 'intencoes': intencoes}


def criar_mensagem(text: str, intencoes: List[RuntimeIntent]) -> MessageInput:
    '''
    Cria o objeto msg do tipo MessageInput
    :param text: Texto da mensagem
    :param intencoes: Intenções anteriores
    :return: MessageInput
    '''

    if len(intencoes) > 0:
        msg = MessageInput(text=text, intents=intencoes)
    else:
        msg = MessageInput(text=text)
        print('sem intencao')
    msg = MessageInput(text=text)
    return msg
