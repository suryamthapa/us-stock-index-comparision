# US stock index comparision site

Available indexes for comparision are:
- S&P 500
- NASDAQ
- FTSE 100

Screenshots
![image](https://github.com/user-attachments/assets/9d1ec138-bd1c-4ef0-83ca-d814a93a2ed9)

![image](https://github.com/user-attachments/assets/3cf301b8-8b66-4b28-b661-4a80708a153e)

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
