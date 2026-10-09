from fastapi import APIRouter, status, Depends, Request
from sqlalchemy import select
from app.database.base import MyDb
from app.models.branches import Branch
from app.models.rooms import Room
from app.schemas.rooms import RoomCreate, RoomResponse
from app.utils.checked import check_ident
from app.utils.rate_limit import limiter, get_user_id_key
from app.utils.security import require_roles


router = APIRouter(tags=['Room'], prefix="/rooms")


@router.post('/', status_code=status.HTTP_201_CREATED)
@limiter.limit('5/minute', key_func=get_user_id_key)
async def create_room(request: Request, room: RoomCreate, db: MyDb,
                      dependencies=Depends(require_roles(["manager", "admin"]))):

    await check_ident(db, Branch, room.branch_id)

    obj = Room(
        **room.model_dump()
    )
    db.add(obj)
    await db.commit()
    return {"msg": "Room created successfully"}


@router.get('/', response_model=list[RoomResponse])
async def list_rooms(db: MyDb, is_active: bool = True):

    result = await db.execute(select(Room).where(Room.is_active == is_active))
    return result.scalars().all()


@router.delete('/{room_id}')
async def delete_room(room_id: int, db: MyDb,
                      dependencies=Depends(require_roles(["manager", "admin"]))):

    room = await check_ident(db, Room, room_id)

    # soft delete
    room.is_active = False

    await db.commit()
    return {"msg": "Room soft delete"}
