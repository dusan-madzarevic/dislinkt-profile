# from .create_db import Session, engine
from database import Session, engine

from pydantic import BaseModel
from .models import Profile as Profiledb, FollowRequest
from .models import User as Userdb, association_table
from typing import Union
from app.routers.auth import get_password_hash
from sqlalchemy.sql import text

local_session = Session(bind=engine)


class Follow(BaseModel):
    follower_id: int
    following_id: int
    accepted: bool


class Profile(BaseModel):
    user_id: int
    profile_id: int
    name: str
    surname: str
    email: str
    password: str
    picture: str
    description: str
    private: bool


def get_follow(id1: int, id2: int):
    # proverava stanje dva korisnika
    # 1 -  moguce je da vec id1 prati id2
    # 2 - moguce je da postoji zahtev za pracenje
    # 3 - moguce je da ne prati id1 id2

    # provera za 1
    statement_get = text("""SELECT * FROM association WHERE 
                 follower_id=:follower_id AND following_id=:following_id""")
    with engine.connect() as con:
        result = con.execute(statement_get, {"follower_id": id1, "following_id": id2})
        for row in result:
            return Follow(follower_id=id1, following_id=id2, accepted=1)

    # provera za 2
    request = local_session.query(FollowRequest).filter(
        FollowRequest.follower_id == id1, FollowRequest.following_id == id2).first()

    if request:
        return Follow(follower_id=id1, following_id=id2, accepted=0)

    # u suprotnom situacija 3
    return Follow(follower_id=0, following_id=0, accepted=0)


def add_following(id1: int, id2: int):
    profile1 = local_session.query(Profiledb).filter(Profiledb.id == id1).first()
    profile2 = local_session.query(Profiledb).filter(Profiledb.id == id2).first()
    if profile2.private:
        add_request(id1, id2)
        return

    profile1.following.append(profile2)
    profile2.follower.append(profile1)
    local_session.commit()


def add_following_for_request(id1: int, id2: int):
    profile1 = local_session.query(Profiledb).filter(Profiledb.id == id1).first()
    profile2 = local_session.query(Profiledb).filter(Profiledb.id == id2).first()

    profile1.following.append(profile2)
    profile2.follower.append(profile1)
    local_session.commit()


def add_request(id1: int, id2: int):
    local_session.add(FollowRequest(follower_id=id1, following_id=id2, accepted=False))
    local_session.commit()


def accept_request(id1: int, id2: int):
    request = local_session.query(FollowRequest).filter(
        FollowRequest.follower_id == id1, FollowRequest.following_id == id2).first()

    request.accepted = True
    local_session.commit()

    add_following_for_request(id1, id2)


def get_requests(id: int):
    requests = local_session.query(FollowRequest).filter(FollowRequest.following_id == id)
    profiles = []
    if not requests:
        return
    for req in requests:
        profile = local_session.query(Profiledb).filter(Profiledb.id == req.follower_id).first()
        if not req.accepted:
            profiles.append(profile)
    return map_db_dto(profiles)


def delete_following(id1: int, id2: int):
    statement_delete = text("""DELETE FROM association WHERE follower_id=:follower_id
             AND following_id=:following_id""")
    with engine.connect() as con:
        con.execute(statement_delete, {"follower_id": id1, "following_id": id2})
        con.close()


def get_following_requests(id: int):
    statement_get = text("""SELECT * FROM association WHERE following_id=:following_id AND accepted=0""")
    with engine.connect() as con:
        result = con.execute(statement_get, {"following_id": id})
        profiles = []
        for row in result:
            profiles.append(local_session.query(Profiledb).filter(Profiledb.id == row['follower_id']).first())
        con.close()
        return map_db_dto(profiles)


def map_db_dto(profiles_db):
    profiles_dto = []
    for profile in profiles_db:
        profiles_dto.append(Profile(user_id=profile.user.id, profile_id=profile.id, name=profile.user.ime,
                                    surname=profile.user.prezime,
                                    email=profile.user.email, password=profile.user.password, role=profile.user.role,
                                    picture=profile.picture, description=profile.description, private=profile.private))
    return profiles_dto


def get_all_profiles():
    profiles_db = local_session.query(Profiledb).all()
    return map_db_dto(profiles_db)


def get_public_profiles():
    profiles_db = local_session.query(Profiledb).filter(Profiledb.private == 0)
    return map_db_dto(profiles_db)


def get_following_profiles(profile_id: int):
    profile = local_session.query(Profiledb).filter(Profiledb.id == profile_id).first()
    with_self = profile.following
    with_self.append(profile)
    return map_db_dto(with_self)


def get_follower_profiles(profile_id: int):
    profile = local_session.query(Profiledb).filter(Profiledb.id == profile_id).first()
    followers = profile.follower
    return map_db_dto(followers)


def update_profile(profile: Profile):
    profile_db = local_session.query(Profiledb).filter(Profiledb.id == profile.id).first()
    #  izmeni profil
    profile_db.user.name = profile.name
    profile_db.user.surname = profile.surname
    profile_db.user.password = get_password_hash(profile.password)
    profile_db.picture = profile.picture
    profile_db.description = profile.description
    profile_db.private = profile.private
    local_session.commit()
    return profile


def search(full_name: str):
    names = full_name.split()
    print(names)
    users_db = local_session.query(Userdb).filter(Userdb.ime.contains(names[0]))
    if full_name == "":
        return get_all_profiles()
    if len(names) == 2:
        users_db = local_session.query(Userdb).filter(Userdb.ime.contains(names[0]),
                                                      Userdb.prezime.contains(names[1]))
    profiles_db = []
    for user in users_db:
        profiles_db.append(user.profile)
    return map_db_dto(profiles_db)



