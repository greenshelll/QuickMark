import utilities.misc.feedback_sheet as Feedback
import random
feedback = Feedback.feedback

answers = list('ABCD')
get_random = lambda: answers[random.randint(0,1)]
length = 100
feedback(
    [answers[random.randint(0,3)] for x in range(length)],
    [[get_random()] for x in range(random.randint(0,3)) for times in range(length)],
    'MULTIPLE CHOICE', length

)