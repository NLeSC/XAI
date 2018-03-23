# extracts image parameters from the input generator


input_file = 'PROBLEM.desc'
number_objects=3


# the output file
output_file = 'PROBLEM_v3.txt'






# what we are inquiring about
# dict('colour,shape,location,rellocation,size)
# 0 - do not ask questions
# 1 - ask questions

language_question = {'color': 1, 'shape': 1, 'location_hor': 1, 'location_vert': 1, 'size': 1} 



# the number of the output sentences
# string 
# one: one question per image (topics randomly chosen amongst possible ones + template randomly chosen)
# oneofeach: one question per possible topics per image (template randomly chosen)
# all: all possible topics and templates per image

language_sentence = 'all'



# the number of objects appearing in questions 
# int (0/n)
# 0 - the same as on the screen,
# n = 1,2

language_objects=2



# the option for the text form
# string (statement, question/answer)

language_form = 'question/answer'



# Some depecrated options...


# the option to include background in description or not
## int (0/1)
# 0 - do not include
# 1 - include

language_background = 0



## the number of objects for negative description
## string ( none / one / some /all)

language_negation = 'none'

