import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
TWILIO_SID = "ACed5df2a47608307b03721b0d454de79c"
TWILIO_AUTH = "168372aaae63d565211ca24fff8fc366"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "VKVJHVDCG3APMPUE"
NEWS_API = "3459232313d7496a8c75932221b73f20"

# stock parameters
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday = data_list[1]
day_before_closing = day_before_yesterday["4. close"]

difference = float(yesterday_closing_price) - float(day_before_closing)
up_down = None
if difference > 0:
    up_down = "🔺️"
else:
    up_down = "🔻️"

percentage_difference = round(difference / float(yesterday_closing_price) * 100)

if abs(percentage_difference) > 1:
    news_parameters = {
        "q": "tesla",
        "apiKey": NEWS_API,
    }
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]

    formatted_articles = [f"{STOCK_NAME}: {up_down}{percentage_difference}%\nHeadline: {article['title']}" for article
                          in three_articles]
    print(formatted_articles)

    client = Client(TWILIO_SID, TWILIO_AUTH)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=TWILIO_NO,
            to=MY_NO,
        )

