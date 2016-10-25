from modules.PrEDIction import PrEDIction
from modules.PrEDIction import PrEDIctionClient
from modules.PrEDIction import PrEDIctionPrinter
import datetime

def process_client(client, data, prediction, printer):

    cut_time_options = ['1H', '3H', '1D', '7D', '14D', 'All']
    
    grouping_weekday_options = ['All']    
    grouping_options = ['1H', '1D']

    folding_weekday_options = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'NoWeekends']
    folding_options = ['1H']
    
    cumsum_weekday_options = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'NoWeekends']
    cumsum_options = ['1H']

    for weekday in grouping_weekday_options:
        for option in grouping_options:
            for cut_time in cut_time_options:
                client.set_weekday(weekday)
                client.set_plot_type('Grouped')
                client.set_cut_time(cut_time)
                pregrouped_data = prediction.pregroup_data(data, option, cut_time)
                prefiltered_data = prediction.prefilter_data_by_weekday(pregrouped_data, weekday)
                grouped_data = prediction.group_data(prefiltered_data, option, client)
                printer.add_data(grouped_data)
                printer.print_grouped()
                printer.clean()
            
#    for weekday in folding_weekday_options:
#        for option in folding_options:
#            client.set_weekday(weekday)
#            client.set_plot_type('Folded')            
#            pregrouped_data = prediction.pregroup_data(data, option)
#            prefiltered_data = prediction.prefilter_data_by_weekday(pregrouped_data, weekday)
#            folded_data = prediction.fold_data(prefiltered_data, option, client)
#            printer.add_data(folded_data)
#            printer.print_folded()
#            printer.clean()
#
#    for weekday in cumsum_weekday_options:
#        for option in cumsum_options:
#            client.set_weekday(weekday)
#            client.set_plot_type('Cumsum')
#            pregrouped_data = prediction.pregroup_data(data, option)
#            prefiltered_data = prediction.prefilter_data_by_weekday(pregrouped_data, weekday)
#            cumsumed_data = prediction.cumsum_folded_data(prefiltered_data)
#            folded_data = prediction.fold_data(cumsumed_data, option, client)
#            printer.add_data(folded_data)
#            printer.print_folded()
#            printer.clean()
            
def main():
    accepted_clients = '''select l1.edi_client_desc, l1.application, count(*) "count"
                          from editt.editt_level1 l1
                          join editt.editt_level2 l2
                          on l2.id_lvl1 = l1.id
                          where l2.line_message_status = 'FULLY_ACCEPTED'
                          group by l1.edi_client_desc, l1.application
                          order by "count" desc'''

    client_1 = '''select l1.transmission_date
                  from editt.editt_level1 l1
                  join editt.editt_level2 l2
                  on l2.id_lvl1 = l1.id
                  where l2.line_message_status = '''
    client_2 = ''' and nvl(l1.edi_client_desc, 'none') = '''
    client_3 = ''' and nvl(l1.application, 'none') = '''
    client_4 = ''' order by l1.transmission_date desc'''
    
    prediction = PrEDIction()
    printer = PrEDIctionPrinter()
    client = PrEDIctionClient()
    
    prediction.set_number_of_clients_limit(1)    
    all_clients = prediction.get_clients(accepted_clients)
    
    for client_info in all_clients:
        client.set_client(client_info)
        print('[' + str(datetime.datetime.now()) + '] ' + 'Working on ' + client.get_id() + ' - got ' + str(client.get_count()) + ' messages' )
        client_query = client_1 + '\'FULLY_ACCEPTED\'' + client_2 + client.get_desc() + client_3 + client.get_document_type() + client_4
        data = prediction.get_data(client_query)
        process_client(client, data, prediction, printer)
        client.clean()
    
if __name__ == '__main__':
    main()    
