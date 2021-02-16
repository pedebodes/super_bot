filename = '1.txt'

#re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", part1, part2) #EmAIL
# return re.search("\d{2}.\d{3}.\d{3}/\d{4}-\d{2}", part1).group() #CNPJ
# return re.search('\(\d{2}\) \s\d{4}\-\d{4}', part1).group() TELEFONE
# return re.search('\(\d{2}\) \s\d{5}\-\d{4}', part1).group() Celular
# return re.search('\d{13}', part1).group() ZAP 
#return re.search(r"CEP: \d{5}.\d{3}", part1).group() cep
# return re.search(r"\d{5}-\d{3}", part1).group()  CEP


import re

textfile = open(filename, 'r')
filetext = textfile.read()
textfile.close()
matches = re.findall("\d{2}.\d{3}.\d{3}/\d{4}-\d{2}", filetext)
print(matches)


# OU
textfile = open(filename, 'r')
matches2 = []
reg = re.compile("\d{2}.\d{3}.\d{3}/\d{4}-\d{2}")
for line in textfile:
    matches2 += reg.findall(line)
textfile.close()
print(matches2)