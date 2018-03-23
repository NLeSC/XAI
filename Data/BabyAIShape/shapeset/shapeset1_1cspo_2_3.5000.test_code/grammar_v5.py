#!/usr/local/bin/python

# includes built-in modules

import sys
import os
import shutil
import random 

from os.path import *

from math import *

# all templates

from templates_v5 import *


#++++++++
from problem import *
# related changes: FID_input changed to be a scene
# reason: we don't want to have to read from a file
#--------



####################################################################################################################


def list_crescent_pairs(number_objects):
	return [[i,j] for i in range(number_objects) for j in range(i+1,number_objects)]

def list_all_pairs(number_objects):
	return [[i,j] for i in range(number_objects) for j in range(i+1,number_objects)+range(0,i)]


# image = (dict) image description
# pair = (list of int) index of the objects in a pair (in range(number_objets) x range(number_objets))
# attributeName = 'size', 'hrz_pos', 'vrt_pos'

def get_relative_attribute(image,pair,attributeName):
	#return eval("images["+str(image)+"]['comparison_"+str(pair[0])+"/"+str(pair[1])+"']['"+attributeName+"']")
	return image["comparison_"+str(pair[0])+"/"+str(pair[1])][attributeName]

# image = (dict) image description
# i_object = (int) index of the object (in range(number_objets))
# attributeName = 'color', 'shape', 'size', 'hrz_pos', 'vrt_pos'

def get_absolute_attribute(image,i_object,attributeName):
	#return eval("images["+str(image)+"]['object_"+str(i_object)+"']['"+attributeName+"']")
	return image["object_"+str(i_object)][attributeName]

#################################################################################################################

# Semantic Knowledge (Rules)

# Grammatical Rules on 

# position with respect to another object

def relative_position_vert(i,j,image):
	
	if i < j:
		# print eval("image"+ "['comparison_"+str(i)+"/"+str(j)+"']['vrtpos']")
		if eval("image"+ "['comparison_"+str(i)+"/"+str(j)+"']['vrtpos']") =='NA':
			position = 'NA'
		if eval("image"+ "['comparison_"+str(i)+"/"+str(j)+"']['vrtpos']") =='higher':
			position='above'
		if eval("image"+ "['comparison_"+str(i)+"/"+str(j)+"']['vrtpos']") =='lower':
			position='below'
	elif i > j:
		if eval("image"+ "['comparison_"+str(j)+"/"+str(i)+"']['vrtpos']")=='NA':
			position = 'NA'
		if eval("image"+ "['comparison_"+str(j)+"/"+str(i)+"']['vrtpos']")=='higher':
			position='below'
		if eval("image"+ "['comparison_"+str(j)+"/"+str(i)+"']['vrtpos']")=='lower':
			position='above'
	else:
		print "ERROR in relative_position_vert : i and j must be different"
		sys.exit(0)
	
        return position                 
			 # vertical placement
def relative_position_hor(i,j,image):
	# print i, j	
	preposition = ['to the','on the']
	prep = RANDOM.choice(preposition)
	
	
	if i < j:
		if eval("image"+ "['comparison_"+str(i)+"/"+str(j)+"']['hrzpos']")=='NA':
			position = 'NA'
		if eval("image"+ "['comparison_"+str(i)+"/"+str(j)+"']['hrzpos']")=='left':
			position=prep+' left of'
		elif eval("image"+ "['comparison_"+str(i)+"/"+str(j)+"']['hrzpos']")=='right':
			position=prep+' right of'
	elif i > j:
		if eval("image"+ "['comparison_"+str(j)+"/"+str(i)+"']['hrzpos']")=='NA':
			position = 'NA'
		if eval("image"+ "['comparison_"+str(j)+"/"+str(i)+"']['hrzpos']")=='left':
			position=prep+' right of'
		elif eval("image"+ "['comparison_"+str(j)+"/"+str(i)+"']['hrzpos']")=='right':
			position=prep+' left of'
	else:
		print "ERROR in relative_position_hor : i and j must be different"
		sys.exit(0)
	# print position
        return position

def abs_position_hor(hrz):
	
	preposition = ['to the ','on the ']
	prep = RANDOM.choice(preposition)
	
	position = prep+hrz
	
	return position

def abs_position_vert(vrt):
	
	preposition = ['at the ','on the ']
	prep = RANDOM.choice(preposition)
	
	position = prep+vrt
	
	return position

def relative_position_hor_ans(i,j,image):
		
	preposition = ['on the']
	
	prep = RANDOM.choice(preposition)
	
	if i < j:
		if eval("image"+ "['comparison_"+str(i)+"/"+str(j)+"']['hrzpos']")=='NA':
			position = 'NA'
		elif eval("image"+ "['comparison_"+str(i)+"/"+str(j)+"']['hrzpos']")=='left':
			position=prep+' left '
		elif eval("image"+ "['comparison_"+str(i)+"/"+str(j)+"']['hrzpos']")=='right':
			position=prep+' right '
	elif i > j:
		if eval("image"+ "['comparison_"+str(j)+"/"+str(i)+"']['hrzpos']")=='NA':
			position = 'NA'
		elif eval("image"+ "['comparison_"+str(j)+"/"+str(i)+"']['hrzpos']")=='left':
			position=prep+' right '
		elif eval("image"+ "['comparison_"+str(j)+"/"+str(i)+"']['hrzpos']")=='right':
			position=prep+' left '
	else:
		position = 'No position'
		sys.exit(0)
			
        return position

def relative_position_hor_short(i,j,image):
	
	if i < j:
		if eval("image"+ "['comparison_"+str(i)+"/"+str(j)+"']['hrzpos']")=='NA':
			position = 'NA'
		elif eval("image"+ "['comparison_"+str(i)+"/"+str(j)+"']['hrzpos']")=='left':
			position= ' left '
		elif eval("image"+ "['comparison_"+str(i)+"/"+str(j)+"']['hrzpos']")=='right':
			position= ' right '
	elif i > j:
		if eval("image"+ "['comparison_"+str(j)+"/"+str(i)+"']['hrzpos']")=='NA':
			position = 'NA'
		elif eval("image"+ "['comparison_"+str(j)+"/"+str(i)+"']['hrzpos']")=='left':
			position= ' right '
		elif eval("image"+ "['comparison_"+str(j)+"/"+str(i)+"']['hrzpos']")=='right':
			position= ' left '
	else:
		position = 'No position'
		sys.exit(0)
			
        return position

#####################################################################################################################

def relative_size(i,j,image):
	# print i, j
	if i < j:
		rel_size = eval("image"+ "['comparison_"+str(i)+"/"+str(j)+"']['size']") 
	
	elif i >j:
		if eval("image"+ "['comparison_"+str(j)+"/"+str(i)+"']['size']") == 'smaller':
			rel_size = 'bigger'
		
		elif eval("image"+ "['comparison_"+str(j)+"/"+str(i)+"']['size']") == 'bigger':
			rel_size = 'smaller'
		
		elif eval("image"+ "['comparison_"+str(j)+"/"+str(i)+"']['size']") == 'NA':
			rel_size = 'NA'	
	# print rel_size	
	return rel_size
		
def compare_comparison(i,j,k,l,attr):
	#print i, j, k, l, attr
	same = 1
	
	if attr == 'size':
		if (relative_size(i,j,image) != relative_size(k,l,image) and relative_size(i,j,image) != 'NA' and relative_size(k,l,image) != 'NA'):
			same = 0
	
	if attr == 'vrtpos':
		if (relative_position_vert(i,j,image) != relative_position_vert(k,l,image) and relative_position_vert(i,j,image) != 'NA' and relative_position_vert(k,l,image) != 'NA'):
			same = 0
			
	if attr == 'hrzpos':
		if (relative_position_hor_short(i,j,image) != relative_position_hor_short(k,l,image) and relative_position_hor_short(i,j,image) != 'NA' and relative_position_hor_short(k,l,image) != 'NA'):
			same = 0
	# print same
	return same		
	
		
