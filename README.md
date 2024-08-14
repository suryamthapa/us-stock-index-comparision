# US stock index comparision site

Available indexes for comparision are:
- S&P 500
- NASDAQ
- FTSE 100

To scrape and save the data.
```bash
$ python scrape.py
```

To run the web server.
```bash
$ export FLASK_APP=web_service.py
$ export FLASK_RUN_PORT=8080
$ flask run
```
