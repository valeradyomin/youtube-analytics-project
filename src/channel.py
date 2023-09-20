import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.get_channel_info(channel_id)
        self.title = self.channel['snippet']["title"]
        self.description = self.channel['snippet']["description"]
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscribers = self.channel["statistics"]["subscriberCount"]
        self.video_count = self.channel["statistics"]["videoCount"]
        self.view_count = self.channel["statistics"]["viewCount"]

    def __str__(self):
        """метод для отображения информации об объекте класса для пользователей"""
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """метод для операции сложения"""
        return int(self.subscribers) + int(other.subscribers)

    def __sub__(self, other):
        """метод для операции вычитания"""
        return int(self.subscribers) - int(other.subscribers)

    def __gt__(self, other):
        """метод для операции сравнения «больше»"""
        return int(self.subscribers) > int(other.subscribers)

    def __ge__(self, other):
        """метод для операции сравнения «больше или равно»"""
        return int(self.subscribers) >= int(other.subscribers)

    def __lt__(self, other):
        """метод для операции сравнения «меньше»"""
        return int(self.subscribers) < int(other.subscribers)

    def __le__(self, other):
        """метод для операции сравнения «меньше или равно»"""
        return int(self.subscribers) <= int(other.subscribers)

    def __eq__(self, other):
        """метод для операции равенства / идентичности"""
        return int(self.subscribers) == int(other.subscribers)

    @property
    def channel_id(self):
        """Геттер приватного атрибута класса"""
        return self.__channel_id

    @classmethod
    def get_channel_info(cls, channel_id: str) -> dict:
        """Получает информацию о канале по его ID."""
        response = cls.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        return response['items'][0]

    @classmethod
    def get_service(cls):
        """Класс-метод возвращающий объект для работы с YouTube API."""
        return cls.youtube

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    def to_json(self, file_name):
        """Метод сохраняющий в файл значения атрибутов экземпляра Channel."""
        channel_info = {
            "channel_id": self.__channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscribers": self.subscribers,
            "videoCount": self.video_count,
            "viewCount": self.view_count,
        }

        json_data = json.dumps(channel_info, indent=2, ensure_ascii=False)

        with open(file_name, "w", encoding="UTF-8") as outfile:
            outfile.write(json_data)
