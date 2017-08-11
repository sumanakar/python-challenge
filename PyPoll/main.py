#task to read csv file
import csv

with open('election_data_2.csv') as csv_file:
    
    read_file =csv.reader(csv_file, delimiter=',')
    voter_ids=[]
    countys=[]
    candidates=[]
    percentage=[]
    winner=[]
   
    #read the rows in csv file
    for row in read_file:
        voter_id=row[0]
        county=row[1]
        candidate=row[2]
        voter_ids.append(voter_id)
        countys.append(county)
        candidates.append(candidate)
    
voter_ids=voter_ids[1:]
countys=countys[1:]
candidates=candidates[1:]

#task to calculate total votes
total_votes=len(voter_ids)
print("Total Votes :" +str(total_votes))

#complete list of candidates who received votes
candidate_unique=[]


for i in candidates:    
    if i not in candidate_unique:        
        candidate_unique.append(i)
        print(i)        

for i in candidate_unique:
    counter=0    
    for j in candidates:        
        if i==j:
            counter=counter+1            
    percent=round((counter/total_votes)*100,2)
    percentage.append(percent)
    winner.append(i)
    print("The total count of votes for " +i+ "is :" +str(counter)+" and percentage of vote is : "+ str(percent) +"%")

maxpercent=max(percentage)
index1=percentage.index(maxpercent)
winner_candidate=winner[index1]

print("the winner is : "+winner_candidate)
            

#percentage of votes each candidate won
# total number of votes each candidate won
#winner
