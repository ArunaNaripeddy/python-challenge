"""
This python script analyzes the election data.
1. It assumes the election data to be available in the form of a CSV file with a list of (voter id, county, candidates) 
2. Input: election data csv file, optional output file 
3. Output: Election result summary is written to a file if provided as an argument to the script, else prints to the terminal
USAGE:
For running the script - python main.py <input_csv_filepath> <output_filepath> 
Required: <input_csv filepath>
Optional: <output_filepath>
"""

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
    # Variables for outputting to a file, if specified as a command line argument
    output_filename = '' 
    output_to_file = False

    # Check if the <input file> is specified else, return
    if(len(argv) < 2):
        print("Input file not specified: Usage Pattern - python main.py budget_data_1.csv")
        return 
    
    # Check if <output file> is specified in the command-line    
    if(len(argv) > 2):
        output_filename = argv[2]
        output_to_file = True

    # Lists to store voters and candidates from the CSV
    voter_id_list = []
    candidate_list = []

    try:
        # Open the CSV file in read-only mode
        with open(argv[1],'r', newline='') as csvfile:
            # reading CSV file
            csvreader = csv.reader(csvfile, delimiter=',')
            # skipping the header row
            next(csvreader)

            # Iterate through all the rows in the CSV file 
            candidate_voter_dict = defaultdict(list)
            for row in csvreader:
                # Dictionary to group the Voter Id's by Candidate and remove duplicates
                candidate_voter_dict[row[2]].append(int(row[0]))           

            # Total number of votes cast
            total_votes_cast = sum(map(len, candidate_voter_dict.values()))

            # List of candidates that received votes 
            candidates_list = list(candidate_voter_dict.keys())
            # Number of votes received by each candidate
            num_votes_candidate = map(len, candidate_voter_dict.values())
            # Election summary dictionary containing candidates and number of votes for each candidate 
            candidate_voter_summary_dict = dict(zip(candidates_list, num_votes_candidate))
            # Highest number of votes
            max_vote_count = max(candidate_voter_summary_dict.values())

            # If output file is specified, election summary is written to the specified file
            if output_to_file:
                with open(output_filename,'w') as outfile:
                    outfile.writelines("Election Results\n")
                    outfile.writelines("--"*30+"\n")
                    outfile.writelines("Total Votes Cast:  {}\n".format(total_votes_cast))
                    outfile.writelines("--"*30+"\n")
                    for candidate, num_votes in candidate_voter_summary_dict.items():
                        percent_votes = round((num_votes/total_votes_cast)*100, 2)
                        if (num_votes == max_vote_count):
                            winner = candidate
                        outfile.writelines("{:12s}:\t{}% ({})\n".format(candidate, percent_votes, num_votes))
                    outfile.writelines("--"*30+"\n")
                    outfile.writelines("Winner: {}\n".format(winner))
            # if output file is not specified, then prints summary to the terminal 
            else:
                print("Election Results")
                print("--"*30)
                print("Total Votes Cast:  {}".format(total_votes_cast))
                print("--"*30)
                for candidate, num_votes in candidate_voter_summary_dict.items():
                    percent_votes = round((num_votes/total_votes_cast)*100, 2)
                    if (num_votes == max_vote_count):
                        winner = candidate
                    print("{:12s}:\t{}% ({})".format(candidate, percent_votes, num_votes))
                print("--"*30)
                print("Winner: {}".format(winner))
            
    # If specified file path is invalid or unable to open   
    except FileNotFoundError:
        print("Wrong file or file path")
    # for all other exceptions
    except:
        print("Unexpected error:", sys.exc_info()[0])

# call main function only when this script (main.py) is the main script file
if(__name__ == "__main__"):
    main(sys.argv)