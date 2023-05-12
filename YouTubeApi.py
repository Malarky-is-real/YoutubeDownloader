import os

from googleapiclient.discovery import build
import googleapiclient.errors

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyAGecwOgVA0LtY0SiZUqu7eOvdJdVKHWuQ"
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = DEVELOPER_KEY)

# Get credentials and create an API client
def getTitle(vidID):
    video_request=youtube.videos().list(
        part='snippet,statistics',
        id = vidID
    )
    video_response = video_request.execute()
 
    title = video_response['items'][0]['snippet']['title']
    return title

 