# delete reduntant words (position in centre and medium size)
def redundant_centre(x,y):
	
        if x == 'upper' and y == 'centre': y = '' 
        if x == 'lower' and y == 'centre': y = '' 
		
	return y

def redundant_middle(x):
        if x == 'middle' : x = '  ' 
		
	return x
	
def redundant_medium(x):
        if x in ['medium','NA']: x = '' 
		
	return x
def restore(x,y):
	y.append(x)
        return y
	
	
######################################################################################################################

def build_question_topics_one_objects():

	q_topics=[]
	q_list=[]	
	
	if language_question['color']==1:
		q_topics.append("['object_0']['color']")
		q_list.append("color_quest")
		
	if language_question['shape']==1:
		q_topics.append("['object_0']['shape']")
		q_list.append("shape_quest")
				
	if language_question['size']==1:
		q_topics.append("['object_0']['size']")
		q_list.append("size_quest")
		
	if language_question['location_hor']==1:
		q_topics.append("['object_0']['hrzpos']")
		q_list.append("hrzpos_quest")
				
	if language_question['location_vert']==1:
		q_topics.append("['object_0']['vrtpos']")
		q_list.append("vrtpos_quest")		
			
	return q_topics, q_list


def build_question_topics_several_objects(i,j):

	q_topics=[]
	q_list=[]	
	
	if language_question['color']==1:
		q_topics.append("['object_"+str(i)+"']['color']")
		q_list.append("color_quest")
		
	if language_question['shape']==1:
		q_topics.append("['object_"+str(i)+"']['shape']")
		q_list.append("shape_quest")
		
	i0=min(i,j)
	j0=max(i,j)
				
	if language_question['size']==1:
		q_topics.append("['comparison_"+str(i0)+"/"+str(j0)+"']['size']")
		q_list.append("size_quest")
		
	if language_question['location_hor']==1:
		q_topics.append("['comparison_"+str(i0)+"/"+str(j0)+"']['hrzpos']")
		q_list.append("hrzpos_quest")
				
	if language_question['location_vert']==1:
		q_topics.append("['comparison_"+str(i0)+"/"+str(j0)+"']['vrtpos']")
		q_list.append("vrtpos_quest")		
			
	return q_topics, q_list




	

def no_question(a,b,c,quest):
	if b== 1 and c==1 and a == 0: quest = 0
	
	return quest


#######################################################################################################################


def printout(text):
        if len(text) == 0:
	   print "ERROR : no text given"
	   sys.exit(0)
	if globals()['sentence'] == 1: # print one sentence per type
		FID_output.write(RANDOM.choice(text)+"\n") 
        else:
		for i in range(len(text)):
			if 'NA' in text[i]:
			   print text
			   sys.exit(0)
			FID_output.write(text[i]+"\n")
 

#####################################################################################################################


#++++++++

def reseed_grammar(seed):
  if seed == None:
          RANDOM.seed(random.random())
  else:
          RANDOM.seed(seed)

def printout_but_not_really(text):
        if len(text) == 0:
	   print "ERROR : no text given"
	   sys.exit(0)
	if globals()['sentence'] == 1: # print one sentence per type
		sentence_list.append(RANDOM.choice(text))
        else:
		for i in range(len(text)):
			if 'NA' in text[i]:
			   print text
			   sys.exit(0)
			sentence_list.append(text[i])

# this is like main but the changes are marked with ##########
def describe(scene_dict, **config):

  globals().update(config) ##########

  # initiate scene parameters
  
  # the number of objects to describe; 
  # if language_objects == 0, then all objects from the image
  if language_objects == 0: number_objects_referedto = number_objects
  else: number_objects_referedto = language_objects
  

  # text format
  if language_form == 'question/answer' and language_question == None:
	print 'Inconsistent language parameters:'+ ' '+language_form+' '+ 'and'+ ' '+language_question
	raise endSearch
  if language_form == 'type_of_sentencement' and (language_question == 'color' or language_question == 'size' or
	language_question == 'shape' or language_question == 'location' or language_question == 'position'):
	print 'Inconsistent language parameters:'+ ' '+language_form+' '+ 'and question'+ ' '+language_question
	raise endSearch

  # the number of output sentences

  if language_sentence == 'one' or language_sentence == 'oneofeach': sentence = 1
  else: sentence = 0

  
  # If there are more than 1 object,
  # we will build the list of possible topics on a case by case (each pair of each image)
  #
  question_topics, quest_list = build_question_topics_one_objects()
  question_topics_index=range(len(question_topics))			
  
  
  globals()['sentence']         = sentence
  globals()['FID_output']       = None ##########
  
  i_image=0
  for whatever in [1]: ########## I didn't feel like untabbing the body

        globals()['sentence_list'] = [] ##########
  
        image = scene_dict ##########
        globals()['image'] = image
  
#         if language_sentence == 'all' or language_sentence == 'oneofeach': ##########
#         	printout(['\nImage '+str(i_image)+':']) ##########
#	print "Image "+str(i_image) ##########
	i_image+=1

	# initialize 
	objects = []
	cl = []
      # shape 
	sh = []
      # vertical position on the screen
	vr = []
      # horizontal position on the screen
	hr = []
      # size
	sz = []
 	# matrix of relative positions from other objects 

	position = []
	
	
	# for random objects from the image


	# include or not background description
	if language_background == 0:
	   bc = ' '
	else:
	   bc = 'on' + ' ' + 'the' + ' ' + image['background']['color'] +'  screen'
	for i in range(number_objects):	
		cl.append(image['object_'+str(i)]['color'])
		sh.append(image['object_'+str(i)]['shape'])
		hr.append(image['object_'+str(i)]['hrzpos'])
		vr.append(image['object_'+str(i)]['vrtpos'])
        	sz.append(image['object_'+str(i)]['size'])  
                objects.append(image['object_'+str(i)])


	# for i in range(len(objects)):
	#	print objects[i]
	 
	# In the question, we refer to more than 2 objects...
	if number_objects_referedto > 1:
		
