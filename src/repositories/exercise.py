from typing import List, Tuple, Optional
from sqlalchemy import or_
from src.models.exercise import Exercise as ExerciseModel
from src.schemas.exercise import Exercise, PaginatedResponse

class ExerciseRepository:
    def __init__(self, db):
        self.db = db

    def get_all_excercises(
        self, 
        page: int = 1, 
        size: int = 10,
        search_name: Optional[str] = None,
        difficulty_id: Optional[int] = None,
        machine_id: Optional[int] = None
    ) -> Tuple[List[ExerciseModel], int]:
        """
        Obtiene todos los ejercicios con paginación y filtros
        
        Args:
            page: Número de página (comienza en 1)
            size: Tamaño de la página
            search_name: Texto para buscar en el nombre
            difficulty_id: ID de la dificultad para filtrar
            machine_id: ID de la máquina para filtrar
            
        Returns:
            Tuple con la lista de ejercicios y el total de registros
        """
        query = self.db.query(ExerciseModel)
        
        if search_name:
            query = query.filter(ExerciseModel.name.ilike(f"%{search_name}%"))
        if difficulty_id:
            query = query.filter(ExerciseModel.dificulty_id == difficulty_id)
        if machine_id:
            query = query.filter(ExerciseModel.machine_id == machine_id)
            
        total = query.count()
        offset = (page - 1) * size
        exercises = query.offset(offset).limit(size).all()
        
        return exercises, total

    def get_excercise_by_id(self, id):
        return self.db.query(ExerciseModel).filter(ExerciseModel.id == id).first()

    def create_new_excercise(self, exercise: Exercise):
        new_excercise = ExerciseModel(**exercise.model_dump())

        self.db.add(new_excercise)
        self.db.commit()
        self.db.refresh(new_excercise)
        return new_excercise

    def delete_excercise(self, id):
        element = self.db.query(ExerciseModel).filter(ExerciseModel.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element
    
    def update_excercise(self, id: int, exercise: Exercise) -> dict:
        element = self.db.query(ExerciseModel).filter(ExerciseModel.id == id).first()
        element.name = exercise.name
        element.description = exercise.description
        element.image = exercise.image
        element.video = exercise.video
        element.dateAdded = exercise.dateAdded
        element.dificulty_id = exercise.dificulty_id
        element.machine_id = exercise.machine_id

        self.db.commit()
        self.db.refresh(element)
        return element