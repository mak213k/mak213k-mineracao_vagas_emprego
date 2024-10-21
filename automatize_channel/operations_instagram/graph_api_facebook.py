# -*- coding: utf-8 -*-
#References
#https://facebook-sdk.readthedocs.io/en/latest/api.html
#https://github.com/mobolic/facebook-sdk
#https://developers.facebook.com/docs/graph-api/reference/
#https://developers.facebook.com/docs/graph-api/reference/

#Permitions:

#pages_read_engagement:
#A fim de receber aprovação para o uso da permissão pages_read_engagement, 
#o envio deve incluir pages_show_list ou seu aplicativo deve ter sido aprovado 
#para usar pages_show_list em um envio anterior.


#pages_manage_posts:
#Com a permissão pages_manage_posts, seu aplicativo pode criar, editar e 
#excluir publicações na sua Página.
#Allowed Usage
#Fazer uma publicação, compartilhar uma foto ou um vídeo na sua Página.
#Atualizar uma publicação, foto ou vídeo na sua Página.
#Excluir uma publicação, foto ou vídeo na sua Página.

#pip install facebook-sdk
#pip install facebook-business

#pip install instagram-private-api
#pip install instagram-private-api-extensions


import sys
#sys.path.append('/config/')

#import config


from enum import Enum

#import urllib3
#import requests
import facebook


import json

import os
from dotenv import load_dotenv

import requests
from urllib.error import URLError


from io import BytesIO
from PIL import Image



class status_code(Enum):
    Ok = 200
    redirect = 301
    badRequest = 400
    notAuthenticated = 401
    resourceForbiden = 403
    notFound = 404
    notHandleRequest = 503

"""
class status_type(Enum):
    Enum ( 'status_type', [ mobile_status_update, created_note, added_photos, added_video, shared_story, created_group, created_event, wall_post, app_created_story, published_story, tagged_in_photo ] )
"""

