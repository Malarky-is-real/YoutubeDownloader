import os
from googleapiclient.discovery import build


class YT_API():
 
    def __init__(self) -> None:
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"
        DEVELOPER_KEY = "AIzaSyAGecwOgVA0LtY0SiZUqu7eOvdJdVKHWuQ"
        self.youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)
            
    
    # Get credentials and create an API client
    def getTitle(self, vidID):
        video_request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id = vidID
        )
        video_response = video_request.execute()
        title = video_response['items'][0]['snippet']['title']  
        return title


    def getAuthor(self, vidID):
        video_request= self.youtube.videos().list(
            part='snippet,statistics',
            id = vidID
        )
        video_response = video_request.execute()
        print(video_response)
        author = video_response['items'][0]['snippet']['channelTitle']  
        return author 

