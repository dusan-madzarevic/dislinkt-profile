from fastapi import APIRouter
from app.profile_service import Profile,\
    get_all_profiles, get_public_profiles, get_follower_profiles, get_following_profiles, update_profile, search, searchPublic
from typing import List

router = APIRouter()


@router.get("/profiles", response_model=List[Profile], tags=["profile"])
async def all_profiles():
    return get_all_profiles()


@router.get("/profiles/public", response_model=List[Profile], tags=["profile"])
async def public_profiles():
    return get_public_profiles()


@router.get("/profiles/followers/{profile_id}", response_model=List[Profile], tags=["profile"])
async def follower_profiles(profile_id):
    return get_follower_profiles(profile_id)


@router.get("/profiles/following/{profile_id}", response_model=List[Profile], tags=["profile"])
async def following_profiles(profile_id):
    return get_following_profiles(profile_id)


# @router.put("/profile", response_model=Profile, tags=["profile"])
# async def change_profile(profile: Profile):
#     return update_profile(profile)


@router.get("/profiles/{name}", response_model=List[Profile], tags=["profile"])
async def search_profiles(name: str):
    return search(name)

@router.get("/public-profiles/{name}", response_model=List[Profile], tags=["profile"])
async def search_public_profiles(name: str):
    return searchPublic(name)