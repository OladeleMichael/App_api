select posts.*, COUNT(votes.post_id) as votes from posts RIGHT JOIN votes ON posts.id = post_id group by posts.id;