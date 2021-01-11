from datetime import datetime
from flask import request, jsonify, Blueprint, abort
from flask_api import db, app
import pycep_correios
from unidecode import unidecode
from sqlalchemy import desc,asc, or_, and_, distinct
# from flask_api.product.models import HolidayBr

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from unidecode import unidecode


engine = create_engine('mysql://lucca10:goku4040@localhost/holiday_db_backup')
Base = declarative_base(engine)

class HolidayBr(Base):
    __tablename__ = 'holidayBr'
    __table_args__ = {'autoload': True}
    # def __repr__(self):
    #     return "<User(name='%s', fullname='%s', nickname='%s')>" % (
    #                     self.name, self.date, self.location)

class Holiday():
    def __init__(self):
        self.aux_dict_holidays = {}
        self.states = {
            'AC': 'Acre',
            'AL': 'Alagoas',
            'AP': 'Amapá',
            'AM': 'Amazonas',
            'BA': 'Bahia',
            'CE': 'Ceará',
            'DF': 'Distrito Federal',
            'ES': 'Espírito Santo',
            'GO': 'Goiás',
            'MA': 'Maranhão',
            'MT': 'Mato Grosso',
            'MS': 'Mato Grosso do Sul',
            'MG': 'Minas Gerais',
            'PA': 'Pará',
            'PB': 'Paraíba',
            'PR': 'Paraná',
            'PE': 'Pernambuco',
            'PI': 'Piauí',
            'RJ': 'Rio de Janeiro',
            'RN': 'Rio Grande do Norte',
            'RS': 'Rio Grande do Sul',
            'RO': 'Rondônia',
            'RR': 'Roraima',
            'SC': 'Santa Catarina',
            'SP': 'São Paulo',
            'SE': 'Sergipe',
            'TO': 'Tocantins'
        }
    

        holidays = {
            'Federal':{},
            'Estadual':{}, 
            'Municipal':{}
        }
        self.list_holidays_no_scope = {}
        self.final_response_dict = {}

    def loadSession(self):
        metadata = Base.metadata
        Session = sessionmaker(bind=engine)
        session = Session()
        return session


    def getHolidayDict(self,scope, holidays, holiday_location):
        session = self.loadSession()
        query_entries = 0
        holiday_query = ''
        state = unidecode((self.states[holiday_location['estado']]).lower().capitalize().replace(" ","-"))
        location = unidecode((holiday_location['cidade']).lower().capitalize().replace(" ","-"))
        print(state,location)
        
        stuff= session.query(HolidayBr).filter(
            or_(and_(HolidayBr.region == state, HolidayBr.scope=='Estadual'), 
            or_(and_(HolidayBr.location == location, HolidayBr.region == state), HolidayBr.scope == 'Federal')
            )).order_by(HolidayBr.date.asc())

        #without scope
        index = 1
        for i in stuff:
          
            a = vars(i)
            dateName = a['name']
            if dateName == 'Feriado Municipal':
                dateName = dateName+'-'+str(index)
                index +=1
                print(dateName, a['date'])
            self.list_holidays_no_scope[dateName] = a['date']
            # for i in self.list_holidays_no_scope.keys():
            #     if self.list_holidays_no_scope.values().count(self.list_holidays_no_scope[i]) > 1:
            #          del self.list_holidays_no_scope[i]
        #with scope
        if scope == 'Federal':
            holiday_query = session.query(HolidayBr).filter(HolidayBr.scope == 'Federal').order_by(HolidayBr.date.asc())
        elif scope == 'Municipal':
            holiday_query = session.query(HolidayBr).filter(HolidayBr.location == location)
            query_entries = session.query(HolidayBr).filter(HolidayBr.location == location).count()
        elif scope =='Estadual':
            holiday_query = session.query(HolidayBr).filter(and_(HolidayBr.region==state, HolidayBr.scope=='Estadual')).order_by(HolidayBr.date.asc())
            query_entries = session.query(HolidayBr).filter(HolidayBr.scope == state).count()
        # print(holiday_query)
        # print('-'*60)
        if query_entries < 200:
            for day in holiday_query:
                day_data = vars(day)
                holidays[scope][day_data['name']] = day_data['date']
               
            # print(self.list_holidays_no_scope)
    def getScopeFromHolidayDateKey(self, holidayName, holidays):
        for scope in holidays:
            for j in holidays[scope]:
                if holidayName == j:
                    return scope


    def findHolidaysOnDateRange(self,initialDate, endDate,cep):
        st = []
        currentDateToDays = 0
        dateFinal= {}
        # dateFinal['Feriados'] = {}
        dateFinal['Feriados'] = []
        holiday_location = {}
        holidays = {
            'Federal':{},
            'Estadual':{}, 
            'Municipal':{}
        }
        neutral = datetime.strptime('1900-01-01','%Y-%m-%d')
        try:
            address = pycep_correios.get_address_from_cep(cep)
            print('-'*80)
            print(address)
        except:
            return "CEP invalido"
        holiday_location['cidade'] = unidecode(address['cidade'])
        holiday_location['estado'] = unidecode(address['uf'])
        # print(holiday_location)
        # print("-"*10)
        scopes = ['Federal', 'Estadual', 'Municipal']
        for scope in scopes:
            self.getHolidayDict(scope, holidays, holiday_location)
        try:
            initialDateFormated = datetime.strptime(initialDate, '%Y-%m-%d')
            initialYear = initialDateFormated.year
            endDateFormated = datetime.strptime(endDate, '%Y-%m-%d')
            endDateToDays = int(abs((endDateFormated - neutral).days))
            initialDateToDays = int(abs((initialDateFormated - neutral).days))
            endYear = endDateFormated.year
            key_list_no_scope_holidays = [items for items in self.list_holidays_no_scope]
            holidayMainKeys = [keys for keys in holidays] #federal, municipal, estadual
            holidayNameKeys = [names for names in holidayMainKeys]
            if(initialDateToDays > endDateToDays):
                return {"message":"initialDateToDays is bigger than endDateToDays"}
            cycles = endYear-initialYear
            for cycle in range(cycles+2):
                year = initialYear+cycle
                # dateFinal['Feriados'][str(year)] = {}
        except:
            return {"message":"Invalid date format",
                    "error": "a"}
          
        index = 0
        j= 0
        # print(self.list_holidays_no_scope)
        dateFinal['status'] = '200'
        while(endDateToDays >  currentDateToDays):
                 
            if index == (len(key_list_no_scope_holidays)):
                index = 0
                initialYear += 1
            holidayScopeKey = holidayMainKeys[index % 3]
            holidayDateKeyList = [days for days in holidays[holidayScopeKey].keys()]           
            dateKey = key_list_no_scope_holidays[index % (len(self.list_holidays_no_scope))]
           
            # print(key)
            
            currentDate = str(initialYear)+"-"+self.list_holidays_no_scope[dateKey]
            currentDateFormated = datetime.strptime(currentDate, '%Y-%m-%d')
            currentDateToDays = int(abs((currentDateFormated - neutral).days))
            if(initialDateToDays <= currentDateToDays):
                if 'Feriado Municipal' in dateKey:
                    dateKey = 'Feriado Municipal'
                scope = self.getScopeFromHolidayDateKey(dateKey, holidays)
                year,month,day = (int(x) for x in currentDate.split('-')) 
                dateAux =  datetime(year, month, day)
                holidayContent = {
                        "holiday": unidecode(dateKey) ,
                        "date": currentDate,
                        "scope": scope,
                        "weekday": dateAux.strftime("%A"),
                        # "location": {
                        #     "city": address['cidade'],
                        #     "region": address['uf']
                        # },
                }
                # if scope == "Federal":
                #     holidayContent['location']['country']= 'Brasil'
                # else:
                #     holidayContent['location']['city']= address['cidade']
                dateFinal['Feriados'].append(holidayContent)
                # dateFinal['Feriados'][str(initialYear)][dateKey] = currentDate
                
            index +=1
            # print(dateFinal)
            # print(dateKey)
            # print(initialDateToDays, currentDateToDays, currentDate)
        dateFinal['Dias'] = holidays
        
        # if not len(dateFinal['Feriados'][str(endYear + 1)]):
        #     del dateFinal['Feriados'][str(endYear + 1)]
        # dateFinal['Feriados'][str(endYear + 1)].popitem()
        response = dateFinal
        del dateFinal
        return response
