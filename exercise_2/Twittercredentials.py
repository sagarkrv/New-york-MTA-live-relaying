import tweepy

consumer_key = "Glu9EiLpkRC53SjiSnUok61lk";
#eg: consumer_key = "YisfFjiodKtojtUvW4MSEcPm";


consumer_secret = "VdPvfM2NgAK1rt9Cd8uyWd6Fir1CNs1lwu9Am8aQE8XlsoaWAg";
#eg: consumer_secret = "YisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPm";

access_token = "928428833476313088-5vt6Db05MJ9cNtJqLu1NVnjnzl9huoC";
#eg: access_token = "YisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPm";

access_token_secret = "6lsRK0iJKtO1lrRjG4L4zrxl7gQf69tQK9rDjFL83KtRS";
#eg: access_token_secret = "YisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPm";


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

