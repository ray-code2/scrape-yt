import os
from dotenv import load_dotenv

load_dotenv()
from googleapiclient.discovery import build
from utils.comment import process_comment, make_csv

API_KEY = os.getenv("API_KEY")
DEVELOPER_KEY = "YOUR_API_KEY"

youtube = build(
        "youtube", "v3", developerKey = API_KEY)

def commentthreads(channelID , to_csv=False):
    comments_list = []
    request = youtube.commentThreads().list(
      part='replies,snippet',
      videoId=channelID,
    )
    response = request.execute()
    comments_list.extend(process_comment(response['items']))
    #print(len(response['items']))
    while response.get('nextPageToken', None):
        request = youtube.commentThreads().list(
        part='replies,snippet',
        videoId=channelID,
        pageToken=response['nextPageToken']
        )
        response = request.execute()
        comments_list.extend(process_comment(response['items']))
    print(f"Tahap Pengambilan data berhasil untuk video {channelID}. terdapat {len(comments_list)} komentar ditemukan")
    if to_csv:
        make_csv(comments_list , channelID)

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    commentthreads('3iyHbndUxo0',to_csv=True) #video id yang mau di ambil komentarnya
   
   


if __name__ == "__main__":
    main()