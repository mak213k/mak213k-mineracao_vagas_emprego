
"""
Collect content in hosts by webscraping for write the content in database.
"""
from collect_data.extractData import collectorDataScrap


##Scraper ApiInfo 
##- Falta filtrar pelo termo Guarulhos
##- Falta pular para a próxima página            
#url = "https://www.apinfo.com/apinfo/inc/list4.cfm"
#Scraper = collectorDataScrap(url)
#Scraper.collectApInfo()


url = "https://www.vagas.com.br/vagas-de-guarulhos"
Scraper = collectorDataScrap(url)
Scraper.collectVagasCom()
            
#url = "https://br.indeed.com/jobs?q=&l=guarulhos%2C%20sp&from=searchOnHP"
#Scraper = collectorDataScrap(url)
#Scraper.collectIndeed()