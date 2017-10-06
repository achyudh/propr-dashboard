import requests, pymongo
from bson.objectid import ObjectId


def profile(user_id):
    # Fetch cursor of relevant entries
    info_coll = pymongo.MongoClient().pr_database.pr_info
    info_cursor = info_coll.find({"user.login": user_id})
    user_pr_urls = list()
    for item in info_cursor:
        user_pr_urls.append(item["html_url"])
    feedback_coll = pymongo.MongoClient().pr_database.pr_feedback
    feedback_cursor = feedback_coll.find({"pr_url": {"$in": user_pr_urls}})

    #Declarations:
    ret_dict = dict()
    avg_review_time = 0
    rev_ratings = [0, 0, 0, 0, 0]
    rev_ratings_bd = [0, 0, 0, 0, 0]
    necessity_ratings = [0, 0, 0, 0, 0]
    review_times = [0 for i in range(13)]
    positive_comments = list()
    negative_comments = list()

    # Construct ret_dict
    if feedback_cursor.count() != 0:
        for item in feedback_cursor:
            if 'rating' in item:
                rev_ratings[int(item['rating']) - 1] += 1

            if 'rating_before_discussion' in item:
                rev_ratings_bd[int(item['rating_before_discussion']) - 1] += 1

            if 'necessity' in item:
                necessity_ratings[int(item['necessity']) - 1] += 1

            if 'review_time' in item:
                review_times[min(int(item['review_time'])//5, 12)] += 1
                avg_review_time += int(item['review_time'])

            if 'positive_comments' in item and item['positive_comments'] != "":
                positive_comments.append([item['positive_comments'], "#%s in %s" % (item['pr_num'], item['full_repo_name']), item['pr_url']])

            if 'negative_comments' in item and item['negative_comments'] != "":
                negative_comments.append([item['negative_comments'], "#%s in %s" % (item['pr_num'], item['full_repo_name']), item['pr_url']])

        ret_dict["avg_rating"] = (rev_ratings[0] + rev_ratings[1] * 2 + rev_ratings[2] * 3 + rev_ratings[3] * 4 + rev_ratings[4] * 5)/sum(rev_ratings)
        ret_dict["avg_rating_before_discussion"] = (rev_ratings_bd[0] + rev_ratings_bd[1] * 2 + rev_ratings_bd[2] * 3 + rev_ratings_bd[3] * 4 + rev_ratings_bd[4] * 5)/sum(rev_ratings_bd)
        ret_dict["avg_necessity"] = (necessity_ratings[0] + necessity_ratings[1] * 2 + necessity_ratings[2] * 3 + necessity_ratings[3] * 4 + necessity_ratings[4] * 5)/sum(necessity_ratings)
        ret_dict["avg_review_time"] = avg_review_time/len(review_times)

    else:
        ret_dict["avg_rating"] = "NA"
        ret_dict["avg_rating_before_discussion"] = "NA"
        ret_dict["avg_necessity"] = "NA"
        ret_dict["avg_review_time"] = "NA"

    ret_dict["ratings"] = rev_ratings
    ret_dict["ratings_before_discussion"] = rev_ratings_bd
    ret_dict["necessity_ratings"] = necessity_ratings
    ret_dict["review_times"] = review_times
    ret_dict["positive_comments"] = positive_comments
    ret_dict["negative_comments"] = negative_comments

    return ret_dict