import praw
import pandas as pd


class Scrape():
    def __init__(self) -> None:
        pass

    def get_posts_df(self, subreddit: str, sortby: str):
        """This function will scrape a specific subreddit and return a dataframe with specified posts.

        Args:
            subreddit (str): The subreddit to scrape
            sortby (str): The method to sort by('hot','new','best','top','rising')
        """
        pass

    def get_comments_df(self, post_id: str) -> pd.DataFrame:
        """A function to retrieve all comments on a post

        Args:
            post_id (str): The id string of the post

        Returns:
            pd.DataFrame: A pandas dataframe containing each comment
        """
        pass

    def filter_comments(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """This function takes retrieves the comments from e

        Args:
            dataframe (pd.DataFrame): The pandas dataframe full of comments

        Returns:
            pd.DataFrame: A pandas dataframe with filtered comments
        """
        filter

    def get_subreddit_hate_comments(subreddit: str, sortby: str) -> pd.DataFrame:
        """A function which scrapes reddit and gives back a dataframe containing comments that only contain hate words.

        Args:
            subreddit (str): The subreddit to scrape
            sortby (str): The method to sort by('hot','new','best','top','rising')

        Returns:
            pd.DataFrame: A dataframe of comments with hate words present
        """
        pass
