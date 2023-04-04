from flask import render_template, request, Blueprint ,jsonify, abort, make_response
from dateutil.relativedelta import relativedelta

import datetime
import requests

from stockapp.search import parser1 as psr
from stockapp.search import utils

search = Blueprint('search', __name__, static_folder='static', template_folder='templates')

api_tiingo_token = "a645fee24b4c7ff5222ad0b26aa9b8819d6788df"
news_api_token = 'f6e2b246217741269a0fa6542cbf9521'
app_error_msg = "Error : No record has been found, please enter a valid symbol."

@search.route("/stock_servise", methods=["GET"])
def stock_service():
    return render_template("stock_service.html")

@search.route("/stock/api/v1.0/outlook/<ticker>", methods=["GET"])
def company_outlook(ticker):
    if not utils.is_valid_ticker(ticker):
        return abort(404)
    meta_endpoint_api = "https://api.tiingo.com/tiingo/daily/" + ticker
    query_params = {"token": api_tiingo_token}
    response = requests.get(meta_endpoint_api, params=query_params)
    # print(response.status_code)
    # print(response.json())
    if response.status_code == requests.codes.ok:
        parsed_response = psr.parse_company_outlook(response.json())
        if parsed_response["parsing"] == False:
            return utils.parse_outlook_error()
        else:
            return utils.append_endpoints(parsed_response, ticker)
    else:
        return abort(404)

@search.route("/stock/api/v1.0/summary/<ticker>", methods=["GET"])
def stock_summary(ticker):
    if not utils.is_valid_ticker(ticker):
        return abort(404)
    top_of_book_api = "https://api.tiingo.com/iex/" + ticker
    query_params = {"token": api_tiingo_token}
    response = requests.get(top_of_book_api, params=query_params)
    if response.status_code == requests.codes.ok:
        parsed_response = psr.parse_stock_summary(response.json()[0])
        if parsed_response["parsing"] == False:
            return utils.parse_stock_summary_error()
        else:
            return utils.append_endpoints(parsed_response, ticker)
    else:
        return abort(404)


@search.route("/stock/api/v1.0/chart/<ticker>", methods=["GET"])
def chart(ticker):
    if not utils.is_valid_ticker(ticker):
        return abort(404)
    historical_endpoint_api = "https://api.tiingo.com/iex/" + ticker + "/prices"
    six_month_prior_date = str(datetime.date.today() - relativedelta(months=6))
    query_params = {
        "startDate": six_month_prior_date,
        "resampleFreq": "12hour",
        "columns": "open,high,low,close,volume",
        "token": api_tiingo_token
    }
    response = requests.get(historical_endpoint_api, params=query_params)
    if response.status_code == requests.codes.ok:
        parsed_response = psr.parse_chart(response.json())
        if parsed_response["parsing"] == False:
            return utils.parse_chart_values_error()
        else:
            return utils.append_endpoints(parsed_response, ticker)
    else:
        return abort(404)

@search.route("/stock/api/v1.0/news/<ticker>", methods=["GET"])
def news(ticker):
    if not utils.is_valid_ticker(ticker):
        return abort(404)
    news_api = "https://newsapi.org/v2/everything"

    page = 1
    news_articles = {}
    news_articles["articles"] = []

    while True:
        query_params = {
            "apiKey": news_api_token,
            "q": ticker,
            "page": page
        }

        response = requests.get(news_api, params=query_params)

        if response.status_code == requests.codes.ok:
            piece_response = psr.parse_news(response.json())
            if piece_response["parsing"] == False:
                return utils.parse_news_error()
                
            for article in piece_response["articles"]:
                news_articles["articles"].append(article)
                if len(news_articles["articles"]) == 5:
                    return utils.append_endpoints(news_articles, ticker) # all articles found!
            page = page + 1
        else:
            if len(news_articles["articles"]) == 0:
                return utils.return_news_error() # no articles found
            else:
                return utils.append_endpoints(news_articles, ticker) # some (< 5) articles found
