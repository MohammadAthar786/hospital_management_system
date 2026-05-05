from sqlalchemy.orm import Session
from typing import TypeVar, Generic, Type, Optional, List

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    """
    Generic CRUD repository.
    Every other repository inherits from this.
    """

    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db    = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def get_by_id(self, id) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def create(self, obj_data: dict) -> ModelType:
        if isinstance(obj_data, dict):
            db_obj = self.model(**obj_data)
        else:
            db_obj = self.model(**obj_data.model_dump())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, id, obj_data: dict) -> Optional[ModelType]:
        db_obj = self.get_by_id(id)
        if not db_obj:
            return None
        # Normalize: accept both Pydantic models and plain dicts
        if isinstance(obj_data, dict):
            data = {k: v for k, v in obj_data.items() if v is not None}
        if hasattr(obj_data, "model_dump"):
            data = obj_data.model_dump(exclude_none=True)
            # db_obj = self.model(**obj_data.model_dump())
        else:
            raise TypeError (f"obj_data must be a Pydantic model or dict, got {type(obj_data)}")
        for key, value in data.items(): 
            setattr(db_obj, key, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id) -> bool:
        db_obj = self.get_by_id(id)
        if not db_obj:
            return False
        self.db.delete(db_obj)
        self.db.commit()
        return True