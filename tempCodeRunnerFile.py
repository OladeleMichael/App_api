def find_post_by_ratings(id):
    for r in my_posts:
        if r["rating"] > 3:
            return r