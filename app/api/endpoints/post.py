from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.schemas.post import PostCreate, Post, PostList
from app.services.auth import get_current_user
from app.models.user import User
from app.models.post import Post as PostModel 
from app.db.session import get_db
from app.core import config

router = APIRouter()

@router.post("/addPost", response_model=PostCreate)
def add_post(
    *,
    db: Session = Depends(get_db),
    post_in: Post,
    current_user: User = Depends(get_current_user)
):
    post = PostModel(text=post_in.text, user_id=current_user.id)  
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"postID": post.id}

@router.get("/getPosts", response_model=List[Post])
def get_posts(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    posts = db.query(PostModel).filter(PostModel.user_id == current_user.id).all()
    if not posts:
        raise HTTPException(status_code=404, detail="Posts not found")
    return posts

@router.delete("/deletePost/{post_id}")
def delete_post(
    *,
    db: Session = Depends(get_db),
    post_id: int,
    current_user: User = Depends(get_current_user)
):
    post = db.query(PostModel).filter(PostModel.id == post_id, PostModel.user_id == current_user.id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"status": "Post deleted successfully"}