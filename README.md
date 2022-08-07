## Mjolnir Rest Api

### **Technologies/Frameworks/Libs used:**

- Flask[async]
- hypercorn - server client for flask async
- pydantic - data validation
- loguru - logs
- python-decouple - files .env
- httpx - to send requests
- aioredis - async data cache
- aioboto3 - to use async DynamoDB
- GeniusAPI - API consumption
- pytest-asyncio e unittest - unit tests

### Step one
#### create a virtual environment
Create and start a virtual env for the project. 

- To create the virtual environment, run:
```bash
python3 -m venv env
```
- To activate the virtual environment run:

    Linux:
    ```bash
    source env/bin/activate
    ```
    Windows:
    ```shell
    env\Scripts\activate.bat
    ```

### Step two
#### Installation of dependencies
1. __Install the packages in the virtual environment from the following command:__
    
    ```bash
    pip install -r requirements.txt
    ```  
    __or if you are going to run the tests:__
    ```bash
    pip install -r requirements-dev.txt
    ``` 

### Step three
#### Create environment variables

1. Create a `.env` file in the project root, following this template:

~~~
GENIUS_CLIENT_ACCESS_TOKEN=FILL_THIS_WITH_YOUR_TOKEN
GENIUS_API_BASE_URL=api.genius.com
GENIUS_MUSICS_PER_PAGE=10
GENIUS_SORTED="popularity"
REDIS_HOST=FILL_THIS_WITH_REDIS_HOST
REDIS_DATA_EXPIRATION_IN_SECONDS=FILL_THIS_WITH_TIME_EXPIRATION_IN_SECONDS
AWS_ACCESS_KEY_ID=FILL_THIS_WITH_YOUR_KEY
AWS_SECRET_ACCESS_KEY=FILL_THIS_WITH_YOUR_SECRET_KEY
AWS_REGION_NAME=FILL_THIS_WITH_AWS_REGION
AWS_TABLE_NAME=FILL_THIS_WITH_TABLE_NAME
~~~

#### **Endpoint:**

## `/top-songs/<int:artist_id>`

> _Endpoint to get the 10 most popular songs by a given artist_

## Requisition

#### **request template:**

**Route HTTP:** `http:{host}/top-songs/357`

> _Artist id must be informed at the end of the route /top-songs/artistid_

**no request body required:**

## Response

#### **response template:**

```json
{
  "result": ["list of the ten most popular songs"],
  "message": "message to detail certain responses",
  "success": "request success, True or False",
  "internal_code": "internal code possibilities just below"
}
```

**internal_code available:**

- **SUCCESS:**
  Code: 0
- **INVALID_PARAMS:**
  Code: 10
- **PARTNERS_ERROR:**
  Code: 21
- **DATA_NOT_FOUND:**
  Code: 99
- **INTERNAL_SERVER_ERROR:**
  Code: 100

#### **it's possible to provide a query_string for caching on Redis:**

**Options**

- False
- True

`http:{host}/top-songs/357?cache=False`

## Example

#### Request:

`http:{host}/top-songs/357`

#### Response:

```json
{
    "result": {
        "top_ten_songs": [
            {
                "artist_name": "Justin Bieber",
                "title": "Despacito (Remix)",
                "full_title": "Despacito (Remix) by Luis Fonsi & Daddy Yankee (Ft. Justin Bieber)",
                "url_song": "https://genius.com/Luis-fonsi-and-daddy-yankee-despacito-remix-lyrics",
                "release_date": "April 17, 2017",
                "song_art_image_url": "https://images.genius.com/4164dff756ddd455675789bd67fe5f1a.1000x1000x1.png"
            },
            {
                "artist_name": "Justin Bieber",
                "title": "I’m the One",
                "full_title": "I'm the One by DJ Khaled (Ft. Chance the Rapper, Justin Bieber, Lil Wayne & Quavo)",
                "url_song": "https://genius.com/Dj-khaled-im-the-one-lyrics",
                "release_date": "April 28, 2017",
                "song_art_image_url": "https://images.genius.com/6127733e5dbc43f75fcbf1b92e48a068.1000x1000x1.png"
            },
            {
                "artist_name": "Justin Bieber",
                "title": "Love Yourself",
                "full_title": "Love Yourself by Justin Bieber",
                "url_song": "https://genius.com/Justin-bieber-love-yourself-lyrics",
                "release_date": "November 13, 2015",
                "song_art_image_url": "https://images.genius.com/c48eb30caab693c9a80f49610e2ddb24.1000x1000x1.png"
            },
            {
                "artist_name": "Justin Bieber",
                "title": "Let Me Love You",
                "full_title": "Let Me Love You by DJ Snake (Ft. Justin Bieber)",
                "url_song": "https://genius.com/Dj-snake-let-me-love-you-lyrics",
                "release_date": "August 4, 2016",
                "song_art_image_url": "https://images.genius.com/073cd0dbdf330c416680c3705d09270a.1000x1000x1.jpg"
            },
            {
                "artist_name": "Justin Bieber",
                "title": "Sorry",
                "full_title": "Sorry by Justin Bieber",
                "url_song": "https://genius.com/Justin-bieber-sorry-lyrics",
                "release_date": "October 23, 2015",
                "song_art_image_url": "https://images.genius.com/ddab64aa5e55030c98e4979aef0bea20.1000x1000x1.png"
            },
            {
                "artist_name": "Justin Bieber",
                "title": "Baby",
                "full_title": "Baby by Justin Bieber (Ft. Ludacris)",
                "url_song": "https://genius.com/Justin-bieber-baby-lyrics",
                "release_date": "January 18, 2010",
                "song_art_image_url": "https://images.genius.com/08d71b1c1d0ecb9c572f210a1054a091.1000x1000x1.png"
            },
            {
                "artist_name": "Justin Bieber",
                "title": "Yummy",
                "full_title": "Yummy by Justin Bieber",
                "url_song": "https://genius.com/Justin-bieber-yummy-lyrics",
                "release_date": "January 3, 2020",
                "song_art_image_url": "https://images.genius.com/61c2d3aa55989ff06133493a22c5516a.1000x1000x1.png"
            },
            {
                "artist_name": "Ariana Grande & Justin Bieber",
                "title": "Stuck with U",
                "full_title": "Stuck with U by Ariana Grande & Justin Bieber",
                "url_song": "https://genius.com/Ariana-grande-and-justin-bieber-stuck-with-u-lyrics",
                "release_date": "May 8, 2020",
                "song_art_image_url": "https://images.genius.com/15e6a3512e6b2196a70701d65d648267.1000x1000x1.png"
            },
            {
                "artist_name": "Lil Dicky",
                "title": "Earth",
                "full_title": "Earth by Lil Dicky",
                "url_song": "https://genius.com/Lil-dicky-earth-lyrics",
                "release_date": "April 18, 2019",
                "song_art_image_url": "https://images.genius.com/d2ffd9d11a2feaeabc74905deeb6bc90.1000x1000x1.png"
            },
            {
                "artist_name": "Justin Bieber",
                "title": "As Long As You Love Me",
                "full_title": "As Long As You Love Me by Justin Bieber (Ft. Big Sean)",
                "url_song": "https://genius.com/Justin-bieber-as-long-as-you-love-me-lyrics",
                "release_date": "June 11, 2012",
                "song_art_image_url": "https://images.genius.com/e03688b4a1a566ce88283e682bdb95e4.1000x1000x1.jpg"
            }
        ]
    },
    "message": null,
    "success": true,
    "internal_code": 0
```
