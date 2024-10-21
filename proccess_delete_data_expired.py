"""
Autonomous / script delete / expire jobs take offline.
"""

import sys
import os
from dotenv import load_dotenv

from sqlalchemy import text

from operations_database.job_ad import job_ad
from  automatize_channel.operations_instagram.graph_api_facebook import GraphApiFacebook

import datetime
import time
from datetime import date, timedelta

from sqlalchemy.orm import Session

from collect_data.extractData import collectorDataScrap



if __name__ == '__main__':
    """
    Esta rotina verifica se a vaga que está no registro job_ad que já foi fechada no site ou está aberta.
    Caso esteja fechada é inserido a data no campo deleted_at para deleta-la.
    """

    job = job_ad()
    query = " SELECT * FROM job_ad WHERE LINK LIKE 'www.vagas.com.br%' AND DELETED_AT IS NULL AND READ_AT IS NULL ; "
    res = job.queryRaw( query )

    for row in res: 
        url=row.LINK
       
        #url="https://www.vagas.com.br/vagas/v2651431/comprador-guarulhos"
        print(url)
        #break
        Scraper = collectorDataScrap('https://'+url)
        isExpired = Scraper.verifiedHostJobExpiredVagasCom()
        print('dados extraído...')
        print(isExpired)
        #print("isExpired: "+str(isExpired))
        if( isExpired ):
            print('erro')
            updateJobAdExpired = "UPDATE job_ad SET DELETED_AT = CURRENT_TIME() WHERE LINK = '"+str(url)+"';"
            print(updateJobAdExpired)
            job.connection.execute(text(updateJobAdExpired))
            job.connection.commit()
    
    
    print('fim')
    exit(0)
    

    