global list_commands, list_responses
list_commands = ['/help', '/list_projects', '/list_skills']
list_responses = {
    '/help': 'BOTINHO \n\n Esse bot serve para você conhecer alguns dos meus trabalhos, e experiências. \n'
             ' Pergunte algo sobre: experiências profissionais ou projetos pessoais!',
    '/list_projects': 'Lista de PROJETOS: \n Botinho, Class_system, Sincronizador',
    '/list_skills': 'Lista de SKILLS: \n java, python,'
    }


def is_command(mensagem: str) -> dict:
    '''
    Verifica se a mensagem recebida é um comando, Caso seja é retornado uma lista como resposta a mensagem
    :param mensagem: Mensagem recebida da origem
    :return: Retorna um objeto dict {command: bool, message: "mensagem"}
    '''
    mensagem_is = False
    resposta = ''
    for i in list_commands:
        if i == mensagem:
            mensagem_is = True

    if mensagem_is:
        resposta = define_response(mensagem)

    return {'command': mensagem_is, 'message': resposta}


def define_response(command: str) -> str:
    '''
    Retorna a mensagem referente ao comando
    :param command: Comando que veio da origem
    :return: Retorna a mensagem a ser enviado a origem
    '''
    resposta = list_responses[command]
    return resposta
