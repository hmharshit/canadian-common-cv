# -*- coding: utf-8 -*-
import datetime
from ccv import app, logging
from ccv.models.posts import Posts
from ccv.schemas.posts import PostsSchema
from ccv.utils.parse_xml import parse_xml_file
from flask import jsonify, request
from sqlalchemy import or_


@app.route('/', methods=['GET'])
def index():
    return "Server is running :)"


@app.route('/api/get-posts', methods=['GET'])
def get_data():
    """
        It returns the posts present in the database in chronological order.
    """
    order_by = request.args.get('order')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    if order_by is None:  # If not given, then ordering chronologically
        posts = Posts.query.order_by(Posts.creation_date.asc()).offset((page - 1) * per_page) \
        .limit(per_page).all()

    elif order_by == "view_count":
        posts = Posts.query.order_by(Posts.view_count.asc()).offset((page - 1) * per_page) \
        .limit(per_page).all()
    
    elif order_by == "score":
        posts = Posts.query.order_by(Posts.score.asc()).offset((page - 1) * per_page) \
        .limit(per_page).all()

    else:
        return jsonify({'result': [], 'message': "Wrong parameter. Use either view_count or score", 
            'error': True})

    result = PostsSchema(many=True).dump(posts) # dumping the result in schema
    return jsonify({'result': result, 'message': "Success", 'error': False, "page_size": len(result)})


@app.route('/api/search-post', methods=['GET'])
def search_post():
    """
        This endpoint searches the posts in the databsse
    """
    query = request.args.get('query', "")
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    posts = Posts.query.filter(or_(Posts.body.contains(query), Posts.title.contains(query))).order_by(Posts.creation_date.asc()).offset((page - 1) * per_page) \
        .limit(per_page).all()  # querying using either title or body

    result = PostsSchema(many=True).dump(posts)  # dumping the result in schema
    return jsonify({'result': result, 'message': "Success", 'error': False, "page_size": len(result)})



@app.route('/api/ingest-data', methods=['GET'])
def ingest_data():
    posts = parse_xml_file("bioinformatics_posts_se.xml")
    for post in posts:
        post = post.attrib
        post_obj = Posts.query.filter_by(post_id=post.get("Id")).first()

        if not post_obj:  # record doesn't exist, create new
            
            post_db = {
                "post_id": int(post.get("Id")),
                "post_type_id": int(post.get("PostTypeId")),
                "accepted_answer_id": post.get("AcceptedAnswerId"),
                "creation_date": datetime.datetime.strptime(post.get("CreationDate"), "%Y-%m-%dT%H:%M:%S.%f"),
                "score": post.get("Score"),
                "view_count": post.get("ViewCount"),
                "body": post.get("Body"),
                "owner_user_id": post.get("OwnerUserId"),
                "last_editor_user_id": post.get("LastEditorUserId"),
                "title": post.get("Title"),
                "tags": post.get("Tags"),
                "answer_count": post.get("AnswerCount"),
                "favorite_count": post.get("FavoriteCount"),
                "comment_count": post.get("CommentCount")
            }

            if 'LastEditDate' in post and isinstance(post['LastEditDate'], str):
                post_db['last_edit_date'] = datetime.datetime.strptime(post.get("LastEditDate"), "%Y-%m-%dT%H:%M:%S.%f")

            if 'LastActivityDate' in post and isinstance(post['LastActivityDate'], str):
                post_db['last_activity_date'] = datetime.datetime.strptime(post.get("LastActivityDate"), "%Y-%m-%dT%H:%M:%S.%f")

            post_obj = Posts(**post_db)
            post_obj.insert(post_obj)  # saving the record in db

    return jsonify({"result": "Data ingested successfuly!", 'message': "Success", 'error': False})