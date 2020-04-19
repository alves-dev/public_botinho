import datetime


class Conversa:
    def __init__(self, session_id: str, chat_id: str, first_name: str, origem: str, intencoes: list = []):
        self.session_id = session_id
        self.chat_id = chat_id
        self.first_name = first_name
        self.origem = origem
        self.intencoes = intencoes
        self.datetime = datetime_atual()


def datetime_atual() -> float:
    '''
    Função pega a data e hora no formato de timestamp
    :return: Retorna o timestamp atual
    '''
    data_hora = datetime.datetime.now().timestamp()
    return data_hora


def calcular_tempo(hora_ini: float) -> bool:
    '''
    Função calcula a diferença de tempo entre o inicio da sessão até o momento atual
    :param hora_ini: Data e hora que esta no objeto conversa
    :return: Retorna True caso diferença do tempo seja maior que 5 minutos, que é o tempo limite para a inatividade de
    uma sessão no Watson
    '''
    diferenca = (datetime_atual() - hora_ini) / 60
    if diferenca > 5:
        return True
    else:
        return False


def verificar_sessoes_ativas(conversas: list, chat_id: str) -> list:
    '''
    Função faz a validação das sessões, caso tenha mais de 5 minutos da ultima mensagem a sessão é apagada da lista,
     e é criada uma nova sessão para o Watson, caso não tenha mais de 5 minutos, a sessão é apenas atualizada.
    :param conversas: Uma lista das sessões
    :param chat_id: ID da conversa para atualização da sessão.
    :return: Uma lista de conversa, atualiza!
    '''
    conversas_verificadas: Conversa = []
    deletado = False
    for i in conversas:
        if calcular_tempo(i.datetime):
            print('DELETAR SESSAO')
            deletado = True

        if not deletado:
            if str(chat_id) == str(i.chat_id):
                print('atualizado')
                con = Conversa(i.session_id, i.chat_id, i.first_name, i.origem, i.intencoes)
                conversas_verificadas.append(con)
            else:
                print('igual')
                conversas_verificadas.append(i)
        deletado = False

    print(f'fim  {conversas_verificadas}')
    for i in conversas_verificadas:
        diferenca = (datetime_atual() - i.datetime) / 60
        print(f'{i.session_id}  tempo: {diferenca}  int:{int(diferenca)}')

    return conversas_verificadas
