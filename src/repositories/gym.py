from typing import List
from src.models.gym import Gym as gym
from src.schemas.gym import Gym

class GymRepository():
    def __init__(self, db) -> None:
        """
        Inicializa una nueva instancia de la clase GymRepository.

        Args:
            db: La base de datos utilizada para realizar las operaciones.

        Precondición:
            - db debe ser una instancia válida de la base de datos.

        Postcondición:
            - Se crea una nueva instancia de GymRepository.
        """
        self.db = db
    
    def get_all_gym(self) -> List[Gym]:
        """
        Obtiene todos los gimnasios.

        Returns:
            Una lista de objetos Gym que representan los gimnasios.

        Postcondición:
            - Se devuelve una lista de objetos Gym.
        """
        query = self.db.query(gym)
        return query.all()
    
    def create_new_gym(self, gym: Gym) -> Gym:
        """
        Crea un nuevo gimnasio.

        Args:
            gym: El objeto Gym que representa el gimnasio a crear.

        Returns:
            El objeto Gym creado.

        Precondición:
            - gym debe ser un objeto Gym válido.

        Postcondición:
            - Se crea un nuevo gimnasio.
        """

        new_gym = gym(**gym.model_dump())
        self.db.add(new_gym)

        self.db.commit()
        self.db.refresh(new_gym)
        return new_gym
    
    def delete_gym(self, id: int) -> dict:
        """
        Elimina un gimnasio específico.
        """
        element = self.db.query(gym).filter(gym.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element
    
    def get_gym_by_id(self, id: int ):
        """
        Obtiene un gimnasio específico por su ID.

        Precondición:
        - La base de datos debe estar conectada y disponible.
        - El ID debe ser un entero válido.

        Postcondición:
        - Devuelve un objeto Gym que representa el gimnasio con el ID especificado.
        """
        element = self.db.query(gym).filter(gym.id == id).first()
        return element
    
