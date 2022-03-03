try:
    import json
    from decouple import config
    from pushbullet import Pushbullet
    from requests import get
    from bs4 import BeautifulSoup as Bfs
except ModuleNotFoundError:
    print("Missing library")
