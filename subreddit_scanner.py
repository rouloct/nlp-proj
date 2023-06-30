import spacy
import praw
import pandas as pd
from data_proccessing import pre_processing as pp

REQ_HATE_TO_COMMENTS_RATIO = 1/40
CHECK_HATE_AFTER = 140
MAX_HATE_PER_POST = 5
MAX_COMMENTS_IN_POST_W_NO_HATE = 30

HATE_CSV = 'hate.csv'

nlp = spacy.load("en_core_web_sm")

reddit = praw.Reddit(client_id='MdsQbwZg54zWz5RRPHiCjA',
                    client_secret='w5GMaJZAYzZErK9aG15whzamwbT9Rg', 
                    user_agent='Reddit scraper (by u/Main_Lion_9307)')

matcher = pp.get_hate_matcher(nlp)
   
   
def subreddit_scanner(sub_reddit, matches_to_find = 20):
    """Scan through a specific subreddit until the desired # of matches are found, or only 1/40 comments find a match, checked after 180 comments. 
    The user decides which comments to add to the .csv.

    Args:
        sub_reddit (praw.Subreddit)
        matches_to_find (int)

    Returns:
        int: # of posts scanned.
        int: # of comments scanned.
        [[str, str]]: matches the user wants to add to the .csv in the form [subreddit name, comment body] .
    """
    all_matches = []
    posts_in_sub = 0
    comments_in_sub = 0
    comments_since_check = 0
    
    print(f"Scanning subreddit: r/{sub_reddit.display_name}.")
    
    for index, submission in enumerate(sub_reddit.hot(limit=1000)):
        posts_in_sub += 1
        comments_in_post, matches = post_scanner(submission, sub_reddit)
        comments_in_sub += comments_in_post
        comments_since_check += comments_in_post
        
        if (len(matches) > 0):
            all_matches.extend(matches)
        
        print(f"Scanned post #{index + 1}: {comments_in_post} comments, {len(matches)} matches Total: {comments_in_sub} comments, {len(all_matches)} matches.")
    
        if comments_in_post == 0:
            continue
                
        if comments_in_sub >= CHECK_HATE_AFTER:
            if len(all_matches) == 0:
                return posts_in_sub, comments_in_sub, []
            if len(all_matches) / comments_in_sub < REQ_HATE_TO_COMMENTS_RATIO:
                matches_to_add = user_add_to_list(all_matches, sub_reddit)
                print(f"\nAdding {len(matches_to_add)} comments then scanning a new subreddit!\n")
                return posts_in_sub, comments_in_sub, matches_to_add
        
        if len(all_matches) >= matches_to_find:
            matches_to_add = user_add_to_list(all_matches, sub_reddit)
            print(f"\nAdding {len(matches_to_add)} comments then scanning a new subreddit!\n")
            return posts_in_sub, comments_in_sub, matches_to_add
                
                    
    if len(all_matches > 0):
        matches_to_add = user_add_to_list(all_matches, sub_reddit)
        print(f"\nAdding {len(matches_to_add)} comments then scanning a new subreddit!\n")
        return posts_in_sub, comments_in_sub, matches_to_add
    else:
        return posts_in_sub, comments_in_sub, []
            

def post_scanner(post, sub_reddit):
    """Scan through a specific post on a subreddit, looking for matches until 40 comments were scanned with no matches, 5 comments matched, or all comments were searched.

    Args:
        post (praw.Submission)
        sub_reddit (praw.Subreddit)

    Returns:
        int: # of comments in post
        [[str, str]]: all comments matched by the matcher in the form [subreddit name, comment body].
    """
    comments_in_post = 0
    matches = []
    
    post.comments.replace_more()
    for comment in post.comments.list():
        comments_in_post += 1
        
        if comment_scanner(comment) == True:
            matches.append([sub_reddit.display_name, comment.body.replace('\n', '\\n')])

        if (comments_in_post == MAX_COMMENTS_IN_POST_W_NO_HATE and len(matches) == 0) or len(matches) == MAX_HATE_PER_POST:
            break
    
    return comments_in_post, matches
    

def comment_scanner(comment) -> bool:
    """Scan through a specific comment looking for matches.

    Args:
        comment (praw.Comment)

    Returns:
        bool: if the Matcher found at least one match in the comment.
    """
    doc = nlp(comment.body)
    matches = matcher(doc)
    
    if (len(matches) > 0):
        return True
    else:
        return False
    

def user_add_to_list(matches, sub_reddit):
    """Prompt the user to decide which of the matches to add to the .csv, which the user enters as a space-separated list, or leaves blank.

    Args:
        matches ([[str, str]]): all comments matched by the matcher in the form [subreddit name, comment body].
        sub_reddit (praw.Subreddit)

    Returns:
        [[str, str]]: the matches the user wants to add.
    """
    print(f"\nMatches found in r/{sub_reddit.display_name}:\n")
    for index, [_, text] in enumerate(matches):
        print(f"{index + 1}: {text}\n")

    user_add_to_list = input("Enter the numbers you'd like to add as a space-separated list, 'a' for all, or leave blank for none, then hit enter: ")

    while True:
        if user_add_to_list == 'a':
            return matches
        try:
            return [matches[int(numStr) - 1 ]for numStr in user_add_to_list.split()]
        except Exception:
            print("User input threw an error. Try again.")
            user_add_to_list = input("Enter the numbers you'd like to add as a comma separated list, or 'a' for all: ")
        

if __name__ == '__main__':
    """ Search through subreddits until the user decides to stop by pressing CTRL+C.
    """
    random = input("Would you like to select random subreddits (r) or enter your own (o)? ")
    while random != 'r' and random != 'o':
        print("Invalid input. try again")
        random = input("Would you like to select random subreddits (r) or enter your own (o)? ")

    total_subs = 0
    total_posts = 0
    total_comments = 0
    all_matches = []
    
    amount = -1
    while amount < 0:
        try:
            amount = int(input("How many matches would you like to find? "))       
        except ValueError:
            print("Not an integer! Try again.")
           
    while True:
        try:
            sub = reddit.random_subreddit()
            if random == 'o':
                sub = reddit.subreddit(input("Enter the name of a subreddit to scan: r/"))
            posts_in_sub, comments_in_sub, matches = subreddit_scanner(sub, amount)
            total_subs += 1
            all_matches.extend(matches)
        except KeyboardInterrupt:
            # TODO: Sometimes prints "0,1" on a file or blank lines.
            if (len(all_matches) > 0):
                pd.DataFrame(data=all_matches).dropna().to_csv(HATE_CSV, mode='a', index=False)
                
            print(f"\nScraped {total_comments} comments from {total_posts} posts on {total_subs} subreddits and wrote {len(all_matches)} comments to {HATE_CSV}.")
            exit()
            
        except Exception:
            print("Invalid subreddit. Try again")
                
            
            
                
    