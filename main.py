"""

Maharshii Patel
251353283
mpate588
The function of this file is mainly just to call upon the functions within sentiment_analysis to analyze the different
files given and write their report. It also makes sure that the files are given in the correct formats otherwise it
raises an exception.

"""

# Import the sentiment_analysis module
from sentiment_analysis import *


def main():  # Main function, takes the input of file names and gives that input to functions to make a report

    keywords = input("Input keyword filename (.tsv file): ")

    if keywords[-4:] != ".tsv":
        raise Exception("Must have tsv file extension!")  # Raise exception if keywords is not a tsv file

    tweet_file = input("Input tweet filename (.csv file): ")

    if tweet_file[-4:] != ".csv":
        raise Exception("Must have csv file extension!")  # Raise exception if tweet_file is not a csv file

    report_file = input("Input filename to output report in (.txt file): ")

    if report_file[-4:] != ".txt":
        raise Exception("Must have txt file extension!")  # Raise exception if report_file is not a txt file

    report = make_report(read_tweets(tweet_file), read_keywords(keywords))  # Make the report

    write_report(report, report_file)  # Write the report to report file


main()
