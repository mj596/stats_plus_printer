import numpy as np
import datetime
import pandas as pd
from modules.DBConnector import DBConnector
from . import PrEDIctionData
from ..TimeUtils import TimeUtils

class PrEDIction:
    
    def __init__(self):
        self.number_of_clients_limit = 5
        self.timeUtils = TimeUtils()
        
    def set_number_of_clients_limit(self, clients):
        self.number_of_clients_limit = clients
        
    def get_data(self, query):
        db = DBConnector()
        db.setCredentials('editt_viewer', 'editt_view2016', 'soadb.raben-group.com', 'EDITT')
        db.connect()
        data = db.execute(query)
        db.disconnect()
        return_data = np.array(data).transpose()[0].transpose()
        
        return return_data

    def get_clients(self, query):
        db = DBConnector()
        db.setCredentials('editt_viewer', 'editt_view2016', 'soadb.raben-group.com', 'EDITT')
        db.connect()
        data = db.execute(query)
        db.disconnect()
        return_data = np.array(data[:self.number_of_clients_limit])
        
        return return_data
    
    def filter_weekends(self, data):
        returnData = []

        for item in data:
            if( self.timeUtils.getWeekday(item) != 'Saturday' and self.timeUtils.getWeekday(item) != 'Sunday' ):
                returnData.append(item)

        return returnData

    def filter_weekday(self, data, weekday):
        returnData = []

        for item in data:
            if( self.timeUtils.getWeekday(item) == weekday ):
                returnData.append(item)

        return returnData

    def pregroup_data(self, data, type):
        data_frame = pd.DataFrame( data=np.ones(len(data)), index=data, columns = ['amount'] )
        grouped = data_frame.groupby( pd.TimeGrouper(freq=type) ).count()
        return grouped
    
    def prefilter_data_by_weekday(self, data, weekday):
        if weekday == 'All':
            filtered = data
        elif weekday == 'NoWeekends':
            no_weekends_array = np.bool_( (np.sum([[data.index.weekday == 0], [data.index.weekday == 1], [data.index.weekday == 2], [data.index.weekday == 3], [data.index.weekday == 4]], axis=0))[0] )
            filtered = data[no_weekends_array]            
        else:
            weekday_number = self.timeUtils.get_weekday_number(weekday)
            filtered = data[data.index.weekday == weekday_number]

        return filtered

    def get_type(self, type):
        time_unit = 'H'
        if 'Min' in type:
            time_unit = 'Min'
        if 'H' in type:
            time_unit = 'H'

        time_amount = int(type.strip(time_unit))
            
        return time_amount, time_unit

    def get_delta_time(self, time_amount, time_unit):
        delta_time = 0
        
        if time_unit == 'Min':
            delta_time = datetime.timedelta(hours=0, minutes=int(0.5*time_amount), seconds=0)
        elif time_unit == 'H':
            delta_time = datetime.timedelta(hours=0, minutes=int(0.5*60*time_amount), seconds=0)
            
        return delta_time

    def group_data(self, data, type):
        time_amount, time_unit = self.get_type(type)
        delta_time = self.get_delta_time(time_amount, time_unit)
        
        tsdc = PrEDIctionData.PrEDIctionData()

        tsdc.set_time_amount(time_amount)
        tsdc.set_time_unit(time_unit)

        selector = [pd.to_datetime(str(t)).strftime("%Y-%m-%d %H:%M") for t in data.index]
        tsdc.set_time(selector)
        tsdc.set_delta_time(np.ones(len(selector)) * delta_time)        
        tsdc.set_mean(data.values.transpose()[0])

        return tsdc

    def cumsum_folded_data(self, data):        
        cumsum_data = data.groupby( pd.TimeGrouper(freq='D'))
        return pd.DataFrame( data=cumsum_data['amount'].cumsum().values, index=data.index, columns = ['amount'] )

    def fold_data(self, data, type, client):
        df = pd.DataFrame(index=pd.date_range("00:00", "23:59", freq=type).time)
        df.name = client.get_desc() + '_' + client.get_document_type() + '_' + type + '_' + client.get_weekday() + '_' + str(data.index.min()) + '_' + str(data.index.max()) + '_' + str(client.get_plot_type())
        
        folded_data = { 'delta': [],
                        'mean': [],
                        'std': [],
                        'min': [],
                        'max': [],
                        'values': [] }
        
        for i in range(len(df.index.values)):
            start = df.index.values[i]
                       
            if i == len(df.index.values)-1:
                end = df.index.values[0]
            else:
                end = df.index.values[i+1]

            selected = data.between_time(start, end, include_start=True, include_end=False).values.transpose()[0]
            folded_data['delta'].append(pd.Timedelta(type))
            folded_data['mean'].append(selected.mean())
            folded_data['std'].append(selected.std())
            folded_data['min'].append(selected.min())
            folded_data['max'].append(selected.max())
            folded_data['values'].append(selected)

        df['delta'] = pd.Series(folded_data['delta'], index=df.index)            
        df['mean'] = pd.Series(folded_data['mean'], index=df.index)
        df['std'] = pd.Series(folded_data['std'], index=df.index)
        df['min'] = pd.Series(folded_data['min'], index=df.index)
        df['max'] = pd.Series(folded_data['max'], index=df.index)
        df['values'] = pd.Series(folded_data['values'], index=df.index)        
        
        return df
