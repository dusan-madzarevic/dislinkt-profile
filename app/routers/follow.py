from fastapi import APIRouter
from app.profile_service import Follow, Profile,\
    add_following, delete_following, get_follow, get_requests, accept_request
from typing import List

router = APIRouter()


@router.post("/follow", response_model=Follow, tags=["follow"])
async def follow_add(follow: Follow):
    add_following(follow.follower_id, follow.following_id)
    return follow


@router.delete("/follow/{id1}/{id2}", response_model=Follow, tags=["follow"])
async def follow_delete(id1, id2):
    delete_following(id1, id2)
    return Follow(follower_id=id1, following_id=id2, accepted="true")


@router.get("/follow/{id1}/{id2}", response_model=Follow, tags=["follow"])
async def check_follow(id1, id2):
    return get_follow(id1, id2)


@router.get("/requests/{id}", response_model=List[Profile], tags=["follow"])
async def get_following_requests(id):
    return get_requests(id)


@router.get("/requests/{id1}/{id2}", tags=["follow"])
async def accept(id1, id2):
    return accept_request(id1, id2)

