class MusicService:
    def __init__(self, artist_validated):
        self.artist_id = artist_validated.get("artist_id")
        self.cache = artist_validated.get("cache")


    def get_ten_most_popular_songs