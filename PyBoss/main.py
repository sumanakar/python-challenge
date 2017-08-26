import os
import csv
import datetime

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

file=os.path.join("employee_data2.csv")


with open(file,'r' ) as data, open("output_pyboss2.csv","w") as file_output:
    
    file_write=csv.writer(file_output,delimiter=",")
        
    file_write.writerow(["first_name","last_name","Date","SSN","State"])
    
    datafile=csv.reader(data,delimiter=',')
    next(datafile)
    
    for row in datafile:
        
        
        fullname=row[1].split()
        first_name=fullname[0]
        lastname=fullname[1]
        new_date= datetime.datetime.strptime(row[2], '%Y-%m-%d').strftime('%m/%d/%Y')
        count=0
        new_ssn=''
        for i in row[3]:
                
            if count <=5 and count!=3:
                i='*'
                new_ssn=new_ssn+i
                count=count+1
                
            
            else:
                new_ssn=new_ssn+i
                count=count+1 
                continue
        
               
        for state,st in us_state_abbrev.items():
            
            if state==row[4]:
                
                newvalue_st=st
            
        rowin=[first_name,lastname,new_date,new_ssn,newvalue_st]
        print(rowin)
            
        file_write.writerow(rowin)
        
                
                
         
         
        
        
        
        
    
        
    
    
    
        
        
     