#		print '2 objects amongst '+str(number_objects) ##########
		
		index_pairs   = [[i,j] for i in range(number_objects) for j in range(0,i)+range(i+1,number_objects)]
		
		index_objects = range(number_objects)
		
		# The objects are chosen randomly in the *desc file,
		# so we do not need this kind of things:
		# (resolved bug)
		#
		# if language_sentence == 'one' or language_sentence == 'oneofeach':
		#	index_pairs = [RANDOM.choice(index_pairs)]
		
			
		for i_pair in index_pairs:
			
			# printout([str(i_pair[0])+ '+' +str(i_pair[1])])
			# print i_pair[0], i_pair[1]
			theobj = []
			
			theobj.append(objects[i_pair[0]])
			theobj.append(objects[i_pair[1]])
			
			same_color_other = [0,0]
			same_shape_other = [0,0]
			same_size_other = [0,0]
			same_abshrz_other = [0,0]
			same_absvrt_other = [0,0]
			same_relsize_other = [0,0]
			same_relhrzpos_other = [0,0]
			same_relvrtpos_other = [0,0]
			
			if number_objects > 2:
				others = []
			
				for i in range(len(objects)):
					if i != i_pair[0] and i != i_pair[1]:
						others.append(i)			
			
				same_relsize_other   = [0,0]
				same_relhrzpos_other = [0,0]
				same_relvrtpos_other = [0,0]
				
				
			
				# check whether there are other objects similar to the object in question
				#print hr[i_pair[0]]
				#print hr[i_pair[1]]
				
				for ob_other in others:
					
					if cl[i_pair[0]] == cl[ob_other]:
						same_color_other[0] = 1
					if sh[i_pair[0]] == sh[ob_other]:
						same_shape_other[0] = 1
					if sz[i_pair[0]] == sz[ob_other]:
						same_size_other[0] = 1
				
					if hr[i_pair[0]] == hr[ob_other]:	
						same_abshrz_other[0] = 1
					
					if vr[i_pair[0]] == vr[ob_other]:	
						same_absvrt_other[0] = 1
					# (resolved bug)
					same_relsize_other[0]   = max(same_relsize_other[0],compare_comparison(i_pair[0],i_pair[1],ob_other,i_pair[1],'size'))
					same_relhrzpos_other[0] = max(same_relhrzpos_other[0],compare_comparison(i_pair[0],i_pair[1],ob_other,i_pair[1],'hrzpos'))
					
					same_relvrtpos_other[0] = max(same_relvrtpos_other[0],compare_comparison(i_pair[0],i_pair[1],ob_other,i_pair[1],'vrtpos'))
					
					
				# check whether there are other objects similar to the object in comparison
				
				for ob_other in others:
					
					if cl[i_pair[1]] == cl[ob_other]:
						same_color_other[1] = 1
					if sh[i_pair[1]] == sh[ob_other]:
						same_shape_other[1] = 1
					if sz[i_pair[1]] == sz[ob_other]:
						same_size_other[1] = 1
					
					if hr[i_pair[1]] == hr[ob_other]:	
						same_abshrz_other[1] = 1
					
					if vr[i_pair[1]] == vr[ob_other]:	
						same_absvrt_other[1] = 1
					# (resolved bug)
					same_relsize_other[1]   = max(same_relsize_other[1],compare_comparison(i_pair[0],i_pair[1],ob_other,i_pair[1],'size'))
					same_relhrzpos_other[1] = max(same_relhrzpos_other[1],compare_comparison(i_pair[0],i_pair[1],ob_other,i_pair[1],'hrzpos'))
					same_relvrtpos_other[1] = max(same_relvrtpos_other[1],compare_comparison(i_pair[0],i_pair[1],ob_other,i_pair[1],'vrtpos'))
			
			# print same_abshrz_other
			# print same_absvrt_other
			#######################################################
			# Here we define all the topics we can talk about...
			# (taking into acount the config file AND the relevant topics for the scene)

			question_topics, quest_list = build_question_topics_several_objects(i_pair[0],i_pair[1])			
			question_topics_index=range(len(question_topics))			
			
			if language_sentence == 'one':
				only_one_question = 0	
		        	tmp=RANDOM.choice(question_topics_index)
				topics=[tmp]
				while eval("image"+question_topics[topics[0]]) == 'NA' or  quest_list[tmp] == 0:
					topics=[RANDOM.choice(question_topics_index)]
					
			elif language_sentence == 'all' or language_sentence == 'oneofeach':
				topics=[]
				only_one_question = 2
				for topic_index in question_topics_index:
					if eval("image"+question_topics[topic_index]) != 'NA':
						topics.append(topic_index)	
			else:	
				print "ERROR: parameter language_sentence not valid (1)"
				sys.exit(0)
			
                        # We then choose one or several topics among the possible ones

			for quest in quest_list:
			        globals()[quest]=0
			for topic in topics:
				globals()[quest_list[topic]]=1				
			
                        # This ''hack'' would be to change...
                        if globals().has_key('hrzpos_quest'):
                                hrzpos_quest=globals()['hrzpos_quest']
                        else:
                                hrzpos_quest=0
                        if globals().has_key('vrtpos_quest'):
                                vrtpos_quest=globals()['vrtpos_quest']
                        else:
                                vrtpos_quest=0
                        if globals().has_key('shape_quest'):
                                shape_quest=globals()['shape_quest']
                        else:
                                shape_quest=0
                        if globals().has_key('color_quest'):
                                color_quest=globals()['color_quest']
                        else:
                                color_quest=0
                        if globals().has_key('size_quest'):
                                size_quest=globals()['size_quest']
                        else:
                                size_quest=0
			
			#######################################################

											
		
			relsize = relative_size(i_pair[0],i_pair[1],image)
								
			relposition_vert =  relative_position_vert(i_pair[0],i_pair[1],image)	
			
			relposition_hor =  relative_position_hor(i_pair[0],i_pair[1],image)	
			
			relpos_hor_ans1 = relative_position_hor_ans(i_pair[0],i_pair[1],image)
							
			if theobj[0].get('shape') != theobj[1].get('shape') and same_shape_other[0] == 0 and same_shape_other[1] == 0:
				adescr1 = an_object(theobj[0].get('shape'),theobj[0].get('color'),theobj[0].get('size'))		
				adescr2 = an_object(theobj[1].get('shape'),theobj[1].get('color'),theobj[1].get('size'))
				thedescr1 = the_object(theobj[0].get('shape'),theobj[0].get('color'),theobj[0].get('size'))		
				thedescr2 = the_object(theobj[1].get('shape'),theobj[1].get('color'),theobj[1].get('size'))
			elif (theobj[0].get('shape') == theobj[1].get('shape') or same_shape_other[0] != 0 or same_shape_other[1] != 0) and (theobj[0].get('color') != theobj[1].get('color') and same_color_other[0] == 0 and same_color_other[1] == 0):
 				adescr1 = an_object_sameShape(theobj[0].get('shape'),theobj[0].get('color'),theobj[0].get('size'))	
				adescr2 = an_object_sameShape(theobj[1].get('shape'),theobj[1].get('color'),theobj[1].get('size'))
				thedescr1 = the_object_sameShape(theobj[0].get('shape'),theobj[0].get('color'),theobj[0].get('size'))	
				thedescr2 = the_object_sameShape(theobj[1].get('shape'),theobj[1].get('color'),theobj[1].get('size'))
			else:  # there are similar shapes and color
				adescr1 = an_object_sameShapeColor(theobj[0].get('shape'),theobj[0].get('color'),theobj[0].get('size'))	
				adescr2 = an_object_sameShapeColor(theobj[1].get('shape'),theobj[1].get('color'),theobj[1].get('size'))
				thedescr1 = the_object_sameShapeColor(theobj[0].get('shape'),theobj[0].get('color'),theobj[0].get('size'))	
				thedescr2 = the_object_sameShapeColor(theobj[1].get('shape'),theobj[1].get('color'),theobj[1].get('size'))
					
			
			
			# Determine the absolute position of the first object
			# (It is 'in the middle' if it is not on the right/left neither on the top/bottom)
			
			absolute_position = ['NA','NA']
			for i in [0,1]:
				if theobj[0].get('hrzpos')==theobj[1].get('hrzpos'):
					same_abshrz_other[i] = 1
				if theobj[0].get('vrtpos')==theobj[1].get('vrtpos'):
					same_absvrt_other[i] = 1

			for i in [0,1]:
				if same_abshrz_other[i] == 0 and same_absvrt_other[i] == 0:
					if theobj[i].get('hrzpos')=='NA':
						if theobj[i].get('vrtpos')=='NA':
			      				absolute_position[i] = 'in the middle'
						else:
			      				absolute_position[i] = abs_position_vert(theobj[i].get('vrtpos'))
					elif theobj[i].get('vrtpos')=='NA':
			   			absolute_position[i] = abs_position_hor(theobj[i].get('hrzpos'))
					else:
			   			absolute_position[i] = RANDOM.choice([abs_position_vert(theobj[i].get('vrtpos')),abs_position_hor(theobj[i].get('hrzpos'))])
				elif same_abshrz_other[i] == 0 and same_absvrt_other[i] == 1:
					if theobj[i].get('hrzpos')!='NA':
						absolute_position[i] = abs_position_hor(theobj[i].get('hrzpos'))	
				elif same_abshrz_other[i] == 1 and same_absvrt_other[i] == 0:	
					if theobj[i].get('vrtpos')!='NA':		 
			      			absolute_position[i] = abs_position_vert(theobj[i].get('vrtpos'))
					
			
			# summarize  differences
			
			diff = [1,1]
			
			if (same_color_other[0] == 1 and same_shape_other[0] == 1 and same_size_other[0] == 1): 
				diff[0] = 0 
					 
			if (same_color_other[1] == 1 and same_shape_other[1] == 1 and same_size_other[1] == 1):
				diff[1] = 0	
			
			if ((theobj[0].get('shape') == theobj[1].get('shape') and  theobj[0].get('color') == theobj[1].get('color')) and (theobj[0].get('size') == theobj[1].get('size') or theobj[0].get('size') == 'medium' or theobj[1].get('size') == 'medum')  ):
				vrtpos_quest = 0
				hrzpos_quest = 0
				
			if (size_quest == 1 and theobj[0].get('shape') == theobj[1].get('shape') and  theobj[0].get('color') == theobj[1].get('color')):
				relposition_hor = 'NA'
				relposition_vert = 'NA'
				
			if diff[1] == 0:
				relposition_hor = 'NA'
				relposition_vert = 'NA'
				size_quest == 0
				
			# allowed questions	
			if same_relhrzpos_other[0] == 0:
				if color_quest == 1:
					if relposition_hor != 'NA':
						text_two_color = two_objects_questions_color(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,relposition_hor)
						printout_but_not_really(text_two_color) ##########
						if only_one_question == 0: break
					elif absolute_position[0] != 'NA':
						text_two_color = two_objects_questions_color_abspos(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,absolute_position[0])
						printout_but_not_really(text_two_color) ##########
						if only_one_question == 0: break
				if shape_quest == 1: 
					if relposition_hor != 'NA':
						text_two_shape = two_objects_questions_shape(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,relposition_hor)
						printout_but_not_really(text_two_shape) ##########
						if only_one_question == 0: break
					elif absolute_position[0] != 'NA':
						text_two_shape = two_objects_questions_shape_abspos(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,absolute_position[0])		
						printout_but_not_really(text_two_shape) ##########
						if only_one_question == 0: break	
				if size_quest == 1:
					if relposition_hor != 'NA':
						text_two_size = two_objects_questions_size(theobj[0].get('color'),theobj[0].get('shape'),theobj[1].get('color'),theobj[1].get('shape'),relposition_hor,relsize)
						printout_but_not_really(text_two_size)	 ##########
						if only_one_question == 0: break
					elif absolute_position[0] != 'NA':
						text_two_size = two_objects_questions_size_abspos(theobj[0].get('color'),theobj[0].get('shape'),theobj[1].get('color'),theobj[1].get('shape'),absolute_position[0],relsize)
						printout_but_not_really(text_two_size) ##########	
						if only_one_question == 0: break
								
			if same_relvrtpos_other[0] == 0:
				if color_quest == 1:				
					if relposition_vert != 'NA':	
						text_two_color= two_objects_questions_color(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,relposition_vert)			
						printout_but_not_really(text_two_color) ##########
						if only_one_question == 0: break
					elif absolute_position[0] != 'NA':
						text_two_color = two_objects_questions_color_abspos(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,absolute_position[0])
						printout_but_not_really(text_two_color) ##########
						if only_one_question == 0: break				
				if shape_quest == 1:	
					if relposition_vert != 'NA':
						text_two_shape = two_objects_questions_shape(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,relposition_vert)			
						printout_but_not_really(text_two_shape) ##########
						if only_one_question == 0: break	
					elif absolute_position[0] != 'NA':
						text_two_shape = two_objects_questions_shape_abspos(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,absolute_position[0])	
						printout_but_not_really(text_two_shape) ##########
						if only_one_question == 0: break	
				if size_quest == 1:
					if relposition_vert != 'NA':
						text_two_size = two_objects_questions_size(theobj[0].get('color'),theobj[0].get('shape'),theobj[1].get('color'),theobj[1].get('shape'),relposition_vert,relsize)
						printout_but_not_really(text_two_size) ##########
						if only_one_question == 0: break
					elif absolute_position[0] != 'NA':
						text_two_size = two_objects_questions_size_abspos(theobj[0].get('color'),theobj[0].get('shape'),theobj[1].get('color'),theobj[1].get('shape'),absolute_position[0],relsize)
						printout_but_not_really(text_two_size) ##########	
						if only_one_question == 0: break
						
			# some questions on colour, shape, size are not permitted
				
			if same_relhrzpos_other[0] == 1 or same_relvrtpos_other[0] == 1:	
				if color_quest == 1:
					if relposition_hor != 'NA' and same_relhrzpos_other[0] == 0:	
						text_two_color = two_objects_questions_color_sameLocationShape(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,relposition_hor)
						printout_but_not_really(text_two_color) ##########
						if only_one_question == 0: break			
					elif relposition_vert != 'NA' and same_relvrtpos_other[0] == 0:
						text_two_color= two_objects_questions_color_sameLocationShape(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,relposition_vert)	
						printout_but_not_really(text_two_color)	 ##########
						if only_one_question == 0: break	
					elif absolute_position[0] != 'NA':
						text_two_color = two_objects_questions_color_abspos(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,absolute_position[0])
						printout_but_not_really(text_two_color) ##########
						if only_one_question == 0: break	
				if size_quest == 1:
					if relposition_hor != 'NA' and same_relhrzpos_other[0] == 0:
						text_two_size = two_objects_questions_size(theobj[0].get('color'),theobj[0].get('shape'),theobj[1].get('color'),theobj[1].get('shape'),relposition_hor,relsize)
						printout_but_not_really(text_two_size) ##########
						if only_one_question == 0: break	
					elif relposition_vert != 'NA' and same_relvrtpos_other[0] == 0:
						text_two_size = two_objects_questions_size(theobj[0].get('color'),theobj[0].get('shape'),theobj[1].get('color'),theobj[1].get('shape'),relposition_vert,relsize)
						printout_but_not_really(text_two_size) ##########
						if only_one_question == 0: break
					elif absolute_position[0] != 'NA':
						text_two_size = two_objects_questions_size_abspos(theobj[0].get('color'),theobj[0].get('shape'),theobj[1].get('color'),theobj[1].get('shape'),absolute_position[0],relsize)
						printout_but_not_really(text_two_size) ##########
						if only_one_question == 0: break	
				if shape_quest == 1:	
					if relposition_hor != 'NA' and same_relhrzpos_other[0] == 0:
						text_two_shape = two_objects_questions_shape_sameLocation(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,relposition_hor)	
						printout_but_not_really(text_two_shape) ##########
						if only_one_question == 0: break	
					elif relposition_vert != 'NA' and same_relvrtpos_other[0] == 0:
						text_two_shape = two_objects_questions_shape_sameLocation(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,relposition_vert)	
						printout_but_not_really(text_two_shape) ##########
						if only_one_question == 0: break
					elif absolute_position[0] != 'NA':
						text_two_shape = two_objects_questions_shape_abspos(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,absolute_position[0])	
						printout_but_not_really(text_two_shape) ##########
						if only_one_question == 0: break		
	
			
				
			if vrtpos_quest == 1 and relposition_vert != 'NA':
				if same_abshrz_other[0] == 0 and theobj[0].get('hrzpos') != 'NA' and diff[0] ==0 and diff[1] == 0: 
						text_two_location_vert = two_objects_questions_location_vert_abs(adescr1,thedescr1,adescr2,thedescr2,relposition_vert,abs_position_hor(theobj[0].get('hrzpos')))
						printout_but_not_really(text_two_location_vert) ##########
						if only_one_question == 0: break
				elif (diff[0] ==1 and diff[1] ==1):
						text_two_location_vert = two_objects_questions_location_vert(adescr1,thedescr1,adescr2,thedescr2,relposition_vert)
						printout_but_not_really(text_two_location_vert) ##########
						if only_one_question == 0: break
					
			if hrzpos_quest == 1 and relposition_hor != 'NA':		
				if same_absvrt_other[0] == 0 and theobj[0].get('vrtpos') != 'NA' and diff[0] ==0 and diff[1] == 0:
						text_two_location_hor = two_objects_questions_location_hor_abs(adescr1,thedescr1,adescr2,thedescr2,relpos_hor_ans1,abs_position_vert(theobj[0].get('vrtpos')))
						printout_but_not_really(text_two_location_hor) ##########
						if only_one_question == 0: break
				elif (diff[0] ==1 and diff[1] ==1):
						text_two_location_hor = two_objects_questions_location_hor(adescr1,thedescr1,adescr2,thedescr2,relpos_hor_ans1)
						printout_but_not_really(text_two_location_hor) ##########
						if only_one_question == 0: break
			
			# if other questions fail:
			if same_shape_other[0] == 0 and theobj[0].get('shape') != theobj[1].get('shape'):
				text_one_color_no_location = one_object_questions_color_no_location(theobj[0].get('color'),theobj[0].get('shape'))
				printout_but_not_really(text_one_color_no_location) ##########
				if only_one_question == 0: break
			elif same_color_other[0] == 0 and theobj[0].get('color') != theobj[1].get('color'):
				text_one_size_no_location = one_object_questions_shape_no_location(theobj[0].get('color'),theobj[0].get('shape'))
				printout_but_not_really(text_one_size_no_location) ##########
				if only_one_question == 0: break
			elif (same_shape_other[0] == 1 and theobj[0].get('shape') == theobj[1].get('shape') and same_shape_other[1] == 1):
				text_one_same_shape = one_object_questions_same_shape(theobj[0].get('shape'))
				printout_but_not_really(text_one_same_shape) ##########
				if only_one_question == 0: break
			elif (same_color_other[0] == 1 and theobj[0].get('color') == theobj[1].get('color') and same_color_other[0] == 1):
				text_one_same_color = one_object_questions_same_color(theobj[0].get('color'))
				printout_but_not_really(text_one_same_color) ##########
				if only_one_question == 0: break	
			
	if number_objects_referedto==1:
		
		
                # Deprecated !!!!!!!!!
                if language_form == 'statement':

