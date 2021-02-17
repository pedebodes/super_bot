# pesquisar
url ='http://www.lucios.com/'
# url ='https://rolimac.com.br'
# url ='https://rolemarolamentos.com.br'
# url ='http://www.casadorolamentobh.amawebs.com'
url = 'https://www.cofermeta.com.br/'

filename = '2.txt'

# import requests
# r = requests.get(url)  
# with open(filename, 'wb') as f:
#     f.write(r.content)



#re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", part1, part2) #EmAIL
# return re.search("\d{2}.\d{3}.\d{3}/\d{4}-\d{2}", part1).group() #CNPJ
# return re.search('\(\d{2}\) \s\d{4}\-\d{4}', part1).group() TELEFONE
# return re.search('\(\d{2}\) \s\d{5}\-\d{4}', part1).group() Celular
# return re.search('\d{13}', part1).group() ZAP 
#return re.search(r"CEP: \d{5}.\d{3}", part1).group() cep
# return re.search(r"\d{5}-\d{3}", part1).group()  CEP
# Telefone: (31) 3290-2000

cnpj = "\d{2}.\d{3}.\d{3}/\d{4}-\d{2}"
email1 = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"
tel1 = '(?:\\+?(\\d{1,2}))?[-.(]*(\\d{3})?[-. )]*(\\d{4})[-. ]*(\\d{4,5})?'

# tel1 = '^(\+?[01])?[-.\s]?\(?[1-9]\d{2}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
# tel1 = '^(\+5?1\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$'



# tel1 = '\(\d{2}\)\s\d{4,5}\-\d{4}'
tel1 = '(\(?\d{2}\)?\s)?(\d{4,5}\-\d{4})'
cep = 'CEP\s*(\d{5})-(\d{3})'
 





# Tel: +55 27 3232 4242
# Fax: +55 27 3232-4214


import re
import json
def removeDuplicado(valor):
    return list(dict.fromkeys(valor))


textfile = open(filename, 'r')
filetext = textfile.read()
textfile.close()
CEP = removeDuplicado(re.findall(cep, filetext))
CNPJ = removeDuplicado(re.findall(cnpj, filetext))
TEL1 = removeDuplicado(re.findall(tel1, filetext))
# TEL2 = removeDuplicado(re.findall(tel2, filetext))
Email1 = removeDuplicado(re.findall(email1, filetext))

# print(CEP)
# print(CNPJ) #OK
# print(TEL1) #OK
# # print(TEL2) #OK
# print(Email1) #OK

print(type(TEL1)) 
print(TEL1) 



def removeDuplicado(valor):
    return list(dict.fromkeys(valor))

def regex(opcao,arquivo):
    tipoRegex={
        'email':r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+',
        'cep': 'CEP\s*(\d{5})-(\d{3})',
        'cnpj': '\d{2}.\d{3}.\d{3}/\d{4}-\d{2}',
        'telefone': '\(\d{2}\)\s\d{4,5}\-\d{4}',
        'telefoneAPI': '\d{13}'
        }
    
    return json.dumps(removeDuplicado(re.findall(tipoRegex.get(opcao), filetext)))
    
    import pdb; pdb.set_trace()
    return tipoRegex.get(
        opcao
        ,"Opcao invalida")
# print (regex('email',filetext))

# import pdb; pdb.set_trace()




# OU Linha a linha
# textfile = open(filename, 'r')
# matches2 = []
# reg = re.compile("\d{2}.\d{3}.\d{3}/\d{4}-\d{2}")
# for line in textfile:
#     matches2 += reg.findall(line)
# textfile.close()
# print(matches2)