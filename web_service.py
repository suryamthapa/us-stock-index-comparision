from flask import Flask
from flask import request
from flask import jsonify, make_response, render_template
import numpy as np

from datetime import datetime, timezone
from db_table import db_table

app = Flask(__name__)

# Set up db connection


def get_db_conn():
    db_schema = {
        "Date": "BIGINT PRIMARY KEY",
        "SNP500": "float",
        "NASDAQ": "float",
        "FTSE100": "float",
    }
    return db_table("Stocks", db_schema)


@app.route('/compare-stocks', methods=["GET"])
def compare_stocks():
    try:
        db = get_db_conn()
        # Making sure we have all the arguments we need
        if not request.args.get("start_date"):
            return make_response(jsonify({"message": "Invalid start date"}), 400)
        if not request.args.get("end_date"):
            return make_response(jsonify({"message": "Invalid end date"}), 400)

        start = request.args.get("start_date")
        end = request.args.get("end_date")

        # Convert datetime to Unix timestamp to index into DB
        start = datetime.strptime(
            start, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp()
        end = datetime.strptime(
            end, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp()

        if start > end:
            return make_response(jsonify({"message": "Start date cannot be greater than end date"}), 400)

        results = db.select_prices_between_dates(start, end, "SNP500")
        snp500_data = {}
        snp500_numpy_array = []
        for result in results:
            date = str(datetime.fromtimestamp(result[0], timezone.utc))
            price = result[1] or -1
            if price == -1:
                continue
            snp500_data[date[:-9]] = price
            snp500_numpy_array.append(price)

        snp500_mean = np.mean(snp500_numpy_array).astype(float)
        snp500_variance = np.var(snp500_numpy_array).astype(float)

        results = db.select_prices_between_dates(start, end, "NASDAQ")
        nasdaq_data = {}
        nasdaq_numpy_array = []
        for result in results:
            date = str(datetime.fromtimestamp(result[0], timezone.utc))
            price = result[1] or -1
            if price == -1:
                continue
            nasdaq_data[date[:-9]] = price
            nasdaq_numpy_array.append(price)

        nasdaq_mean = np.mean(nasdaq_numpy_array).astype(float)
        nasdaq_variance = np.var(nasdaq_numpy_array).astype(float)

        results = db.select_prices_between_dates(start, end, "FTSE100")
        ftse100_data = {}
        ftse100_numpy_array = []
        for result in results:
            date = str(datetime.fromtimestamp(result[0], timezone.utc))
            price = result[1] or -1
            if price == -1:
                continue
            ftse100_data[date[:-9]] = price
            ftse100_numpy_array.append(price)

        ftse100_mean = np.mean(ftse100_numpy_array).astype(float)
        ftse100_variance = np.var(ftse100_numpy_array).astype(float)

        return_data = {
            "start_date": start,
            "end_date": end,
            "SNP500_mean": round(snp500_mean, 2),
            "SNP500_variance": round(snp500_variance, 2),
            "NASDAQ_mean": round(nasdaq_mean, 2),
            "NASDAQ_variance": round(nasdaq_variance, 2),
            "FTSE100_mean": round(ftse100_mean, 2),
            "FTSE100_variance": round(ftse100_variance, 2)
        }

        return make_response(jsonify(return_data), 200)
    except Exception as error:
        return make_response(jsonify({"message": str(error)}), 400)


@app.route('/')
def index():
    return render_template('index.html')


app.run(port=8080)
