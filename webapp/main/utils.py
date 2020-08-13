from sqlalchemy import func, text
from webapp import db
from webapp.posts.models import Post, Tag, tags


# Recent posts and top tags for right part of body page
def sidebar_data():
    recent = Post.query.order_by(Post.publish_date.desc()).limit(5).all()
    top_tags = db.session.query(Tag, func.count(tags.c.post_id).label("total")).join(tags).group_by(Tag).order_by(text('total DESC')).limit(5).all()
    return recent, top_tags