class GraphApiFacebook:

    def __init__(self, id_client, client_secret, app_id, access_token, app_version = "3.1", host = 'https://graph.facebook.com', oath_grant_type="client_credentials", app_version_instagram="v19.0"):
        self.id_client = id_client
        self.client_secret = client_secret
        self.app_id = app_id
        self.access_token = access_token
        self.host = host
        self.app_version = app_version
        self.app_version_instagram = app_version_instagram
        self.oath_grant_type= oath_grant_type


    def get_page_access_token(self, app_id, app_secret, page_id):
        """
        app_access_token_url = f"https://graph.facebook.com/oauth/access_token"
        print(app_access_token_url)
        param = {
            "client_id":self.id_client,
            "client_secret":self.client_secret,
            "grant_type":self.oath_grant_type
            }
        response = requests.post(app_access_token_url, param)
        print(response)
        exit(0)
        app_access_token = response.json()["access_token"]
        
        print(response)
        exit(0)
        """
        
        page_access_token_url = f"https://graph.facebook.com/{page_id}?fields=access_token&access_token={app_access_token}"
        response = requests.get(page_access_token_url)
        page_access_token = response.json()["access_token"]

        return page_access_token
            
    
    #método à implementar para autenticar o cliente
    def auth_url_client(app_id, canvas_url, perms):
        app_id=app_id
        canvas_url = canvas_url
        perms = ["pages_read_engagement","pages_manage_posts"]
        fb_login_url = graph.get_auth_url(app_id, canvas_url, perms)
        print(fb_login_url)
        return fb_login_url
    
    def auth_url_client1(self, client_id, client_secret):
        url = self.host+"/oauth/access_token?client_id="+client_id+"&client_secret="+client_secret+"&grant_type=client_credentials"
        print(url)
        response = requests.post(url)
        print(url)
        print(response.json())



    def getLatestPostFromFacebook(self, page_id, facebook_access_token):
        graph = facebook.GraphAPI(facebook_access_token)
        posts = graph.get_object(f'/{page_id}/posts', fields='created_time,message,message_tags,full_picture,location', limit=1)
        latest_post = posts['data'][0] if 'data' in posts and posts['data'] else None
        return latest_post


    def getAllPosts(self):
        graph = facebook.GraphAPI(self.access_token, version=self.app_version)
        profile = graph.get_object("me")
        return graph.get_connections(profile['id'], "posts")['data']


    def getIdPost(self,id):
        graph = facebook.GraphAPI(self.access_token, version=self.app_version)
        post_message = graph.get_object(id=id )
        return post_message
    
    def getPermissionsGrantedByUser(self):
        graph = facebook.GraphAPI(self.access_token, version=self.app_version)
        response = graph.get_permissions("2671594396328546")
        return response

    def getMeAccountData(self):
        app_access_token_url = f""+self.host()+"/"+self.app_version_instagram+"/me/accounts?access_token={app_secret}"
        response = requests.get(app_access_token_url)
        print(app_access_token_url)
        print(response.json())
        exit(0)

    """
    Create a post with params passed to facebook page
    Development stage: Not tested
    """
    def createPost(self, mensagem, link, imagePath, schedule, published = True):
        
        try:
            PAGE_ID=os.getenv("PAGE_ID")

            body = {}

            if(published == True):
                body['caption'] = mensagem
                body['link'] = link
                body['published'] = True

            if(published == False):
                body['message'] = mensagem
                body['link'] = mensagem
                body['scheduled_publish_time'] = False


            graph = facebook.GraphAPI(self.access_token, version=self.app_version)


            #response = graph.put_object("me","feed",message=body['message'], link=body['link'], published=body['published'], schedule=body['schedule'], source=imagePath)
            #response = graph.put_object(parent_object = )
            response = graph.put_photo(image=open(imagePath, 'rb'),
                                    message=mensagem)
            ##, **{'tags':tags}
            
            #url = self.host+"/"+self.app_version_instagram+"/"+PAGE_ID+"/photos"
            #response = requests.post(url, body)
            print('postando facebook..')
            #print(url)
            print(response)
            #print(response.json())

            #exit();
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
    
    

    def createPost_instagramByApiMedia( self, access_token, caption, image_url, params):
        """
        Function that create post in instagram api
        """

        try:

            url = self.host+"/"+self.app_version_instagram+"/"+self.id_client+"/media"
            print(url)
            
            response = requests.post(url, params=params)
            print(url)
            print(response.json())

            if 'error' in response.json() and response.json()['error'] is not None:
                if response.json()['error']['type'] == 'OAuthException':
                    raise NameError('OAuthException, código:'+str(response.json()['error']['code'])+', Erro:'+response.json()['error']['error_user_msg'])

            print("Conteiner made with success")
            return response.json()

        except URLError as ue:
            print("The Server Could Not be Found")
            print(ue.args[0])

        except requests.exceptions.HTTPError as err:
            print("HTTP error")
            print(err.args[0])

        except IndexError:
            print("Index not exists")
        
        print(response)


    def createPost_instagramByApiMediaPublish(self, idInstagramConteiner, params):

        try:
        
            url = self.host+"/"+self.app_version_instagram+"/"+self.id_client+"/media_publish?"+"creation_id="+idInstagramConteiner
            response = requests.post(url, params=params)

            print(url)
            print(response)
            print("Postado com sucesso")
            return response.json()

        except requests.exceptions.HTTPError as err:
            print("HTTP error")
            print(err.args[0])
        
        print(response)


    def createUploadPhoto(self, mensagem, path_photo):
        """
        facebook.GraphAPIError: (#200) This endpoint is deprecated since the required permission publish_actions is deprecated
        """
        graph = facebook.GraphAPI(self.access_token, version=self.app_version)
        graph.put_photo(image=open(path_photo, 'rb'),
        message=mensagem)

        print("success...")


    def updatePost( self, post_id, mensagem, link ):
        body = {
        "message": mensagem,
        "link":link
        }
        graph = facebook.GraphAPI(self.access_token, version=self.app_version)
        response = graph.put_object( parent_object=str(post_id), connection_name='',message=body['message'], link=body['link'] )
        return response


    def deletePost(self, id):
        graph = facebook.GraphAPI(self.access_token, version=self.app_version)
        response = graph.delete_object(id=id)
        return response

    

    def post_facebook_to_instagram(self, instagram_username, instagram_password, post):
        """
        instagram_api = Client(instagram_username, instagram_password)
        image_url = post['full_picture']
        response = requests.get(image_url)
        image_data = response.content
        caption = post['message']

        photo_data, photo_size = media.prepare_image(image_url, aspect_ratios=MediaRatios.standard)
        
        # Open the image using PIL (Python Imaging Library)
        image = Image.open(BytesIO(image_data))

        # Get the size of the image
        width, height = image.size

        #if width < 320:
        #    raise ValueError('Invalid image width. Image width must be at least 320 pixels.')
        
        instagram_api.post_photo(image_data, (width, height) , caption)

        #instagram_api.post_photo(photo_data=image_data, size=(width, height) , caption=caption)
        """

        """
        image_url = post['full_picture']
        caption = post['message']
        bot = Bot(like_delay=60)
        bot.login(username=instagram_username,password=instagram_password)
        bot.upload_photo(image_url,caption=caption)
        print("Posting complete...")
        """

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

    """
    Object that connect api Facebook.
    """
    gaf_facebook = GraphApiFacebook( OATH_FACEBOOK_CLIENT_ID, OATH_CLIENT_SECRET_TOKEN, APP_ID, PAGE_ACCESS_TOKEN )
    gaf_instagram = GraphApiFacebook( OATH_INSTAGRAM_CLIENT_ID, OATH_CLIENT_SECRET_TOKEN, APP_ID, PAGE_ACCESS_TOKEN )
    
    #print(gaf.getIdPost('110793635453520_122143824452028277'))
    
    #print( gaf_facebook.getAllPosts() )
    #exit(0)
    #print(gaf.updatePost( '110793635453520_122143824452028277', "Nova tentativa 12:35 20 dez 23 test 2222", "https://developers.facebook.com/" ))
    #print(gaf.auth_url_client())
    #print(gaf.getPermissionsGrantedByUser())

    newToken = gaf_facebook.auth_url_client1(PAGE_ID, PAGE_ACCESS_TOKEN)
    print(newToken)
    exit(0)
"""
    post_facebook = gaf_facebook.createPost( "Nova tentativa 23:17 31 07 abril test 2222", "https://developers.facebook.com/", "2024-04-07T23:18:36+00:00", True )
    latest_post = gaf_facebook.getLatestPostFromFacebook(PAGE_ID, PAGE_ACCESS_TOKEN)    
    print("Iniciando conteiner")
    paramsInstagram = {
        'access_token':gaf_facebook.client_secret,
        'caption': latest_post['message'],
        'image_url': latest_post['picture']
    }
    
    response = gaf_instagram.createPost_instagramByApiMedia( OATH_CLIENT_SECRET_TOKEN, paramsInstagram['caption'], paramsInstagram['image_url'], paramsInstagram )
    print("Iniciando a postagem...")
    print( gaf_instagram.createPost_instagramByApiMediaPublish(response['id'], paramsInstagram) )
    exit("Fim")
"""




