from scrapy import addDominiosIgnorados,pesquisa, getDados

url = ['https://www.casasbahia.com.br/','https://www.carrefour.com.br','https://www.alibaba.com/','https://pt.aliexpress.com/','https://www.mercadolivre.com.br/','https://www.uai.com.br/','https://www.globo.com/','https://g1.globo.com/','https://www.terra.com.br/','https://www.uol.com.br/','https://www.facebook.com/','https://instagram.com/','https://twitter.com/','https://www.jusbrasil.com.br/','https://pt.wikipedia.org/','https://www.netshoes.com.br/','https://www.timken.com/','https://www.jusbrasil.com.br/','https://esportes.mercadolivre.com.br/','https://lista.mercadolivre.com.br/','https://portuguese.alibaba.com/','https://m.portuguese.alibaba.com','https://www.autopecas-online.pt','https://www.autopecasonline24.pt/','https://www.pecasauto24.pt','https://parts.cat.com','https://www.amazon.com.br/','https://www.americanas.com.br/','https://www.multasbr.com.br/','https://www.reposicaoonline.com.br','https://foegerbicicletas.com.br','https://www.magazineluiza.com.br/','https://pt.ebay.com/','http://cnpj.info','https://www.shoptime.com.br/','https://m.kabum.com.br','https://sead.amapa.gov.br/','https://www.autopecas24.pt/','https://m.topautopecas.pt','https://shop.bpwtrapaco.com/','https://br.linkedin.com/','https://support.google.com','https://www.google.com/','https://maps.google.com','https://policies.google.com','https://produto.mercadolivre.com.br','https://webcache.googleusercontent.com','http://webcache.googleusercontent.com','https://www.youtube.com']




print (addDominiosIgnorados(url))
print(pesquisa("rolamentos",1))
# print(getDados(14))
