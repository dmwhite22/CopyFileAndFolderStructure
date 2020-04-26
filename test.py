import unittest
from unittest.mock import patch
import verify
import datetime
import os
import copyfunc
import shutil


class MyTestCase(unittest.TestCase):
    @patch('tkinter.messagebox.showerror', return_value=None)
    def test_integer_check_string(self, user_input):
        result = verify.integer_check('a', 'Start Date')
        self.assertEqual(result, None)

    def test_integer_check_decimal(self):
        result = verify.integer_check(10.3, 'Start Date')
        self.assertEqual(type(result), int)

    def test_integer_check_negative(self):
        result = verify.integer_check(-1, 'Start Date')
        self.assertEqual(type(result), int)

    def test_integer_check_huge_number(self):
        result = verify.integer_check(1239583409573498572340.23498723489723897234, 'Start Date')
        self.assertEqual(type(result), int)

    @patch('tkinter.messagebox.showerror', return_value=None)
    def test_integer_check_none(self, user_input):
        result = verify.integer_check('', 'Start Date')
        self.assertEqual(result, None)

    def test_month_check_good_month(self):
        result = verify.month_check('1', 'Start Date')
        self.assertEqual(result, 1)

    @patch('tkinter.messagebox.showerror', return_value=None)
    def test_month_check_negative(self, filler):
        result = verify.month_check('-1', 'Start Date')
        self.assertEqual(result, -1)

    @patch('tkinter.messagebox.showerror', return_value=None)
    def test_month_check_over(self, filler):
        result = verify.month_check('13', 'Start Date')
        self.assertEqual(result, 13)

    def test_date_check_good_days(self):
        result = verify.date_check('20', 'Start Date', 1)
        self.assertEqual(result, 20)

    @patch('tkinter.messagebox.showerror', return_value=None)
    def test_date_check_negative(self, filler):
        result = verify.date_check('-1', 'Start Date', 1)
        self.assertEqual(result, None)

    @patch('tkinter.messagebox.showerror', return_value=None)
    def test_date_check_over(self, filler):
        result = verify.date_check('32', 'Start Date', 1)
        self.assertEqual(result, None)

    @patch('tkinter.messagebox.showerror', return_value=None)
    def test_date_check_february(self, filler):
        result = verify.date_check('31', 'Start Date', 2)
        self.assertEqual(result, 28)

    @patch('tkinter.messagebox.showerror', return_value=None)
    def test_year_check_under(self, filler):
        result = verify.year_check('1900', 'Start Date')
        self.assertEqual(result, 1900)

    def test_year_check_middle(self):
        result = verify.year_check('2018', 'Start Date')
        self.assertEqual(result, 2018)

    @patch('tkinter.messagebox.showerror', return_value=None)
    def test_year_check_over(self, filler):
        result = verify.year_check('2050', 'Start Date')
        self.assertEqual(result, 2050)

    def test_verify_end_date_start_before_end(self):
        date1 = datetime.datetime.now() - datetime.timedelta(days=1)
        date2 = datetime.datetime.now()
        result, valid = verify.verify_end_date(date1, date2)
        self.assertEqual(result, date2)
        self.assertEqual(valid, True)

    @patch('tkinter.messagebox.showerror', return_value=None)
    def test_verify_end_date_before_start(self, filler):
        date1 = datetime.datetime.now() + datetime.timedelta(days=1)
        date2 = datetime.datetime.now()
        result, valid = verify.verify_end_date(date1, date2)
        self.assertEqual(result, date2)
        self.assertEqual(valid, False)

    @patch('tkinter.messagebox.showwarning', return_value=None)
    def test_verify_end_date_after_today(self, filler):
        date1 = datetime.datetime.now()
        date2 = datetime.datetime.now() + datetime.timedelta(days=5)
        result, valid = verify.verify_end_date(date1, date2)
        self.assertEqual(result, date1 + datetime.timedelta(days=1))
        self.assertEqual(valid, True)

    def test_verify_creation_date_before_range(self):
        date1 = datetime.datetime.now() + datetime.timedelta(days=3)
        date2 = datetime.datetime.now() + datetime.timedelta(days=5)
        creation_time = datetime.datetime.now()
        result = verify.verify_creation_date(date1, date2, creation_time)
        self.assertEqual(result, False)

    def test_verify_creation_date_during_range(self):
        date1 = datetime.datetime.now()
        date2 = datetime.datetime.now() + datetime.timedelta(days=5)
        creation_time = datetime.datetime.now() + datetime.timedelta(days=3)
        result = verify.verify_creation_date(date1, date2, creation_time)
        self.assertEqual(result, True)

    def test_verify_creation_date_after_range(self):
        date1 = datetime.datetime.now()
        date2 = datetime.datetime.now() + datetime.timedelta(days=3)
        creation_time = datetime.datetime.now() + datetime.timedelta(days=5)
        result = verify.verify_creation_date(date1, date2, creation_time)
        self.assertEqual(result, False)

    @patch('tkinter.messagebox.showerror', return_value=None)
    def test_verify_path_none(self, filler):
        result1 = verify.verify_path('')
        self.assertEqual(result1, False)

    def test_verify_path_valid_path(self):
        result1 = verify.verify_path(os.getcwd())
        self.assertEqual(result1, True)

    @patch('tkinter.messagebox.showerror', return_value=None)
    def test_verify_path_invalid_path(self, filler):
        path_string = os.path.abspath(os.getcwd()) + 'sldfjsakl12'
        result1 = verify.verify_path(path_string)
        self.assertEqual(result1, False)

    @patch('tkinter.messagebox.askyesno', return_value=True)
    def test_verify_filetype_none_yes(self, user_response):
        result = verify.verify_filetype('')
        self.assertEqual(result, True)

    @patch('tkinter.messagebox.askyesno', return_value=False)
    def test_verify_filetype_none_no(self, user_response):
        result = verify.verify_filetype('')
        self.assertEqual(result, False)

    def test_verify_filetype_any(self):
        result = verify.verify_filetype('.csv')
        self.assertEqual(result, True)

    # Currently don't have a good way to test
    # def test_open_dialog(self):

    @patch('verify.verify_creation_date', return_value=True)
    @patch('tkinter.messagebox.showinfo', return_value=None)
    def test_copy_files_valid_input(self, valid_creation, msgbx_filler):
        start_time = datetime.datetime.now()
        path = os.path.join(os.getcwd(), "TestScenario")
        copy_from = path
        if os.path.exists(path):
            pass
        else:
            os.mkdir(path)
        os.chdir(path)
        path = os.path.join(os.getcwd(), "Test")
        copy_to = path
        if os.path.exists(path):
            pass
        else:
            os.mkdir(path)
        os.chdir(path)
        f = open("Blank.txt", "w+")
        f.write("This is a test of the emergency broadcasting system")
        f.close()
        os.chdir("..")
        os.chdir("..")
        end_time = datetime.datetime.now()
        result = copyfunc.copy_files(start_time, end_time, copy_from, copy_to, '.txt')
        self.assertEqual(result, 'Found Files')
        path = os.path.join(os.getcwd(), "TestScenario")
        if os.path.exists(path):
            shutil.rmtree(path)

    @patch('verify.verify_creation_date', return_value=True)
    @patch('tkinter.messagebox.showinfo', return_value=None)
    def test_copy_files_different_filetype(self, valid_creation, msgbx_filler):
        start_time = datetime.datetime.now()
        path = os.path.join(os.getcwd(), "TestScenario")
        copy_from = path
        if os.path.exists(path):
            pass
        else:
            os.mkdir(path)
        os.chdir(path)
        path = os.path.join(os.getcwd(), "Test")
        copy_to = path
        if os.path.exists(path):
            pass
        else:
            os.mkdir(path)
        os.chdir(path)
        f = open("Blank.txt", "w+")
        f.write("This is a test of the emergency broadcasting system")
        f.close()
        os.chdir("..")
        os.chdir("..")
        end_time = datetime.datetime.now()
        result = copyfunc.copy_files(start_time, end_time, copy_from, copy_to, '.csv')
        self.assertEqual(result, 'Found No Files')
        path = os.path.join(os.getcwd(), "TestScenario")
        if os.path.exists(path):
            shutil.rmtree(path)

    def test_make_time_end_of_day(self):
        result = copyfunc.make_time_end_of_day(1, 3, 2020)
        outside_function = datetime.datetime.strptime(
            str(1) + "/" + str(3) + "/" + str(2020) + " 23:59:59", "%d/%m/%Y %H:%M:%S")
        self.assertEqual(result, outside_function)

    @patch('verify.date_check', return_value='a')
    def test_validate_user_data_int_for_date(self, start_date):
        result = copyfunc.validate_user_data('a', 4, 2020, 4, 4, 2020, os.getcwd(), os.getcwd(), '.txt')
        self.assertEqual(result, 'Dates Not Valid')

    @patch('verify.verify_filetype', return_value=False)
    def test_validate_user_data_user_discontinue(self, filler):
        # end_date = copyfunc.make_time_end_of_day(4, 4, 2020)
        # verify.verify_end_date.side_effect = Mock(return_value=[end_date, False])
        result = copyfunc.validate_user_data(1, 4, 2020, 4, 4, 2020, os.getcwd(), os.getcwd(), '')
        self.assertEqual(result, 'Dates Valid, User Discontinue')

    @patch('verify.verify_filetype', return_value=True)
    @patch('tkinter.messagebox.showinfo', return_value=None)
    def test_validate_user_data_user_continue(self, filler1, filler2):
        # end_date = copyfunc.make_time_end_of_day(4, 4, 2020)
        # verify.verify_end_date.side_effect = Mock(return_value=[end_date, False])
        result = copyfunc.validate_user_data(1, 4, 2020, 4, 4, 2020, os.getcwd(), os.getcwd(), '')
        self.assertEqual(result, 'Files Copied')

    @patch('tkinter.messagebox.showerror', return_value=None)
    def test_validate_user_data_bad_path(self, filler):
        result = copyfunc.validate_user_data(4, 4, 2020, 4, 4, 2020, os.getcwd() + 'foofoofoo', os.getcwd(), '.txt')
        self.assertEqual(result, 'Dates Valid, User Continue, Paths Invalid')

    @patch('tkinter.messagebox.showinfo', return_value=None)
    def test_validate_user_data_file_copy(self, filler):
        result = copyfunc.validate_user_data(4, 4, 2020, 4, 4, 2020, os.getcwd(), os.getcwd(), '.blahblahblah')
        self.assertEqual(result, 'Files Copied')


if __name__ == '__main__':
    unittest.main()
