import datetime as datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, VARCHAR, Date, Boolean, Float, TIMESTAMP
from sqlalchemy.orm import declarative_base
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--date", dest="date")
parser.add_argument("--host", dest="host")
parser.add_argument("--dbname", dest="dbname")
parser.add_argument("--user", dest="user")
parser.add_argument("--jdbc_password", dest="jdbc_password")
parser.add_argument("--port", dest="port")
args = parser.parse_args()

print('date = ' + str(args.date))
print('host = ' + str(args.host))
print('dbname = ' + str(args.dbname))
print('user = ' + str(args.user))
print('jdbc_password = ' + str(args.jdbc_password))
print('port = ' + str(args.port))

v_host = str(args.host)
v_dbname = str(args.dbname)
v_user = str(args.user)
v_password = str(args.jdbc_password)
v_port = str(args.port)


Base = declarative_base()


SQLALCHEMY_DATABASE_URI = f"postgresql://{str(v_user)}:{str(v_password)}@{str(v_host)}:{str(v_port)}/{str(v_dbname)}"

#------------------------------------------
class Weather(Base):
    __tablename__ = "tyumen_weather"
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    temp = Column(Float, nullable=False)
    feels_like = Column(Float, nullable=False)
    description = Column(VARCHAR(50), nullable=False)
    current_date = Column(TIMESTAMP, nullable=False, index=True)
# ------------------------------------------
import yaml

class My_yaml:

    name: str
    data: list

    def file_save(self, data, name):
        self.data = data
        self.name = name
        with open(name, 'w') as yml_file:
            docs = yaml.dump(self.data, yml_file)


    def file_open(self,name):
        self.name = name
        with open(name, 'r') as yml_file:
            my_file = yaml.load(yml_file, Loader=yaml.FullLoader)
        return my_file
#----------------------------------------
def my_weather():

    import requests
    from datetime import datetime

    # API openweathermap.org
    api_key = 'ca6f71b26580230c13c6d6bcf10d45c6'
    URL = f'http://api.openweathermap.org/data/2.5/find'

    my_yaml = My_yaml()  # creating My_yaml class for manipulating with yaml-file
    #my_city = my_yaml.file_open('data_files/city.yml')  # reading city name from yaml-file
    city = 'Tyumen'

    params = {'q': city, 'APPID': api_key, 'units': 'metric'}
    r = requests.get(url=URL, params=params)
    result = r.json()

    # print(json.dumps(result, indent=4))
    #date_time = str(datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))
    #my_yaml.file_save(result, f'data_files/{date_time}.yml')

    temp = result['list'][0]['main']['temp']
    feels_like = result['list'][0]['main']['feels_like']
    description = result['list'][0]['weather'][0]['description']

    return temp, feels_like, description
#----------------------------------------

engine = create_engine(SQLALCHEMY_DATABASE_URI)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session_local = SessionLocal()

temp, feels_like, description = my_weather()
new_record = Weather(
                    temp=temp,
                    feels_like=feels_like,
                    description=description,
                    current_date=datetime.datetime.utcnow()
                    )

session_local.add(new_record)

session_local.commit()