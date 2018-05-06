# Module for reading CSV's
import csv
# Importing system modules
import os
import sys
from collections import defaultdict

"""
FUNCTION (main): 
This is the main function, where the analysis of Election CSV file is done

INPUT: 
argv - list of command-line arguments

OUTPUT:
Election summary is written to a file if provided as an argument to the script, else prints to the terminal
"""
def main(argv):
    #Variables for outputting to a file, if specified as a command line argument
    output_filename = '' 
    output_to_file = False

    #Check if the <input file> is specified else, return
    if(len(argv) < 2):
        print("Input file not specified: Usage Pattern - python main.py budget_data_1.csv")
        return 
    
    #Check if <output file> is specified in the command-line    
    if(len(argv) > 2):
        output_filename = argv[2]
        output_to_file = True

    # Lists to store dates and revenue from the CSV
    voter_id_list = []
    candidate_list = []

    

    try:
        #Open the CSV file in read-only mode
        with open(argv[1],'r', newline='') as csvfile:
            #reading CSV file
            csvreader = csv.reader(csvfile, delimiter=',')
            #skipping the header row
            next(csvreader)

            #Iterate through all the rows in the CSV file 
            for row in csvreader:
                #Adding the Voter Id to the list
                voter_id_list.append(int(row[0]))
                #Adding the Candidate to the list               
                candidate_list.append(row[2])

            candidate_voter_list = []
            for i in range(len(voter_id_list)):
                candidate = candidate_list[i]
                voter = voter_id_list[i]
                candidate_voter_list.append(tuple((candidate, voter)))
            
            # Dictionary to group the Voter Id's by Candidate and remove duplicates
            candidate_voter_dict = defaultdict(list)
            for candidate, voter in candidate_voter_list:
                candidate_voter_dict[candidate].append(voter)

            total_votes_cast = sum(map(len, candidate_voter_dict.values()))

            votes_candidates_received = list(candidate_voter_dict.keys())
            num_votes_candidate = map(len, candidate_voter_dict.values())
            candidate_voter_summary_dict = dict(zip(votes_candidates_received,num_votes_candidate))
            
            max_vote_count = max(candidate_voter_summary_dict.values())
     
            if output_to_file:
                with open(output_filename,'w') as outfile:
                    outfile.writelines("Election Results\n")
                    outfile.writelines("--"*30+"\n")
                    outfile.writelines("Total Votes Cast:  {}\n".format(total_votes_cast))
                    outfile.writelines("--"*30+"\n")
                    for candidate, num_votes in candidate_voter_summary_dict.items():
                        percent_votes = (num_votes/total_votes_cast)*100
                        if (num_votes == max_vote_count):
                            winner = candidate
                        outfile.writelines("{}:\t{}% ({})\n".format(candidate, percent_votes, num_votes))
                    outfile.writelines("--"*30+"\n")
                    outfile.writelines("Winner: {}\n".format(winner))
            # if output file is not specified, then prints summary to the terminal 
            else:
                print("Election Results")
                print("--"*30)
                print("Total Votes Cast:  {}".format(total_votes_cast))
                print("--"*30)
                for candidate, num_votes in candidate_voter_summary_dict.items():
                    percent_votes = (num_votes/total_votes_cast)*100
                    if (num_votes == max_vote_count):
                        winner = candidate
                    print("{}:\t{}% ({})".format(candidate, percent_votes, num_votes))
                print("--"*30)
                print("Winner: {}".format(winner))
            

         
    except FileNotFoundError:
        print("Wrong file or file path")
    # for all other execptions
    except:
        print("Unexpected error:", sys.exc_info()[0])

# call main function only when this script (main.py) is the main script file
if(__name__ == "__main__"):
    main(sys.argv)