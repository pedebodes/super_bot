import re
import json

def removeDuplicado(valor):
    return list(dict.fromkeys(valor))
    
def regex(opcao,arquivo):
    tipoRegex={
        'email':r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+',
        'cep': 'CEP\s*(\d{5})-(\d{3})',
        'cnpj': '\d{2}.\d{3}.\d{3}/\d{4}-\d{2}',
        'telefone': '(\(?\d{2}\)?\s)?(\d{4,5}\-\d{4})',
        'telefoneAPI': '\d{13}'
        }
    return json.dumps(
        removeDuplicado(
            re.findall(
                tipoRegex.get(opcao), arquivo
                )
            )
        )
    
