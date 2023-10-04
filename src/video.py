import os

from googleapiclient.discovery import build


class Video:
    """Класс для получения статистики видео по его id"""
    api_key = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, id_video: str):
        """Инициализация атрибутов с предварительной проверкой валидности id видео"""
        self.id_video = id_video
        try:
            self.info_video = self.get_video_info(id_video)
        except LookupError:
            print("Видео id не существует.")
            self.info_video = self.title = self.url_video = self.watched_count = self.like_count = None
        else:
            self.info_video = self.get_video_info(id_video)
            self.title = self.info_video["snippet"]["title"]
            self.url_video = f"https://www.youtube.com/watch?v={self.id_video}"
            self.watched_count = self.info_video["statistics"]["viewCount"]
            self.like_count = self.info_video["statistics"]["likeCount"]

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
        """Метод для отображения информации об объекте класса для пользователей"""
        return self.title


class PLVideo(Video):
    """Саб-класс для получения данных по видеоролику в плейлисте"""
    def __init__(self, id_video: str, id_playlist: str):
        self.id_video = id_video
        self.playlist_videos = Video.get_service().playlistItems().list(playlistId=id_playlist,
                                                                        part='contentDetails',
                                                                        maxResults=250,
                                                                        ).execute()

        self.video_ids = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        if self.id_video in self.video_ids:
            super().__init__(id_video)
            self.id_playlist = id_playlist
        else:
            raise ValueError("В этом плейлисте видео не найдено")
