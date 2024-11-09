from typing import List
from src.schemas.muscle import Muscle
from src.models.muscle import Muscle as muscles

class MuscleRepository():
    def __init__(self, db) -> None:
        """
        Constructor de la clase MuscleRepository.

        Parámetros:
        - db: objeto de la base de datos.

        Precondición:
        - db debe ser un objeto válido de la base de datos.

        Postcondición:
        - Se inicializa una instancia de la clase MuscleRepository con el objeto de la base de datos asignado.
        """
        self.db = db
    
    def get_all_muscles(self) -> List[Muscle]:
        """
        Obtiene todos los músculos de la base de datos.

        Precondición:
        - No hay ninguna precondición.

        Postcondición:
        - Retorna una lista de objetos Muscle que representan todos los músculos de la base de datos.
        """
        query = self.db.query(muscles)
        return query.all()
    
    def get_muscle_by_id(self, id: int ):
        """
        Obtiene un músculo de la base de datos por su ID.

        Parámetros:
        - id: ID del músculo a buscar.

        Precondición:
        - id debe ser un entero válido.

        Postcondición:
        - Retorna un objeto Muscle que representa el músculo encontrado en la base de datos.
        """
        element = self.db.query(muscles).filter(muscles.id == id).first()
        return element
    
    def delete_muscle(self, id: int ) -> dict:
        """
        Elimina un músculo de la base de datos por su ID.

        Parámetros:
        - id: ID del músculo a eliminar.

        Precondición:
        - id debe ser un entero válido.

        Postcondición:
        - Retorna un diccionario que contiene la información del músculo eliminado de la base de datos.
        """
        element: Muscle= self.db.query(muscles).filter(muscles.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element

    def create_new_muscle(self, muscle:Muscle ) -> dict:
        """
        Crea un nuevo músculo en la base de datos.

        Parámetros:
        - muscle: objeto Muscle que representa el nuevo músculo a crear.

        Precondición:
        - muscle debe ser un objeto válido de la clase Muscle.

        Postcondición:
        - Retorna un diccionario que contiene la información del nuevo músculo creado en la base de datos.
        """
        new_muscle = muscles(**muscle.model_dump())
        self.db.add(new_muscle)
        
        self.db.commit()
        self.db.refresh(new_muscle)
        return new_muscle
    
    def update_muscle(self, id: int, muscle: Muscle) -> dict:
        """
        Actualiza un músculo existente en la base de datos.

        Parámetros:
        - id: ID del músculo a actualizar.
        - muscle: objeto Muscle que contiene los nuevos datos del músculo.

        Precondición:
        - id debe ser un entero válido.
        - muscle debe ser un objeto válido de la clase Muscle.

        Postcondición:
        - Retorna un diccionario que contiene la información del músculo actualizado en la base de datos.
        """
        element = self.db.query(muscles).filter(muscles.id == id).first()
        element.name = muscle.name
        element.description = muscle.description

        self.db.commit()
        self.db.refresh(element)
        return element