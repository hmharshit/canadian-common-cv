# -*- coding: utf-8 -*-

import time
from ccv.models.posts import Posts
from ccv import ma

class PostsSchema(ma.ModelSchema):
    class Meta:
        model = Posts
        