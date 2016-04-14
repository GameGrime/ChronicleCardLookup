import io, json, re, os, praw, OAuth2Util
from pprint import pprint

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

if not os.path.isfile("posts_replied_to.txt"):
	posts_replied_to = []
	
else:
	with open("posts_replied_to.txt", "r") as file:
		posts_replied_to = file.read()
		posts_replied_to = posts_replied_to.split("\n")
		posts_replied_to = filter(None, posts_replied_to)
	
with open('cardData.json') as data_file:
	cardsInfo = json.load(data_file)

def reddit_setup():
	subreddit = "chronicletest"
	user_agent = "Chronicle Card Reporter for /r/{} ".format(subreddit)
	r= praw.Reddit(user_agent=user_agent)
	o= OAuth2Util.OAuth2Util(r)
	o.refresh(force=True)
	sub = r.get_subreddit(subreddit)
	return r, sub
	
def check_condition(c):
	text = c.body
	tokens = text.split()
	if "[[" in tokens and "]]" in tokens:
		if c.id not in posts_replied_to:
			posts_replied_to.append(c.id)
			pprint(posts_replied_to)
			with open("posts_replied_to.txt", "w") as file:
				for comment_id in posts_replied_to:
					file.write(comment_id + "\n")
			return True
			


def bot_action(c, verbose=True, respond=False):
	fixed = re.sub(r'[*\[\]\\]*', '', c.body)
	print(fixed)
		# if verbose:
		# print c.body.encode("UTF-8")
		# print "\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n"
		# print fixed.encode("UTF-8")
	if respond:
		head = "Hi! Let me try to beautify the list in  your comment:\n\n"
		tail = "\n\nI am a bot. You can provide feedback in my subreddit: /r/ListFormatFixer"
		c.reply(head + fixed + tail)


if __name__ == "__main__":
	#configuration()
	abspath = os.path.abspath(__file__)
	dname = os.path.dirname(abspath)
	os.chdir(dname)
	r, subreddit = reddit_setup()
	
	for c in praw.helpers.comment_stream(r, subreddit):
		if check_condition(c):
            # set 'respond=True' to activate bot responses. Must be logged in.
			bot_action(c, respond=False)