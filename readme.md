# GENCON & LORCANA

Within this repository, there are currently two different scripts utilitizing the same core base functionality with selenium.

[Lorcana](https://github.com/mriffey1/gencon/tree/master/lorcana)</br>
This script utilizies pickle to "login" into my account, and proceeds to open each link in the database, get the available tickets (if any), tweets if tickets are available, and then updates the database once a new tweet for that event has gone out. </br>
<b>Language:</b> Python 3.10.8</b></br>
<b>Libraries:</b> [selenium](https://pypi.org/project/selenium/), pickle (built-in), [mysql-connector-python](https://pypi.org/project/mysql-connector-python/), [python-dotenv](https://pypi.org/project/python-dotenv/), [tweepy](https://pypi.org/project/tweepy/), datetime (built-in).

<img src="image.png" alt="Image of tweet for a Lorcana event" width="450">
