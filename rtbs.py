import json
import asyncio
from requests_oauthlib import OAuth1Session
import requests
import urllib.parse
from datetime import datetime
import time

ENVIRON = getenv("REAPT_EGOSEARCH_ENV").split(";")
discord_hook = ENVIRON[0]
twitter = OAuth1Session(
    ENVIRON[1],
    client_secret=ENVIRON[2],
    resource_owner_key=ENVIRON[3],
    resource_owner_secret=ENVIRON[4],
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
    print(query)
    start = int(start)
    print(start)
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
        """
        with open("response.json", mode="w", encoding="utf-8") as f:
            json.dump(
                r_json,
                f,
                ensure_ascii=False,
                indent=4,
                sort_keys=True,
                separators=(",", ": "),
            )
        """
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
                        discord_hook, discord_content, headers=headers
                    )
                    time.sleep(0.5)
                    print(return_msg)
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
