from models.user import User

class Customer(User):
    def __init__(self, user_id, name, email, is_registered=False):
        super().__init__(user_id, name, email)
        self.is_registered = is_registered
        self.equipment_list = []

    def add_equipment(self, equipment):
        self.equipment_list.append(equipment)

