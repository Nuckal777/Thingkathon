from cobweb.app import db
from cobweb.models import Apartment
from cobweb.models import Ownership
from cobweb.models import Producer, Production, Consumption
from datetime import datetime

#delete all
db.session.query(Apartment).delete()
db.session.commit()

db.session.query(Producer).delete()
db.session.commit()

db.session.query(Ownership).delete()
db.session.commit()

db.session.query(Production).delete()
db.session.commit()

db.session.query(Consumption).delete()
db.session.commit()

# fill the database
apartment01 = Apartment(name="Apartment 1")
db.session.add(apartment01)
apartment02 = Apartment(name="Apartment 2")
db.session.add(apartment02)
apartment03 = Apartment(name="Apartment 3")
db.session.add(apartment03)
apartment04 = Apartment(name="Apartment 4")
db.session.add(apartment04)
apartment05 = Apartment(name="Apartment 5")
db.session.add(apartment05)
apartment06 = Apartment(name="Apartment 6")
db.session.add(apartment06)
db.session.commit()

producer01 = Producer()
db.session.add(producer01)
producer01 = Producer()
db.session.add(producer01)
producer01 = Producer()
db.session.add(producer01)
producer01 = Producer()
db.session.add(producer01)
producer01 = Producer()
db.session.add(producer01)
producer01 = Producer()
db.session.add(producer01)
db.session.commit()

ownership01 = Ownership(apartment_id=apartment06.id, producer_id=producer01.id, percentage=10.00)
db.session.add(ownership01)
db.session.commit()

production01 = Production(producer_id=producer01.id, energy=10.0, price=0.2, time=datetime(2019, 1,1))
db.session.add(production01)
db.session.commit();

energy_val_solar=10.0
energy_val_battery=5.0
energy_val_external=0.0
day = 0
price_neighboor=0.1
price_normal=0

for i in range(28):
    energy_val_solar = energy_val_solar + 0.1
    energy_val_battery = energy_val_battery + 0.1
    energy_val_external = energy_val_battery + energy_val_solar
    day = day + 1    

    if i % 3 == 0:
        consumption02 = Consumption(apartment_id=apartment06.id, energy=energy_val_battery,price=price_neighboor,origin="battery", time=datetime(2019,2,day))
    else:
        consumption02 = Consumption(apartment_id=apartment06.id, energy=energy_val_battery,price=price_normal,origin="battery", time=datetime(2019,2,day))

    consumption01 = Consumption(apartment_id=apartment06.id, energy=energy_val_solar,price=0.06,origin="solar", time=datetime(2019,2,day))     

    consumption03 = Consumption(apartment_id=apartment06.id, energy=energy_val_external,price=0.29,origin="external", time=datetime(2019,2,day))
    db.session.add(consumption01)
    db.session.add(consumption02)
    db.session.add(consumption03)
    db.session.commit()



''' print(apartment01.json())
print(ownership01.json())
print(producer01.json())
print(production01.json()) '''
#print(consumption01.json())
