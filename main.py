from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from models.models import Curso
from connection.database import engine, Base, get_db
from repository_pattern.repository import CursoRepository
from models.schemas import CursoRequest, CursoResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/api/cursos", response_model=CursoResponse, status_code=status.HTTP_201_CREATED)
async def create(request: CursoRequest, db: Session = Depends(get_db)):
    create_obj = CursoRepository.save(db, Curso(** request.dict()))
    return CursoResponse.from_orm(create_obj)


@app.get("/api/cursos", response_model=list[CursoResponse])
async def find_all(db: Session = Depends(get_db)):
    all_obj = CursoRepository.find_all(db)
    return [CursoResponse.from_orm(curso) for curso in all_obj]


@app.get("/api/cursos/{id}", response_model=CursoResponse)
async def find_by_id(id: int, db: Session = Depends(get_db)):
    get_obj = CursoRepository.find_by_id(db, id)
    if not get_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso nao encontrado")
    return CursoResponse.from_orm(get_obj)



@app.delete("/api/cursos/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(id: int, db: Session = Depends(get_db)):
    if not CursoRepository.exists_by_id(db, id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso nao encontrado")
    CursoRepository.delete_by_id(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/api/cursos/{id}", response_model=CursoResponse)
async def update(id: int, request: CursoRequest, db: Session = Depends(get_db)):
    if not CursoRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Curso nao encontrado"
        )
    update_obj = CursoRepository.save(db, Curso(id=id, **request.dict()))
    return CursoResponse.from_orm(update_obj)