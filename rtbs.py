from typing import Final

# Load libraries for environ
from os import getenv
from os.path import join, dirname
from dotenv import load_dotenv

# Load libraries for API request
import requests
from requests_oauthlib import OAuth1Session

# Load libraries for parsing JSON
import json
import urllib.parse
from datetime import datetime
import time

# Load libraries for loop
import asyncio

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


DISCORD_HOOK_URL: Final[str] = getenv("DISCORD_HOOK_URL")
TW_KEY: Final[str] = getenv("TWITTER_API_KEY")
TW_SECRET: Final[str] = getenv("TWITTER_API_SECRET")
TW_TOKEN: Final[str] = getenv("TWITTER_ACCESS_TOKEN")
TW_TOKEN_SECRET: Final[str] = getenv("TWITTER_ACCESS_SECRET")

twitter = OAuth1Session(
    TW_KEY,
    client_secret=TW_SECRET,
    resource_owner_key=TW_TOKEN,
    resource_owner_secret=TW_TOKEN_SECRET,
)

headers = {"Content-Type": "application/json"}
skip_author = {"re__apt", "ReApt_JP", "ptcm_order"}

url = "https://api.twitter.com/1.1/search/tweets.json"
word_tuple = (
    '"reapt"',
    '"Re:Apt"',
    '"リアプト"',
    '"りあぷと"',
)
query = urllib.parse.quote(" OR ".join(word_tuple))


def main(start, loop):
    start = int(start)
    print(f"ID {start} 以降のツイートを検索します")
    params = {
        "q": query,
        "count": 15,
        "result_type": "recent",
        "lang": "ja",
        "since_id": start,
    }

    response = twitter.get(url, params=params)
    r_json = response.json()

    if response.status_code == 200:
        if len(r_json["statuses"]) > 0:
            for i in r_json["statuses"]:
                if i["user"]["screen_name"] not in skip_author:
                    profile_url = "https://twitter.com/" + i["user"]["screen_name"]
                    tweet_url = "https://twitter.com/{}/status/{}".format(
                        i["user"]["screen_name"], i["id_str"]
                    )
                    timestamp = datetime.strptime(
                        i["created_at"], "%a %b %d %H:%M:%S %z %Y"
                    )
                    timestamp = timestamp.strftime("%Y-%m-%dT%H:%M:%S.000Z")
                    content = {
                        "embeds": [
                            {
                                "title": "URL",
                                "url": tweet_url,
                                "author": {
                                    "name": i["user"]["name"],
                                    "url": profile_url,
                                    "icon_url": i["user"]["profile_image_url_https"],
                                },
                                "description": i["text"],
                                "timestamp": timestamp,
                            },
                        ]
                    }
                    discord_content = json.dumps(content)
                    return_msg = requests.post(
                        DISCORD_HOOK_URL, discord_content, headers=headers
                    )
                    time.sleep(0.5)
                    print(f"Discordに送信しました。ステータスは: {return_msg} です。")
                else:
                    print("指定外のツイートです")
            start = r_json["statuses"][0]["id_str"]
            with open("tmp.txt", mode="w", encoding="ascii") as f:
                f.write(start)
        else:
            print("検索しましたが、新しいツイートはありませんでした")
    else:
        print("An error was happend:{}".format(response.status_code))
    loop.call_later(15, main, start, loop)


loop = asyncio.get_event_loop()
with open("tmp.txt", mode="r", encoding="ascii") as f:
    start = int(f.read())

loop.call_soon(main, start, loop)

try:
    loop.run_forever()
finally:
    loop.close()
