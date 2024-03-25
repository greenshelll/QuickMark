import utilities.misc.feedback_sheet as Feedback
import random
feedback = Feedback.feedback

answers = list('ABCD')
get_random = lambda: answers[random.randint(0,1)]
length = 100
feedback(
     ['T','T','F'],
    [['T'],['T'],['F']],
    'TRUE OR FALSE', length

)