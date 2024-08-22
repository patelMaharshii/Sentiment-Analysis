"""

Maharshii Patel
251353283
mpate588
This file has the following functions: reading TSV files(keyword files), reading CSV files(reading tweets), 
removing all characters all non-alphabetical characters other than spaces and replacing uppercase letters with
lowercase letters in a string, calculating the sentiment value of a string, classifying whether that sentiment is 
positive, neutral, or negative, putting all the information gathered from the TSV and CSV into a dictionary, and
writing that information onto a txt document which acts as a report.

"""


def read_keywords(keyword_file_name):  # Reads the words from a TSV files and puts it into a dictionary
    try:
        with open(keyword_file_name, "r") as text:
            lines = text.readlines()
            my_dict = {}

            for line in lines:
                line = line.split("\t")
                my_dict[line[0]] = int(line[1].removesuffix("\n"))

            return my_dict  # Word will be key and sentimental score of word will be value

    except IOError:  # If file doesn't exist, then it will be said in output and returns an empty dictionary
        print("Could not open file {}!".format(keyword_file_name))
        return {}


def clean_tweet_text(tweet_text):
    # This function takes a string and turns all uppercase letters into lowercase and removes all non-alphabetical
    # letters except spaces and returns that final string
    new_text = ""

    for char in tweet_text:
        if char.isalpha():
            new_text += char.lower()
        elif char == " ":
            new_text += " "
        else:
            continue

    return new_text


def calc_sentiment(tweet_text, keyword_dict):
    # Calculates the sentiment value by seeing if a word from a tweet is also a keyword and if it is, then its
    # sentiment score is added to the total sentiment score and that value is returned
    total_sentiment = 0
    tweet_text = tweet_text.split()

    for word in tweet_text:
        if word in keyword_dict:
            total_sentiment += keyword_dict[word]

    return total_sentiment


def classify(score):
    # returns positive, negative, or neutral if the sentiment score is greater than 0, less than 0, or equal to 0
    if score > 0:
        return "positive"
    elif score < 0:
        return "negative"
    else:
        return "neutral"


def read_tweets(tweet_file_name):
    # This function returns a list of dictionaries and each dictionary contains all information for 1 tweet
    try:
        with open(tweet_file_name, "r") as text:
            lines = text.readlines()
            my_arr = []

            for line in lines:  # Creates the list of dictionaries
                line = line.split(",")
                line[-1] = line[-1].removesuffix("\n")
                my_dict = {'date': line[0], 'text': clean_tweet_text(line[1]), 'user': line[2], 'retweet': int(line[3]),
                           'favorite': int(line[4]), 'lang': line[5], 'country': line[6], 'state': line[7],
                           'city': line[8]}

                if line[9] == 'NULL':
                    my_dict['lat'] = 'NULL'
                else:
                    my_dict['lat'] = float(line[9])

                if line[10] == 'NULL':
                    my_dict['lon'] = 'NULL'
                else:
                    my_dict['lon'] = float(line[10])

                my_arr += [my_dict]

            # The values in the dictionary are: date, tweet text, username, retweet count, favorite count, language,
            # country, state/province, city
            return my_arr
    except IOError:  # If file doesn't exist, then it will be said in output and returns an empty list
        print("Could not open file {}!".format(tweet_file_name))
        return []


