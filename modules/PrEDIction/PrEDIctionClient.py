class PrEDIctionClient:

    def __init__(self):
        self.client = None
        self.weekday = None
        self.plot_type = None
        self.cut_time = None
        
    def set_client(self, client):
        self.client = client

    def clean(self):
        self.client = None
        
    def get_desc(self):
        if self.client[0] is None:
            self.client[0] = 'none'
            
        return '\''+self.client[0]+'\''

    def get_document_type(self):
        if self.client[1] is None:
            self.client[1] = 'none'

        return '\''+self.client[1]+'\''
    
    def get_id(self):
        if self.client[0] is None:
            self.client[0] = 'none'
        if self.client[1] is None:
            self.client[1] = 'none'

        return self.client[0] + '_' + self.client[1]

    def get_count(self):
        return self.client[2]

    def set_weekday(self, weekday):
        self.weekday = weekday

    def get_weekday(self):
        return self.weekday

    def set_plot_type(self, plot_type):
        self.plot_type = plot_type

    def get_plot_type(self):
        return self.plot_type

    def set_cut_time(self, cut_time):
        self.cut_time = cut_time

    def get_cut_time(self):
        return self.cut_time
