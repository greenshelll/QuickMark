import pickle
from datetime import datetime

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
        self.local_file_directory = r"assets\localdb.pkl"
        self.open_index = 0

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
            pickle.dump(self, file)

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
    def __init__(self, fs_obj, answer_key=None,**kwargs):
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
            diff = current_length - number
            self.items = self.items[:diff]
            self.show_items = diff
    
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


class TrueOrFalse(MultipleChoice):
    """
    Represents a true or false question.
    """
    def __init__(self,fs_obj, **kwargs):
        self.items = []
        self.fs_obj = fs_obj


class Identification(MultipleChoice):
    """
    Represents an identification question.
    """
    def __init__(self, fs_obj,**kwargs):
        self.items = []
        self.fs_obj = fs_obj


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
        self.idtf = Identification(fs)
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
    def __init__(self,date_created, fs_obj,**kwargs):
        self.date_created = date_created
        self.fs_obj = fs_obj
        self.answer_key = fs_obj.sheets[fs_obj.open_index].answer_key
        self.mc = self.answer_key.mc
        self.tf = self.answer_key.tf
        self.idtf = self.answer_key.idtf
        self.open_index = 0


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
                                 fs_obj=self.fs_obj)
        self.check_sessions.append(instance)

    def get_session(self, index):
        """
        Retrieves a session from the check sheets.

        Args:
            index (int): The index of the session to retrieve.

        Returns:
            CheckSession: The specified session object.
        """
        self.open_index = index
        return self.check_sessions[index]


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
        self.fs_obj = fs_obj


fs = FileSystem()
fs.add_sheet()
sheet = fs.get_sheet(0)
ans_keys = sheet.answer_key
multiple_choice = ans_keys.mc
print(dir(multiple_choice))
multiple_choice.set_items(75)
print(multiple_choice.items[0])