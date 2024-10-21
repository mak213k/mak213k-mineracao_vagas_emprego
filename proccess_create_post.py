"""
Script to processing collected information and sent to appropriate channel.
The complete cicle is:collect of data, creation of content in the support format
(that's, in the case, is an instagram post) and sent the web destination

Script para processamento das informações coletadas e enviadas para o canal apropriado.
O ciclo completo é: Coleta dos dados, confecção do conteúdo no formato de suporte 
(que, no caso, é post de instagram) e envio aos destinatários da rede.
"""

from sqlalchemy import text
from operations_database.job_ad import job_ad
from manage_content.postInstagram import PostInstagram



def migrationJobAdToPost():

    try:
        """
        Variável que limita a quantidade de registros processados por vez para serem criados às postagems
        """
        limit = 10

        #query = " SELECT ID_JOB_AD,TITLE,LOCATION,MODALITY,MESSAGE,LINK,READ_AT FROM JOB_AD WHERE ( READ_AT = 0 OR READ_AT IS NULL ) AND ( DELETED_AT = 0 OR DELETED_AT IS NULL )  ORDER BY RAND() LIMIT "+str(limit)+" "
        query = " SELECT * FROM ( \
SELECT FILHO.ID_JOB_AD, FILHO.TITLE,FILHO.LOCATION,FILHO.MODALITY,FILHO.MESSAGE,FILHO.LINK, FILHO.ID_PAI,FILHO.READ_AT FROM JOB_AD AS PAI \
INNER JOIN JOB_AD AS FILHO \
ON PAI.ID_JOB_AD = FILHO.ID_PAI \
WHERE ( FILHO.READ_AT = 0 OR FILHO.READ_AT IS NULL ) AND ( FILHO.DELETED_AT = 0 OR FILHO.DELETED_AT IS NULL ) LIMIT 10 \
) FILHOS \
LEFT JOIN ( \
SELECT SEM_FILHO.ID_JOB_AD, SEM_FILHO.TITLE, SEM_FILHO.LOCATION, SEM_FILHO.MODALITY, SEM_FILHO.MESSAGE, SEM_FILHO.LINK, SEM_FILHO.ID_PAI, SEM_FILHO.READ_AT \
FROM JOB_AD AS SEM_FILHO \
LEFT JOIN JOB_AD AS FILHO \
ON SEM_FILHO.ID_JOB_AD=FILHO.ID_JOB_AD AND SEM_FILHO.ID_PAI = 0 AND SEM_FILHO.ID_PAI <> FILHO.ID_PAI \
) UNICO \
ON FILHOS.ID_JOB_AD=UNICO.ID_JOB_AD \
ORDER BY RAND() "

        #print(query)
        #exit(0)
        job = job_ad()
        res = job.queryRaw(query)

        """
        update = ''
        job.queryRaw(update)
        insert=''
        """

        """
        Processo à ser implementado: Revisão dos posts antes de serem postados. 
        A revisão passa por um processo automático feito pela IA e manual para aprovação.

        """
        """
        for row in res:
            print(row)
        
        exit(0)
        """

        for row in res:
            modality = ''
            if str(row[3]) != 'None':
                modality = str(row[3])
            

            #generatePostImage = postInstagram(row)

            bind = dict()
            bind['title'] = str(row[1])
            bind['message'] = row[4]
            #bind['message'] = (row[4] +"\\n"+ row[5])
            posttInserted = "INSERT INTO POST( TITLE, LOCATION, MODALITY, MESSAGE,LINK,READ_AT,REVISED_AT) VALUES( '"+bind['title']+"','"+row[2]+"','"+modality+"','"+bind['message']+"','"+row[5]+"',null,null );"
            job.connection.execute(text(posttInserted))
            postUpdated = "UPDATE `job_ad` SET READ_AT = CURRENT_TIMESTAMP() WHERE ID_JOB_AD='"+str(row[0])+"';"
            job.connection.execute(text(postUpdated))
            job.connection.commit()
            #print(posttInserted)



    except Exception as err:
        print(f"Erro: {err}, type{err}")

# id_post, id_client, title, location, links, message

if __name__=='__main__':
   postInstagram = PostInstagram()
   ##postInstagram.ad_jobToPost()
   #migrationJobAdToPost()
   postInstagram.createImagePostRevised()
   