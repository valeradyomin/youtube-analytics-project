import os
import isodate
import datetime
from googleapiclient.discovery import build


class PlayList:
    api_key = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        """Инициализирует объект класса"""
        self.playlist_id = playlist_id
        self.channel_playlists = self.get_channel_playlists()
        self.playlist = self.get_playlist()
        self.title = self.playlist["snippet"]["title"]
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    def get_channel_playlists(self):
        """Получает список плейлистов канала"""
        playlist_response = self.youtube.playlistItems().list(part='snippet', playlistId=self.playlist_id).execute()
        channel_id = playlist_response['items'][0]['snippet']['channelId']
        channel_playlists = self.youtube.playlists().list(channelId=channel_id,
                                                          part='contentDetails,snippet',
                                                          maxResults=50,
                                                          ).execute()
        return channel_playlists['items']

    def get_playlist(self):
        """Получает информацию о плейлисте"""
        for playlist in self.channel_playlists:
            if playlist["id"] == self.playlist_id:
                return playlist

    def get_playlist_videos_id(self):
        """Получает идентификаторы видео в плейлисте"""
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        return video_ids

    @property
    def total_duration(self):
        """Возвращает общую продолжительность плейлиста"""
        video_ids = self.get_playlist_videos_id()
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()

        total_duration = datetime.timedelta()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        """Возвращает ссылку на видео с наибольшим количеством лайков в плейлисте"""
        video_ids = self.get_playlist_videos_id()
        best_likes_count = 0
        best_video_id = None
        for video_id in video_ids:
            video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                        id=video_id
                                                        ).execute()
            like_count = video_response['items'][0]['statistics']['likeCount']
            if int(like_count) > int(best_likes_count):
                best_likes_count = like_count
                best_video_id = video_id
        return f"https://youtu.be/{best_video_id}"
