"""
This python script analyzes the budget data.
1. It assumes the budget data to be available in the form of a CSV file with a list of (date, revenue) 
2. Input: Supported date formats are - (mm-yy, mm-yyyy, month-yyyy, mm/yy, mm/yyyy, mm.yy, mm.yyyy, yyyy-mm-dd, dd.mm.yyyy, dd/mm/yyyy
3. Output: Budget summary is written to a file if provided as an argument to the script, else prints to the terminal
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
from datetime import datetime as dt


"""
FUNCTION (Parse_date): 
It parses the date against the different date patterns. 
Currently, few patterns are supported, new patterns can be added easily 

INPUT: 
Date - Takes the date as input

OUTPUT:
Returns the datetime object
Raises exception for unsupported date patterns
"""
def parse_date(text):
    #Checking the date against supported date patterns
    for fmt in ('%b-%y','%b-%Y', '%b/%y','%b/%Y', '%b.%y','%b.%Y','%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y'):
        try:
            return dt.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('No valid date format found')

"""
FUNCTION (main): 
This is the main function, where the analysis of Budget CSV file is done

INPUT: 
argv - list of command-line arguments

OUTPUT:
Budget summary is written to a file if provided as an argument to the script, else prints to the terminal
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
    budget_date_list = []
    revenue = []

    try:
        #Open the CSV file in read-only mode
        with open(argv[1],'r', newline='') as csvfile:
            #reading CSV file
            csvreader = csv.reader(csvfile, delimiter=',')
            #skipping the header row
            next(csvreader)

            #Iterate through all the rows in the CSV file 
            for row in csvreader:
                #Adding the date to the list
                budget_date_list.append(row[0])
                #Adding the revenue to the list               
                revenue.append(int(row[1]))

            # Iterate through all the dates to split the year and month
            # Year and month are added as a tuple in a list                         
            year_month_list = []
            for i in range(len(budget_date_list)):
                date_time = parse_date(budget_date_list[i])
                year, month = date_time.year, date_time.month
                year_month_list.append(tuple((year,month)))
            
            # Dictionary to group the months by year and remove duplicates
            year_month_dict = defaultdict(list)
            for year, month in year_month_list:
                year_month_dict[year].append(month)
            # Total months is count of all the months in the dataset 
            # Map function returns the count of months for each year
            total_months = sum(map(len, year_month_dict.values()))

            # Total revenue is the sum of all the revenues in the dataset
            for i in revenue:
                total_revenue = sum(revenue)

            # List to maintain the revenue change between each month 
            revenue_change = []
            # List to maintain the revenue dates associated with each revenue change
            revenue_date = []
            # Iterate through all the dates
            for i in range(len(budget_date_list) - 1):
                # Change in revenue between consecutive months
                revenue_change.append(revenue[i+1] - revenue[i])
                # Associated revenue date for the above revenue change
                revenue_date.append(budget_date_list[i+1])

            # average revenue change rounded to 2 
            average_revenue_change = round(sum(revenue_change)/len(revenue_change), 2)
            # greatest revenue increase is the max of all revenue changes
            greatest_revenue_increase = max(revenue_change)
            # associated date for the greatest revenue increase
            greatest_revenue_increase_date = revenue_date[revenue_change.index(greatest_revenue_increase)]   

            # greatest revenue decrease is the min of all revenue changes
            greatest_revenue_decrease = min(revenue_change)
            # associated date for the greatest revenue decrease
            greatest_revenue_decrease_date = revenue_date[revenue_change.index(greatest_revenue_decrease)]   

            # if output file is specified, then write the summary to the specified file
            if output_to_file:
                with open(output_filename,'w') as outfile:
                    outfile.write('Financial Analysis\n')
                    outfile.write('-'*30 + '\n')
                    outfile.writelines('Total Months:  {} \n'.format(total_months))
                    outfile.writelines('Total Revenue:  ${} \n'.format(total_revenue))
                    outfile.writelines('Average Revenue Change:  ${} \n'.format(average_revenue_change))
                    outfile.writelines('Greatest Increase in Revenue:  {}  (${}) \n'.format(greatest_revenue_increase_date, greatest_revenue_increase))
                    outfile.writelines('Greatest Decrease in Revenue:  {}  (${}) \n'.format(greatest_revenue_decrease_date, greatest_revenue_decrease))
            # if output file is not specified, then prints summary to the terminal 
            else:
                print('Financial Analysis')
                print('-'*30)
                print('Total Months:  {}'.format( total_months))
                print('Total Revenue:  ${}'.format( total_revenue))
                print('Average Revenue Change:  ${}'.format(average_revenue_change))
                print('Greatest Increase in Revenue:  {}  (${})'.format(greatest_revenue_increase_date, greatest_revenue_increase))
                print('Greatest Decrease in Revenue:  {}  (${})'.format(greatest_revenue_decrease_date, greatest_revenue_decrease))
    # If specified file doesn't open
    except FileNotFoundError:
        print("Wrong file or file path")
    # for all other execptions
    except:
        print("Unexpected error:", sys.exc_info()[0])

# call main function only when this script (main.py) is the main script file
if(__name__ == "__main__"):
    main(sys.argv)