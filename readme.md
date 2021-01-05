# RTBS(Re:Apt Twitter Bot System)

The Japanese documentation is under the English version. / 日本語版は下にあります。

## English Version

### What's this?

This script notify new tweets including specific keywords to the Discord Web Hook.

### Technology used

- Python 3.8 or later
- asyncio
- requests
- oauthlib
- dotenv

### Initial Configuration

1. Make a venv: `python3 -m venv rtbs`
1. Activate the venv: `source ./rtbs/bin/activate`
1. Install packages: `python3 -m pip install -r require.txt`
1. Make a text file named `.env`, and write tokens between double quotations:

```python:
DISCORD_HOOK_URL=""
TWITTER_API_KEY=""
TWITTER_API_SECRET=""
TWITTER_ACCESS_TOKEN=""
TWITTER_ACCESS_TOKEN_SECRET=""
```

5. add search queries to the tuple on line 44 like this:

```
url = "https://api.twitter.com/1.1/search/tweets.json"
word_tuple = (
'"word1"',
'"word2"',
)
```

6. If you want to skip tweets by specific users, add screen names to the set on line 41 like this:

```
skip_authors = {"user1", "user2"}
```

### How to use

1. Activate the venv: `source ./rtbs/bin/activate`
1. Run the script: `python3 rtbs.py`

## 日本語版

### このスクリプトについて

Discord の Web Hook にあるキーワードを含むツイートを通知するスクリプト

### 使用技術

- Python 3.8 以降
- asyncio
- requests
- oauthlib
- dotenv

### 初期設定

1. Python の venv を作成する: `python3 -m venv rtbs`
1. venv を有効化する: `source ./rtbs/bin/activate`
1. パッケージを導入する: `python3 -m pip install -r require.txt`
1. `.env`という名前のファイルを作成し、ダブルクオーテーション内に対応するトークン類を入れて書き込む:

```python:
DISCORD_HOOK_URL=""
TWITTER_API_KEY=""
TWITTER_API_SECRET=""
TWITTER_ACCESS_TOKEN=""
TWITTER_ACCESS_TOKEN_SECRET=""
```

5. 44 行目のタプルに検索したい単語を以下のように追加する:

```
url = "https://api.twitter.com/1.1/search/tweets.json"
word_tuple = (
'"word1"',
'"word2"',
)
```

6. 特定のユーザーのツイートを除外したい場合、以下のように 41 行目の集合に追加する

```
skip_authors = {"user1", "user2"}
```

### 使い方

1. venv を有効化する: `source ./rtbs/bin/activate`
1. 実行する: `python3 rtbs.py`
