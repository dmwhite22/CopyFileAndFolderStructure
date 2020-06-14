import datetime
import shutil
import stat
import os
import tkinter
from tkinter import filedialog
from tkinter import messagebox
import verify


def open_file_dialog(entry):
    # Function to call when user needs to select a folder
    # Takes in entry
    # Returns null

    file_path = filedialog.askdirectory(master=None, title="Select Directory", mustexist=True)
    entry.insert(0, file_path)
    return


def copy_files(start_date, end_date, copy_from_folder, copy_to_folder, filetype):
    # Function creating a mirror folder structure of original content when desired file type is found, then copies
    # the file into the destination folder
    # Takes in date_range of type datetime.datetime array length two, path of copy_from_folder, and path of
    # copy_to_folder and filetype
    # Returns null

    copy_counter = 0
    current_time = datetime.datetime.today().strftime('%m-%d-%Y-%I%M')

    search_terms = verify.get_search_terms(filetype)

    for subdir, dirs, files in os.walk(copy_from_folder):

        # Verifies the sub-directory creation time is in between the date range provided by the user,
        # if so go check if the files have the .csv files
        subdir_creation_time = datetime.datetime.fromtimestamp(os.stat(subdir)[stat.ST_CTIME])
        if verify.verify_creation_date(start_date, end_date, subdir_creation_time):
            for filename in files:
                filepath = subdir + os.sep + filename
                folderpath = subdir + os.sep
                directorypath = copy_to_folder + '/' + 'Copied-' + current_time + folderpath[len(copy_from_folder):]

                for term in search_terms:
                    if filepath.endswith(term):
                            os.makedirs(directorypath, exist_ok=True)
                            shutil.copy2(filepath, directorypath)
                            copy_counter = copy_counter + 1

    if copy_counter > 0:
        tmp = str(copy_counter)
        tkinter.messagebox.showinfo(title=None, message="Copying Complete\nCopied: " + tmp + " files\n\nNew Files "
                                                                                             "Located "
                                                                                             "in: \n" + copy_to_folder)
        return 'Found Files'
    else:
        tkinter.messagebox.showinfo(title=None, message="No files of file type " + filetype + " or no files within "
                                                                                              "date range found to "
                                                                                              "copy.")
        return 'Found No Files'


def make_time_end_of_day(day, month, year):
    # Function that takes in a particular day and makes the time the end time for that day
    # Takes in day, month and year
    # Returns the end time of the specified day

    end_of_day = datetime.datetime.strptime(
        str(day) + "/" + str(month) + "/" + str(year) + " 23:59:59", "%d/%m/%Y %H:%M:%S")
    return end_of_day


def make_time_start_of_day(day, month, year):
    # Function that takes in a particular day and makes the time the start time for that day
    # Takes in day, month, year
    # Returns the start time of the specified day

    start_of_day = datetime.datetime.strptime(
        str(day) + "/" + str(month) + "/" + str(year) + " 00:00:00", "%d/%m/%Y %H:%M:%S")
    return start_of_day


def get_input_data(sd_entry, sm_entry, sy_entry, ed_entry, em_entry, ey_entry, filepath_from_entry, filepath_to_entry,
                   filetype_entry):
    # Gets all user data entered on the form
    # Takes in start date entry, start month entry, start year entry, end day entry, end month entry, end year entry,
    # copy source path entry, copy destination path entry, and filetype entry
    # Returns error code

    start_month = sm_entry.get()
    start_day = sd_entry.get()
    start_year = sy_entry.get()
    end_month = em_entry.get()
    end_day = ed_entry.get()
    end_year = ey_entry.get()
    filepath_from = filepath_from_entry.get()
    filepath_to = filepath_to_entry.get()
    filetype = filetype_entry.get()

    validate_user_data(start_day, start_month, start_year, end_day, end_month, end_year, filepath_from, filepath_to,
                       filetype)

    return


def validate_user_data(sd, sm, sy, ed, em, ey, filepath_from, filepath_to, filetype):
    # Function that runs based on all the information specified by the user in the GUI. If all the user inputs provided
    # by the user are valid, then call copy files function
    # Takes in start date, start month, start year, end day, end month, end year, copy source path, copy destination
    # path, and filetype
    # Returns error code

    start_month = verify.month_check(sm, "Start Month")
    start_day = verify.date_check(sd, "Start Day", start_month)
    start_year = verify.year_check(sy, "Start Year")

    end_month = verify.month_check(em, "End Month")
    end_day = verify.date_check(ed, "End Day", end_month)
    end_year = verify.year_check(ey, "End Year")

    if isinstance(start_month, int) and isinstance(start_day, int) and isinstance(start_year, int) and \
            isinstance(end_month, int) and isinstance(end_day, int) and isinstance(end_year, int):
        start_date = make_time_start_of_day(start_day, start_month, start_year)
        end_date = make_time_end_of_day(end_day, end_month, end_year)

        # Verifies the dates provided by the user make sense
        end_date, start_end_date_valid = verify.verify_end_date(start_date, end_date)

        copy_from_folder_valid = verify.verify_path(filepath_from)
        copy_to_folder_valid = verify.verify_path(filepath_to)
        continue_on_filetype = verify.verify_filetype(filetype)

        if continue_on_filetype is True:
            if start_end_date_valid is True and copy_from_folder_valid is True and copy_to_folder_valid is True:
                copy_files(start_date, end_date, filepath_from, filepath_to, filetype)
                return 'Files Copied'
            return 'Dates Valid, User Continue, Paths Invalid'
        return 'Dates Valid, User Discontinue'
    return 'Dates Not Valid'
