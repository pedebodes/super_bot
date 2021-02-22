import re
import json
def removeDuplicado(valor):
    return list(dict.fromkeys(valor))

# pesquisar
url ='http://www.lucios.com/'
# url ='https://rolimac.com.br'
# url ='https://rolemarolamentos.com.br'
# url ='http://www.casadorolamentobh.amawebs.com'
# url = 'https://www.cofermeta.com.br/'
url = 'http://www.cldrolamentos.com.br/'



# https://rolimac.com.br/ # tem zap https://api.whatsapp.com/send?phone=5531984199002&amp;text=Ol%C3%A1!%20Vim%20através%20do%20site
filename = '1.txt'

import requests
r = requests.get(url)  
with open(filename, 'wb') as f:
    f.write(r.content)



#re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", part1, part2) #EmAIL
# return re.search("\d{2}.\d{3}.\d{3}/\d{4}-\d{2}", part1).group() #CNPJ
# return re.search('\(\d{2}\) \s\d{4}\-\d{4}', part1).group() TELEFONE
# return re.search('\(\d{2}\) \s\d{5}\-\d{4}', part1).group() Celular
# return re.search('\d{13}', part1).group() ZAP 
#return re.search(r"CEP: \d{5}.\d{3}", part1).group() cep
# return re.search(r"\d{5}-\d{3}", part1).group()  CEP
# Telefone: (31) 3290-2000

# cnpj = "\d{2}.\d{3}.\d{3}/\d{4}-\d{2}"
# email1 = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"
# tel1 = '(?:\\+?(\\d{1,2}))?[-.(]*(\\d{3})?[-. )]*(\\d{4})[-. ]*(\\d{4,5})?'

# # tel1 = '^(\+?[01])?[-.\s]?\(?[1-9]\d{2}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
# # tel1 = '^(\+5?1\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$'



# # tel1 = '\(\d{2}\)\s\d{4,5}\-\d{4}'
# tel1 = '(\(?\d{2}\)?\s)?(\d{4,5}\-\d{4})'
# cep = 'CEP\s*(\d{5})-(\d{3})'
 





# Tel: +55 27 3232 4242
# Fax: +55 27 3232-4214




textfile = open(filename, 'r')
filetext = textfile.read()
textfile.close()

# CEP = removeDuplicado(re.findall(cep, filetext))
# CNPJ = removeDuplicado(re.findall(cnpj, filetext))
# TEL1 = removeDuplicado(re.findall(tel1, filetext))
# # TEL2 = removeDuplicado(re.findall(tel2, filetext))
# Email1 = removeDuplicado(re.findall(email1, filetext))

# print(CEP)
# print(CNPJ) #OK
# print(TEL1) #OK
# # print(TEL2) #OK
# print(Email1) #OK

# print(type(TEL1)) 
# print(TEL1) 



def removeDuplicado(valor):
    return list(dict.fromkeys(valor))

def regex(opcao,arquivo):
    tipoRegex={
        'email':r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+',
        'cep': 'CEP\s*(\d{5})-(\d{3})',
        'cnpj': '\d{2}.\d{3}.\d{3}/\d{4}-\d{2}',
        'telefone': '\(\d{2}\)\s\d{4,5}\-\d{4}',
        'telefoneAPI': r"\+?[\d]{2}\s*[\d]{2}\s*[\d]{4,5}\s*[\d]{4}",
        'telefoneAPIw': r'\=?[\d]{13}'
        }
    
    return json.dumps(removeDuplicado(re.findall(tipoRegex.get(opcao), filetext)))
    

print (regex('email',filetext))
print (regex('cep',filetext))
print (regex('cnpj',filetext))
print (regex('telefone',filetext))
print (regex('telefoneAPI',filetext))
print (regex('telefoneAPIw',filetext))

# import pdb; pdb.set_trace()

# regex ='(\d{2})\D*(\d{4,5})\D*(\d{4})'

regex =r"\+?[\d]{2}\s*[\d]{2}\s*[\d]{4,5}\s*[\d]{4}"
regex = r'\+[\d]{2}\D*[\d]{2}\D*[\d]{4,5}\D*[\d]{4}'
regex = r'\=?[\d]{13}'
r'\+?5?5?\W*(\d{2})\W*(\d{4,5})\W*(\d{4})'
print (json.dumps(removeDuplicado(re.findall(regex, filetext))))

import pdb; pdb.set_trace()
# phonePattern = re.compile(r'^(\d{3})-(\d{3})-(\d{4})-(\d+)$') 
# phonePattern.search('800-555-1212-1234').groups() 
#  https://api.whatsapp.com/send?phone=5531984199002&amp;text=Ol%C3%A1!%20Vim%20através%20do%20site
# +000-000-000
# +55 (31) 2105.9900    +55 (34) 3233.9700   +55 (16) 3979.7009
# ["(31) 3290-2000", "(31) 3392-7666", "(31) 3595-5757", "(31) 3829-6944"]
# OU Linha a linha
# textfile = open(filename, 'r')
# matches2 = []
# reg = re.compile("\d{2}.\d{3}.\d{3}/\d{4}-\d{2}")
# for line in textfile:
#     matches2 += reg.findall(line)
# textfile.close()
# print(matches2)