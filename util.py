import re

def getEmail(part1, part2):
    try:
        return list(
            dict.fromkeys(
                re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", part1, part2)
                )
            )
    except:
        return None

def getCnpj(part1):
    try:
        return re.search("\d{2}.\d{3}.\d{3}/\d{4}-\d{2}", part1).group()
    except:
        return None
      
    pass
def getTelefoneFixo(part1):
    try:
      return re.search('\(\d{2}\) \s\d{4}\-\d{4}', part1).group()
    except:
        return None
    
def getCelular(part1):
    try:
        return re.search('\(\d{2}\) \s\d{5}\-\d{4}', part1).group()
    except:
        return None
def getCelularAPI(part1):
    try:
        return re.search('\d{13}', part1).group()
    except:
        return None
      
def getCep(part1):
    try:
        return re.search(r"CEP: \d{5}.\d{3}", part1).group()
    except:
        return None
def getCep1(part1):
    try:
        return re.search(r"\d{5}-\d{3}", part1).group()
    except:
        return None