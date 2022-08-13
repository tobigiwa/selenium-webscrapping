import os

result_folder = 'result_tsv'

if os.path.exists(result_folder):
    for files in os.scandir(result_folder):
        os.remove(files)
else:
    os.makedirs(result_folder)

tsv_path = os.path.join(os.getcwd(), result_folder)




# header_row = ['scrappedURL', 'eventname', 'startdate', 'enddate', 'timming', 'eventinfo', 'ticketlist',\
#     'orgProfile', 'orgName', 'orgWeb', 'logo', 'sponsor', 'agendalist', 'type', 'category', 'city',\
#     'country', 'venue', 'event_website', 'googlePlaceUrl', 'ContactMail', 'Speakerlist', 'online_event']

# with open(f'{tsv_path}/scape_data.tsv', 'w+') as tsv_file:
#         writer = csv.writer(tsv_file, delimiter='\t')
#         writer.writerow(header_row)

# __all__ = [tsv_path]