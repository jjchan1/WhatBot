# Author: Jonathan Chan
# Credit: u/busterino

import praw
import time
import os


# authenticate bot
def authenticate():
    print("Authenticating...")
    reddit = praw.Reddit('WhatBot', user_agent="u/jjchan1's WhatBot v0.1")
    print("Authenticated as {}\n".format(reddit.user.me()))

    return reddit


# search OS list of previously replied comments
def get_comments_replied():
    # if no such list exists, make a new file and list
    if not os.path.isfile("comments_replied.txt"):
        comments_replied = []
    else:
        with open("comments_replied.txt", "r") as file:
            comments_replied = file.read()
            comments_replied = comments_replied.split("\n")
            comments_replied = filter(None, comments_replied)

    return comments_replied


# main
def main():
    reddit = authenticate()
    comments_replied = get_comments_replied()
    while True:
        run_what_bot(reddit, comments_replied)


# run bot
def run_what_bot(reddit, comments_replied):
    # for the first n=100 comments, check to see if the comment is what/wat/wut/wot
    # if yes, reply to comment with a picture of the what girl
    for comment in reddit.subreddit('test').comments(limit=100):
        if ("what" == comment.body.lower() or
            "wat" == comment.body.lower() or
            "wut" == comment.body.lower() or
            "wot" == comment.body.lower() and
            comment.id not in comments_replied):
            comment.reply("[What...](http://i.imgur.com/hQpkcKh.jpg)")

            # add comment.id to list of comments already replied to to prevent spamming
            comments_replied.append(comment.id)

            # update txt file with new commend.id
            with open("comments_replied.txt", "a") as file:
                file.write(comment.id + "\n")
            print("Replied to comment " + comment.id)

    # sleep to prevent overcommenting
    time.sleep(10)
    print("Sleeping...")


if __name__ == '__main__':
    main()
