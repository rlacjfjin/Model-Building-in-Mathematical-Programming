
class Farm:
    def __init__(self,name,farm_id,x,y,requirement,need_to_visit):
        self.name = name
        self.index = farm_id
        self.x = x
        self.y = y
        self.requirement = requirement
        self.need_to_visit = need_to_visit


class Problem:
    def __init__(self,farms,capacity):
        self.farms = farms
        self.capacity = capacity

    def data_processing(self):
        pass
    
    def mip_model(self):
        pass
