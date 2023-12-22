import sys
from colorama import Fore, Style
from models import Base, Motor
from engine import engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from settings import SCALE_nmotor,SCALE_volume,SCALE_tangki,SCALE_daya,SCALE_torsi,SCALE_harga

session = Session(engine)

def create_table():
    Base.metadata.create_all(engine)
    print(f'{Fore.GREEN}[Success]: {Style.RESET_ALL}Database has created!')

class BaseMethod():

    def __init__(self):
        # 1-5
        self.raw_weight = {
            'nmotor': 3, 
            'volume': 5, 
            'tangki': 3, 
            'daya': 3, 
            'torsi': 3, 
            'harga': 2
            }

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {k: round(v/total_weight, 2) for k,v in self.raw_weight.items()}

    @property
    def data(self):
        query = select(Motor)
        return [{'id': motor.id, 
        'nmotor': SCALE_nmotor[motor.nmotor], 
        'volume': SCALE_volume[motor.volume], 
        'tangki': SCALE_tangki[motor.tangki], 
        'daya': SCALE_daya[motor.daya], 
        'torsi': SCALE_torsi[motor.torsi], 
        'harga': SCALE_harga[motor.harga]} 
        for motor in session.scalars(query)]
    
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
    @property
    def calculate(self):
        weight = self.weight
        # calculate data and weight[WP]
        result =  {row['id']:
            round(
        row['nmotor'] ** weight['nmotor'] *
        row['volume'] ** weight['volume'] *
        row['tangki'] ** weight['tangki'] *
        row['daya'] ** weight['daya'] *
        row['torsi'] ** weight['torsi'] *
        row['harga'] ** weight['harga']
        , 2
    )
            for row in self.normalized_data
        }
        # sorting
        return dict(sorted(result.items(), key=lambda x:x[1], reverse=True))


class SimpleAdditiveWeighting(BaseMethod):
    @property
    def calculate(self):
        weight = self.weight
        # calculate data and weight
        result =  {row['id']:
            round(row['nmotor'] * weight['nmotor'] +
            row['volume'] * weight['volume'] +
            row['tangki'] * weight['tangki'] +
            row['daya'] * weight['daya'] +
            row['torsi'] * weight['torsi'] +
            row['harga'] * weight['harga'], 2)
            for row in self.normalized_data
        }
        # sorting
        return dict(sorted(result.items(), key=lambda x:x[1]))

def run_saw():
    saw = SimpleAdditiveWeighting()
    print('result:', saw.calculate)
    

def run_wp():
    wp = WeightedProduct()
    print('result:', wp.calculate)
    pass

if len(sys.argv)>1:
    arg = sys.argv[1]

    if arg == 'create_table':
        create_table()
    elif arg == 'saw':
        run_saw()
    elif arg =='wp':
        run_wp()
    else:
        print('command not found')
