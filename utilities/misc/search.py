import numpy as np

def levenshtein_distance(s1, s2):
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


def rate_similarity(strings, pattern):
    """
    Rate the similarity of each string in the list to a given pattern using Levenshtein distance.

    Args:
    - strings (list): List of strings to rate.
    - pattern (str): The pattern to compare against.

    Returns:
    - dict: A dictionary where keys are strings from the list and values are their similarity scores.
    """
    similarity_scores = {}
    for string in strings:
        similarity_scores[string] = levenshtein_distance(string, pattern)
    return similarity_scores

