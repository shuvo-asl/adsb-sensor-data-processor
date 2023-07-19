from db import db

class Order(db.Model):
    __tablename__ = 'ordering_number'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.Integer)

    def __repr__(self):
        return f'<Order(id={self.id}, order_number={self.order_number})>'

    def json(self):
        return {
            "id":self.id,
            "order_number":self.order_number,
        }

    @staticmethod
    def get_singleton():
        # Retrieve the singleton order from the database
        order = Order.query.first()

        if order is None:
            # If no order exists, create a new one
            order = Order(order_number=1)
            db.session.add(order)
            db.session.commit()

        return order
    



    def save(self):
        db.session.add(self)
        db.session.commit()