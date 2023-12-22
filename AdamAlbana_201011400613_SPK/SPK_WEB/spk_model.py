from settings import SCALE_nmotor,SCALE_volume,SCALE_tangki,SCALE_daya,SCALE_torsi,SCALE_harga

class BaseMethod():

    def __init__(self, data_dict, **setWeight):
        self.dataDict = data_dict

        # 1-7 (Kriteria)
        self.raw_weight = {
            'nmotor': 3, 
            'volume': 5, 
            'tangki': 3, 
            'daya': 3, 
            'torsi': 3, 
            'harga': 2
        }

        if setWeight:
            for item in setWeight.items():
                temp1 = setWeight[item[0]] # value int
                temp2 = {v: k for k, v in setWeight.items()}[item[1]] # key str

                setWeight[item[0]] = item[1]
                setWeight[temp2] = temp1

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {c: round(w/total_weight, 2) for c,w in self.raw_weight.items()}

    @property
    def data(self):
        return [{
            'id': motor['id'],
            'nmotor': SCALE_nmotor[motor['nmotor']],
            'volume': SCALE_volume[motor['volume']],
            'tangki': SCALE_tangki[motor['tangki']],
            'daya': SCALE_daya[motor['daya']],
            'torsi': SCALE_torsi[motor['torsi']],
            'harga': SCALE_harga[motor['harga']]
        } for motor in self.dataDict]
    
    @property
    def normalized_data(self):
        # x/max [benefit]
        # min/x [cost]
        nmotor = [] # max
        volume = [] # max
        tangki = [] # max
        dayas = [] # max
        torsis = [] # max
        hargas = [] # min
        
        for data in self.data:
            nmotor.append(data['nmotor'])
            volume.append(data['volume'])
            tangki.append(data['tangki'])
            dayas.append(data['daya'])
            torsis.append(data['torsi'])
            hargas.append(data['harga'])

        max_nmotor = max(nmotor)
        max_volume = max(volume)
        max_tangki = max(tangki)
        max_daya = max(dayas)
        max_torsi = max(torsis)
        min_harga = min(hargas)
        return [
            {   'id': data['id'],
                'nmotor': data['nmotor']/max_nmotor, # benefit
                'volume': data['volume']/max_volume, # benefit
                'tangki': data['tangki']/max_tangki, # benefit
                'daya': data['daya']/max_daya, # benefit
                'torsi': data['torsi']/max_torsi, # benefit
                'harga': min_harga/data['harga'] # cost
                }
            for data in self.data
        ]

class WeightedProduct(BaseMethod):
    def __init__(self, dataDict, setWeight:dict):
        super().__init__(data_dict=dataDict, **setWeight)
    @property
    def calculate(self):
        weight = self.weight
        result = {row['id']:
    round(
        row['nmotor'] ** weight['nmotor'] *
        row['volume'] ** weight['volume'] *
        row['tangki'] ** weight['tangki'] *
        row['daya'] ** weight['daya'] *
        row['torsi'] ** weight['torsi'] *
        row['harga'] ** weight['harga']
        , 2
    )
    for row in self.normalized_data}

        #sorting
        # return result
        return dict(sorted(result.items(), key=lambda x:x[1], reverse=True))