import numpy as np
import re

class SearchSystem: 
    def __init__(self, str_keys, content):
        """Class for managing search

        Args:
            str_keys (list of strings): the basis of searching; to be used as keys. 
            content (any): can be anything that links to str keys.  str_keys and content must have the same 1d length


            returns sorted content
        """
        self.keys = str_keys
        self.content = content
        self.content_repr = [x for x in range(len(content))] # represent content as integers
        self.unique_keys = None # tbprocessed
        self.dict_tags = None #tbprocessed
        self._search_result = None 
        self.process()

    def process(self):
        self._generate_tags()
        return self
    
    def search(self, string, print_result=False):
        # Split the input string into individual patterns
        splitted_pattern = self._split(string)
        print("SPLITTED PATTERN",splitted_pattern)
        temp = []
        for pattern in splitted_pattern:
            if pattern != '':
                temp.append(pattern)
        
        # Initialize a list to store the sum of their similarity ranks
        # scorer, self.content_repr, self.content corresponds to the same index for the same content 
        scorer = [0 for x in range(len(self.content))]
        
        # Iterate over each pattern in the input string
        for pattern in temp:
            # Get the sorted keys based on the similarity to the current pattern
            sorted_keys = self._rate_similarity(pattern)
            
            # Initialize an empty list to store unique content representations for each pattern
            sorted_content = []
            
            # Iterate over each key in the sorted keys 
            for key_index in range(len(sorted_keys)):
                key = sorted_keys[key_index]
                
                # Iterate over each content representation associated with the current key
                for content_repr in self.dict_tags[key]:
                    # Get the index of the content representation in the content_repr list
                    score_index = self.content_repr.index(content_repr)
                    
                    # Update the scorer based on the key index and content representation
                    if content_repr not in sorted_content: # prevent duplicates
                        scorer[score_index] += key_index  # key index; the smaller, the better similarity; index also represent rank
                        sorted_content.append(content_repr) # indicator that it is done
            
        # Initialize a list to store the search results
        search_result = []
        
        # Sort the scorer list to get the indices of the content in ascending order of similarity scores
        sorted_scorer = sorted(scorer)

        print("SCORERS", scorer)
        # Iterate over each score in the sorted scorer list
        for score in sorted_scorer:
            # Get the index of the current score in the scorer list that have the same score
            indices = [i for i, x in enumerate(scorer) if x == score]
            for x in indices:
                search_result.append(self.content[x]) if self.content[x] not in search_result else None # append result using true content object; prevent duplicates
        
        # Print the search result if print_result is True
        print('SEARCH RESULT', search_result) if print_result else None
        
        # Return the search result
        return search_result



    def _generate_tags(self):
        """Splits strings linked to content into unique keys and each key corresponds to a list of contents it is linked.
        """
        str_keys = ' '.join(self.keys).lower() # cmbine list of strings into single string
        unique_keys = np.unique(self._split(str_keys)) # split strings using non alphanum as separator and get unique strings
        print('UNIQUE KEYS',unique_keys)
        self.unique_keys = unique_keys 

        dict_tags = {key:[] for key in unique_keys} # initialize unique keys
        for key,content in zip(self.keys, self.content_repr): 
            split_keys = self._split(key.lower())
            for key in split_keys:
                dict_tags[key].append(content) # append content to list with designated unique key
        print('DICT TAGS',dict_tags)
        self.dict_tags = dict_tags

    def _split(self, input_string):
        # Input string
        # Split the string using non-alphanumeric characters as separator
        split_strings = re.split(r'[^a-zA-Z0-9]+', input_string)

        return split_strings
    
    def _levenshtein_distance(self, s1, s2):
        """
        Calculate the Levenshtein distance between two strings.

        Args:
        - s1 (str): The first string.
        - s2 (str): The second string.

        Returns:
        - int: The Levenshtein distance between the two strings.
        """
        m = len(s1)
        n = len(s2)

        # Initialize a matrix to store the distances
        dp = np.zeros((m + 1, n + 1), dtype=int)

        # Initialize the first row and column
        dp[:, 0] = np.arange(m + 1)
        dp[0, :] = np.arange(n + 1)

        # Calculate the distances
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i, j] = dp[i - 1, j - 1]
                else:
                    dp[i, j] = 1 + min(dp[i - 1, j],      # deletion
                                    dp[i, j - 1],      # insertion
                                    dp[i - 1, j - 1])  # substitution

        return dp[m, n]


    def _rate_similarity(self, pattern):
        """
        Rate the similarity of each string in the list to a given pattern using Levenshtein distance.

        Args:
        - pattern (str): The pattern to compare against.

        Returns:
        - list: A list of unique keys sorted by their similarity scores.
        """
        # Create a list to store similarity scores along with the corresponding unique keys
        similarity_scores = []

        # Calculate similarity scores for each unique key
        for string in self.unique_keys:
            similarity_score = self._levenshtein_distance(string, pattern)
            similarity_scores.append((string, similarity_score))

        # Sort the list of tuples by the similarity score
        similarity_scores.sort(key=lambda x: x[1])

        # Extract the unique keys from the sorted list
        sorted_keys = [item[0] for item in similarity_scores]

        return sorted_keys


if __name__ == "__main__":
    # samples

    keys = ['apple cidar mango', 'apple cidar blue', 'green_mango', 'triple-W mango']
    keys = keys + keys # duplicates string keys
    content = ['object1','object2','object3','object4','object5', 'object6', 'object7', 'object8']

    ss = SearchSystem(keys, content)
    print(ss.search('blue apple'))
    # result->['object2', 'object6', 'object1', 'object5', 'object4', 'object8', 'object3', 'object7']


    ss = SearchSystem(
        str_keys= ['Hello World', 'I love you', 'Hello!, Good Morning'],
        content = ["HW OBJECT", "ILY OBJECT", "GM OBJECT"]
    )
    ss.search('I love morning',True)
    # result->SEARCH RESULT ['ILY OBJECT', 'GM OBJECT', 'HW OBJECT'] 
    ss.search('Hello!',True)
    # result-> ['HW OBJECT', 'GM OBJECT', 'ILY OBJECT']