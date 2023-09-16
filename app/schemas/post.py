from typing import List
from datetime import datetime
from pydantic import BaseModel

# Model for creating a new post
class PostCreate(BaseModel):
    postID: int

# Model for displaying post data with its associated user
class Post(BaseModel):
    text: str

    class Config:
        orm_mode = True

# Model for displaying a list of posts
class PostList(BaseModel):
    posts: List[Post]
