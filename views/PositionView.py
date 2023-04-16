from flask_restful import Resource
from schedule import data_pulling
from models.Position import Position
class PositionView(Resource):
    def get(self):
        data_pulling()
        data = Position.getAllPositions()
        positions = [item.json() for item in data]
        return {
            "status":"success",
            "positions":positions
        }