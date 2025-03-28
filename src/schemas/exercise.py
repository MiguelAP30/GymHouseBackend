from pydantic import BaseModel, Field, validator, model_validator
from typing import List, Optional

class Exercise(BaseModel):
    id: Optional[int] = Field(default=None, title="Id del ejercicio")
    name: str = Field(min_length=4, max_length=60, title="Nombre del ejercicio")
    description: str = Field(min_length=4, max_length=200, title="Descripcion del ejercicio")
    video: str = Field(title="Video del ejercicio")
    image: str = Field(title="Imagen del ejercicio")
    dateAdded: str = Field(title="Fecha de creacion del ejercicio")
    dificulty_id: Optional[int] = Field(default=None, title="Id de la dificultad")
    machine_id: Optional[int] = Field(default=None, title="Id de la maquina")

    @validator("name")
    def name_must_not_be_empty(cls, value):
        assert isinstance(value,str), ValueError("el nombre debe ser un string")
        return value
    
    @validator("description")
    def description_must_not_be_empty(cls, value):
        assert isinstance(value,str), ValueError("la descripcion debe ser un string")
        return value
    
    @validator("dateAdded")
    def dateAdded_must_not_be_empty(cls, value):
        assert value.strip() != "", ValueError("La fecha no debe estar vacia")
        return value
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Press de banca con barra",
                "description": "El press de banca es un ejercicio de empuje que trabaja principalmente los músculos del pecho, los tríceps y los hombros.",
                "video": "https://www.youtube.com/watch?v=1",
                "image": "https://www.google.com",
                "dateAdded": "2024-05-07",
                "dificulty_id": 1,
                "machine_id": 1
            }
        }

class PaginatedResponse(BaseModel):
    items: List[Exercise]
    total: int
    page: int
    size: int
    pages: int

