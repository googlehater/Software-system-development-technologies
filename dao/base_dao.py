from sqlalchemy.orm import Session

class BaseDAO:
    def __init__(self, session: Session, model):
        self.session = session
        self.model = model

    def create(self, *, instance=None, **kwargs):  
        # создание новой записи
        if instance is not None:
            obj = instance
        else:
            obj = self.model(**kwargs)
        self.session.add(obj)
        self.session.commit()
        return obj
    
    def get_all(self):  
        # получение всех записей
        return self.session.query(self.model).all()
    
    def get_by_id(self, id: int):
        # получение записей по id
        return self.session.get(self.model, id)
    
    def update(self, id: int, **data):
        # обновление записи по id
        instance = self.get_by_id(id)
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
            self.session.commit()
            return instance
        return None
    
    def delete(self, id: int):
        # удаление записи
        instance = self.get_by_id(id)
        if instance:
            self.session.delete(instance)
            self.session.commit()
            return True
        return False
    
