#This file takes in the point source emissions data and creates MONTHLY profiles for every source given.
# NOTE: This is run BEFORE mk_PTREF.py
#The name for the MONTHLY profiles have the following format: (Site ID)_(Stack ID)_(Process ID)
#The format of inputted data should be:
#FIPS	NAICS	SIC	Site ID	Site Name	Component ID	Process ID	SCC	Stack ID	Stack Height	Stack Diameter	Stack Temp	Stack Flow	Stack Velocity	Latitude	Longitude	Hrs/Day	Days/Wk	Wks/Yr	Hrs/Yr	Jan %	Feb %	Mar %	Apr %	May %	Jun %	Jul %	Aug %	Sep %	Oct %	Nov %	Dec %	2011 Tons/Yr	Pollutant

import csv

# PARAMS:
outp_dir = '2019 business as usual/Provo NA only'
csv_file = outp_dir + '/PM2.5 Utah County SIP - 2019 Point Source Data - 120117.csv'
monthly_ptpro = outp_dir + '/ptpro_monthly_2019_provoNA_4dec2017.txt'
#

monthly_codes = {}
mon_incr = 1
mon_file = outp_dir + '/moncodes.txt'
ofh = open(mon_file,'w')

with open(csv_file,'rb') as csvimport: #INPUT FILE
    csvfile = list(csv.reader(csvimport))
    row_storage = []
    row_storage.append([0, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, '""'])	#DEFAULT
    row_storage.append(['FLAT', 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, 0.0833, '""'])  #FLAT
    for row in csvfile:
        if row[0] == 'FIPS':
            continue

        denominator = 0
        for cell in range(20, 32):
            denominator += float(row[cell])
        for cell in range(20,32):
            row[cell]= float(row[cell])/denominator	#normalize

        uniq_id = [row[7],row[0],row[3],row[5],row[8],row[6]]
            
        new_row = [uniq_id, "{:.6f}".format(row[20]),"{:.6f}".format(row[21]),"{:.6f}".format(row[22]),
                   "{:.6f}".format(row[23]),"{:.6f}".format(row[24]),"{:.6f}".format(row[25]),"{:.6f}".format(row[26]),
                   "{:.6f}".format(row[27]),"{:.6f}".format(row[28]),"{:.6f}".format(row[29]),"{:.6f}".format(row[30]),
                   "{:.6f}".format(row[31]), '""' ]
        
        if new_row in row_storage:	#Prevent duplicates
            continue
        else:
            row_storage.append(new_row)
            monthly_code_ix = ','.join(uniq_id)
            monthly_codes[monthly_code_ix] = mon_incr
            new_row[0] = str(mon_incr)  # Change to simpler code Alias for PTREF
            ofh.write('{0},{1}\n'.format(monthly_code_ix,mon_incr))
            mon_incr += 1
            
ofh.close()

with open(monthly_ptpro, 'wb') as csvexport1:   #EXPORT FILE
    outputcsv1 = csv.writer(csvexport1,quotechar="'")
    for row in row_storage:
        outputcsv1.writerow(row)

    print 'Finished!'




