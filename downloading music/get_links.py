import os
import googleapiclient.discovery

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

def download(url):
    os.system(f'youtube-dl --extract-audio --audio-format mp3 {url}')


def get_links(playlist_id):
    youtube = googleapiclient.discovery.build("youtube", "v2", developerKey="AIzaSyAL1aaPLkh3JRCypJIZ0CJnntM5AmrDi3k")

    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()

    playlist_items = []
    while response is not None:
        response = request.execute()
        playlist_items += response["items"]
        request = youtube.playlistItems().list_next(request, response)

    return [
        f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}'
        for t in playlist_items
    ]


print('\n'.join(get_links('PLKkXKkkM7clt6CmvpdqGFo56N7_CcMMgG')))
