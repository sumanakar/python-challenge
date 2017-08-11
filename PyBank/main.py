import csv

from pip._vendor.distlib.compat import raw_input



input_file = raw_input("Enter the CSV file name.Enter the file extension at the end\n")
    
#Open CSV file
with open(input_file) as csvfile1:            
    readCSV1 = csv.reader(csvfile1, delimiter=',')
    #declare two variable
    budget1_dates = []                                    
    budget1_revenues = []
    
    
    #read the rows in csv file
    
    for row1 in readCSV1:                                   
        budget1_date = row1[0]
        budget1_revenue = row1[1]
        budget1_dates.append(budget1_date)
        budget1_revenues.append(budget1_revenue)

excludedateheader=budget1_dates[1:]
excluderevenueheader= budget1_revenues[1:]
# Total Months
Total_Months=len(excludedateheader)
Total_Revenue=0
i=0
# Total Revenue
while (i<len(excluderevenueheader)):
    
    Total_Revenue=Total_Revenue+int(excluderevenueheader[i-1])
    i=i+1
# Average Revenue Change

Average_Revenue_Change=round(Total_Revenue/Total_Months,2)

#Greatest Increase Revenue

Greatest_Increase_Revenue=max(excluderevenueheader)
index1=excluderevenueheader.index(Greatest_Increase_Revenue)
Greatest_Increase_Revenue_date=excludedateheader[index1]

#Greatest decrease Revenue
Greatest_decrease_Revenue=min(excluderevenueheader)
index2=excluderevenueheader.index(Greatest_decrease_Revenue)
Greatest_decrease_Revenue_date=excludedateheader[index2]

#output

print("Financial Analysis")
print("----------------------------")
print("Total_Months :  " + str(Total_Months))
print("Total_Revenue: " + str(Total_Revenue))
print("Greatest Increase Revenue: "+ str(Greatest_Increase_Revenue))
print("Greatest Decrease Revenue: "+ str(Greatest_decrease_Revenue))


#output in txt

f=open("output.txt","w+");

f.write("Financial Analysis\n")
f.write("----------------------------\n")
f.write("Total_Months :  " + str(Total_Months)+"\n")
f.write("Total_Revenue: " + str(Total_Revenue)+"\n")
f.write("Greatest Increase Revenue: "+ str(Greatest_Increase_Revenue)+"\n")
f.write("Greatest Decrease Revenue: "+ str(Greatest_decrease_Revenue)+"\n")
f.close()                                 