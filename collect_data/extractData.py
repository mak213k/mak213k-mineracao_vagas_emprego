##!pip install undetected-chromedriver
##!pip install SQLAlchemy
##!pip install python-dotenv
##!pip install pandas
##!pip install numpy
##pip install flask-sqlalchemy 

import os
from dotenv import load_dotenv
import time
import re

#from selenium import webdriver

#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.common.by import By
#from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

import undetected_chromedriver as uc

from bs4 import BeautifulSoup
import requests
import time
from sqlalchemy import create_engine, insert, text

import numpy as np
import pandas as pd

import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from operations_database.job_ad import JobAd, job_ad


#from operations_database.post import Post



class collectorDataScrap:
    
    def __init__(self, host):
        self.host=host;
       ##self.params = params;

    def collectApInfo(self):

        try:
            print("iniciando a extração")
            repetible= ""
            options = uc.ChromeOptions()
            #options = Options()
            #options.add_argument('--headless')
            #options.add_argument('--window-size=1920x1080')
            #options.add_argument("--headless=new")
            options.headless = False
            #options.add_argument('--ignore-certificate-errors')
            headers = {"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
            undetect_driver = uc.Chrome(options=options)
            undetect_driver.get(self.host)
            print("passou por aqui")
            keyword_field = undetect_driver.find_element(By.ID,"keyw")
            keyword_field.send_keys("guarulhos")
            undetect_driver.find_element(By.ID,"radio4").click()
            undetect_driver.find_element(By.ID,"radio2").click()
            undetect_driver.find_element(By.CSS_SELECTOR, "#form-busca > div.btn-submit.center > input[type=submit]").click()
            job_ad_record = job_ad()
            while(True):
                    print("Iniciando a extração...")
                    html=BeautifulSoup(undetect_driver.page_source, 'html.parser', from_encoding='iso-8859-1')
                    log_scrapers = html.find_all("div",class_='box-vagas linha pd')
                    for log_scraper in log_scrapers:
                        title = log_scraper.find("div",class_='cargo m-tb')
                        location = log_scraper.find("div",class_='info-data')
                        message = log_scraper.find("div",class_='texto')
                        copia_message = message
                        link = copia_message.find('a').get('href')
                        title = str( title.get_text() ).strip(" ").strip('\n').replace("  "," ")
                        location = str( location.get_text() ).strip(" ").strip('\n').replace("  "," ")
                        message = str( message.get_text() ).strip(" ").strip('\n').replace("  "," ")
                        message= message.replace("'","").replace("%","")
                        title = title.replace("'","").replace("%","")

                        location = location.replace("'","")
                        location = location.replace("\"","")
                        location = location.replace("%","")

                        print("vamos ver...")
                        #print(message)
                        #print("SELECT * FROM JOB_AD WHERE LOWER(TITLE) LIKE LOWER('"+title+"') AND LOWER(MESSAGE) LIKE LOWER('"+message+"')")
                        post_duplicate = job_ad_record.queryRaw("SELECT * FROM JOB_AD WHERE LOWER(TITLE) LIKE LOWER('"+title+"') AND LOWER(MESSAGE) LIKE LOWER('"+message+"')")
                        if len(post_duplicate) == 0:
                            print("Linha não registrada no banco ")
                            job_dict = {'title':[],'location':[],'message':[],'log_scraper':[], 'link':[], 'id_pai':[]}
                            job_dict['title'].append( ( title ) )
                            job_dict['location'].append( ( location ) )
                            job_dict['message'].append( ( message ) )
                            job_dict['link'].append(link)
                            job_dict['log_scraper'].append(log_scraper)
                            job_dict['id_pai'].append(0)

                            df = pd.DataFrame.from_dict(job_dict)
                            print("Preparando para gravar no banco...")
                            ##Charge .env file variables
                            load_dotenv()
                            USERNAME_DB=os.getenv("USERNAMEDB")
                            PASSWORD=os.getenv("PASSWORD")
                            HOST=os.getenv("HOST")
                            DATABASE=os.getenv("DATA_BASE")
                            ##engine=create_engine('mysql+pymysql://'+str(USERNAME_DB)+':'+str(PASSWORD)+'@'+str(HOST)+'/'+str(DATABASE)+'?charset=utf8', pool_pre_ping=True )
                            df.to_sql(con=job_ad_record.engine, name='job_ad', if_exists='append', index=False)

                    print("começando o procedimento")
                    #ok_text = undetect_driver.find_element(By.CSS_SELECTOR,"input[type=text][name=pag]")
                    ok_text = WebDriverWait(undetect_driver,120).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[type=text][name=pag]")))
                    print("continua...")
                    print(ok_text.get_attribute("value"))
                    if repetible != ok_text.get_attribute("value"):
                        print("entrou no if")
                        repetible = ok_text.get_attribute("value")
                        print("final de pagina")
                        ##undetect_driver.execute_script("window.scrollTo(0,4400)")
                        ok_button = undetect_driver.find_element(By.CSS_SELECTOR, "input[type=submit][value=OK]")
                        print(" comecando localizacao ")
                        js_code = "arguments[0].scrollIntoView();"
                        #y = ok_button.location['y']
                        #print(" y ")
                        #undetect_driver.execute_script('window.scrollTo(0, {0})'.format(y))
                        print("scrollTo")
                        undetect_driver.execute_script(js_code, ok_button)
                        ok_button.click()
                        print("next page")
                    else:
                        print("finish")
                        undetect_driver.close()
                        undetect_driver.quit()
                        exit(0)
                        break


        except Exception as e:
            print(f"Error: {e}")
            undetect_driver.close()
            undetect_driver.quit()
            #exit(0)
            
        finally:
            print(f"Erro não mapeado")
            undetect_driver.close()
            undetect_driver.quit()
            exit(0)
            
            
        undetect_driver.close()
        undetect_driver.quit()
        exit(0)


    def collectVagasCom(self):
        print(" comecando localizacao 1")
        repetible= ""
        options = Options()
        #options.add_argument('--headless')
        ##options.add_argument('--window-size=1920x1080')
        options.headless = False
        #options.add_argument('--ignore-certificate-errors')
        headers = {"header":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
        ##options.add_argument(f"user-agent={headers['header']}")
        undetect_driver = uc.Chrome(version_main = 126,  options=options)
        undetect_driver.get(self.host)
        
        try:

            while(True):
                
                    html=BeautifulSoup(undetect_driver.page_source, 'html.parser', from_encoding='iso-8859-1')
                    ##html = html.encode("utf-8")
                    mais_vagas = undetect_driver.find_element(By.ID,"maisVagas")
                    print(" comecando localizacao ")
                    #y = mais_vagas.location['y']
                    js_code = "arguments[0].scrollIntoView();"
                    print(" y ")
                    #undetect_driver.execute_script('window.scrollTo(0, {0})'.format(y))
                    print("scrollTo")
                    undetect_driver.execute_script(js_code, mais_vagas)
                    print("Mais vagas")

                    log_scrapers = html.select("li.vaga")
                    #log_scrapers = html.find_all("div",class_='vaga')
                    job_ad_record = job_ad()
                    print("point0")
                    for log_scraper in log_scrapers:
                        print("point1")
                        title = log_scraper.find("h2",class_='cargo')
                        link = title.find("a")
                        host_basis = self.host.split("/")
                        link = host_basis[2]+link.get('href')
                        
                        location = log_scraper.find("span",class_='vaga-local')
                        message = log_scraper.find("div",class_='detalhes')
                        print("point1")
                        title = str( title.get_text() ).strip(" ").strip('\n').replace("  "," ")
                        location = str( location.get_text() ).strip(" ").strip('\n').replace("  "," ")
                        message = str( message.get_text() ).strip(" ").strip('\n').replace("  "," ")
                        message= message.replace("'","").replace("%","")
                        title = title.replace("'","").replace("%","")

                        location = location.replace("'","")
                        location = location.replace("\"","")
                        location = location.replace("%","")

                        print("point2")
                        job_dict = {'title':[],'location':[],'message':[],'log_scraper':[], 'link':[], 'id_pai':[]}
                        job_dict['title'].append(title)
                        job_dict['location'].append(location)
                        job_dict['message'].append(message)
                        job_dict['link'].append(link)
                        job_dict['log_scraper'].append(log_scraper)
                        job_dict['id_pai'].append(0)
                        df = pd.DataFrame.from_dict(job_dict)
                            
                        print("point3")
                        df.to_sql(con=job_ad_record.engine, name='job_ad', if_exists='append', index=False)
                        job_ad_record.connection.commit()

                        inserted_id = job_ad_record.queryRaw("SELECT job_ad.ID_JOB_AD as ID_JOB_AD from job_ad ORDER BY job_ad.ID_JOB_AD DESC LIMIT 1")
                        print("contagem id...")
                        link = 'https://'+link
                        undetect_driver.get(link)
                        html_subnivel=BeautifulSoup(undetect_driver.page_source, 'html.parser', from_encoding='utf-8')
                        log_scraper_subnivel = html_subnivel.find("article")
                            
                        ##Subnível da vagas.com
                        title = title
                        link = link
                        location = location
                        message = log_scraper_subnivel.find("div", class_='texto')
                        print('chegou')
                        #title = str( title.get_text() ).strip(" ").strip('\n').replace("  "," ")
                        #location = str( location.get_text() ).strip(" ").strip('\n').replace("  "," ")
                        message = str( message.get_text() ).strip(" ").strip('\n').replace("  "," ")
                        message= message.replace("'","").replace("%","")
                        #title = title.replace("'","").replace("%","")

                        location = location.replace("'","")
                        location = location.replace("\"","")
                        location = location.replace("%","")

                        print(message)    
                        job_dict = {'title':[],'location':[],'message':[],'log_scraper':[], 'link':[], 'id_pai':[]}
                        job_dict['title'].append(title)
                        job_dict['location'].append(location)
                        job_dict['message'].append(message)
                        job_dict['link'].append(link)
                        job_dict['log_scraper'].append(log_scraper_subnivel)
                        job_dict['id_pai'].append(inserted_id[0][0])
                                
                        del inserted_id
                        df = pd.DataFrame.from_dict(job_dict)
                        post_duplicate = job_ad_record.queryRaw("SELECT * FROM JOB_AD WHERE LOWER(TITLE) LIKE LOWER('"+title+"') AND LOWER(MESSAGE) LIKE LOWER('"+message+"')")
                        if len(post_duplicate) == 0:
                            ##Charge .env file variables
                            df.to_sql(con=job_ad_record.engine, name='job_ad', if_exists='append', index=False)
                            job_ad_record.connection.commit()
                            print('Objeto gravado...')

            undetect_driver.close()
            undetect_driver.quit()
            exit(0)
            
        except Exception as e:
            print(f"Error: {e}")
            undetect_driver.close()
            undetect_driver.quit()
            exit(0)
            #break 
            
        finally:
            print(f"Error não mapeado")
            undetect_driver.close()
            undetect_driver.quit()
            exit(0)
            #break

        undetect_driver.close()
        undetect_driver.quit()
        exit(0)

    def collectIndeed(self):
        repetible= ""
        #options = uc.ChromeOptions()
        options = Options()
        #options.add_argument('--headless')
        ##options.add_argument('--window-size=1920x1080')
        options.headless = False
        #options.add_argument('--ignore-certificate-errors')
        headers = {"header":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
        ##options.add_argument(f"user-agent={headers['header']}")
        undetect_driver = uc.Chrome(version_main = 126,  options=options)
        ##undetect_driver.quit()
        ##undetect_driver = uc.Chrome()
        undetect_driver.get(self.host)

        while(True):
            try:
                
                html=BeautifulSoup(undetect_driver.page_source, 'html.parser')
                #log_scrapers = html.select("li.vaga")
                log_scrapers = html.find_all("div",class_='job_seen_beacon')
                
                job_ad_record = job_ad()
                for log_scraper in log_scrapers:
                    title = log_scraper.find("td",class_='resultContent')
                    location = log_scraper.find("div",class_='company_location')
                    message = log_scraper.find("div",class_='css-1u8dvic eu4oa1w0')
                    message = message.find("div",class_='underShelfFooter')
                    message = message.find("div",class_='css-193h767')
                    message = message.find("div",class_='css-9446fg eu4oa1w0')
                    
                    #print(message)
                    #exit(0)

                    link = title.find('a').get('href')
                    
                    #message_sublevel = message.find("a")
                    #print(message.find('a'))
                    title = str( title.get_text() ).strip(" ").strip('\n').replace("  "," ")
                    location = str( location.get_text() ).strip(" ").strip('\n').replace("  "," ")
                    message = str( message.get_text() ).strip(" ").strip('\n').replace("  "," ")
                    link = 'https://'+self.host.split('/')[2] + link
                    message= message.replace("'","")
                    message= message.replace("\"","")
                    message= message.replace("%","")
                    title = title.replace("'","")
                    title = title.replace("\"","")
                    title = title.replace("%","")

                    location = location.replace("'","")
                    location = location.replace("\"","")
                    location = location.replace("%","")
                    
                    #message = re.escape(message) 
                    #title = re.escape(title)                     

                    post_duplicate = job_ad_record.queryRaw("SELECT * FROM JOB_AD WHERE LOWER(TITLE) LIKE LOWER('"+title+"') AND LOWER(MESSAGE) LIKE LOWER('"+message+"')")
                    if len(post_duplicate) == 0:
                        job_dict = {'title':[],'location':[],'message':[],'log_scraper':[], 'link':[], 'id_pai':[]}
                        job_dict['title'].append(title);
                        job_dict['location'].append(location);
                        job_dict['message'].append(message);
                        job_dict['link'].append(link)
                        job_dict['log_scraper'].append(log_scraper);
                        job_dict['id_pai'].append(0)
                        df = pd.DataFrame.from_dict(job_dict)

                        #print(str(job_dict['title'][0]))
                        #exit(0)

                        ##Charge .env file variables
                        load_dotenv()
                        USERNAME_DB=os.getenv("USERNAMEDB")
                        PASSWORD=os.getenv("PASSWORD")
                        HOST=os.getenv("HOST")
                        DATABASE=os.getenv("DATA_BASE")
                        #engine = create_engine('mysql+pymysql://'+str(USERNAME_DB)+':'+str(PASSWORD)+'@'+str(HOST)+'/'+str(DATABASE)+'?charset=utf8' )
                        
                        df.to_sql(con=job_ad_record.engine, name='job_ad', if_exists='append', index=False)
                        job_ad_record.connection.commit()
                        print('gravando...')

                        """
                        insert_job = insert(JobAd).values(
                            TITLE=job_dict['title'],
                            LOCATION=job_dict['location'],
                            MESSAGE=job_dict['message'],
                            LINK=job_dict['link'],
                            LOG_SCRAPER=job_dict['log_scraper'],
                            ID_PAI=job_dict['id_pai']
                        )
                        """
                        #job_ad_record.insertRaw("INSERT INTO JOB_AD(TITLE,LOCATION,MESSAGE,LINK,LOG_SCRAPER,ID_PAI) VALUES('"+str(job_dict['title'][0])+"','"+str(job_dict['location'][0])+"','"+str(job_dict['message'][0])+"','"+str(job_dict['link'][0])+"','"+str(job_dict['log_scraper'][0])+"',"+str(job_dict['id_pai'][0])+")")
                        #job_ad.insertRaw(JobAd, job_dict)
                        
                        #query_results = job_ad_record.queryRaw("SELECT MAX(job_ad.ID_JOB_AD) as ID_JOB_AD from job_ad")
                        #query_results = job_ad_record.queryRaw("SELECT LAST_INSERT_ID() as ID_JOB_AD")
                        
                      
                        #if query_results:
                        #    inserted_id = query_results[0][0]
                        #else:
                        #    print('No records')

                        inserted_id = job_ad_record.queryRaw("SELECT job_ad.ID_JOB_AD as ID_JOB_AD from job_ad ORDER BY job_ad.ID_JOB_AD DESC LIMIT 1")
                        print("contagem id...")
                        print(inserted_id[0][0])
                        
                        """
                        Coleta de dados da página da vaga. Subnível da página pai.
                        """
                        undetect_driver.get(link)
                        html_subPage=BeautifulSoup(undetect_driver.page_source, 'html.parser', from_encoding="utf-8")
                        #title = html_subPage.find('#viewJobSSRRoot > div.fastviewjob.jobsearch-ViewJobLayout--standalone.css-10576t8.eu4oa1w0.hydrated > div.css-1quav7f.eu4oa1w0 > div > div > div.jobsearch-JobComponent.css-u4y1in.eu4oa1w0.jobsearch-JobComponent-bottomDivider > div.jobsearch-InfoHeaderContainer.jobsearch-DesktopStickyContainer.css-zt53js.eu4oa1w0 > div:nth-child(1) > div.jobsearch-JobInfoHeader-title-container.css-bbq8li.eu4oa1w0 > h1')
                        #title = html_subPage.find('#jobDescriptionText')
                        body_job = html_subPage.find("div", class_='jobsearch-BodyContainer')
                        if body_job:
                            title = job_dict['title']
                            location=job_dict['location']
                            beneficio=body_job.find("div",id="benefits")
                            message = body_job.find("div", id='jobDescriptionText')
                            print('iniciando subconsulta...')
                            

                            if beneficio is not None:
                                beneficio=str( beneficio.get_text() ).strip(" ").strip('\n').replace("  "," ")
                                                            
                                
                            #title = str( title ).strip(" ").strip('\n').replace("  "," ")
                            #location = str( location.get_text() ).strip(" ").strip('\n').replace("  "," ")
                            message = str( message.get_text() ).strip(" ").strip('\n').replace("  "," ")
                            message= message.replace("'","").replace("%","")
                            #title = title.replace("'","").replace("%","")

                            location = location.replace("'","")
                            location = location.replace("\"","")
                            location = location.replace("%","")
                            
                            if beneficio is not None:
                                message = message+" \\n "+beneficio


                            job_dict1 = {'title':[],'location':[],'message':[],'log_scraper':[], 'link':[], 'id_pai':[]}
                            job_dict1['title'].append(title);
                            job_dict1['location'].append(location);
                            job_dict1['message'].append(message);
                            job_dict1['link'].append(link)
                            job_dict1['log_scraper'].append(log_scraper);
                            job_dict1['id_pai'].append(inserted_id[0][0])
                            df1 = pd.DataFrame.from_dict(job_dict1)
                            del inserted_id
                            print("chegou aqui")
                            #exit(0)
                            #engine = create_engine('mysql+pymysql://'+str(USERNAME_DB)+':'+str(PASSWORD)+'@'+str(HOST)+'/'+str(DATABASE)+'?charset=utf8' )
                            df1.to_sql(con=job_ad_record.engine, name='job_ad', if_exists='append', index=False)
                            job_ad_record.connection.commit()
                            

                print("fim")
                undetect_driver.close()
                undetect_driver.quit()
                exit(0)

            except Exception as e:
                print(f"Error: {e}")
                undetect_driver.close()
                undetect_driver.quit()
                exit(0)
                break 

            finally:
                print(f"Error não mapeado")
                undetect_driver.close()
                undetect_driver.quit()
                exit(0)
                break

        undetect_driver.close()
        undetect_driver.quit()
        exit(0)
    

    def verifiedHostJobExpiredVagasCom(self):
        try:
            print("0000")
            options = Options()
            options.headless = False
            headers = {"header":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
            print("1111")
            undetect_driver = uc.Chrome(version_main = 126,  options=options)
            undetect_driver.get(self.host)
            
            print("Iniciando a extração...")
            html=BeautifulSoup(undetect_driver.page_source,'html.parser')
            log_scrapers = html.find_all("div",class_='job-expired__text')
            print(log_scrapers)
            res=''

            if len(log_scrapers) > 0:
                print("Vaga expirada")
                res=True
            else:
                print("Vaga ativa")
                res=False
                
                        
        except Exception as e:
            print(f"Error: {e}")
        
        except requests.RequestException as e:
            print(f"Error request: {e}")
        
        finally:
            print(f"Error não mapeado. Tente outra vez...")
            undetect_driver.close()
            undetect_driver.quit()
        
        print('retornando...')
        return res

if __name__=='__main__':
    ##Scraper ApiInfo 
    ##- Falta filtrar pelo termo Guarulhos
    ##- Falta pular para a p´roxima página            
    #url = "https://www.apinfo.com/apinfo/inc/list4.cfm"
    #Scraper = collectorDataScrap(url)
    #Scraper.collectApInfo()



    #url = "https://www.vagas.com.br/vagas-de-guarulhos"
    #Scraper = collectorDataScrap(url)
    #Scraper.collectVagasCom()
            
    #url = "https://br.indeed.com/jobs?q=&l=guarulhos%2C%20sp&from=searchOnHP"
    #Scraper = collectorDataScrap(url)
    #Scraper.collectIndeed()
    #print("fim1")

    #url="https://www.vagas.com.br/vagas/v2651431/comprador-guarulhos"
    url="https://www.vagas.com.br/vagas/v2640881/coordenador-de-auditoria"
    Scraper = collectorDataScrap('https://'+"www.vagas.com.br/vagas/v2611141/vendedor-b2b-guarulhos-sp")
    Scraper.verifiedHostJobExpiredVagasCom()
    exit(0)