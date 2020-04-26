import datetime
import os
import tkinter
from tkinter import messagebox


def verify_end_date(start_date, end_date):
    # Function to see if end date is after start date and makes sure date is not after today + 1.
    # Takes in array of length two of type datetime.datetime, with start date and end date listed in seconds
    # Returns date_range, and returns whether the value was acceptable

    if end_date < start_date:
        tkinter.messagebox.showerror(title="Invalid Date", message="End date was before start date. Try running again.")
        return end_date, False
    elif end_date > datetime.datetime.now() + datetime.timedelta(days=1):
        end_date = datetime.datetime.now() + datetime.timedelta(days=1)
        tkinter.messagebox.showwarning(title="Warning", message="End date is after today, changing end date to today.")
        return end_date, True
    else:
        return end_date, True


def verify_creation_date(start_date, end_date, creation_time):
    # Function to verify whether the creation time is in the range of dates date_range
    # Takes in array of date_range length of 2 of type datetime.datetime, and takes in time of subdirectory creation of
    # type datetime.datetime
    # Returns boolean if creation time falls within date_range
    fall_in_range = False
    if start_date <= creation_time <= end_date:
        fall_in_range = True
    return fall_in_range


def verify_path(selected_path):
    # Function to verify the selected path is acceptable and if not show user message
    # Inputs selected path
    # Returns boolean

    exists = os.path.exists(selected_path)
    if exists:
        return exists
    else:
        tkinter.messagebox.showerror(title="Path Error", message=selected_path + "\nis not a valid path. Please "
                                                                                 "reselect and try again.")
        return exists


def verify_filetype(filetype):
    # Function to determine whether anything is entered into the field and post a warning if not
    # Inputs string filetype
    # Returns boolean if the user would like to continue

    if filetype == '':
        user_response = tkinter.messagebox.askyesno(title="Continue", message="The file type box is empty, this will "
                                                                              "copy all files and folder directories. "
                                                                              "Would you like to continue?")
        return user_response
    else:
        return True


def integer_check(user_input, time_string):
    # Verifies the number provided is an integer
    # Takes in user_input provided in the passed box, and the time string associated with that box
    # Returns the user_input

    try:
        user_input = int(user_input)
    except ValueError:
        user_input = tkinter.messagebox.showerror("Try Again",
                                                  "The value for " + time_string + " must be an integer.")
    return user_input


def month_check(month, time_string):
    # Verifies the month is between legitimate values for months and asks 3 times, if user fails then exit program
    # Takes in string (month) and time string associated with that month
    # Returns month if month value is valid, otherwise posts error to user and returns none

    if isinstance(month, int) is False:
        # if month is not None:
        month = integer_check(month, time_string)
        if month is not None and isinstance(month, int) is True:
            if month <= 0 or month > 12:
                tkinter.messagebox.showerror("Try Again", "The value for " + time_string +
                                             "can only be an integer between 1 and 12")
            elif month > 0 or month < 13:
                return month
        # else:
        #     tkinter.messagebox.showerror(title=None,
        #                                  message="Missing a specified month. Please enter month in " + time_string)
    return month


def date_check(date, time_string, month):
    # Verifies the date is between legitimate values for dates and asks 3 times, if user fails then exit program
    # Takes in date, time string associated with that date, and month
    # Returns date if day is valid, otherwise posts errors and returns null

    date = integer_check(date, time_string)

    if date is not None and isinstance(date, int) is True:
        if date <= 0 or date > 31:
            tkinter.messagebox.showerror(title="Try Again",
                                         message="The value for the date can only be an integer "
                                                 "between 1 and 31")
        elif date > 0 or date < 31:
            # Checks to make sure if the user specifies day 31 in a month with 30 days the last day of the
            # month will be specified
            if isinstance(month, int) is True:
                try:
                    datetime.datetime.strptime(str(date) + "/" + str(month), "%d/%m")
                except ValueError:
                    tkinter.messagebox.showerror(title="Error",
                                                 message="Month does not have numbers of days specified, "
                                                         "changing date to last day of the specified month")
                    if month == 4 or month == 6 or month == 9 or month == 11:
                        date = 30
                    elif month == 2:
                        date = 28
                return date


def year_check(year, time_string):
    # Verifies the year is between legitimate values for dates
    # Takes in year and time string associated with the year
    # Returns year if valid, otherwise posts error and returns year

    year = integer_check(year, time_string)
    if year is not None and isinstance(year, int):
        if year <= 1920 or year > datetime.datetime.now().year:
            tkinter.messagebox.showerror(title="Try Again", message="The value for the year must by entered as 4 "
                                                                    "digits and no later than the current year (i.e. "
                                                                    "year 2010 is entered as '2010'")
        return year
