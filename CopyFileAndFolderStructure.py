import sys
import datetime
import shutil
import stat
import os
import tkinter
import subprocess
from tkinter import filedialog
from tkinter import messagebox


def select_date_range():
    # Runs through a series of prompts that asks the user the range of dates for which they want to pull data
    # Does not take in any input into function.
    # Returns array of length two of type datetime.datetime

    # date_range array is an array that will store the start and end dates in the format of [M,D,Y,M,D,Y]
    # date_range[0-2] is the start date
    # date_range[3-5] is the end date
    date_range = [0, 0, 0, 0, 0, 0]
    date_range[0] = month_check(integer_check(input("Enter the month to start copying data (Enter 1-12):")))
    date_range[1] = date_check(integer_check(input("Enter the date to start copying data (Enter 1-31):")),
                               date_range[0])
    date_range[2] = year_check(integer_check(input("Enter the year to start copying data (Enter YYYY):")))

    date_range[3] = month_check(integer_check(input("Enter the month to end copying data (Enter 1-12:):")))
    date_range[4] = date_check(integer_check(input("Enter the date to end copying data (Enter 1-31):")), date_range[3])
    date_range[5] = year_check(integer_check(input("Enter the year to end copying data (Enter YYYY):")))

    start_date = datetime.datetime.strptime(
        str(date_range[1]) + "/" + str(date_range[0]) + "/" + str(date_range[2]) + " 23:59:59", "%d/%m/%Y %H:%M:%S")

    end_date = datetime.datetime.strptime(
        str(date_range[4]) + "/" + str(date_range[3]) + "/" + str(date_range[5]) + " 23:59:59", "%d/%m/%Y %H:%M:%S")

    start_end_date = [start_date, end_date]

    return start_end_date


def integer_check(user_input):
    # Verifies the number provided is an integer
    # Takes in user_input
    # Returns the user_input if it is an integer

    i = 0
    while isinstance(user_input, int) is False or i < 3:
        try:
            user_input = int(user_input)
            return user_input
        except ValueError:
            user_input = input("The value must be an integer, please input an integer (whole numbers):")
            i = i + 1

    input("Failed to enter an integer. Please try again. Press any key to continue...")
    sys.exit()


def month_check(month):
    # Verifies the month is between legitimate values for months and asks 3 times, if user fails then exit program
    # Takes in integer (month) and returns month if month value is valid, exits otherwise
    for i in range(2):
        if month is None:
            input("Program Cancelled By User. Press any key to continue...")
            sys.exit()
        else:
            while month <= 0 or month > 12:
                month = integer_check(input("The value for the month can only be an integer between 1 and 12, "
                                            "please enter a value between 1 and 12:"))
                if month > 0 or month < 13:
                    break

    if month <= 0 or month > 12:
        input("Failed to Select a Valid Month. Press any key to continue...")
        sys.exit()
    return month


def date_check(date, month):
    # Verifies the date is between legitimate values for dates and asks 3 times, if user fails then exit program
    # Takes in day, and returns date if day is valid or exits program if not

    for i in range(2):
        if date is None:
            input("Program Cancelled by User. Press any key to continue...")
            sys.exit()
        else:
            while date <= 0 or date > 31:
                date = integer_check(input("The value for the date can only be an integer between 1 and 31, "
                                           "please enter a value between 1 and 31:"))
                if date > 0 or date < 31:
                    break

    if date <= 0 or date > 31:
        input("Failed to select valid date. Press any key to continue...")
        sys.exit()

    # Checks to make sure if the user specifies day 31 in a month with 30 days the last day of the
    # month will be specified
    try:
        datetime.datetime.strptime(str(date) + "/" + str(month), "%d/%m")
    except:
        print("Month does not have numbers of days specified, "
              "changing date to last day of the specified month")
        if month == 4 or month == 6 or month == 9 or month == 11:
            date = 30
        elif month == 2:
            date = 28
    return date


def year_check(year):
    # Verifies the date is between legitimate values for dates and asks 3 times, if user fails then exit program
    # Takes in year and returns year if year is valid, exits program if year is not valid
    for i in range(2):
        if year is None:
            input("Program cancelled by user. Press any key to continue...")
            sys.exit()
        else:
            while year <= 1920 or year > datetime.datetime.now().year:
                year = integer_check(
                    input("The value for the year must by entered as 4 digits and no later than the current year"
                          "(i.e. year 2010 is entered as '2010':"))
                if year > 1920 or year < datetime.datetime.now().year:
                    break

    if year <= 1920 or year > datetime.datetime.now().year:
        input("Failed to select valid year. Press any key to continue")
        sys.exit()
    return year


def verify_response(user_response):
    # Verifies the response whether 'Cancel' or 'No' was selected from a user in order to continue program
    # Takes in type int or None
    # Returns to program if not type none
    if user_response:
        return
    else:
        input("Program cancelled by user. Press any key to continue...")
        sys.exit()


