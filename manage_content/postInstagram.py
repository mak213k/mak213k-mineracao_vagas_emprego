"""
Class that generate image post and update field IMAGE_POST_NAME in revised post
"""

from dotenv import load_dotenv
import os 
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from sqlalchemy.orm import Session

from datetime import datetime

import facebook
import json

import requests

from operations_database.post import Post, PostCreated
from operations_database.job_ad import JobAd, job_ad
from automatize_channel.operations_instagram.graph_api_facebook import GraphApiFacebook



class PostInstagram:

    def delete_png_files(self, directory):
        actual_directory = os.path.dirname(os.path.realpath(__file__))
        path_real = actual_directory + '\\' + directory + '\\'
        # Iterate over all files in the directory
        for filename in os.listdir(path_real):
            # Check if the file is a PNG file
            if filename.endswith(".png"):
                # Construct the full path to the file
                file_path = os.path.join(path_real, filename)
                # Attempt to remove the file
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except OSError as e:
                    print(f"Error deleting {file_path}: {e}")


    def break_text(self, text, max_width=74):
        words = text.split()  # Split the text into words
        lines = []
        current_line = ''

        for word in words:
            if len(current_line) + len(word) <= max_width:  # Check if adding the word exceeds max_width
                current_line += word + ' '  # Add the word to the current line
            else:
                lines.append(current_line.strip())  # Add the current line to the list of lines
                current_line = word + ' '  # Start a new line with the current word

        if current_line:
            lines.append(current_line.strip())  # Add the remaining line if any
        
        return '\n'.join(lines)  # Join the lines with newline characters
    
    def break_text_link(self, text, max_length):
        res = ''
        lines = []
        while len(text) > max_length:
            line, text = text[:max_length], text[max_length:]
            lines.append(line)
            res += '\n'+res
        lines.append(text)
        return res


    def assembleNameImagePost(self, id_client, id_post):
        image_name = "image"+str(id_post)+"_"+str(id_client)+".png"
        return image_name


    def generatePostImage(self, id_post, id_client, title, location, links, message):
        actual_directory = os.path.dirname(os.path.realpath(__file__))
        image= Image.open(actual_directory+'\\'+'template_job_V3.png')
        draw = ImageDraw.Draw(image)
        fontPath = 'font\\tahomabd.ttf'
        fonte = ImageFont.truetype(fontPath,25)
        colorText = "0,0,0,255"
        broken_text = self.break_text(message)
        broken_text = broken_text[:1025]
        broken_title= self.break_text(title)

        jobX = 45
        jobtY = 410
        job = self.break_text(title[:100])
        draw.text((jobX,jobtY), broken_title, font=fonte, fill=(0,0,0,255))

        textX = 45
        textY = 510
        link = broken_text[:100]
        draw.text((textX,textY), broken_text,font=fonte, fill=(0,0,0,255))

        linkX = 45 
        linkY = 220
        fonte_title = ImageFont.truetype(fontPath,25)

        #broken_links = self.break_text_link(links, 74)
        broken_links = 'Link no caption da imagem.'
        draw.text((linkX,linkY),broken_links,font=fonte_title, fill=(0,0,0,255))
        image_name = self.assembleNameImagePost(id_client, id_post)
        
        imagePath = actual_directory+"//post_created//"+image_name
        image.save(f""+imagePath)
        return image_name


    def createImagePostRevised(self):
        i=0
        self.delete_png_files('post_created')
        post = Post()
        session = Session(post.engine)
        stmt = post.PostRevised()
        for post1 in session.scalars((stmt)):
            PostCreated1 = PostCreated()
            PostCreated1.ID_POST = post1.ID_POST
            PostCreated1.ID_CLIENT = post1.ID_CLIENT
            PostCreated1.IMAGE_MESSAGE = post1.IMAGE_MESSAGE
            PostCreated1.MESSAGE = post1.MESSAGE
            PostCreated1.TITLE = post1.TITLE
            PostCreated1.LOCATION = post1.LOCATION 
            PostCreated1.LINK = post1.LINK
            PostCreated1.IMAGE_POST_NAME = post1.IMAGE_POST_NAME

            #message_image  = PostCreated1.IMAGE_MESSAGE
            message_image = ( PostCreated1.MESSAGE )
            
            #textsSize = len(post1.IMAGE_MESSAGE)
            imageName = self.generatePostImage(PostCreated1.ID_POST, PostCreated1.ID_CLIENT, PostCreated1.TITLE, PostCreated1.LOCATION, PostCreated1.LINK, message_image)
        
            PostCreated1.IMAGE_POST_NAME = imageName
            #message = ( PostCreated1.MESSAGE + "\n" + "\n" + PostCreated1.LINK + "\n" + "\n" + "\n" + "Curta, comente e compartilha.")
            
            if PostCreated1.MESSAGE.find("Curta, comente e compartilha.") == -1:
                print('entrou errado')
                message = ( PostCreated1.MESSAGE + "\n" + "\n" + "\n" + "Curta, comente e compartilha.")
            else:
                message = ( PostCreated1.MESSAGE )
            
            colunms = dict(IMAGE_POST_NAME=PostCreated1.IMAGE_POST_NAME, MESSAGE=message )
            where = " ID_POST= "+str(PostCreated1.ID_POST)+" AND CREATE_POST_AT IS NULL OR CREATE_POST_AT ='' "
            message_image=''
            message =''
            post.updateScript(PostCreated, colunms, where )
            
        print('posts gerados com sucesso.')

    def ad_jobToPost(self):
        jobs = job_ad()
        session = Session(jobs.engine)
        stmt = (jobs.query(JobAd, '', 'INSERT_AT DESC'))
        post = Post()
        
        for job in session.scalars((stmt)):
            print(job)

            postCreatedDict = dict(TITLE=job.TITLE, MESSAGE=job.MESSAGE, LINK=job.LINK)
            print("Extract with success...")
            
            post.insertScript(PostCreated, postCreatedDict)
            print("Insert with success...")


        print("Finish...")

        
    def exec_postInstagram(self, caption, image_url):
        """
        ad_jobToPost
        Function that extract ad_job rows and insert in Post.
        In the moment only extract and insert directly.
        Will have procedure that will rewrite the text by IA.
        """
        #ad_jobToPost()
        #createImagePostRevised()

        """
            Criar consulta de post para extrair e enviar para o instagram pela classe abaixo
        """

        """
        Loading environment variables.
        """
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
        """
        Object that connect api Facebook.
        """

        """
        gaf_facebook = GraphApiFacebook( OATH_FACEBOOK_CLIENT_ID, OATH_CLIENT_SECRET_TOKEN, APP_ID, PAGE_ACCESS_TOKEN )
        gaf_instagram = GraphApiFacebook( OATH_INSTAGRAM_CLIENT_ID, OATH_CLIENT_SECRET_TOKEN, APP_ID, PAGE_ACCESS_TOKEN )
        """


        #print(gaf.getIdPost('110793635453520_122143824452028277'))
        
        #print( gaf_facebook.getAllPosts() )
        #exit(0)
        #print(gaf.updatePost( '110793635453520_122143824452028277', "Nova tentativa 12:35 20 dez 23 test 2222", "https://developers.facebook.com/" ))
        #print(gaf.auth_url_client())
        #print(gaf.getPermissionsGrantedByUser())

        """
        now = datetime.now()
        post_facebook = gaf_facebook.createPost( caption, image_url, now, True )
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

if __name__=='__main__':
    
    postInstagram = PostInstagram()
    #postInstagram.ad_jobToPost()
    postInstagram.createImagePostRevised()
    print("Feito com sucesso")
    exit(0)
    #exec_postInstagram("Nova tentativa 12:35 20 dez 23 test 2222", os.getcwd()+"\post_created\image55_0.png")
    