#This file takes in the point source emissions data and creates a PTREF for the data given
# NOTE: This is run AFTER mk_PTPRO_MONTHLY.py
#The allday profiles should have the naming convention PTHR_num where num is the number of hours the source runs per day.  e.g. PTHR_24
#The weekly profiles should have the naming convention PTWK_days where days is the number of days per week that the source runs.  e.g. PTWK_7
#The monthly profiles should have the format "site ID"_"stack ID".  e.g. 10008_927579

# Update: Adding SCC and replacing 0 with -9 for G "Pollutant name"

#The format of inputted data should be:
#FIPS	NAICS	SIC	Site ID	Site Name	Component ID	Process ID	SCC	Stack ID	Stack Height	Stack Diameter	Stack Temp	Stack Flow	Stack Velocity	Latitude	Longitude	Hrs/Day	Days/Wk	Wks/Yr	Hrs/Yr	Jan %	Feb %	Mar %	Apr %	May %	Jun %	Jul %	Aug %	Sep %	Oct %	Nov %	Dec %	2011 Tons/Yr	Pollutant

"""
scc = 7
fips = 0
plant_id = 3
component_id = 5
stack_id = 8
process_cd = 6
"""

import csv
import math

# PARAMS:
outp_dir = '2019 business as usual/Provo NA only'
csv_file = outp_dir + '/PM2.5 Utah County SIP - 2019 Point Source Data - 120117.csv'
ptref_file = outp_dir + '/ptref_2019_provoNA_4dec2017.txt'
#

# Output a lookup table for the PTREF script
monthly_codes = {}
mon_file = outp_dir + '/moncodes.txt'
# Load monthly code alias file:
with open(mon_file,'r') as ifh:
    for line in ifh:
        scc,fips,plant_id,component_id,stack_id,process_cd,moncode = line.rstrip().split(',')
        monthly_code_ix = ','.join([scc,fips,plant_id,component_id,stack_id,process_cd])
        monthly_codes[monthly_code_ix] = moncode

dup_tracker = {}

with open(csv_file,'rb') as csvimport: #INPUT FILE
    csvfile = list(csv.reader(csvimport))
    row_storage = []
    row_storage.append(['0','','','','','','','ALLDAY', 'PTHR_24', '""'])
    row_storage.append(['0','','','','','','','MONTHLY', 'FLAT', '""'])
    row_storage.append(['0','','','','','','','WEEKLY', 'PTWK_7', '""'])
    for row in csvfile:
        if row[0] == "FIPS":
            continue
		
        if float(row[16]) <= 0.5 and float(row[16]) != 0: #anything not zero rounds to one hour
            row[16] = '1'

        if float(row[16]) == 0:
            row[16] = math.ceil(float(row[19])/365)  #any hour/day that is zero, replace it with the given hours/yr data

        if float(row[17]) == 0:
            row[17] = math.ceil(float(row[19])/(24*52))  #any days/week that is zero, replace with given hours/yr data

        # Check for duplicates:
        #scc, fips, plant_id, component_id, stack_id, process_cd
        monthly_code_ix = ','.join([row[7],row[0],row[3],row[5],row[8],row[6]])
        moncode = monthly_codes[monthly_code_ix]
        if monthly_code_ix in dup_tracker:
            continue
        else:
            dup_tracker[monthly_code_ix] = 1

        # Check not greater than 24 hours/day
        pthr = int(math.ceil(float(row[16])))
        if pthr > 24:
            pthr = 24
            
        row_storage.append([row[7],row[0],row[3],row[5],row[8],row[6],'-9','ALLDAY','PTHR_'+str(pthr),'""'])
        row_storage.append([row[7],row[0],row[3],row[5],row[8],row[6],'-9','WEEKLY','PTWK_'+str(int(float(row[17]))),'""'] )
        row_storage.append([row[7],row[0],row[3],row[5],row[8],row[6],'-9','MONTHLY',moncode,'""' ])

with open(ptref_file, 'wb') as csvexport1:   #export
    outputcsv1 = csv.writer(csvexport1,quotechar="'")
    for row in row_storage:
        outputcsv1.writerow(row)

    print 'Finished!'




