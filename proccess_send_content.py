"""

Autonomous / script to send content to recipients. In first moment should have management of content by instagram.
Others media can to be includes in next steps. How email to newsletter, whatsapp and others forms of communication with
the final users.

Autônomo / script para envio de conteúdo para os destinatários. Em primeiro momento será feito controle de conteúdo via instagram.
Outras mídias poderão ser incluídas nos próximos passos. Como email para newsletter, whatsapp e outras formas de comunicação com
o usuário final.
"""

import sys
import os
from dotenv import load_dotenv

from sqlalchemy import text

from operations_database.job_ad import job_ad
from  automatize_channel.operations_instagram.graph_api_facebook import GraphApiFacebook

import datetime
from datetime import date, timedelta

if __name__ == '__main__':
    
    """
    Loading environment variables.
    """
    load_dotenv()
    PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
    OATH_FACEBOOK_CLIENT_ID = os.getenv("OATH_FACEBOOK_CLIENT_ID")
    OATH_INSTAGRAM_CLIENT_ID = os.getenv("OATH_INSTAGRAM_CLIENT_ID")
    OATH_CLIENT_SECRET_TOKEN = os.getenv("OATH_CLIENT_SECRET_TOKEN")
    APP_ID=os.getenv("APP_ID")
    APP_ACCESS_TOKEN=os.getenv("APP_ACCESS_TOKEN")
    PAGE_ID=os.getenv("PAGE_ID")
    PATH_ROOT=os.getenv("PATH_ROOT")

    """
    Object that connect api Facebook.
    """
    gaf_facebook = GraphApiFacebook( OATH_FACEBOOK_CLIENT_ID, OATH_CLIENT_SECRET_TOKEN, APP_ID, PAGE_ACCESS_TOKEN )
    gaf_instagram = GraphApiFacebook( OATH_INSTAGRAM_CLIENT_ID, OATH_CLIENT_SECRET_TOKEN, APP_ID, PAGE_ACCESS_TOKEN )


    limit = 5
    query = " SELECT MESSAGE, LINK, IMAGE_POST_NAME, ID_POST FROM `POST` WHERE ( DELETED_AT IS NULL) AND ( REVISED_AT IS NOT NULL ) AND POSTED_AT IS NULL LIMIT "+str(limit)+" "
    print(query)
    job = job_ad()
    posts = job.queryRaw(query)
    print(posts)
    image__path=PATH_ROOT
    calendar_post_instagram = ''
    interval_calendar = 0
    for post in posts:
        print(post)
        print("Criando classe de postagem no instagram.")
        
        #interval_calendar = interval_calendar + 0
        #hourly = datetime.timedelta(hours=interval_calendar)
        #calendar_post_instagram = datetime.datetime.today() + hourly

        calendar_post_instagram = datetime.datetime.today()

        image_facebook=image__path+"\\"+post[2]
        
        post_facebook = gaf_facebook.createPost( post[0], post[1], image_facebook, calendar_post_instagram, False )
        id_post=post[3]
        #exit(0);

        latest_post = gaf_facebook.getLatestPostFromFacebook(PAGE_ID, PAGE_ACCESS_TOKEN)    
        
        print("Iniciando conteiner")
        paramsInstagram = {
            'access_token':gaf_facebook.client_secret,
            'caption': latest_post['message'],
            'image_url': latest_post['full_picture']
        }

        
        response = gaf_instagram.createPost_instagramByApiMedia( OATH_CLIENT_SECRET_TOKEN, paramsInstagram['caption'], latest_post['full_picture'], paramsInstagram )
        print("Iniciando a postagem...")
        print( gaf_instagram.createPost_instagramByApiMediaPublish(response['id'], paramsInstagram) )
        updatePostedAt = "UPDATE POST SET POSTED_AT=CURRENT_TIMESTAMP() WHERE ID_POST="+str(id_post)
        print(updatePostedAt)
        job.connection.execute(text(updatePostedAt))
        job.connection.commit()
        
    exit("Fim")


    