#			print '1'+' '+'object'
			theobj = RANDOM.choice(objects)		
			theobj['size'] = redundant_medium(theobj['size'])
			thedescr = an_object(theobj.get('shape'),theobj.get('color'),theobj.get('size'))		
			text_one = one_object(thedescr,theobj['vrtpos'],theobj['hrzpos'])
			printout_but_not_really(text_one)
			if theobj.get('size') == '': theobj['size'] = 'medium'
			text_part = object_partial(theobj.get('shape'),theobj.get('color'),theobj.get('size'))
			printout_but_not_really(text_part)
			
			
		elif language_form == 'question/answer':


#			print '1'+' '+'object'	
			theobj = objects[0]	
			adescr = an_object(theobj.get('shape'),theobj.get('color'),theobj.get('size'))
			thedescr = the_object(theobj.get('shape'),theobj.get('color'),theobj.get('size'))

                        if 'medium' in thedescr:
			   print theobj
			   sys.exit(0)

			if language_sentence == 'one':
		        	tmp=RANDOM.choice(question_topics_index)
				topics=[tmp]
				while eval("image"+question_topics[topics[0]]) in ['medium','NA'] or  quest_list[tmp] == 0:
					topics=[RANDOM.choice(question_topics_index)]
					
			elif language_sentence == 'all' or language_sentence == 'oneofeach':
				topics=[]
				for topic_index in question_topics_index:
					if eval("image"+question_topics[topic_index]) not in ['medium','NA']:
						topics.append(topic_index)	
			else:	
				print "ERROR: parameter language_sentence not valid (1)"
				sys.exit(0)
			
                        # We then choose one or several topics among the possible ones

			for quest in quest_list:
			        globals()[quest]=0
			for topic in topics:
				globals()[quest_list[topic]]=1				
			
                        # This ''hack'' would be to change...
                        if globals().has_key('hrzpos_quest'):
                                hrzpos_quest=globals()['hrzpos_quest']
                        else:
                                hrzpos_quest=0
                        if globals().has_key('vrtpos_quest'):
                                vrtpos_quest=globals()['vrtpos_quest']
                        else:
                                vrtpos_quest=0
                        if globals().has_key('shape_quest'):
                                shape_quest=globals()['shape_quest']
                        else:
                                shape_quest=0
                        if globals().has_key('color_quest'):
                                color_quest=globals()['color_quest']
                        else:
                                color_quest=0
                        if globals().has_key('size_quest'):
                                size_quest=globals()['size_quest']
                        else:
                                size_quest=0

