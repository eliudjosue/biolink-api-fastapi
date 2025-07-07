from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from database import engine
from models.models import User, Link
from typing import List
from auth import get_current_user

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello word!"}

@router.post("/users/", response_model=User)
def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

@router.get("/users/{username}/links", response_model=List[Link])
def get_links(username: str):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == username)).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        links = session.exec(select(Link).where(Link.user_id == user.id).order_by(Link.order)).all()
        return links

@router.post("/links/", response_model=Link)
def create_link(link: Link, current_user: User = Depends(get_current_user)):
    link.user_id = current_user.id
    with Session(engine) as session:
        session.add(link)
        session.commit()
        session.refresh(link)
        return link

@router.put("/links/{link_id}", response_model=Link)
def update_link(link_id: int, new_data: Link, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        link = session.get(Link, link_id)
        if not link:
            raise HTTPException(status_code=404, detail="Link no encontrado")
        if link.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="No tienes permiso para modificar este link")

        if new_data.title is not None:
            link.title = new_data.title
        if new_data.url is not None:
            link.url = new_data.url
        if new_data.order is not None:
            link.order = new_data.order

        session.commit()
        session.refresh(link)
        return link


@router.delete("/links/{link_id}")
def delete_link(link_id: int, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        link = session.get(Link, link_id)
        if not link:
            raise HTTPException(status_code=404, detail="Link no encontrado")
        if link.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="No tienes permiso para eliminar este link")
        session.delete(link)
        session.commit()
        return {"message": "Link eliminado"}

@router.post("/links/{link_id}/click")
def count_click(link_id: int):
    with Session(engine) as session:
        link = session.get(Link, link_id)
        if not link:
            raise HTTPException(status_code=404, detail="Link no encontrado")
        link.click_count += 1
        session.commit()
        return {"message": "Click contado"}
