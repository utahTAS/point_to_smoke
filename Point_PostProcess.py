#This file is meant to format the data given in house by Scott for point emissions formatting.
#This file assumes all emission magnitudes are given in tons/year
#The only changes needed to run are the INPUT and EXPORT file names, and a check of the naming convention.
#The input csv format should be as follows
#FIPS	NAICS	SIC	Site ID	Site Name	Component ID	Process ID	SCC	Stack ID	Stack Height	Stack Diameter	Stack Temp	Stack Flow	Stack Velocity	Latitude	Longitude	Hrs/Day	Days/Wk	Wks/Yr	Hrs/Yr	Jan %	Feb %	Mar %	Apr %	May %	Jun %	Jul %	Aug %	Sep %	Oct %	Nov %	Dec %	2011 Tons/Yr	Pollutant

# 9/21/2016 - Some usage changes, cjp
import csv
import re

BTEX = False #change to include or exclude Benzene, Toluene, Xylene
csv_name = 'PM2.5 Utah County SIP - 2019 Point Source Data - 120117.csv'
orl_name = '2019point_provoNA.orl'
with open(csv_name,'rb') as csvimport: #INPUT FILE
  csvfile = csv.reader(csvimport)
  row_storage = []
  if BTEX == True:    #Switch
    re_search = re.compile(r'71432|108883|1330207|^CO$|NH3|NOX|SO2|VOC|PM10|PM2_5|7782505|7647010|')
  else:
    re_search = re.compile(r'^CO$|NH3|NOX|SO2|VOC|PM10|PM2_5|7782505|7647010')

  for row in csvfile: #name conventions <======= CHECK THIS
    if row[0] == "FIPS":
      continue

    if row[33] == 'PM10X':
      row[33] = 'PM10'
    elif row[33] == 'PM25X' or row[33] == 'PM25':
      row[33] = 'PM2_5'
    elif row[33] == 'benzene' or row[33] == 'Benzene':
      row[33] = '71432'
    elif row[33] == 'toluene' or row[33] == 'Toluene':
      row[33] = '108883'
    elif row[33] == 'xylene' or row[33] == 'Xylene':
      row[33] = '1330207'
    elif row[33] == 'SOX':
      row[33] = 'SO2'
    elif row[33] == 'Chlorine' or row[33] == 'chlorine':
      row[33] = '7782505'
    elif row[33] == 'HCl':
      row[33] = '7647010'

    if float(row[32]) < 0:
      row[32] = 0

    if len(row[4]) > 40:	#make sure name isn't longer than 40 characters
      row[4] = row[4][0:40]

    # Substitute underscores for spaces:
    row[4] = row[4].replace(' ', '_')
    if row[10] == '0':		#stack diameters cannot be zero
      row[10] = '-9'

    if re_search.findall(str(row[33])) == []:    #ignore unwated species
      continue
    else:
      ton_d = float(row[32])/365 #t/yr to ton/day
      row_storage.append([row[0],row[3],row[5],row[8],row[6],row[4],row[7],"02","01",row[9],row[10],row[11],row[12],row[13],row[2],'-9',row[1],'L',row[15],row[14],'-9',row[33],"{:10.6f}".format(float(row[32])),"{:10.6f}".format(ton_d),'0','100'])

with open(orl_name, 'wb') as csvexport1:   #EXPORT FILE
  outputcsv1 = csv.writer(csvexport1, delimiter='\t')
  for row in row_storage:
    outputcsv1.writerow(row)

print 'Finished!'