# 			hrzpos_quest=globals()['hrzpos_quest']
# 			vrtpos_quest=globals()['vrtpos_quest']
# 			shape_quest=globals()['shape_quest']
# 			color_quest=globals()['color_quest']
# 			size_quest=globals()['size_quest']



	
			if vrtpos_quest == 1:
				text_one_quest = one_object_questions_location_vert(thedescr,adescr,theobj.get('vrtpos'))	
				printout_but_not_really(text_one_quest)	##########	
				
			if hrzpos_quest == 1:
				text_one_quest = one_object_questions_location_hor(thedescr,adescr,theobj.get('hrzpos'))	
				printout_but_not_really(text_one_quest)	##########	
				
			if color_quest == 1:
				text_one_quest = one_object_questions_color(theobj.get('color'),theobj.get('size'),theobj.get('shape'),theobj.get('vrtpos'),theobj.get('hrzpos'))				
				printout_but_not_really(text_one_quest)	##########	
				
			if shape_quest == 1:
				text_one_quest = one_object_questions_shape(theobj.get('color'),theobj.get('size'),theobj.get('shape'),theobj.get('vrtpos'),theobj.get('hrzpos'))
				printout_but_not_really(text_one_quest) ##########	

			if size_quest == 1:
				text_one_quest = one_object_questions_size(theobj.get('color'),theobj.get('size'),theobj.get('shape'),theobj.get('vrtpos'),theobj.get('hrzpos'))
				printout_but_not_really(text_one_quest)	##########			

		
  # FID_output.close() ##########

  return sentence_list ##########

        
#--------


