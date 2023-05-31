from sqlalchemy.orm import Session
from models.models import Curso

class CursoRepository:

    @staticmethod
    #get all objects
    def find_all(db: Session) -> list[Curso]:
        return db.query(Curso).all()

    @staticmethod
    def save(db: Session, curso:Curso) -> Curso:
        if curso.id:
            db.merge(curso)
        else:
            db.add(curso)
        db.commit()
        return curso
    
    @staticmethod
    def find_by_id(db: Session, id: int) -> Curso:
        return db.query(Curso).filter(Curso.id == id).first()
    
    @staticmethod
    def exists_by_id(db: Session, id:int) -> bool:
        return db.query(Curso).filter(Curso.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id:int) -> None:
        obj = db.query(Curso).filter(Curso.id == id).first()
        if obj is not None:
            db.delete(obj)
            db.commit()