from flask_restful import Resource
import requests
from models.PositionHistory import PositionHistory
class PositionHistoryView(Resource):
    def get(self,unique_code):
        if unique_code is None:
            return {
                "status" : "Failed",
                "msg":"Unknown Request"
            },404

        histories = PositionHistory.getAllPositionHistoryByUniqueCode(unique_code)

        data = [item.json() for item in histories]

        return {
            "status":"success",
            "data":data
        },200

