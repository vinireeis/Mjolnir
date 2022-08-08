#Mjolnir
from .stubs import stub_songs_treated_template, stub_songs_result_genius, stub_dynamodb_item

# Standards
from unittest.mock import patch

# Third party
import pytest


@pytest.mark.asyncio
@patch('src.services.artist.ArtistService._get_or_set_artist_songs_on_redis', return_value=stub_songs_treated_template)
async def test_when_success_to_get_artist_then_returns_ten_most_popular_songs(mock_get_or_set_on_redis, setup_artist_service):
    songs_treated_template = await setup_artist_service.get_ten_most_popular_songs()

    assert isinstance(songs_treated_template, dict)


@pytest.mark.asyncio
@patch('src.services.artist.ArtistService._get_or_set_artist_songs_on_redis', return_value=stub_songs_treated_template)
async def test_when_success_to_get_artist_then_returns_stub_correctly(mock_get_or_set_on_redis, setup_artist_service):
    songs_treated_template = await setup_artist_service.get_ten_most_popular_songs()

    song = songs_treated_template.get('top_ten_songs')[0]
    assert song.get("artist_name") == "Justin Bieber"
    assert song.get("title") == "Despacito (Remix)"
    assert song.get("full_title") == "Despacito (Remix) by Luis Fonsi & Daddy Yankee (Ft. Justin Bieber)"
    assert song.get("url_song") == "https://genius.com/Luis-fonsi-and-daddy-yankee-despacito-remix-lyrics"
    assert song.get("release_date") == "April 17, 2017"
    assert song.get("song_art_image_url") == "https://images.genius.com/4164dff756ddd455675789bd67fe5f1a.1000x1000x1.png"


@pytest.mark.asyncio
@patch('src.services.artist.ArtistService._get_or_set_artist_songs_on_redis', return_value=stub_songs_treated_template)
async def test_when_success_to_get_artist_then_mock_was_called(mock_get_or_set_on_redis, setup_artist_service):
    songs_treated_template = await setup_artist_service.get_ten_most_popular_songs()

    mock_get_or_set_on_redis.assert_called_once_with()


@pytest.mark.asyncio
@patch('src.services.artist.ArtistService._clean_up_redis_and_save_on_dynamo', return_value=stub_songs_treated_template)
async def test_when_success_to_get_artist_and_cache_false_then_returns_ten_most_popular_songs(
        mock_clean_up_redis_and_save_on_dynamo,
        setup_artist_service
):
    setup_artist_service.cache = False
    songs_treated_template = await setup_artist_service.get_ten_most_popular_songs()

    assert isinstance(songs_treated_template, dict)


@pytest.mark.asyncio
@patch('src.services.artist.ArtistService._clean_up_redis_and_save_on_dynamo', return_value=stub_songs_treated_template)
async def test_when_success_to_get_artist_and_cache_false_then_returns_stub_correctly(
        mock_clean_up_redis_and_save_on_dynamo,
        setup_artist_service
):
    setup_artist_service.cache = False
    songs_treated_template = await setup_artist_service.get_ten_most_popular_songs()

    song = songs_treated_template.get('top_ten_songs')[1]
    assert song.get("artist_name") == "Justin Bieber"
    assert song.get("title") == "I’m the One"
    assert song.get("full_title") == "I'm the One by DJ Khaled (Ft. Chance the Rapper, Justin Bieber, Lil Wayne & Quavo)"
    assert song.get("url_song") == "https://genius.com/Dj-khaled-im-the-one-lyrics"
    assert song.get("release_date") == "April 28, 2017"
    assert song.get("song_art_image_url") == "https://images.genius.com/6127733e5dbc43f75fcbf1b92e48a068.1000x1000x1.png"


@pytest.mark.asyncio
@patch('src.services.artist.ArtistService._clean_up_redis_and_save_on_dynamo', return_value=stub_songs_treated_template)
async def test_when_success_to_get_artist_and_cache_false_then_mock_was_called(
        mock_clean_up_redis_and_save_on_dynamo,
        setup_artist_service
):
    setup_artist_service.cache = False
    songs_treated_template = await setup_artist_service.get_ten_most_popular_songs()

    mock_clean_up_redis_and_save_on_dynamo.assert_called_once_with()


@pytest.mark.asyncio
@patch('src.services.artist.DynamodbRepository.put_items')
@patch('src.services.artist.MusicApi.get_ten_most_popular_musics_on_genius',
       return_value=stub_songs_result_genius)
@patch('src.services.artist.RedisRepository.delete')
async def test_when_cleanup_function_then_returns_treated_songs(mock_redis, mock_genius_api, mock_dynamodb, setup_artist_service):
    songs_treated_template = await setup_artist_service._clean_up_redis_and_save_on_dynamo()

    assert isinstance(songs_treated_template, dict)


@pytest.mark.asyncio
@patch('src.services.artist.DynamodbRepository.put_items')
@patch('src.services.artist.MusicApi.get_ten_most_popular_musics_on_genius',
       return_value=stub_songs_result_genius)
@patch('src.services.artist.RedisRepository.delete')
async def test_when_cleanup_function_then_mock_was_called(mock_redis, mock_genius_api, mock_dynamodb, setup_artist_service):
    songs_treated_template = await setup_artist_service._clean_up_redis_and_save_on_dynamo()

    mock_redis.assert_called_once_with(key='12345')
    mock_genius_api.assert_called_once_with(artist_id=12345)
    mock_dynamodb.assert_called_once()
