import json
import sys
import urllib.request


def usage():
    print('Este script busca informações online sobre números de CNPJ')
    print('Modo de uso: {0} "CNPJ[1]" "CNPJ[2]" ... "CNPJ[N]"'.format(sys.argv[0]))
    sys.exit(1)


def valida_cnpj(cnpj):
    'Recebe um CNPJ e retorna True se formato válido ou False se inválido'

    cnpj = parse_input(cnpj)
    if len(cnpj) != 14 or not cnpj.isnumeric():
        return False

    verificadores = cnpj[-2:]
    lista_validacao_um = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    lista_validacao_dois = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    'Calcular o primeiro digito verificador'
    soma = 0
    for numero, ind in zip(cnpj[:-1], range(len(cnpj[:-2]))):
        soma += int(numero) * int(lista_validacao_um[ind])

    soma = soma % 11
    digito_um = 0 if soma < 2 else 11 - soma

    'Calcular o segundo digito verificador'
    soma = 0
    for numero, ind in zip(cnpj[:-1], range(len(cnpj[:-1]))):
        soma += int(numero) * int(lista_validacao_dois[ind])

    soma = soma % 11
    digito_dois = 0 if soma < 2 else 11 - soma

    return verificadores == str(digito_um) + str(digito_dois)


def parse_input(i):
    'Retira caracteres de separação do CNPJ'

    i = str(i)
    i = i.replace('.', '')
    i = i.replace(',', '')
    i = i.replace('/', '')
    i = i.replace('-', '')
    i = i.replace('\\', '')
    return i


def busca_cnpj(cnpj):
    url = 'http://receitaws.com.br/v1/cnpj/{0}'.format(cnpj)
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-agent',
         " Mozilla/5.0 (Windows NT 6.2; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0")]

    with opener.open(url) as fd:
        content = fd.read().decode()

    dic = json.loads(content)

    if dic['status'] == "ERROR":
        print('CNPJ {0} rejeitado pela receita federal\n\n'.format(cnpj))
    else:
        try:
            return dic
            # print('Nome: {0}'.format(dic['nome']))
            # print('Nome fantasia: {0}'.format(dic['fantasia']))
            # print('CNPJ: {0}   Data de abertura: {1}'.format(dic['cnpj'], dic['abertura']))
            # print('Natureza: {0}'.format(dic['natureza_juridica']))
            # print('Situação: {0}  Situação especial: {1}  Tipo: {2}'.format(dic['situacao'],
            #                                                                 dic['situacao_especial'],
            #                                                                 dic['tipo']))
            # print('Motivo Situação especial: {0}'.format(dic['motivo_situacao']))
            # print('Data da situação: {0}'.format(dic['data_situacao']))
            # print('Atividade principal:')
            # print(' '*10 + '{0} - {1}'.format(dic['atividade_principal'][0]['code'],
            #                                   dic['atividade_principal'][0]['text']))
            # print('Atividades secundárias:')
            # for elem in dic['atividades_secundarias']:
            #     print(' '*10 + '{0} - {1}'.format(elem['code'], elem['text']))

            # print('Endereço:')
            # print(' '*10 + '{0}, {1}'.format(dic['logradouro'],
            #                                  dic['numero']))
            # print(' '*10 + '{0}'.format(dic['complemento']))
            # print(' '*10 + '{0}, {1}'.format(dic['municipio'],
            #                                  dic['uf']))
            # print('Telefone: {0}'.format(dic['telefone']))
            # print('Email: {0}\n\n'.format(dic['email']))
        except KeyError:
            pass



def consulta(cnpj):
    return busca_cnpj(parse_input(cnpj))




# print(consulta('29.302.348/0001-15'))
# import pdb; pdb.set_trace()
# if __name__ == '__main__':
#     if len(sys.argv) == 1 or sys.argv[1] in {'-h', '--help'}:
#         usage()

#     for arg in sys.argv[1:]:
#         if not valida_cnpj(arg):
#             print('CNPJ "{0}" tem formato inválido'.format(arg))
#         else:
#             busca_cnpj(parse_input(arg))