def main(config_file):

  execfile(config_file,globals())


  # initiate scene parameters
  
  # the number of objects to describe; 
  # if language_objects == 0, then all objects from the image
  if language_objects == 0: number_objects_referedto = number_objects
  else: number_objects_referedto = language_objects


  # text format
  if language_form == 'question/answer' and language_question == None:
	print 'Inconsistent language parameters:'+ ' '+language_form+' '+ 'and'+ ' '+language_question
	raise endSearch
  if language_form == 'type_of_sentencement' and (language_question == 'color' or language_question == 'size' or
	language_question == 'shape' or language_question == 'location' or language_question == 'position'):
	print 'Inconsistent language parameters:'+ ' '+language_form+' '+ 'and question'+ ' '+language_question
	raise endSearch

  # the number of output sentences

  if language_sentence == 'one' or language_sentence == 'oneofeach': sentence = 1
  else: sentence = 0

  
  # If there are more than 1 object,
  # we will build the list of possible topics on a case by case (each pair of each image)
  #
  question_topics, quest_list = build_question_topics_one_objects()
  question_topics_index=range(len(question_topics))			
  
  
  FID_input  = open(input_file, "r")
  if isfile(output_file):
     print "STOP: "+output_file+" already exists, please remove it"
     sys.exit(0)
  FID_output = open(output_file,"w")

  globals()['sentence']         = sentence
  globals()['FID_output']       = FID_output
  
  RANDOM.seed(12345)
  
  i_image=0
  for line in FID_input:
  
        image = eval(line)
        globals()['image'] = image
  
        if language_sentence == 'all' or language_sentence == 'oneofeach':
        	printout(['\nImage '+str(i_image)+':'])
	print "Image "+str(i_image)
	i_image+=1

	# initialize 
	objects = []
	cl = []
      # shape 
	sh = []
      # vertical position on the screen
	vr = []
      # horizontal position on the screen
	hr = []
      # size
	sz = []
 	# matrix of relative positions from other objects 

	position = []
	
	
	# for random objects from the image


	# include or not background description
	if language_background == 0:
	   bc = ' '
	else:
	   bc = 'on' + ' ' + 'the' + ' ' + image['background']['color'] +'  screen'
	for i in range(number_objects):	
		cl.append(image['object_'+str(i)]['color'])
		sh.append(image['object_'+str(i)]['shape'])
		hr.append(image['object_'+str(i)]['hrzpos'])
		vr.append(image['object_'+str(i)]['vrtpos'])
        	sz.append(image['object_'+str(i)]['size'])  
                objects.append(image['object_'+str(i)])


	# for i in range(len(objects)):
	#	print objects[i]
	 
	# In the question, we refer to more than 2 objects...
	if number_objects_referedto > 1:
		
		print '2 objects amongst '+str(number_objects)
		
		index_pairs   = [[i,j] for i in range(number_objects) for j in range(0,i)+range(i+1,number_objects)]
		
		index_objects = range(number_objects)
		
		# The objects are chosen randomly in the *desc file,
		# so we do not need this kind of things:
		# (resolved bug)
		#
		# if language_sentence == 'one' or language_sentence == 'oneofeach':
		#	index_pairs = [RANDOM.choice(index_pairs)]
		
			
		for i_pair in index_pairs:
			
			# printout([str(i_pair[0])+ '+' +str(i_pair[1])])
			# print i_pair[0], i_pair[1]
			theobj = []
			
			theobj.append(objects[i_pair[0]])
			theobj.append(objects[i_pair[1]])
			
			same_color_other = [0,0]
			same_shape_other = [0,0]
			same_size_other = [0,0]
			same_abshrz_other = [0,0]
			same_absvrt_other = [0,0]
			same_relsize_other = [0,0]
			same_relhrzpos_other = [0,0]
			same_relvrtpos_other = [0,0]
			
			if number_objects > 2:
				others = []
			
				for i in range(len(objects)):
					if i != i_pair[0] and i != i_pair[1]:
						others.append(i)			
			
				same_relsize_other   = [0,0]
				same_relhrzpos_other = [0,0]
				same_relvrtpos_other = [0,0]
				
				
			
				# check whether there are other objects similar to the object in question
				#print hr[i_pair[0]]
				#print hr[i_pair[1]]
				
				for ob_other in others:
					
					if cl[i_pair[0]] == cl[ob_other]:
						same_color_other[0] = 1
					if sh[i_pair[0]] == sh[ob_other]:
						same_shape_other[0] = 1
					if sz[i_pair[0]] == sz[ob_other]:
						same_size_other[0] = 1
				
					if hr[i_pair[0]] == hr[ob_other]:	
						same_abshrz_other[0] = 1
					
					if vr[i_pair[0]] == vr[ob_other]:	
						same_absvrt_other[0] = 1
					# (resolved bug)
					same_relsize_other[0]   = max(same_relsize_other[0],compare_comparison(i_pair[0],i_pair[1],ob_other,i_pair[1],'size'))
					same_relhrzpos_other[0] = max(same_relhrzpos_other[0],compare_comparison(i_pair[0],i_pair[1],ob_other,i_pair[1],'hrzpos'))
					
					same_relvrtpos_other[0] = max(same_relvrtpos_other[0],compare_comparison(i_pair[0],i_pair[1],ob_other,i_pair[1],'vrtpos'))
					
					
				# check whether there are other objects similar to the object in comparison
				
				for ob_other in others:
					
					if cl[i_pair[1]] == cl[ob_other]:
						same_color_other[1] = 1
					if sh[i_pair[1]] == sh[ob_other]:
						same_shape_other[1] = 1
					if sz[i_pair[1]] == sz[ob_other]:
						same_size_other[1] = 1
					
					if hr[i_pair[1]] == hr[ob_other]:	
						same_abshrz_other[1] = 1
					
					if vr[i_pair[1]] == vr[ob_other]:	
						same_absvrt_other[1] = 1
					# (resolved bug)
					same_relsize_other[1]   = max(same_relsize_other[1],compare_comparison(i_pair[0],i_pair[1],ob_other,i_pair[1],'size'))
					same_relhrzpos_other[1] = max(same_relhrzpos_other[1],compare_comparison(i_pair[0],i_pair[1],ob_other,i_pair[1],'hrzpos'))
					same_relvrtpos_other[1] = max(same_relvrtpos_other[1],compare_comparison(i_pair[0],i_pair[1],ob_other,i_pair[1],'vrtpos'))
			
			# print same_abshrz_other
			# print same_absvrt_other
			#######################################################
			# Here we define all the topics we can talk about...
			# (taking into acount the config file AND the relevant topics for the scene)

			question_topics, quest_list = build_question_topics_several_objects(i_pair[0],i_pair[1])			
			question_topics_index=range(len(question_topics))			
			
			if language_sentence == 'one':
				only_one_question = 0	
		        	tmp=RANDOM.choice(question_topics_index)
				topics=[tmp]
				while eval("image"+question_topics[topics[0]]) == 'NA' or  quest_list[tmp] == 0:
					topics=[RANDOM.choice(question_topics_index)]
					
			elif language_sentence == 'all' or language_sentence == 'oneofeach':
				topics=[]
				only_one_question = 2
				for topic_index in question_topics_index:
					if eval("image"+question_topics[topic_index]) != 'NA':
						topics.append(topic_index)	
			else:	
				print "ERROR: parameter language_sentence not valid (1)"
				sys.exit(0)
			
                        # We then choose one or several topics among the possible ones

			for quest in quest_list:
			        globals()[quest]=0
			for topic in topics:
				globals()[quest_list[topic]]=1				
			
                        # This ''hack'' would be to change...
			hrzpos_quest=globals()['hrzpos_quest']
			vrtpos_quest=globals()['vrtpos_quest']
			shape_quest=globals()['shape_quest']
			color_quest=globals()['color_quest']
			size_quest=globals()['size_quest']
			
			#######################################################

											
		
			relsize = relative_size(i_pair[0],i_pair[1],image)
								
			relposition_vert =  relative_position_vert(i_pair[0],i_pair[1],image)	
			
			relposition_hor =  relative_position_hor(i_pair[0],i_pair[1],image)	
			
			relpos_hor_ans1 = relative_position_hor_ans(i_pair[0],i_pair[1],image)
							
			if theobj[0].get('shape') != theobj[1].get('shape') and same_shape_other[0] == 0 and same_shape_other[1] == 0:
				adescr1 = an_object(theobj[0].get('shape'),theobj[0].get('color'),theobj[0].get('size'))		
				adescr2 = an_object(theobj[1].get('shape'),theobj[1].get('color'),theobj[1].get('size'))
				thedescr1 = the_object(theobj[0].get('shape'),theobj[0].get('color'),theobj[0].get('size'))		
				thedescr2 = the_object(theobj[1].get('shape'),theobj[1].get('color'),theobj[1].get('size'))
			elif (theobj[0].get('shape') == theobj[1].get('shape') or same_shape_other[0] != 0 or same_shape_other[1] != 0) and (theobj[0].get('color') != theobj[1].get('color') and same_color_other[0] == 0 and same_color_other[1] == 0):
 				adescr1 = an_object_sameShape(theobj[0].get('shape'),theobj[0].get('color'),theobj[0].get('size'))	
				adescr2 = an_object_sameShape(theobj[1].get('shape'),theobj[1].get('color'),theobj[1].get('size'))
				thedescr1 = the_object_sameShape(theobj[0].get('shape'),theobj[0].get('color'),theobj[0].get('size'))	
				thedescr2 = the_object_sameShape(theobj[1].get('shape'),theobj[1].get('color'),theobj[1].get('size'))
			else:  # there are similar shapes and color
				adescr1 = an_object_sameShapeColor(theobj[0].get('shape'),theobj[0].get('color'),theobj[0].get('size'))	
				adescr2 = an_object_sameShapeColor(theobj[1].get('shape'),theobj[1].get('color'),theobj[1].get('size'))
				thedescr1 = the_object_sameShapeColor(theobj[0].get('shape'),theobj[0].get('color'),theobj[0].get('size'))	
				thedescr2 = the_object_sameShapeColor(theobj[1].get('shape'),theobj[1].get('color'),theobj[1].get('size'))
					
			
			
			# Determine the absolute position of the first object
			# (It is 'in the middle' if it is not on the right/left neither on the top/bottom)
			
			absolute_position = ['NA','NA']
			for i in [0,1]:
				if theobj[0].get('hrzpos')==theobj[1].get('hrzpos'):
					same_abshrz_other[i] = 1
				if theobj[0].get('vrtpos')==theobj[1].get('vrtpos'):
					same_absvrt_other[i] = 1

			for i in [0,1]:
				if same_abshrz_other[i] == 0 and same_absvrt_other[i] == 0:
					if theobj[i].get('hrzpos')=='NA':
						if theobj[i].get('vrtpos')=='NA':
			      				absolute_position[i] = 'in the middle'
						else:
			      				absolute_position[i] = abs_position_vert(theobj[i].get('vrtpos'))
					elif theobj[i].get('vrtpos')=='NA':
			   			absolute_position[i] = abs_position_hor(theobj[i].get('hrzpos'))
					else:
			   			absolute_position[i] = RANDOM.choice([abs_position_vert(theobj[i].get('vrtpos')),abs_position_hor(theobj[i].get('hrzpos'))])
				elif same_abshrz_other[i] == 0 and same_absvrt_other[i] == 1:
					if theobj[i].get('hrzpos')!='NA':
						absolute_position[i] = abs_position_hor(theobj[i].get('hrzpos'))	
				elif same_abshrz_other[i] == 1 and same_absvrt_other[i] == 0:	
					if theobj[i].get('vrtpos')!='NA':		 
			      			absolute_position[i] = abs_position_vert(theobj[i].get('vrtpos'))
					
			
			# summarize  differences
			
			diff = [1,1]
			
			if (same_color_other[0] == 1 and same_shape_other[0] == 1 and same_size_other[0] == 1): 
				diff[0] = 0 
					 
			if (same_color_other[1] == 1 and same_shape_other[1] == 1 and same_size_other[1] == 1):
				diff[1] = 0	
			
			if ((theobj[0].get('shape') == theobj[1].get('shape') and  theobj[0].get('color') == theobj[1].get('color')) and (theobj[0].get('size') == theobj[1].get('size') or theobj[0].get('size') == 'medium' or theobj[1].get('size') == 'medum')  ):
				vrtpos_quest = 0
				hrzpos_quest = 0
				
			if (size_quest == 1 and theobj[0].get('shape') == theobj[1].get('shape') and  theobj[0].get('color') == theobj[1].get('color')):
				relposition_hor = 'NA'
				relposition_vert = 'NA'
				
			if diff[1] == 0:
				relposition_hor = 'NA'
				relposition_vert = 'NA'
				size_quest == 0
				
			# allowed questions	
			if same_relhrzpos_other[0] == 0:
				if color_quest == 1:
					if relposition_hor != 'NA':
						text_two_color = two_objects_questions_color(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,relposition_hor)
						printout(text_two_color)
						if only_one_question == 0: break
					elif absolute_position[0] != 'NA':
						text_two_color = two_objects_questions_color_abspos(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,absolute_position[0])
						printout(text_two_color)
						if only_one_question == 0: break
				if shape_quest == 1: 
					if relposition_hor != 'NA':
						text_two_shape = two_objects_questions_shape(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,relposition_hor)
						printout(text_two_shape)
						if only_one_question == 0: break
					elif absolute_position[0] != 'NA':
						text_two_shape = two_objects_questions_shape_abspos(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,absolute_position[0])		
						printout(text_two_shape)
						if only_one_question == 0: break	
				if size_quest == 1:
					if relposition_hor != 'NA':
						text_two_size = two_objects_questions_size(theobj[0].get('color'),theobj[0].get('shape'),theobj[1].get('color'),theobj[1].get('shape'),relposition_hor,relsize)
						printout(text_two_size)	
						if only_one_question == 0: break
					elif absolute_position[0] != 'NA':
						text_two_size = two_objects_questions_size_abspos(theobj[0].get('color'),theobj[0].get('shape'),theobj[1].get('color'),theobj[1].get('shape'),absolute_position[0],relsize)
						printout(text_two_size)	
						if only_one_question == 0: break
								
			if same_relvrtpos_other[0] == 0:
				if color_quest == 1:				
					if relposition_vert != 'NA':	
						text_two_color= two_objects_questions_color(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,relposition_vert)			
						printout(text_two_color)
						if only_one_question == 0: break
					elif absolute_position[0] != 'NA':
						text_two_color = two_objects_questions_color_abspos(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,absolute_position[0])
						printout(text_two_color)
						if only_one_question == 0: break				
				if shape_quest == 1:	
					if relposition_vert != 'NA':
						text_two_shape = two_objects_questions_shape(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,relposition_vert)			
						printout(text_two_shape)
						if only_one_question == 0: break	
					elif absolute_position[0] != 'NA':
						text_two_shape = two_objects_questions_shape_abspos(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,absolute_position[0])	
						printout(text_two_shape)
						if only_one_question == 0: break	
				if size_quest == 1:
					if relposition_vert != 'NA':
						text_two_size = two_objects_questions_size(theobj[0].get('color'),theobj[0].get('shape'),theobj[1].get('color'),theobj[1].get('shape'),relposition_vert,relsize)
						printout(text_two_size)
						if only_one_question == 0: break
					elif absolute_position[0] != 'NA':
						text_two_size = two_objects_questions_size_abspos(theobj[0].get('color'),theobj[0].get('shape'),theobj[1].get('color'),theobj[1].get('shape'),absolute_position[0],relsize)
						printout(text_two_size)	
						if only_one_question == 0: break
						
			# some questions on colour, shape, size are not permitted
				
			if same_relhrzpos_other[0] == 1 or same_relvrtpos_other[0] == 1:	
				if color_quest == 1:
					if relposition_hor != 'NA' and same_relhrzpos_other[0] == 0:	
						text_two_color = two_objects_questions_color_sameLocationShape(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,relposition_hor)
						printout(text_two_color)
						if only_one_question == 0: break			
					elif relposition_vert != 'NA' and same_relvrtpos_other[0] == 0:
						text_two_color= two_objects_questions_color_sameLocationShape(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,relposition_vert)	
						printout(text_two_color)	
						if only_one_question == 0: break	
					elif absolute_position[0] != 'NA':
						text_two_color = two_objects_questions_color_abspos(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,absolute_position[0])
						printout(text_two_color)
						if only_one_question == 0: break	
				if size_quest == 1:
					if relposition_hor != 'NA' and same_relhrzpos_other[0] == 0:
						text_two_size = two_objects_questions_size(theobj[0].get('color'),theobj[0].get('shape'),theobj[1].get('color'),theobj[1].get('shape'),relposition_hor,relsize)
						printout(text_two_size)
						if only_one_question == 0: break	
					elif relposition_vert != 'NA' and same_relvrtpos_other[0] == 0:
						text_two_size = two_objects_questions_size(theobj[0].get('color'),theobj[0].get('shape'),theobj[1].get('color'),theobj[1].get('shape'),relposition_vert,relsize)
						printout(text_two_size)
						if only_one_question == 0: break
					elif absolute_position[0] != 'NA':
						text_two_size = two_objects_questions_size_abspos(theobj[0].get('color'),theobj[0].get('shape'),theobj[1].get('color'),theobj[1].get('shape'),absolute_position[0],relsize)
						printout(text_two_size)
						if only_one_question == 0: break	
				if shape_quest == 1:	
					if relposition_hor != 'NA' and same_relhrzpos_other[0] == 0:
						text_two_shape = two_objects_questions_shape_sameLocation(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,relposition_hor)	
						printout(text_two_shape)
						if only_one_question == 0: break	
					elif relposition_vert != 'NA' and same_relvrtpos_other[0] == 0:
						text_two_shape = two_objects_questions_shape_sameLocation(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,relposition_vert)	
						printout(text_two_shape)
						if only_one_question == 0: break
					elif absolute_position[0] != 'NA':
						text_two_shape = two_objects_questions_shape_abspos(theobj[0].get('color'),theobj[0].get('size'),theobj[0].get('shape'),adescr2,thedescr2,absolute_position[0])	
						printout(text_two_shape)
						if only_one_question == 0: break		
	
			
				
			if vrtpos_quest == 1 and relposition_vert != 'NA':
				if same_abshrz_other[0] == 0 and theobj[0].get('hrzpos') != 'NA' and diff[0] ==0 and diff[1] == 0: 
						text_two_location_vert = two_objects_questions_location_vert_abs(adescr1,thedescr1,adescr2,thedescr2,relposition_vert,abs_position_hor(theobj[0].get('hrzpos')))
						printout(text_two_location_vert)
						if only_one_question == 0: break
				elif (diff[0] ==1 and diff[1] ==1):
						text_two_location_vert = two_objects_questions_location_vert(adescr1,thedescr1,adescr2,thedescr2,relposition_vert)
						printout(text_two_location_vert)
						if only_one_question == 0: break
					
			if hrzpos_quest == 1 and relposition_hor != 'NA':		
				if same_absvrt_other[0] == 0 and theobj[0].get('vrtpos') != 'NA' and diff[0] ==0 and diff[1] == 0:
						text_two_location_hor = two_objects_questions_location_hor_abs(adescr1,thedescr1,adescr2,thedescr2,relpos_hor_ans1,abs_position_vert(theobj[0].get('vrtpos')))
						printout(text_two_location_hor)
						if only_one_question == 0: break
				elif (diff[0] ==1 and diff[1] ==1):
						text_two_location_hor = two_objects_questions_location_hor(adescr1,thedescr1,adescr2,thedescr2,relpos_hor_ans1)
						printout(text_two_location_hor)
						if only_one_question == 0: break
			
			# if other questions fail:
			if same_shape_other[0] == 0 and theobj[0].get('shape') != theobj[1].get('shape'):
				text_one_color_no_location = one_object_questions_color_no_location(theobj[0].get('color'),theobj[0].get('shape'))
				printout(text_one_color_no_location)
				if only_one_question == 0: break
			elif same_color_other[0] == 0 and theobj[0].get('color') != theobj[1].get('color'):
				text_one_size_no_location = one_object_questions_shape_no_location(theobj[0].get('color'),theobj[0].get('shape'))
				printout(text_one_size_no_location)
				if only_one_question == 0: break
			elif (same_shape_other[0] == 1 and theobj[0].get('shape') == theobj[1].get('shape') and same_shape_other[1] == 1):
				text_one_same_shape = one_object_questions_same_shape(theobj[0].get('shape'))
				printout(text_one_same_shape)
				if only_one_question == 0: break
			elif (same_color_other[0] == 1 and theobj[0].get('color') == theobj[1].get('color') and same_color_other[0] == 1):
				text_one_same_color = one_object_questions_same_color(theobj[0].get('color'))
				printout(text_one_same_color)
				if only_one_question == 0: break	
			
	if number_objects_referedto==1:
		
		
                # Deprecated !!!!!!!!!
                if language_form == 'statement':

