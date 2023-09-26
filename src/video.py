import os

from googleapiclient.discovery import build


class Video:
    api_key = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, id_video: str):
        self.id_video = id_video
        self.info_video = self.get_video_info(id_video)
        self.title_video = self.info_video["snippet"]["title"]
        self.url_video = f"https://www.youtube.com/watch?v={self.id_video}"
        self.watched_count = self.info_video["statistics"]["viewCount"]
        self.liked_count = self.info_video["statistics"]["likeCount"]

    @classmethod
    def get_service(cls):
        return cls.youtube

    @classmethod
    def get_video_info(cls, id_video: str):
        """Получает информацию о видео по его ID."""
        video_response = cls.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                         id=id_video).execute()
        return video_response['items'][0]

    def __str__(self):
        return self.title_video



