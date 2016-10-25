import matplotlib.pyplot as plt
import numpy as np
import datetime
import time
import os
import pandas as pd
from matplotlib.font_manager import FontProperties

class PrEDIctionPrinter:
    
    weekdayLabels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    font = FontProperties()
    font.set_family('sans-serif')
    font.set_variant('small-caps')
    font.set_size(8)
    font.set_family('monospace')
    
    def __init__(self):
        self.data = None
        self.filename = 'test_filename'
        self.folder = 'printer_out/test_folder'
        
    def add_data(self, tsdc):
        self.data = tsdc

    def clean(self):
        self.data = None

    def set_filename(self, filename):
        self.filename = filename

    def set_folder(self, folder):
        self.folder = 'printer_out/' + folder

    def print_folded(self):        
        plt.clf()
        with plt.style.context(('ggplot')):
            time = []
            for i in self.data.index:
                time.append( datetime.datetime.combine(datetime.datetime.now().date(), i) )
                
            time_error = datetime.timedelta( seconds=0.5*int(self.data['delta'].values[0])/1e9 ) * np.ones(len(self.data['delta'].values))

            plt.errorbar(time, self.data['mean'], xerr=time_error, yerr=self.data['std'], fmt='b.', capsize=0, label='mean +- std deviation')
            plt.errorbar(time, self.data['min'], xerr=time_error, fmt='r.', markersize=0, capsize=0, label='min/max')
            plt.errorbar(time, self.data['max'], xerr=time_error, fmt='r.', markersize=0, capsize=0, label=None)
            
            for key in self.data.index:
                time = [datetime.datetime.combine(datetime.datetime.now().date(), key) for i in self.data['values'][key]]
                plt.plot(time, self.data['values'][key], 'go', alpha=0.1)
            
            client_desc = (self.data.name.split('_')[0]).replace('\'','')
            client_document_type = (self.data.name.split('_')[1]).replace('\'','')
            client_type = self.data.name.split('_')[2]
            client_weekday = self.data.name.split('_')[3]
            time_range_start = self.data.name.split('_')[4]
            time_range_end = self.data.name.split('_')[5]            
            plot_type = self.data.name.split('_')[6]
            
            plt.text('00:00:00', 0.75*self.data['max'].max(), 'Client: ' + client_desc + '\n' + 'Application: ' + client_document_type + '\n' + 'Weekday: ' + client_weekday + '\n' + 'Grouped by: ' + client_type + '\n' + 'From: ' + time_range_start + '\n' + 'To: ' + time_range_end + '\n' + 'PlotType: ' + plot_type, fontproperties=self.font)

            plt.ylim([-10, 1.1*self.data['max'].max()])

            plt.legend(loc=2, prop=self.font, fancybox=None, frameon=None)

            plt.xticks(rotation=20, fontproperties=self.font)
            plt.yticks(fontproperties=self.font)
            plt.ylabel('Number of EDI transmissions', fontproperties=self.font)

            self.folder = 'printer_out' + '/' + plot_type + '/' + 'Client' + client_desc + 'Application' + client_document_type
            self.filename = 'Client' + client_desc + 'Application' + client_document_type + 'Weekday' + client_weekday + 'GroupedBy' + client_type + 'PlotType' + plot_type + 'folded'
        
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
            
        plt.savefig(self.folder + '/' + self.filename+'.png', dpi=300)
        
    def print_grouped(self):
        plt.clf()
        
        with plt.style.context(('ggplot')):
            xtime = [self.datetime.datetime.strptime(elem, '%Y-%m-%d %H:%M') for elem in self.data.get_time()]
            histogram_width_in_days = 2*self.data.get_delta_time()[0].total_seconds()/(3600*24)
            plt.bar(xtime, self.data.get_mean(), width=histogram_width_in_days, alpha=0.5)
                    
            plt.xticks(rotation=20, size=10)
                    
            plt.title(self.filename)
            plt.ylabel('Number of EDI transmissions')

        if not os.path.exists(self.folder):
            os.makedirs(self.folder + '/out/')
            
        plt.savefig(self.folder + '/out/' + self.filename+'.png', dpi=300)