def verify_end_date(date_range):
    # Function to see if end date is after start date. If the end date is before the start date switch end and start
    # date
    # Takes in array of length two of type datetime.datetime, with start date and end date listed in seconds
    # Returns null or exits program

    if date_range[1] < date_range[0]:
        input("End date was before start date. Try running again. Press any key to continue...")
        sys.exit()
    elif date_range[1] > datetime.datetime.now() + datetime.timedelta(days=1):
        date_range[1] = datetime.datetime.now() + datetime.timedelta(days=1)
        print("End date is after today, changing end date to today.")
        return date_range
    else:
        return date_range


def verify_creation_date(date_range, creation_time):
    # Function to verify whether the creation time is in the range of dates date_range
    # Takes in array of date_range length of 2 of type datetime.datetime, and takes in time of subdirectory creation of
    # type datetime.datetime
    # Returns boolean if creation time falls within date_range
    fall_in_range = False
    if date_range[0] <= creation_time <= date_range[1]:
        fall_in_range = True
    return fall_in_range


def copy_files(date_range, copy_from_folder, copy_to_folder):
    # Function creating a mirror folder structure of original content when desired file type is found, then copies the
    # file into the destination folder
    # Takes in date_range of type timetuple array length two, path of copy_from_folder, and path of copy_to_folder
    # Returns null

    copy_counter = 0
    current_time = datetime.datetime.today().strftime('%m-%d-%Y-%I%M')
    for subdir, dirs, files in os.walk(copy_from_folder):
        subdir_creation_time = datetime.datetime.fromtimestamp(os.stat(subdir)[stat.ST_CTIME])

        # Verifies the sub-directory creation time is in between the date range provided by the user,
        # if so go check if the files have the .csv files
        if verify_creation_date(date_range, subdir_creation_time):
            for filename in files:
                filepath = subdir + os.sep + filename
                folderpath = subdir + os.sep
                directorypath = copy_to_folder + '/' + 'Copied-' + current_time + folderpath[len(copy_from_folder):]
                if filepath.endswith(".csv"):
                    os.makedirs(directorypath, exist_ok=True)
                    shutil.copy2(filepath, directorypath)
                    copy_counter = copy_counter + 1
    print("\nCopying Complete\nCopied:", copy_counter, "files")
    return


def display_start_message():
    # Does not take in any arguments
    # Returns boolean for whether user selects to continue or not

    if sys.platform == "darwin":
        selected_response = subprocess.run("osascript -e 'Tell application \"System Events\" to display dialog \""
                                           "Select the directory from where to pull files?\" with title \"Continue?\"")
    elif sys.platform == "win32" or sys.platform == "linux" or sys.platform == "linux2":
        selected_response = messagebox.askyesnocancel("Continue?", "Select the directory from where to pull files?")
    else:
        selected_response = False

    return selected_response


root = tkinter.Tk()
root.withdraw()
welcome_statement = "********************************************************************\n" \
                    "*************************     Welcome     **************************\n" \
                    "********************************************************************\n" \
                    "This program searches subdirectories for files of a certain type    \n" \
                    "specified by the user from the source path specified by the user    \n" \
                    "then copies the folder structure with the files to the destination  \n" \
                    "folder.  This program will only copy files where the creation time  \n" \
                    "for the file is within the date range specified by the user."

print(welcome_statement)
input("\nPress and key to continue...")

# Prompt user for confirmation before starting to run application.
select_folder_response = display_start_message()

# Verifies whether the user would like to continue based on yes, no or cancel selection
verify_response(select_folder_response)

# Prompts user where the user would like to copy from
file_path_copyfrom = filedialog.askdirectory(master=None, title="Select Where You Would Like to Copy From",
                                             mustexist=True)
# Verifies whether the user would like to continue based on yes, no or cancel selection
verify_response(file_path_copyfrom)

# Prompts user where the user would like to copy to
file_path_copyto = filedialog.askdirectory(master=None, title="Select Where You Would Like to Copy To")

# Verifies whether the user would like to continue based on yes, no or cancel selection
verify_response(file_path_copyto)
print("******************************************************************************************\n" \
    "Copy From: " + file_path_copyfrom + "\n" \
    "    _||_  \n" \
    "    \  / \n" \
    "     \/  \n" \
    "Copy To: " + file_path_copyto + "\n" \
    "******************************************************************************************")

# Asks user for the date range they would like to copy files for
user_input_range = select_date_range()

# Verifies the dates provided by the user make sense
user_input_range = verify_end_date(user_input_range)

# Copy the files and create the folder structure
copy_files(user_input_range, file_path_copyfrom, file_path_copyto)

# Wait until the user exits the program
end_program = input("\nPress any key to Exit...")
