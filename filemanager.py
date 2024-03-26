from utilities.misc.feedback_sheet import *
import random
import pickle


#
fbc,errors= PRESAVE_FEEDBACK(1,175,'mc')
write_presaved_feedback(fbc)
print(errors)

print(fbc.mc[171])
input("CONTINUE TO TF?: ")
#fbc = read_presaved_feedback()
fbc,errors = PRESAVE_FEEDBACK(1,300,'tf',fbc)
write_presaved_feedback(fbc)

#fbc = read_presaved_feedback()
#print(fbc.get_mc_by_count(3)[11])

answers = list('ABCD')
get_random = lambda: answers[random.randint(0,1)]
length = 50
feedback_quick(
     ['T','F','F']*length,
    [['T','F'],['F'],['T']]*length,
    'TRUE OR FALSE', length*3

)
