# import pandas as pd
# import numpy as np
import urllib
from fake_useragent import UserAgent
import requests
import re
# from urllib.request import Request, urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from tabelas import engine, Resultados,session




# informar termo de pesquisa , numero de resultados por pagina
def google_results(busca, n_results):
    busca = urllib.parse.quote_plus(busca)
    n_results = n_results
    ua = UserAgent()
    google_url = "https://www.google.com/search?q=" + busca + "&num=" + str(n_results)
    response = requests.get(google_url, {"User-Agent": ua.random})
    soup = BeautifulSoup(response.text, "html.parser")
    result = soup.find_all('div', attrs = {'class': 'ZINbbc'})
    results=[re.search('\/url\?q\=(.*)\&sa',str(i.find('a', href = True)['href'])) for i in result]
    
    
    links=[i.group(1) for i in results if i != None]
    for x in results:
        if x != None:
            print ("########################")
            print (x.group(1))
            print (urlparse(x.group(1)).netloc)
            print ("########################")
            session.add(Resultados(dominio = urlparse(x.group(1)).netloc,url = x.group(1)))
            
    session.commit()
            
    
    
    return (links)


# x = google_results('6206', 30)
# print(x)





# c1 = Customers(name = 'Ravi Kumar', address = 'Station Road Nanded', email = 'ravi@gmail.com')


# session.add(c1)
# session.commit()

# session.add_all([
#    Customers(name = 'Komal Pande', address = 'Koti, Hyderabad', email = 'komal@gmail.com'), 
#    Customers(name = 'Rajender Nath', address = 'Sector 40, Gurgaon', email = 'nath@gmail.com'), 
#    Customers(name = 'S.M.Krishna', address = 'Budhwar Peth, Pune', email = 'smk@gmail.com')]
# )

# session.commit()



# result = session.query(Customers).all()

# for row in result:
#    print ("Name: ",row.name, "Address:",row.address, "Email:",row.email)


result = session.query(Resultados)\
    .distinct()\
    .all()

for row in result:
   print ("Dominio: ",row.dominio, " <<>>> Url: ",row.url)