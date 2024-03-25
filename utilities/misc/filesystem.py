import pickle
from datetime import datetime
import os
import math
import numpy as np

class FileSystem:
    """
    Represents a file system.

    Attributes:
        sheets (list): A list of Sheets objects.
        local_file_directory (str): The directory where the local file is stored.
        open_index (int): Index of the currently open sheet.
    """
    def __init__(self, **kwargs):
        self.sheets = []
        self.local_file_directory = "assets/localdb.pkl"
        self.open_index = 0
        self.filemanager_last_dir = None
        
        
    def add_sheet(self):
        """
        Adds a new sheet to the file system.
        """
        # Get the current date and time
        current_date_time = datetime.now()

        # Format the current date and time without seconds
        formatted_date_time = current_date_time.strftime("%Y-%m-%d %H:%M")
        date = formatted_date_time
        sheet = Sheets(date_created=date,
                       fs_obj=self)
        self.sheets.append(sheet)

    def get_sheet(self, index):
        """
        Retrieves a sheet from the file system.

        Args:
            index (int): The index of the sheet to retrieve.

        Returns:
            Sheets: The specified sheet object.
        """
        self.open_index = index
        return self.sheets[index]
    
    def save(self):
        """
        Saves the file system object to a pickle file.
        """
        with open(self.local_file_directory, "wb") as file:
            # Serialize and write the object to the file using pickle.dump()
            pickle.dump(self, file, protocol=5)

    def load(self):
        """
        Loads the file system object from a pickle file.

        Returns:
            FileSystem: The loaded file system object.
        """
        with open(self.local_file_directory, 'rb') as file:
            return pickle.load(file)


class Item:
    """
    Represents an item.

    Attributes:
        points (int): The points associated with the item.
        answer_key (str): The answer key for the item.
        fs_obj (FileSystem): The file system object associated with the item.
    """
    def __init__(self, fs_obj, answer_key=[],**kwargs):
        self.points = 1
        self.answer_key = answer_key
        self.fs_obj = fs_obj

    def evaluate(self, answer):
        """
        Evaluates the item based on the provided answer.

        Args:
            answer (str): The answer to evaluate against.

        Returns:
            bool: True if the answer is correct, False otherwise.
        """
        if self.answer_key == answer:
            return True
        else:
            return False


class MultipleChoice:
    """
    Represents a multiple choice question.

    Attributes:
        items (list): A list of Item objects.
        show_items (int): The number of items to display.
        fs_obj (FileSystem): The file system object associated with the multiple choice question.
    """
    def __init__(self,fs_obj, **kwargs):
        self.items = []
        self.show_items = 0
        self.fs_obj = fs_obj
        

    def set_items(self, number):
        """
        Sets the number of items to display.

        Args:
            number (int): The number of items to display.
        """
        current_length = len(self.items)
        if number > current_length:
            diff = number - current_length
            for x in range(diff):
                self.items.append(Item(self.fs_obj))
                self.show_items += 1
        else:
            self.show_items = number
    
    def get_items(self):
        """
        Retrieves the items to display.

        Returns:
            list: A list of Item objects to display.
        """
        lis_result = []
        for i in range(self.show_items):
            lis_result.append(self.items[i])
        return lis_result


class TrueOrFalse:
    """
    Represents a true or false question.
    """
    def __init__(self,fs_obj, **kwargs):
        self.items = []
        self.fs_obj = fs_obj
        self.show_items = 0

    def set_items(self, number):
        """
        Sets the number of items to display.

        Args:
            number (int): The number of items to display.
        """
        current_length = len(self.items)
        if number > current_length:
            diff = number - current_length
            for x in range(diff):
                self.items.append(Item(self.fs_obj))
                self.show_items += 1
        else:
            self.show_items = number
    
    def get_items(self):
        """
        Retrieves the items to display.

        Returns:
            list: A list of Item objects to display.
        """
        lis_result = []
        for i in range(self.show_items):
            lis_result.append(self.items[i])
        return lis_result


class Identification:
    """
    Represents an identification question.
    """
    def __init__(self, fs_obj,**kwargs):
        self.items = []
        self.fs_obj = fs_obj
        self.show_items = 0
    def set_items(self, number):
        """
        Sets the number of items to display.

        Args:
            number (int): The number of items to display.
        """
        current_length = len(self.items)
        if number > current_length:
            diff = number - current_length
            for x in range(diff):
                self.items.append(Item(self.fs_obj))
                self.show_items += 1
        else:
            self.show_items = number
    
    def get_items(self):
        """
        Retrieves the items to display.

        Returns:
            list: A list of Item objects to display.
        """
        lis_result = []
        for i in range(self.show_items):
            lis_result.append(self.items[i])
        return lis_result


class AnswerKeys:
    """
    Represents answer keys for different question types.

    Attributes:
        mc (MultipleChoice): The answer key for multiple choice questions.
        tf (TrueOrFalse): The answer key for true or false questions.
        idtf (Identification): The answer key for identification questions.
        fs_obj (FileSystem): The file system object associated with the answer keys.
    """
    def __init__(self, fs_obj, **kwargs):
        self.mc = MultipleChoice(fs_obj)
        self.tf = TrueOrFalse(fs_obj)
        self.idtf = Identification(fs_obj)
        self.fs_obj = fs_obj


