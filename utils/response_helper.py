from data_class.response import Response
from data_class.multilabel import MultilabelObject as MO
from data_class.staff import Staff
from data_class.drinker import Drinker
class ResponseHelper:
    @staticmethod
    def create_response(data: list[MO]) -> Response:
        res = Response(products=[], staffs=[], drinker=[])
        for d in data:
            if(d.type == 'staff'):
                staff = Staff(position=d.position, value=d.value)
                res.staffs.append(staff)
            elif(d.type == 'drinker'):
                drinker = Drinker(position=d.position, value=d.value)
                res.drinker.append(drinker)
            else:
                res.products.append(d)
        return res