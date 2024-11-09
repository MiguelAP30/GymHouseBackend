from typing import List
from src.schemas.machine import Machine
from src.models.machine import Machine as machines

class MachineRepository():
    def __init__(self, db) -> None:
        """
        Constructor de la clase MachineRepository.

        Parámetros:
        - db: objeto de la base de datos.

        Precondición:
        - db debe ser un objeto válido de la base de datos.

        Postcondición:
        - Se crea una instancia de la clase MachineRepository con el objeto de la base de datos asignado.
        """
        self.db = db
    
    def get_all_machines(self) -> List[Machine]:
        """
        Obtiene todas las máquinas.

        Precondición:
        - No hay ninguna precondición.

        Postcondición:
        - Devuelve una lista de todas las máquinas en la base de datos.
        """
        query = self.db.query(machines)
        return query.all()
    
    def get_machine_by_id(self, id: int ):
        """
        Obtiene una máquina por su ID.

        Parámetros:
        - id: ID de la máquina a buscar.

        Precondición:
        - id debe ser un entero válido.

        Postcondición:
        - Devuelve la máquina correspondiente al ID proporcionado.
        """
        element = self.db.query(machines).filter(machines.id == id).first()
        return element
    
    def delete_machine(self, id: int ) -> dict:
        """
        Elimina una máquina por su ID.

        Parámetros:
        - id: ID de la máquina a eliminar.

        Precondición:
        - id debe ser un entero válido.

        Postcondición:
        - Elimina la máquina correspondiente al ID proporcionado de la base de datos y devuelve la máquina eliminada.
        """
        element: Machine= self.db.query(machines).filter(machines.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element

    def create_new_machine(self, machine:Machine ) -> dict:
        """
        Crea una nueva máquina.

        Parámetros:
        - machine: objeto de la máquina a crear.

        Precondición:
        - machine debe ser un objeto válido de la clase Machine.

        Postcondición:
        - Crea una nueva máquina en la base de datos, devuelve la máquina creada.
        """
        new_machine = machines(**machine.model_dump())
        self.db.add(new_machine)
        
        self.db.commit()
        self.db.refresh(new_machine)
        return new_machine
    
    def update_machine(self, id: int, machine: Machine) -> dict:
        """
        Actualiza una máquina por su ID.

        Parámetros:
        - id: ID de la máquina a actualizar.
        - machine: objeto de la máquina actualizada.

        Precondición:
        - id debe ser un entero válido.
        - machine debe ser un objeto válido de la clase Machine.

        Postcondición:
        - Actualiza la máquina correspondiente al ID proporcionado en la base de datos, devuelve la máquina actualizada.
        """
        element = self.db.query(machines).filter(machines.id == id).first()
        element.name = machine.name
        element.description = machine.description

        self.db.commit()
        self.db.refresh(element)
        return element