class CheckSession:
    """
    Represents a check session.

    Attributes:
        date_created (str): The date and time when the session was created.
        fs_obj (FileSystem): The file system object associated with the session.
        answer_key (AnswerKeys): The answer key for the session.
        mc (MultipleChoice): The multiple choice questions for the session.
        tf (TrueOrFalse): The true or false questions for the session.
        idtf (Identification): The identification questions for the session.
        open_index (int): Index of the currently open session.
    """
    def __init__(self,date_created, fs_obj, name, check_obj,**kwargs):
        self.date_created = date_created
        self.name = name
        self.fs_obj = fs_obj
        self.mc_answer = []
        self.tf_answer = []
        self.idtf_answer = []
        self._mc_score = None
        self._tf_score = None
        self._idtf_score = None
        self.mc_eval_array = []
        self.tf_eval_array = []
        self.idtf_eval_array = []
        self.check_obj = check_obj

    def count_tf_answer(self):
        array = np.array(self.tf_answer)
        return sum(array=='T'), np.sum(array=='F')
    
    def count_mc_answer(self):
        array = np.array(self.mc_answer)
        temp_result = []
        for char in ['A','B','C','D']:
            temp_result.append(np.sum(array==char))
        return tuple(temp_result)
    
    def count_mc_stat(self):
        class mc:
            class stat:
                def __init__(self):
                    self.true = 0
                    self.false = 0
            def __init__(self):
                self.a = mc.stat()
                self.b = mc.stat()
                self.c = mc.stat()
                self.d = mc.stat()

        mc_stat = mc()
        for answer, eval in zip(self.mc_answer, self.mc_eval_array):
            if answer == 'A':
                if eval == 1:
                    mc_stat.a.true += 1
                else:
                    mc_stat.a.false += 1
            if answer == 'B':
                if eval == 1:
                    mc_stat.b.true += 1
                else:
                    mc_stat.b.false += 1
            if answer == 'C':
                if eval == 1:
                    mc_stat.c.true += 1
                else:
                    mc_stat.c.false += 1
            if answer == 'D':
                if eval == 1:
                    mc_stat.d.true += 1
                else:
                    mc_stat.d.false += 1

    def count_tf_stat(self):
        class tf:
            class stat:
                def __init__(self):
                    self.true = 0
                    self.false = 0
            def __init__(self):
                self.t = tf.stat()
                self.f = tf.stat()

        tf_stat = tf()
        for answer, eval in zip(self.tf_answer, self.tf_eval_array):
            if answer == 'T':
                if eval == 1:
                    tf_stat.t.true += 1
                else:
                    tf_stat.t.false += 1
            if answer == 'F':
                if eval == 1:
                    tf_stat.f.true += 1
                else:
                    tf_stat.f.false += 1
                    
    def get_mc_score(self):
        self._mc_score = sum([x if x is not None else 0 for x in self.mc_eval_array])
        print(self.mc_eval_array)
        return self._mc_score
    
    def get_tf_score(self):
        self._tf_score = sum([x if x is not None else 0 for x in self.tf_eval_array])
        print(self._tf_score)
        print(self.tf_eval_array)
        return self._tf_score
        
    def _reset_order(self, reordered_lst, interval):
        repeat_times = math.floor(len(reordered_lst)/interval)
        result = []
        for index in range(len(reordered_lst)):
            temp_index = index
            for repeat in range(0,repeat_times+1):
                temp_index = temp_index + repeat*interval
                result.append(temp_index)
                if len(result) == len(reordered_lst): # stop, complete
                    break
            if len(result) == len(reordered_lst): #stop complete
                break

        
        dic = {key:corr for key,corr in zip(result, reordered_lst)}
        sorted_d = dict(sorted(dic.items()))

        return list(sorted_d.values())
    



class CheckSheets:
    """
    Represents check sheets.

    Attributes:
        check_sessions (list): A list of CheckSession objects.
        fs_obj (FileSystem): The file system object associated with the check sheets.
    """
    def __init__(self,fs_obj ,**kwargs):
        self.check_sessions = []
        self.fs_obj = fs_obj
        self.session_open_index = None

    def add_session(self):
        """
        Adds a new session to the check sheets.
        """
        # Get the current date and time
        current_date_time = datetime.now()

        # Format the current date and time without seconds
        formatted_date_time = current_date_time.strftime("%Y-%m-%d %H:%M")
        date = formatted_date_time
        instance = CheckSession(date_created=date, 
                                 fs_obj=self.fs_obj,
                                 name = len(self.check_sessions),
                                 check_obj=self)
        self.check_sessions.append(instance)

    def get_session(self, index):
        """
        Retrieves a session from the check sheets.

        Args:
            index (int): The index of the session to retrieve.

        Returns:
            CheckSession: The specified session object.
        """
        self.session_open_index = index
        return self.check_sessions[index]
    
    
    def del_session(self):
        """
        Deletes last oepened check session
        """
        self.check_sessions = self.check_sessions.pop(self.session_open_index)


class Sheets:
    """
    Represents sheets.

    Attributes:
        date_created (str): The date and time when the sheet was created.
        name (str): The name of the sheet.
        answer_key (AnswerKeys): The answer key for the sheet.
        check_sheets (CheckSheets): The check sheets associated with the sheet.
        fs_obj (FileSystem): The file system object associated with the sheet.
    """
    def __init__(self, date_created, fs_obj, **kwargs):
        self.date_created = date_created
        self.name = ''
        self.answer_key = AnswerKeys(fs_obj=fs_obj)
        self.check_sheets = CheckSheets(fs_obj=fs_obj)
        self.check_sheet = self.check_sheets
        self.fs_obj = fs_obj

fs = FileSystem()
fs.add_sheet()
