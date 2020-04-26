import sys
import tkinter
import copyfunc


def run_canvas():
    # Function to run main GUI for program
    # Does not take any inputs
    # Returns null

    root = tkinter.Tk()

    # Creates Overall Canvas
    canvas1 = tkinter.Canvas(root, width=600, height=600)
    canvas1.pack()

    # Setting position data for buttons, labels, entries, and menus
    loc_start_column_label = 25
    loc_start_column_input = loc_start_column_label + 115
    loc_end_column_label = loc_start_column_label + 275
    loc_end_column_input = loc_end_column_label + 115
    loc_date_row_input = 225
    loc_month_row_input = 200
    loc_year_row_input = 250
    loc_copyfrom_row = 400
    loc_path_label_column = 100
    loc_path_entry_column = loc_path_label_column + 265
    loc_copyto_row = 425
    loc_path_button = loc_path_label_column + 435
    loc_run_button = 435
    loc_cancel_button = loc_run_button + 100
    loc_filetype_label = 200
    loc_filetype = loc_filetype_label + 225

    # Setting Font Sizes
    dates_font_size = 8
    header_font_size = 10

    # Creating Welcome statement label
    welcome_statement = "******************************************************************************************\n" \
                        "***********************************     Welcome     ************************************\n" \
                        "******************************************************************************************\n" \
                        "This program searches a directory specified and all subdirectories for the \n" \
                        "files of the specified file type and within the specified date range then \n" \
                        "copies the folder structure with the files to the destination folder.  This \n" \
                        "program will only copy files where the creation time for the file is within \n" \
                        "the date range specified by the user."
    welcome_label = tkinter.Label(root, text=welcome_statement, justify="left")
    welcome_label.config(font=('helvetica', 8))
    canvas1.create_window(300, 70, window=welcome_label)

    # Creating header label for Start Date
    start_header_label = tkinter.Label(root, text="Enter a Start Date")
    start_header_label.config(font=('helvetica', header_font_size))
    canvas1.create_window(loc_start_column_input, 175, window=start_header_label)

    # Creating header label for End Date
    end_header_label = tkinter.Label(root, text="Enter an End Date")
    end_header_label.config(font=('helvetica', header_font_size))
    canvas1.create_window(loc_end_column_input, 175, window=end_header_label)

    # Creating entry and label for user to input start month
    start_month_entry = tkinter.Entry(root)
    canvas1.create_window(loc_start_column_input, loc_month_row_input, window=start_month_entry)
    start_month_label = tkinter.Label(root, text="Start Month:", anchor='e', width=15)
    start_month_label.config(font=('helvetica', dates_font_size))
    canvas1.create_window(loc_start_column_label, loc_month_row_input, window=start_month_label)

    # Creating entry and label for user to input start date
    start_date_entry = tkinter.Entry(root)
    canvas1.create_window(loc_start_column_input, loc_date_row_input, window=start_date_entry)
    start_day_label = tkinter.Label(root, text="Start Day:", anchor='e', width=15)
    start_day_label.config(font=('helvetica', dates_font_size))
    canvas1.create_window(loc_start_column_label, loc_date_row_input, window=start_day_label)

    # Creating entry and label for user to input start year
    start_year_entry = tkinter.Entry(root)
    canvas1.create_window(loc_start_column_input, loc_year_row_input, window=start_year_entry)
    start_year_label = tkinter.Label(root, text="Start Year:", anchor='e', width=15)
    start_year_label.config(font=('helvetica', dates_font_size))
    canvas1.create_window(loc_start_column_label, loc_year_row_input, window=start_year_label)

    # Creating entry and label for user to input end month
    end_month_entry = tkinter.Entry(root)
    canvas1.create_window(loc_end_column_input, loc_month_row_input, window=end_month_entry)
    end_month_label = tkinter.Label(root, text="End Month:", anchor='e', width=15)
    end_month_label.config(font=('helvetica', dates_font_size))
    canvas1.create_window(loc_end_column_label, loc_month_row_input, window=end_month_label)

    # Creating entry and label for user to input end date
    end_date_entry = tkinter.Entry(root)
    canvas1.create_window(loc_end_column_input, loc_date_row_input, window=end_date_entry)
    end_day_label = tkinter.Label(root, text="End Day:", anchor='e', width=15)
    end_day_label.config(font=('helvetica', dates_font_size))
    canvas1.create_window(loc_end_column_label, loc_date_row_input, window=end_day_label)

    # Creating entry and label for user to input end year
    end_year_entry = tkinter.Entry(root)
    canvas1.create_window(loc_end_column_input, loc_year_row_input, window=end_year_entry)
    end_year_label = tkinter.Label(root, text="End Year:", anchor='e', width=15)
    end_year_label.config(font=('helvetica', dates_font_size))
    canvas1.create_window(loc_end_column_label, loc_year_row_input, window=end_year_label)

    # Creating path source entry, label and browse button
    file_path_copyfrom_entry = tkinter.Entry(root, width=50)
    file_path_copyfrom_label = tkinter.Label(root, text="Browse or Provide Source Path:", anchor='e', width=35)
    file_path_copyfrom_label.config(font=('helvetica', dates_font_size))
    canvas1.create_window(loc_path_label_column, loc_copyfrom_row, window=file_path_copyfrom_label)
    canvas1.create_window(loc_path_entry_column, loc_copyfrom_row, window=file_path_copyfrom_entry)
    browse_source_button = tkinter.Button(root, text="...", width=3, height=1,
                                          command=lambda: copyfunc.open_file_dialog(file_path_copyfrom_entry))
    canvas1.create_window(loc_path_button, loc_copyfrom_row - 1, window=browse_source_button)

    # Creating path destination entry, label and browse button
    file_path_copyto_entry = tkinter.Entry(root, width=50)
    file_path_copyto_label = tkinter.Label(root, text="Browse or Provide Destination Path:", anchor='e', width=35)
    file_path_copyto_label.config(font=('helvetica', dates_font_size))
    canvas1.create_window(loc_path_label_column, loc_copyto_row, window=file_path_copyto_label)
    canvas1.create_window(loc_path_entry_column, loc_copyto_row, window=file_path_copyto_entry)
    browse_dest_button = tkinter.Button(root, text="...", width=3, height=1,
                                        command=lambda: copyfunc.open_file_dialog(file_path_copyto_entry))
    canvas1.create_window(loc_path_button, loc_copyto_row + 1, window=browse_dest_button)

    # Creating filetype entry and label for entry
    filetype_entry = tkinter.Entry(root, width=20)
    filetype_label = tkinter.Label(root, text="Enter the file type you would like to copy (e.g. Enter \".csv\"):",
                                   anchor='e', width=50)
    filetype_label.config(font=('helvetica', dates_font_size))
    canvas1.create_window(loc_filetype_label, 500, window=filetype_label)
    canvas1.create_window(loc_filetype, 500, window=filetype_entry)

    # Creating Run Button
    run_button = tkinter.Button(root, text="Run", width=10,
                                command=lambda: copyfunc.get_input_data(start_date_entry, start_month_entry,
                                                                        start_year_entry, end_date_entry,
                                                                        end_month_entry,
                                                                        end_year_entry, file_path_copyfrom_entry,
                                                                        file_path_copyto_entry, filetype_entry))
    canvas1.create_window(loc_run_button, 570, window=run_button)

    # Creating Cancel Button
    cancel_button = tkinter.Button(root, text="Cancel", width=10, command=sys.exit)
    canvas1.create_window(loc_cancel_button, 570, window=cancel_button)
    root.mainloop()
    return


run_canvas()
