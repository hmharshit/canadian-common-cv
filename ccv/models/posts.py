# -*- coding: utf-8 -*-

from ccv import db
from sqlalchemy.sql import func


class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column('id', db.Integer, primary_key=True, index=True)
    created_at = db.Column('created_at', db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column('updated_at', db.DateTime(timezone=True), default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())
    post_id = db.Column(db.Integer, unique=True)
    post_type_id = db.Column(db.Integer)
    accepted_answer_id = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime(timezone=True))
    score = db.Column(db.Integer)
    view_count = db.Column(db.Integer)
    body = db.Column(db.Text)
    owner_user_id = db.Column(db.Integer)
    last_editor_user_id = db.Column(db.Integer)
    last_edit_date = db.Column(db.DateTime(timezone=True))
    last_activity_date = db.Column(db.DateTime(timezone=True))
    title = db.Column(db.String)
    tags = db.Column(db.String)
    answer_count = db.Column(db.Integer)
    favorite_count = db.Column(db.Integer)
    comment_count = db.Column(db.Integer)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return "{}-{}".format(self.id, self.title)

    @staticmethod
    def insert(obj):
        db.session.add(obj)
        db.session.commit()
        db.session.flush()
