import re
import json
def removeDuplicado(valor):
    return list(dict.fromkeys(valor))

# pesquisar
url ='http://www.lucios.com/'
url ='https://rolimac.com.br'
# url ='https://rolemarolamentos.com.br'
url ='https://rolemarolamentos.com.br/contato/'
# url = 'https://www.cofermeta.com.br/'
# url = 'http://www.cldrolamentos.com.br/'
url= 'https://www.irsa.com.br/'

url = 'https://www.oliveirarolamentos.com.br/'

# https://rolimac.com.br/ # tem zap https://api.whatsapp.com/send?phone=5531984199002&amp;text=Ol%C3%A1!%20Vim%20através%20do%20site
filename = '4.txt'

# import requests
# r = requests.get(url)  
# with open(filename, 'wb') as f:
#     f.write(r.content)

textfile = open(filename, 'r')
filetext = textfile.read()
textfile.close()

def removeDuplicado(valor):
    return list(dict.fromkeys(valor))

def regex(opcao,arquivo):
    # tipoRegex={
    #     'email':r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+',
    #     'cep': 'CEP\s*(\d{5})-(\d{3})',
    #     'cnpj': '\d{2}.\d{3}.\d{3}/\d{4}-\d{2}',
    #     'telefone': '\(\d{2}\)\s\d{4,5}\-\d{4}',
    #     'telefoneAPI': r"\+?[\d]{2}\s*[\d]{2}\s*[\d]{4,5}\s*[\d]{4}",
    #     'telefoneAPIw': r'\=?[\d]{13}'
    #     }
    
    tipoRegex={
        'email':re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+'),
        'cep': re.compile(r'\s+(\d{5})[- ](\d{3})\s*'),
        'cnpj': re.compile(r'\d{2}.\d{3}.\d{3}/\d{4}-\d{2}'),
        'telefone': re.compile(r'\+?5?5?[\-\.\s]*\(?(\d{2})\)?\s+(\d{4,5})[-. ]?(\d{4})'),
        'telefoneAPI': re.compile(r'\=+[\d]{13}\&+')
        }
    
    return re.findall(tipoRegex.get(opcao), filetext)
    return json.dumps({'results': removeDuplicado(re.findall(tipoRegex.get(opcao), filetext))})


    return json.dumps(removeDuplicado(re.findall(tipoRegex.get(opcao), filetext)))

x= regex('email',filetext)
# print(type(x))
# print(x)

# import pdb; pdb.set_trace()

# print(regex('email',filetext))
# r = re.compile(regex)
# x = (re.findall(r,filetext))

x = regex('telefone',filetext)

for i in x:
    print(i)
    import pdb; pdb.set_trace()

import pdb; pdb.set_trace()
# print ("Email " + regex('email',filetext))
print ("cep " +regex('cep',filetext))
print ("cnpj " +regex('cnpj',filetext))
print ("telefone " +regex('telefone',filetext))
print ("telefoneAPI " +regex('telefoneAPI',filetext))
# print ("telefoneAPIw " + regex('telefoneAPIw',filetext))

import pdb; pdb.set_trace()
def validaTelefoneDDD(valor):
    for x in valor:
        x = [x for x in list(valor) if x != ' ']
        ddd =[11,12,13,14,15,16,17,18,19,21,22,24,27,28,31,32,33,34,35,37,38,41,42,43,44,45,46,47,48,49,51,53,54,55,61,62,63,64,65,66,67,68,69,71,73,74,75,77,79,81,82,83,84,85,86,87,88,89,91,92,93,94,95,96,97,98,99]
        # import pdb; pdb.set_trace()
        ret = []
        if int(x[0]) in ddd:
            ret.append(x)
    
    return ret




# regex =r"\+?[\d]{2}\s*[\d]{2}\s*[\d]{4,5}\s*[\d]{4}"
# regex = r'\+[\d]{2}\D*[\d]{2}\D*[\d]{4,5}\D*[\d]{4}'
# regex =r'\=?[\d]{13}'
# regex = r'\+?5?5?\W*(\d{2})\W*(\d{4,5})\W*(\d{4})'
# regex = r'\(\d{2}\)\s\d{4,5}\-\d{4}'
# regex = r"\+?[\d]{2}\s*[\d]{2}\s*[\d]{4,5}\s*[\d]{4}"
# regex = r'\+?5?5?\d*(\d{2})\W*(\d{4,5})\W*(\d{4})\D'
# regex = r'\+?5?5?\d*(\d{2})\W*(\d{4,5})\W*(\d{4})'
# regex = r'\+?5?5?[\-\.\s]*\(?(\d{2})\)?[\-\.\s]+(\d{4,5})[-. ]?(\d{4})'
# regex = r'\+?5?5?[\-\.\s]*\(?(\d{2})\)?\s+(\d{4,5})[-. ]?(\d{4})'  #FUNCIONANDO

# regex = r'\=+[\d]{13}\&+' # web zap
# regex = r"\=+\+?[\d]{2}\s*[\d]{2}\s*[\d]{4,5}\s*[\d]{4}\&+"

# CEP
# regex = 'CEP\s*(\d{5})-(\d{3})'
# regex = r'\s+(\d{5})[- ](\d{3})\s*'



# 3  CEP: 30710-040
# 2  CEP 32010-040


regex = r'\d{2}.\d{3}.\d{3}/\d{4}-\d{2}'


# print (json.dumps(removeDuplicado(re.findall(regex, filetext))))

r = re.compile(regex)
x = (re.findall(r,filetext))
# +55 (16) 3979.7009
# print(x)
# for i in x:
#     print(validaTelefoneDDD(i))