def make_report(tweet_list, keyword_dict):
    # This function returns a list of statistics for list of tweets to put onto a report,
    # the statistics are said on the return statement on line 185

    # Declared variables
    countries_sentiment = {}
    num_favorite = 0  #
    num_negative = 0  #
    num_neutral = 0  #
    num_positive = 0  #
    num_retweet = 0
    num_tweets = 0  #
    top_five = []
    total_favorite = 0
    avg_favorite = "NAN"
    total_retweet = 0
    avg_retweet = "NAN"
    total_sentiment = 0  #
    avg_sentiment = "NAN"  #

    for tweet in tweet_list:
        num_tweets += 1
        sentiment_value = calc_sentiment(clean_tweet_text(tweet["text"]), keyword_dict)  # Get sentiment value of tweet

        if tweet['favorite'] > 0:  # Add to total favorite sentiment value and the total count of favorited tweets
            total_favorite += sentiment_value
            num_favorite += 1

        if tweet['retweet'] > 0:  # Add to total retweet sentiment value and the total count of retweeted tweets
            total_retweet += sentiment_value
            num_retweet += 1

        sentiment = classify(sentiment_value)
        total_sentiment += sentiment_value

        if sentiment == "positive":
            num_positive += 1
        elif sentiment == "neutral":
            num_neutral += 1
        else:
            num_negative += 1

        if tweet["country"] != "NULL":  # Creates a dictionary of all countries and their total sentiment score
            if tweet["country"] in countries_sentiment:
                countries_sentiment[tweet["country"]][0] += sentiment_value  # {country: [total_sentiment value, count of country]}
                countries_sentiment[tweet["country"]][1] += 1
            else:
                countries_sentiment[tweet["country"]] = [sentiment_value, 1]

    if num_favorite != 0:
        # If there's at least 1 tweet which favorited, then the favorited tweets' avg sentiment value is calculated
        avg_favorite = round(total_favorite / num_favorite, 2)

    if num_retweet != 0:
        # If there's at least 1 tweet which retweeted, then the retweeted tweets' avg sentiment value is calculated
        avg_retweet = round(total_retweet / num_retweet, 2)

    if num_tweets != 0:
        # If there's at least 1 tweet, then the tweets' avg sentiment value is calculated
        avg_sentiment = round(total_sentiment / num_tweets, 2)

    print(countries_sentiment)

    if countries_sentiment != {}:
        for country in countries_sentiment:
            countries_sentiment[country] = round(countries_sentiment[country][0] / countries_sentiment[country][1], 2)

        # The sorted() function takes the tuple version of the countries_sentiment and sort it from greatest to least
        # based off the second value in each tuple "(("country", value), ("country", value),...)"
        countries_sentiment = sorted(countries_sentiment.items(), key=lambda x: x[1], reverse=True)
        countries_sentiment = dict(countries_sentiment)  # Convert the tuple back into a dictionary

        for country in countries_sentiment:
            if len(top_five) == 5:
                break
            top_five += [country]

        top_five = ", ".join(top_five)

    return {"avg_favorite": avg_favorite, "avg_retweet": avg_retweet, "avg_sentiment": avg_sentiment,
            "num_favorite": num_favorite, "num_negative": num_negative, "num_neutral": num_neutral,
            "num_positive": num_positive, "num_retweet": num_retweet, "num_tweets": num_tweets, "top_five": top_five}


def write_report(report, output_file):
    # This function takes the report made from the function make_report and writes it onto a txt file
    try:
        with open(output_file, "a") as file:
            lines = [
                "Average sentiment of all tweets: " + str(report["avg_sentiment"]) + "\n",
                "Total number of tweets: " + str(report["num_tweets"]) + "\n",
                "Number of positive tweets: " + str(report["num_positive"]) + "\n",
                "Number of negative tweets: " + str(report["num_negative"]) + "\n",
                "Number of neutral tweets: " + str(report["num_neutral"]) + "\n",
                "Number of favorited tweets: " + str(report["num_favorite"]) + "\n",
                "Average sentiment of favorited tweets: " + str(report["avg_favorite"]) + "\n",
                "Number of retweeted tweets: " + str(report["num_retweet"]) + "\n",
                "Average sentiment of retweeted tweets: " + str(report["avg_retweet"]) + "\n",
                "Top five countries by average sentiment: " + str(report["top_five"])
            ]

            file.writelines(lines)
            print("Wrote report to {}".format(output_file))

    except IOError:  # If file doesn't exist, then it will be said in output
        print("Could not open file {}".format(output_file))
