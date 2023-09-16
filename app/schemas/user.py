from typing import List
from .post import Post
from pydantic import BaseModel, EmailStr

# Model for user signup
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class AuthSuccess(BaseModel):
    access_token: str
    token_type: str

# Model for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Model for displaying user data
class User(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    # You can extend this model to include more fields if needed

    class Config:
        orm_mode = True

# Model for user data including their posts
class UserWithPosts(User):
    posts: List[Post]  # Assuming you've imported Post from .post
