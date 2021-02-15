from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
# ################################################################
# entrada = input("Pesquisar: ")
entrada = '6206' # rolamento
entrada = entrada.replace(' ', '')
paginas =1

# ################################################################

# TODO: Navegar no google e pesquisar pelo item informado na pesquisa
driver = webdriver.Chrome(ChromeDriverManager(version="87.0.4280.88").install())
driver.get("https://www.google.com")


for i in range(paginas): 
    driver.get("https://www.google.com/search?q=" +entrada + "&start=" + str(i)) 
    # TODO: incluir delay caso possua mais de 1 pagina de pesquisa
    # time.splep(1)
    # print(driver.current_url) # Url de pesquisa
    html = driver.page_source



# TODO: Coletar todoas a url da pesquisa
# results = driver.find_elements_by_xpath("//div[@class='g']//div[@class='r']//a[not(@class)]");
# results = driver.find_elements_by_xpath('//*[@id="rso"]');
# for result in results:
#     print(result.get_attribute("href"))
# ids = driver.find_elements_by_xpath("//div[@class='sbqs_c']")
# print(ids)
# for ii in ids:
#        #print ii.text
#        print(ii.text)
       
# import pdb; pdb.set_trace()
soup=BeautifulSoup(html)
for link in soup.findAll("div", {"class": "g"}):
    print(link.get('yuRUbf'))
    # print(link)




# TODO: Criar banco sqlite e armazenar as urls
# TODO: navegar pelas urls do banco e pesquisar
