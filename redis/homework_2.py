import redis
import datetime


ONE_WEEK_IN_SECONDS = 7 * 86400
VOTE_SCORE = 432

def article_vote(redis, user, article):
    cutoff = datetime.datetime.now() - datetime.timedelta(seconds=ONE_WEEK_IN_SECONDS)

    if not datetime.datetime.fromtimestamp(redis.zscore('time:', article)) < cutoff:
        article_id = article.split(':')[-1]
        if redis.sadd('voted:' + artical_id, user):
            redis.zincrby('score:', VOTE_SCORE, article)
            reids.hincrby(article, 'votes', 1)

def article_switch_vote(redis, user, from_article, to_article):
    from_article_id = from_article.split(':')[-1]
    to_article_id = to_article.split(':')[-1]
   
    redis.zincrby(name = 'score:', value = from_article, amount = VOTE_SCORE*(-1))
    redis.hincrby(name = from_article, key='votes', amount = -1)
    redis.srem('voted:' + from_article_id, user)

    redis.zincrby(name = 'score:', value = to_article, amount = VOTE_SCORE)
    redis.hincrby(name = to_article, key ='votes', amount = 1)
    redis.sadd('voted:' + to_article_id, user)


redis = redis.StrictRedis(host='localhost', port=6379, db=0)
# user:3 up votes article:1
article_vote(redis, "user:3", "article:1")
# user:3 up votes article:3
article_vote(redis, "user:3", "article:3")
# user:5 switches their vote from article:1 to article:0
article_switch_vote(redis, "user:2", "article:8", "article:1")


article = redis.zrangebyscore('score:', 10, 20)
if len(article) > 1:
    result = article[0]
article_id = result[0].split(':')[-1]
print(redis.hget("article:" +  article_id, "link"))

