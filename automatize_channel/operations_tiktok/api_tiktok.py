import sys
import os
from dotenv import load_dotenv

from Tiktok_Uploader import uploadVideo

class ApiTikTok:

    def __init__(self, id_client, client, access, host):
        self.id_client = id_client
        self.client = client
        self.access = access
        self.host = host

    def authTikTok():
        pass

    def uploadImage(session_id, file, title, tags):
        pass

    def uploadVideos(session_id, file, title, tags):
        uploadVideo(session_id, file, title, tags, verbose=True)


if __name__=='__main__':
    load_dotenv()
    