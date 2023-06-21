import spacy
import praw
from data_proccessing import pre_processing as pp

nlp = spacy.load("en_core_web_sm")

reddit = praw.Reddit(client_id='MdsQbwZg54zWz5RRPHiCjA',
                    client_secret='w5GMaJZAYzZErK9aG15whzamwbT9Rg', 
                    user_agent='Reddit scraper (by u/Main_Lion_9307)')

sub_reddit = reddit.subreddit("PoliticalHumor")

matcher = pp.get_hate_matcher(nlp)

file = open("potential_hate.txt", "w")

# for submission in sub_reddit.hot(limit=1):
#     submission.comments.replace_more(limit=None)
#     for comment in submission.comments.list():
#         print(comment.body)

num = 0
for submission in sub_reddit.hot(limit=1):
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        num+= 1
    
print(num)


# for submission in sub_reddit.hot(limit=10):        
#     for comment in submission.comments.replace_more():
#         doc = nlp(comment.body)
#         matches = matcher(doc)
#         if len(matches) > 0:
#             file.write(comment.body + "\n")
        
file.close()
