# import re
# from urllib.request import urlopen

# url = "https://rolamentoscbf.com.br/"
# website = urlopen(url).read().decode('utf8')

# print()
# print()
# print("Phone Numbers: ")
# numbers = (re.findall(r"((?:\d{3}|\(\d{3}\))?(?:\s|-|\.)?\d{3}(?:\s|-|\.)\d{4})",website))
# print (', '.join(map(str, numbers)))
# print()
# print()
# print("Emails: ")
# emails = (re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}",website))
# print (', '.join(map(str, emails)))


import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
from urllib.parse import urlparse
from tabelas import session, Resultados,DominiosIgnorados
import pathlib

def pesquisaWeb(query,ignorar):
    g_clean = [ ] 
    url = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&num=3000&oe=utf-8'.format(query)
    try:
            html = requests.get(url)
            if html.status_code==200:
                soup = BeautifulSoup(html.text, 'lxml')
                a = soup.find_all('a') 
                for i in a:
                    k = i.get('href')
                    try:
                        m = re.search("(?P<url>https?://[^\s]+)", k)
                        n = m.group(0)
                        url = n.split('&')[0]
                        domain = urlparse(url)
                        if(re.search('google.com', domain.netloc)):
                            continue
                        else:
                            ignorar = session.query(DominiosIgnorados).filter(DominiosIgnorados.dominio.ilike(urlparse(url).netloc.split('.')[1])).all()
                            if len(ignorar) == 0:
                                ext = pathlib.Path(url).suffix
                                ignorarExtensoes = ['.xls','.xlsx', '.pdf', '.rar', '.exe'] 
                                result = list(filter(lambda x: str(ext).lower() in x, ignorarExtensoes)) 
                                if len(result) > 0:
                                    g_clean.append(url)
                                    session.add(Resultados(dominio = urlparse(url).netloc,url =urlparse(url).scheme+"://"+urlparse(url).netloc))
                                else:
                                    session.add(Resultados(dominio = urlparse(url).netloc,url = url))
                                session.commit()
                    except:
                        continue
    except Exception as ex:
            print(str(ex))
    finally:
            return g_clean


# Consulta URl para ignorar
ignorar = session.query(DominiosIgnorados).all()

x = (pesquisaWeb("rolamentos",ignorar))

print(x)