#			print '1'+' '+'object'
			theobj = RANDOM.choice(objects)		
			theobj['size'] = redundant_medium(theobj['size'])
			thedescr = an_object(theobj.get('shape'),theobj.get('color'),theobj.get('size'))		
			text_one = one_object(thedescr,theobj['vrtpos'],theobj['hrzpos'])
			printout(text_one)
			if theobj.get('size') == '': theobj['size'] = 'medium'
			text_part = object_partial(theobj.get('shape'),theobj.get('color'),theobj.get('size'))
			printout(text_part)
			
			
		elif language_form == 'question/answer':


#			print '1'+' '+'object'	
			theobj = objects[0]	
			adescr = an_object(theobj.get('shape'),theobj.get('color'),theobj.get('size'))
			thedescr = the_object(theobj.get('shape'),theobj.get('color'),theobj.get('size'))

                        if 'medium' in thedescr:
			   print theobj
			   sys.exit(0)

			if language_sentence == 'one':
		        	tmp=RANDOM.choice(question_topics_index)
				topics=[tmp]
				while eval("image"+question_topics[topics[0]]) in ['medium','NA'] or  quest_list[tmp] == 0:
					topics=[RANDOM.choice(question_topics_index)]
					
			elif language_sentence == 'all' or language_sentence == 'oneofeach':
				topics=[]
				for topic_index in question_topics_index:
					if eval("image"+question_topics[topic_index]) not in ['medium','NA']:
						topics.append(topic_index)	
			else:	
				print "ERROR: parameter language_sentence not valid (1)"
				sys.exit(0)
			
                        # We then choose one or several topics among the possible ones

			for quest in quest_list:
			        globals()[quest]=0
			for topic in topics:
				globals()[quest_list[topic]]=1				
			
                        # This ''hack'' would be to change...
			hrzpos_quest=globals()['hrzpos_quest']
			vrtpos_quest=globals()['vrtpos_quest']
			shape_quest=globals()['shape_quest']
			color_quest=globals()['color_quest']
			size_quest=globals()['size_quest']



	
			if vrtpos_quest == 1:
				text_one_quest = one_object_questions_location_vert(thedescr,adescr,theobj.get('vrtpos'))	
				printout(text_one_quest)				
				
			if hrzpos_quest == 1:
				text_one_quest = one_object_questions_location_hor(thedescr,adescr,theobj.get('hrzpos'))	
				printout(text_one_quest)				
				
			if color_quest == 1:
				text_one_quest = one_object_questions_color(theobj.get('color'),theobj.get('size'),theobj.get('shape'),theobj.get('vrtpos'),theobj.get('hrzpos'))				
				printout(text_one_quest)				
				
			if shape_quest == 1:
				text_one_quest = one_object_questions_shape(theobj.get('color'),theobj.get('size'),theobj.get('shape'),theobj.get('vrtpos'),theobj.get('hrzpos'))
				printout(text_one_quest)				

			if size_quest == 1:
				text_one_quest = one_object_questions_size(theobj.get('color'),theobj.get('size'),theobj.get('shape'),theobj.get('vrtpos'),theobj.get('hrzpos'))
				printout(text_one_quest)				

		
  FID_output.close()

def man():
    print "Usage : " + sys.argv[0] + " <config file>"
    sys.exit(0)


if __name__ == '__main__':
    
    if len(sys.argv) < 2:
       WORKDIR=dirname(sys.argv[0])
       if len(WORKDIR) > 0:
          WORKDIR=WORKDIR+'/'
       config_file=WORKDIR+'grammar_v3_config.py'
    elif len(sys.argv) == 2:
       config_file=sys.argv[1]
    else :
       man()
    if isfile(config_file)==False:
       print "ERROR : cannot find " + config_file
       print 
       man()
    
    main(config_file)
