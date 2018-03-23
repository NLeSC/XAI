#!/usr/local/bin/python

# builds sets of templates

from random import Random


#++++++++
RANDOM = Random()
# related changes: s/random/RANDOM/
# reason: different modules should use different random number generators so they don't step on each others' toes
#--------


################################################################################################################


# Semantic Knowledge (Vocabulary)

# Hierarchical relations, including
 
 # "is-a" 
 
vowels = 'aeiou'

VERB = ['is','are','Is','Are']

NEGATION = 'not'

article = 'a'

# references

DETERMIN = ['the','There','The','this'] 

PRONOUN = ['it','they','its','It','their']

# Spacial relations, including 

# positionAt

spacePREPOSITION = ['on','of','in','at']

# Clause relations, including

# CONJUNCTIONs

CONJUNCTION = ['and','with']

# DISJUNCTION

DISJUNCTION = ['or','than']

# Temporal relations, including

# precedence

timePREPOSITION = ['before','after']

# Measure relations, including

# cardinal numbers (upto the number of objects)

CARDINAL = ['one','two','tree']

# ordinal numbers (counting the number of objects)

ORDINAL = ['first','second','third']

COMPSIZE = ['smaller','bigger']

# lists of positions

vertical = ['top','bottom']

horizontal = ['left','right']

##############################################################################################################

# Production RUles for Object description
	
	# randomized description of an object
def the_object(shape,color,size):
	#1. a shape
	#2. a color shape
	#3. a size color shape	
	if size.rstrip() in ['medium','NA']: size = ''
		
	description = [DETERMIN[0] + ' ' +shape, DETERMIN[0] +' '+color +' '+ shape, DETERMIN[0] +' '+ size+ ' '+color +' '+ shape]
	
	return RANDOM.choice(description)

def the_object_sameShape(shape,color,size):
	#1. a shape
	#2. a color shape
	#3. a size color shape	
	if size.rstrip() in ['medium','NA']: size = ''

		
	description = [DETERMIN[0] +' '+color +' '+ shape, DETERMIN[0] +' '+ size+ ' '+color +' '+ shape]
	
	return RANDOM.choice(description)

def the_object_sameShapeColor(shape,color,size):
	#1. a shape
	#2. a color shape
	#3. a size color shape	
	if size.rstrip() in ['medium','NA']: size = ''

		
	return DETERMIN[0] +' '+ size+ ' '+color +' '+ shape
	

def an_object(shape,color,size):
	#1. a shape
	#2. a color shape
	#3. a size color shape	
	if size.rstrip() in ['medium','NA']: size = ''

	article0 = choose_article(shape)
	
	article1 = choose_article(color)
	
	article2 = choose_article(size)
		
	if size == '': article2 = choose_article(shape)
			
	description = [article0 + ' ' +shape, article1 +' '+color +' '+ shape, article2 +' '+ size+ ' '+ shape]
	
	return RANDOM.choice(description)

def an_object_sameShape(shape,color,size):
	#1. a shape
	#2. a color shape
	#3. a size color shape	
	if size.rstrip() in ['medium','NA']: size = ''

	article1 = choose_article(color)
	
	article2 = choose_article(size)
		
	if size == '': article2 = choose_article(color)
			
	description = [article1 +' '+color +' '+ shape, article2 +' '+ size+ ' '+ color+ ' '+ shape]
	
	return RANDOM.choice(description)

def an_object_sameShapeColor(shape,color,size):
	#1. a shape
	#2. a color shape
	#3. a size color shape	
	if size.rstrip() in ['medium','NA']: size = ''

	article2 = choose_article(size)
		
	if size == '': article2 = choose_article(color)
			
	return article2 +' '+ size+ ' '+ color+ ' '+ shape
		
def choose_article(word):
	if len(word)==0:
	   return "MISSING"
	article = 'a'
	if word.replace(" ","")[0] in vowels: article = 'an'
	return article


#####################################################################################################################
#Questions for one object, WITHOUT reference to other objects on a screen


def one_object_questions_location_vert(obj,obj1,vr): 
     

        questionOut = [ DETERMIN[1]+ ' '+ VERB[0]+ ' '+ obj1 + '. '+  VERB[2] +' '+ PRONOUN[0] + ' '  + spacePREPOSITION[3] + ' ' + DETERMIN[0]+ ' ' + vertical[0] + ' '+DISJUNCTION[0]+' '+DETERMIN[0]+ ' '+ vertical[1]+'?'+' '+vr,
	DETERMIN[1]+ ' '+ VERB[0]+ ' '+ obj1 + '. '+  VERB[2] +' '+ PRONOUN[0] + ' '  + 'more to' + ' '+ DETERMIN[0]+ ' ' + vertical[0] + ' '+DISJUNCTION[0]+' '+DETERMIN[0]+ ' '+ vertical[1]+'?'+' '+vr,	
         VERB[2] +' '+ obj + ' ' + spacePREPOSITION[3] + ' ' +  DETERMIN[0]+ ' ' + vertical[0] + ' '+DISJUNCTION[0]+' '+ DETERMIN[0]+ ' '+vertical[1]+'?'+' '+vr,	
	 VERB[2] +' '+ obj + ' ' + 'more' + ' '+'to'+ ' ' +  DETERMIN[0]+ ' ' + vertical[0] + ' '+DISJUNCTION[0]+' '+ DETERMIN[0]+ ' '+vertical[1]+'?'+' '+vr, 
         VERB[2] +  ' '+ obj +' '+ spacePREPOSITION[3] +' ' + DETERMIN[0]+ ' '+ vertical[0] + ' '+ DISJUNCTION[0]+ ' ' + DETERMIN[0]+' '+vertical[1]+'?'+' '+vr,
	 'Where' + ' '+ VERB[0]+ ' '+ obj+','+' '+'more'+ ' '+'to'+ ' '+ DETERMIN[0]+' '+vertical[0] + ' '+DISJUNCTION[0]+' '+DETERMIN[0]+ ' '+ vertical[1]+'?'+' '+vr,
	 'Where' + ' '+ VERB[0]+ ' '+ obj+','+' '+'closer'+ ' '+'to'+ ' '+ DETERMIN[0]+' '+vertical[0] + ' '+DISJUNCTION[0]+' '+DETERMIN[0]+ ' '+ vertical[1]+'?'+' '+vr,
	 'Where' + ' '+ VERB[0]+ ' '+ obj+'?'+' '+VERB[2] +' '+ 'it' + ' '  + 'more to' + ' ' + DETERMIN[0]+ ' ' + vertical[0] + ' '+DISJUNCTION[0]+' '+DETERMIN[0]+ ' '+ vertical[1]+'?'+' '+vr,
	 'Where' + ' '+ VERB[0]+ ' '+ obj+'?'+ ' ' + VERB[2] +' '+ 'it' + ' '  + 'closer' + ' '+'to'+' ' + DETERMIN[0]+ ' ' + vertical[0] + ' '+DISJUNCTION[0]+' '+DETERMIN[0]+ ' '+ vertical[1]+'?'+' '+vr]
		
	return questionOut 

def one_object_location_answer_vert(obj,vert):	
	return obj +' '+ VERB[0]+' '+spacePREPOSITION[3]+' '+DETERMIN[0]+' '+vert
	

def one_object_questions_location_hor(obj,obj1,hr): 
      # templates 
      # 1. There is a color shape. Is it in the top or the bottom?
      #2 There is a size color shape. It is at the top or the bottom?     
      #3. Is an object in the top or bottom?

        questionOut = [ DETERMIN[1]+ ' '+ VERB[0]+ ' '+ obj1 + '. '+  VERB[2] +' '+ 'it' + ' '  + ' '+ spacePREPOSITION[3] + ' ' + 
         DETERMIN[0]+ ' ' + horizontal[0] + ' '+DISJUNCTION[0]+ ' ' + DETERMIN[0]+' '+horizontal[1]+'?'+' '+hr,
	 DETERMIN[1]+ ' '+ VERB[0]+ ' '+ obj1 + '. '+  VERB[2] +' '+ 'it' + ' '  + ' ' + 'closer' + ' '+'to'+ ' ' +  DETERMIN[0]+ ' ' + horizontal[0] + ' '+DISJUNCTION[0]+ ' ' + DETERMIN[0]+' '+horizontal[1]+'?'+' '+hr,	  
	 VERB[2] + ' '+ obj +' '+ spacePREPOSITION[3] + ' ' + DETERMIN[0]+' ' + horizontal[0] + ' '+ DISJUNCTION[0]+ ' ' + DETERMIN[0]+' '+horizontal[1]+'?'+' '+hr,
	 VERB[2] + ' '+ obj +' '+ 'closer' + ' '+'to'+ ' ' + DETERMIN[0]+' ' + horizontal[0] + ' '+ DISJUNCTION[0]+ ' ' + DETERMIN[0]+' '+horizontal[1]+'?'+' '+hr,
	 'Where' + ' '+ VERB[0]+ ' '+ obj+','+' '+'more'+ ' '+'to'+ ' '+ DETERMIN[0]+' '+horizontal[0] + ' '+DISJUNCTION[0]+' '+DETERMIN[0]+ ' '+ horizontal[1]+'?'+' '+hr,
	 'Where' + ' '+ VERB[0]+ ' '+ obj+'? '+VERB[2] +' '+ PRONOUN[0] + ' '  + ' '+ 'more to' + ' ' +  DETERMIN[0]+ ' ' + horizontal[0] + ' '+DISJUNCTION[0]+ ' ' + DETERMIN[0]+' '+horizontal[1]+'?'+' '+hr,
	 'Where' + ' '+ VERB[0]+ ' '+ obj+','+  'closer' + ' '+'to'+ ' ' + DETERMIN[0]+ ' ' + horizontal[0] + ' '+DISJUNCTION[0]+ ' ' + DETERMIN[0]+' '+horizontal[1]+'?'+' '+hr]
		
	return questionOut 

def one_object_location_answer_hor(obj,hor):	
	return obj +' '+ VERB[0]+' '+spacePREPOSITION[3]+' '+DETERMIN[0]+' '+hor
	


def one_object_questions_shape(cl,sz,sh,v,w): 

   #6. A color object is in hor vert. What is its shape?
   #7. Is an object in the top or bottom?     
   article= choose_article(cl)

   if sz in ['medium','NA']: sz=''


   if v == 'NA' and w == 'NA':
			
        sentenceOut = ['What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'shape'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' '  + cl +' '+ 'object' +'?'+' '+sh,
	'What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'shape'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' '  + ' '+ sz+ ' '+ cl +' '+ 'object' +'?'+' '+sh,
	'What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'shape'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' '  + cl +' '+ 'object' +'?'+' '+sh,
	'What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'shape'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' '  + ' '+ sz+ ' '+ cl +' '+ 'object'+'?'+' '+sh,		 
	 DETERMIN[1]+' '+ VERB[0]+' ' + article +' '+cl+' '+'object'+ '. '+ ' '+'What'+' '+VERB[0]+' '+PRONOUN[2]+' '+'shape' +'?'+' '+sh,
	 DETERMIN[1]+' '+ VERB[0]+' ' + article +' '+cl+' '+'object'+ '. '+ ' '+'What'+' '+'shape'+' '+ VERB[0]+' '+PRONOUN[0] +'?'+' '+sh]

   else:
	if v == 'NA': v=''
	if w == 'NA': w=''
        sentenceOut = ['What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'shape'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' '  + cl +' '+ 'object' + ' ' + spacePREPOSITION[3] + ' '+ DETERMIN[0]+ ' ' + v + ' '+ w +'?'+' '+sh,
	'What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'shape'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' '  + ' '+ sz+ ' '+ cl +' '+ 'object' + ' ' + spacePREPOSITION[3] + ' '+ DETERMIN[0]+ ' ' + v + ' '+ w+'?'+' '+sh,
	'What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'shape'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' '  + cl +' '+ 'object' +'?'+' '+sh,
	'What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'shape'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' '  + ' '+ sz+ ' '+ cl +' '+ 'object'+'?'+' '+sh,		 
	 DETERMIN[1]+' '+ VERB[0]+' ' + article +' '+cl+' '+'object'+ '. '+ ' '+'What'+' '+VERB[0]+' '+PRONOUN[2]+' '+'shape' +'?'+' '+sh,
	 DETERMIN[1]+' '+ VERB[0]+' ' + article +' '+cl+' '+'object'+ '. '+ ' '+'What'+' '+'shape'+' '+ VERB[0]+' '+PRONOUN[0] +'?'+' '+sh]
		
   return sentenceOut 


def one_object_questions_size(cl,sz,sh,v,w): 

   #6. A color object is in hor vert. What is its shape?
   #7. Is an object in the top or bottom?     
   article= choose_article(cl)
	
   if v == 'NA' and w == 'NA':
			
        sentenceOut = ['What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'size'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' '  + cl +' '+ 'object' +'?'+' '+sz,
	'What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'size'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' '  + ' '+ cl +' '+ sh +'?'+' '+sz,
	'What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'size'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' '  + cl +' '+ 'object' +'?'+' '+sz,
	'What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'size'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' '  + ' '+ cl +' '+ sh +'?'+' '+sz,
	 DETERMIN[1]+' '+ VERB[0]+' ' + article +' '+cl+' '+'object'+ '. '+ ' '+'What'+' '+VERB[0]+' '+PRONOUN[2]+' '+'size' +'?'+' '+sz,
	 DETERMIN[1]+' '+ VERB[0]+' ' + article +' '+cl+' '+'object'+ '. '+ ' '+'What'+' '+'size'+' '+ VERB[0]+' '+PRONOUN[0] +'?'+' '+sz]

   else:
	if v == 'NA': v=''
	if w == 'NA': w=''

        sentenceOut = ['What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'size'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' '  + cl +' '+ 'object' + ' ' + spacePREPOSITION[3] + ' '+ DETERMIN[0]+ ' ' + v + ' '+ w +'?'+' '+sz,
	'What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'size'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+ ' '+ cl +' '+ sh  + ' ' + spacePREPOSITION[3] + ' '+ DETERMIN[0]+ ' ' + v + ' '+ w+'?'+' '+sz,
	'What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'size'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' '  + cl +' '+ 'object' +'?'+' '+sz,
	'What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'size'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' '  + ' '+ cl +' '+ sh +'?'+' '+sz,
	 DETERMIN[1]+' '+ VERB[0]+' ' + article +' '+cl+' '+'object'+ '. '+ ' '+'What'+' '+VERB[0]+' '+PRONOUN[2]+' '+'size' +'?'+' '+sz,
	 DETERMIN[1]+' '+ VERB[0]+' ' + article +' '+cl+' '+'object'+ '. '+ ' '+'What'+' '+'size'+' '+ VERB[0]+' '+PRONOUN[0] +'?'+' '+sz]

		
   return sentenceOut 



def one_object_questions_color(cl,sz,sh,v,w): 
      # templates 

      # 3. A shape is in the horisontal vertical. What is its color?
      #4. A shape is in the horisontal vertical. Is it color or non-color?
      #5. A shape is in the horisontal vertical. Is this color or non-color color?     

	if sz in ['medium','NA']:
	
            article1 = choose_article(sh)
		
       	    if v == 'NA' and w == 'NA':
        	sentenceOut = [ 'What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'color'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' '  + sh +'?'+' '+cl,
			DETERMIN[1]+' '+ VERB[0]+' an  object'+ '. '+ ' '+'What'+' '+VERB[0]+' '+PRONOUN[2]+' '+'color' +'?'+' '+cl,
	 		DETERMIN[1]+' '+ VERB[0]+' ' + article1 +' '+sh +'.'+ ' '+'What'+' '+'color'+' '+VERB[0]+' '+PRONOUN[0] +'?'+' '+cl, 
	 		'What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'color'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' '+ sh +'?'+' '+cl]

            else:
          	if v == 'NA': v=''
	        if w == 'NA': w=''
        	sentenceOut = [ 'What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'color'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' '  + sh + ' ' + 'more to' + ' '+ DETERMIN[0]+ ' ' + v + ' '+ w+'?'+' '+cl,
			DETERMIN[1]+' '+ VERB[0]+' an  object'+ '. '+ ' '+'What'+' '+VERB[0]+' '+PRONOUN[2]+' '+'color' +'?'+' '+cl,
	 		DETERMIN[1]+' '+ VERB[0]+' ' + article1 +' '+sh + ' ' + spacePREPOSITION[3] + ' '+ DETERMIN[0]+ ' ' + v + ' '+ w+'.'+ ' '+'What'+' '+'color'+' '+VERB[0]+' '+PRONOUN[0] +'?'+' '+cl, 
	 		'What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'color'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' '+ sh + ' ' + spacePREPOSITION[3] + ' '+ DETERMIN[0]+ ' ' + v + ' '+ w+'?'+' '+cl]
			
	else:

  	    article = choose_article(sz)	
   	    article1 = choose_article(sh)
		  
       	    if v == 'NA' and w == 'NA':
        	sentenceOut = [ 'What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'color'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' '  + sh +'?'+' '+cl,
			DETERMIN[1]+' '+ VERB[0]+' ' + article +' '+ sz +' '+'object'+ '. '+ ' '+'What'+' '+VERB[0]+' '+PRONOUN[2]+' '+'color' +'?'+' '+cl,
	 		DETERMIN[1]+' '+ VERB[0]+' ' + article1 +' '+sh + '.'+ ' '+'What'+' '+'color'+' '+VERB[0]+' '+PRONOUN[0] +'?'+' '+cl, 
	 		'What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'color'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' '  +sz+' '+ sh + '?'+' '+cl]

            else:
          	if v == 'NA': v=''
	        if w == 'NA': w=''
        	sentenceOut = [ 'What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'color'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' '  + sh + ' ' + 'more to' + ' '+ DETERMIN[0]+ ' ' + v + ' '+ w+'?'+' '+cl,
			DETERMIN[1]+' '+ VERB[0]+' ' + article +' '+ sz +' '+'object'+ '. '+ ' '+'What'+' '+VERB[0]+' '+PRONOUN[2]+' '+'color' +'?'+' '+cl,
	 		DETERMIN[1]+' '+ VERB[0]+' ' + article1 +' '+sh + ' ' + spacePREPOSITION[3] + ' '+ DETERMIN[0]+ ' ' + v + ' '+ w+'.'+ ' '+'What'+' '+'color'+' '+VERB[0]+' '+PRONOUN[0] +'?'+' '+cl, 
	 		'What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'color'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' '  +sz+' '+ sh + ' ' + spacePREPOSITION[3] + ' '+ DETERMIN[0]+ ' ' + v + ' '+ w+'?'+' '+cl]

		
	return sentenceOut 





#######################################################################################################
# Questions for two objects


def two_objects_questions_color(cl1,sz1,sh1,obj2,obj2t,relposition): 
	 
        article = choose_article(sh1)
	
	if sz1 in ['medium','NA']: sz1 = ''
	
        sentenceOut = ['What' + ' ' + VERB[0] + ' ' + DETERMIN[0] + ' ' + 'color' + ' ' + spacePREPOSITION[1] + ' ' + DETERMIN[0] + ' '+ sh1 + ' ' +relposition + ' ' + obj2t + '?' + ' '+ cl1, 
	'What' + ' ' + VERB[0] + ' ' + DETERMIN[0] + ' ' + 'color' + ' ' + spacePREPOSITION[1] + ' ' + DETERMIN[0] + ' '+ sz1 + ' ' + sh1 + ' ' +relposition + ' ' + obj2t + '?' + ' '+ cl1, 
	DETERMIN[1] + ' ' +VERB[0] +' '+ article +' '+ sh1 + ' ' + relposition + ' '+ obj2 +'.'+' '+ 'What'+' '+'color'+' '+ VERB[0] + ' ' + PRONOUN[0] + '?'+' ' +cl1, 
	DETERMIN[1] + ' ' +VERB[0]+' '+ 'an' +' ' + 'object' + ' ' + relposition + ' '+ obj2 + '.' + ' ' + 'What' + ' ' + VERB[0] + ' ' + PRONOUN[2] + ' ' + 'color' +  '?' + ' ' + cl1]
	
		
	return sentenceOut 

def two_objects_questions_color_sameLocation(cl1,sz1,sh1,obj2,obj2t,relposition): 
     
        article = choose_article(sh1)
	
	if sz1 in ['medium','NA']: sz1 = ''
	
        sentenceOut = ['What' + ' ' + VERB[0] + ' ' + DETERMIN[0] + ' ' + 'color' + ' ' + spacePREPOSITION[1] + ' ' + DETERMIN[0] + ' '+ sh1 + ' ' +relposition + ' ' + obj2t + '?' + ' '+ cl1, 
	'What' + ' ' + VERB[0] + ' ' + DETERMIN[0] + ' ' + 'color' + ' ' + spacePREPOSITION[1] + ' ' + DETERMIN[0] + ' '+ sz1 + ' ' + sh1 + ' ' +relposition + ' ' + obj2t + '?' + ' '+ cl1, 
	DETERMIN[1] + ' ' +VERB[0] +' '+ article +' '+ sh1 + ' ' + relposition + ' '+ obj2 +'.'+' '+ 'What'+' '+'color'+' '+ VERB[0] + ' ' + PRONOUN[0] + '?'+' ' +cl1]
		
	return sentenceOut 
	
def two_objects_questions_color_sameLocationShape(cl1,sz1,sh1,obj2,obj2t,relposition): 
     
        article = choose_article(sh1)
	
	if sz1 in ['medium','NA']: sz1 = ''
	
        sentenceOut = [ 'What' + ' ' + VERB[0] + ' ' + DETERMIN[0] + ' ' + 'color' + ' ' + spacePREPOSITION[1] + ' ' + DETERMIN[0] + ' '+ sz1 + ' ' + sh1 + ' ' +relposition + ' ' + obj2t + '?' + ' '+ cl1]
		
	return sentenceOut 

def two_objects_questions_color_abspos(cl1,sz1,sh1,obj2,obj2t,abspos): 
      # templates 

      # 3. A shape is in the horisontal vertical. What is its color?
      #4. A shape is in the horisontal vertical. Is it color or non-color?
      #5. A shape is in the horisontal vertical. Is this color or non-color color?    
       
        article = choose_article(sz1)
	
	if sz1 in ['medium','NA']: 
		sz1 = ''
		article = choose_article(sh1)
        sentenceOut = [article + ' '+ sz1+ ' '+ sh1+ ' ' + VERB[0] + ' ' + abspos +'.'+' '+'What'+' '+ VERB[0]+' '+ PRONOUN[2] + ' ' + 'color' + '?' + ' '+cl1]
		
	return sentenceOut 



def two_objects_questions_shape(cl1,sz1,sh1,obj2,obj2t,relposition): 
    
        article = choose_article(cl1)
	
	if sz1 in ['medium','NA']: sz1 = ''
	

        sentenceOut = [ 'What'+' '+ VERB[0]+' '+DETERMIN[0]+' ' + 'shape' + ' ' +spacePREPOSITION[1] + ' '+ DETERMIN[0]+' '+ 'object' + ' ' +relposition + ' '+obj2t+'?'+' '+sh1,
	'What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'shape'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' ' +cl1+' ' + 'object' + ' ' + relposition + ' '+obj2t+'?' + ' '+ sh1,
	 DETERMIN[1] + ' ' +VERB[0]+' '+ 'an' +' '+'object' + ' ' + relposition + ' '+ obj2 +'.'+' '+ 'What'+' '+'shape'+' '+ VERB[0] + ' ' + PRONOUN[0] + '?'+' ' +sh1,
	 DETERMIN[1]+' '+VERB[0]+' '+ article +' '+cl1+' '+'object' + ' ' +relposition + ' '+obj2 +'.'+' '+'What'+' '+ VERB[0]+' '+ PRONOUN[2] + ' ' + 'shape' + '?' + ' '+sh1,
	 DETERMIN[1]+' '+VERB[0]+' '+ article+' '+sz1+' '+cl1+' '+'object' + ' ' +relposition + ' '+obj2 +'.'+' '+'What'+' '+ VERB[0]+' '+ PRONOUN[2] + ' ' + 'shape' + '?' + ' '+sh1]
		
	return sentenceOut 
			
def two_objects_questions_shape_sameLocationColor(cl1,sz1,sh1,obj2,obj2t,relposition): 
      # templates 

      # 3. A shape is in the horisontal vertical. What is its color?
      #4. A shape is in the horisontal vertical. Is it color or non-color?
      #5. A shape is in the horisontal vertical. Is this color or non-color color?    
       
        article = choose_article(cl1)
	
	if sz1 in ['medium','NA']: sz1 = ''
	
        sentenceOut = [ DETERMIN[1]+' '+VERB[0]+' '+ article +' '+sz1+' '+'object' + ' ' +relposition + ' '+obj2 +'.'+' '+'What'+' '+ VERB[0]+' '+ PRONOUN[2] + ' ' + 'shape' + '?' + ' '+sh1,
	 DETERMIN[1]+' '+VERB[0]+' '+ article+' '+sz1+' '+cl1+' '+'object' + ' ' +relposition + ' '+obj2 +'.'+' '+'What'+' '+ VERB[0]+' '+ PRONOUN[2] + ' ' + 'shape' + '?' + ' '+sh1]
		
	return sentenceOut 
	
def two_objects_questions_shape_sameLocationSize(cl1,sz1,sh1,obj2,obj2t,relposition): 
      # templates 

      # 3. A shape is in the horisontal vertical. What is its color?
      #4. A shape is in the horisontal vertical. Is it color or non-color?
      #5. A shape is in the horisontal vertical. Is this color or non-color color?    
       
        article = choose_article(cl1)
	
	if sz1 in ['medium','NA']: sz1 = ''
	
        sentenceOut = ['What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'shape'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' ' +cl1+' ' + 'object' + ' ' + relposition + ' '+obj2t+'?' + ' '+ sh1,
	 DETERMIN[1]+' '+VERB[0]+' '+ article +' '+cl1+' '+'object' + ' ' +relposition + ' '+obj2 +'.'+' '+'What'+' '+ VERB[0]+' '+ PRONOUN[2] + ' ' + 'shape' + '?' + ' '+sh1,
	 DETERMIN[1]+' '+VERB[0]+' '+ article+' '+sz1+' '+cl1+' '+'object' + ' ' +relposition + ' '+obj2 +'.'+' '+'What'+' '+ VERB[0]+' '+ PRONOUN[2] + ' ' + 'shape' + '?' + ' '+sh1]
		
	return sentenceOut 

def two_objects_questions_shape_sameLocationColorSize(cl1,sz1,sh1,obj2,obj2t,relposition): 
      # templates 

      # 3. A shape is in the horisontal vertical. What is its color?
      #4. A shape is in the horisontal vertical. Is it color or non-color?
      #5. A shape is in the horisontal vertical. Is this color or non-color color?    
       
        article = choose_article(cl1)
	
	if sz1 in ['medium','NA']: sz1 = ''
	
        sentenceOut = ['What'+' '+ VERB[0]+' '+DETERMIN[0]+' '+'shape'+' '+spacePREPOSITION[1]+' '+DETERMIN[0]+' ' +cl1+' ' + 'objects' + ' ' + relposition + ' '+obj2t+'?' + ' '+ sh1,
	 DETERMIN[1]+' '+VERB[1]+' ' +sz1+' '+'objects' + ' ' +relposition + ' '+obj2 +'.'+' '+'What'+' '+ VERB[0]+' '+ PRONOUN[4] + ' ' + 'shape' + '?' + ' '+sh1,
	 DETERMIN[1]+' '+VERB[0]+' '+ sz1+' '+cl1+' '+'objects' + ' ' +relposition + ' '+obj2 +'.'+' '+'What'+' '+ VERB[0]+' '+ PRONOUN[4] + ' ' + 'shape' + '?' + ' '+sh1]
		
	return sentenceOut 

def two_objects_questions_shape_abspos(cl1,sz1,sh1,obj2,obj2t,abspos): 
      # templates 

      # 3. A shape is in the horisontal vertical. What is its color?
      #4. A shape is in the horisontal vertical. Is it color or non-color?
      #5. A shape is in the horisontal vertical. Is this color or non-color color?    
       
        article = choose_article(sz1)
	
	if sz1 in ['medium','NA']: 
		sz1 = ''
		article = choose_article(cl1)
        sentenceOut = [article + ' '+ sz1+ ' '+ cl1+ ' '+ 'object' +' '+ VERB[0] + ' ' + abspos +'.'+' '+'What'+' '+ VERB[0]+' '+ PRONOUN[2] + ' ' + 'shape' + '?' + ' '+sh1]
		
	return sentenceOut 

def two_objects_questions_location_hor (obj1,obj1t,obj2,obj2t,relposition,absp): 
      # templates 

      # 3. A shape is in the horisontal vertical. What is its color?
      #4. A shape is in the horisontal vertical. Is it color or non-color?
      #5. A shape is in the horisontal vertical. Is this color or non-color color? 
        hor_choice = '0'
	 
	hor_choice = RANDOM.choice('12')
	
	if hor_choice == '1':
		hor1 = 'left'
		hor2 = 'right'       
	elif hor_choice == '2':
		hor1 = 'right'
		hor2 = 'left'
		
	preposition = ['to the','']
	
	prep = RANDOM.choice(preposition)
		  
        sentenceOut = [ VERB[2]+' '+ obj1t +' '+ prep + ' ' + hor1 + ' '+ DISJUNCTION[0] + ' '+prep +' '+hor2 +' '+ spacePREPOSITION[1]+' '+obj2t+'?'+' ' +relposition,
	 obj1 + ' ' + VERB[0] + ' ' + absp+'.'+' '+ VERB[2]+' '+ PRONOUN[0]  +' '+ prep + ' ' + hor1 + ' '+ DISJUNCTION[0] + ' '+prep +' '+hor2 +' '+ spacePREPOSITION[1]+' '+obj2t+'?'+' ' +relposition]
		
	return sentenceOut 
	
def two_objects_questions_location_hor_abs(obj1,obj1t,obj2,obj2t,relposition,absp): 
      # templates 

      # 3. A shape is in the horisontal vertical. What is its color?
      #4. A shape is in the horisontal vertical. Is it color or non-color?
      #5. A shape is in the horisontal vertical. Is this color or non-color color? 
        hor_choice = '0'
	 
	hor_choice = RANDOM.choice('12')
	
	if hor_choice == '1':
		hor1 = 'left'
		hor2 = 'right'       
	elif hor_choice == '2':
		hor1 = 'right'
		hor2 = 'left'
		
	preposition = ['to the','']
	
	prep = RANDOM.choice(preposition)
	
	  
        sentenceOut = [ obj1 + ' ' + VERB[0] + ' ' + abspos+'.'+' '+ VERB[2]+' '+ PRONOUN[0]  +' '+ prep + ' ' + hor1 + ' '+ DISJUNCTION[0] + ' '+prep +' '+hor2 +' '+ spacePREPOSITION[1]+' '+obj2t+'?'+' ' +relposition]
		
	return sentenceOut 
	
	

def two_objects_questions_location_vert (obj1,obj1t,obj2,obj2t,relposition,absp): 
      # templates 

      # 3. A shape is in the horisontal vertical. What is its color?
      #4. A shape is in the horisontal vertical. Is it color or non-color?
      #5. A shape is in the horisontal vertical. Is this color or non-color color?    
	vert_choice = RANDOM.choice('12')
	
	if vert_choice == '1':
		vert1 = 'above'
		vert2 = 'below'       
	elif vert_choice == '2':
		vert1 = 'below'
		vert2 = 'above'

			  
        sentenceOut = [ VERB[2]+' '+ obj1t  + ' ' + vert1 + ' '+ DISJUNCTION[0] +' '+vert2 +' '+ spacePREPOSITION[1]+' '+obj2t+'?'+' ' +relposition,
	 obj1 + ' ' + VERB[0] + ' ' + absp +'.'+' '+ VERB[2]+' '+ PRONOUN[0]   + ' ' + vert1 + ' '+ DISJUNCTION[0]  +' '+ vert2 +' '+ spacePREPOSITION[1]+' '+obj2t+'?'+' ' +relposition]
		
	return sentenceOut 

def two_objects_questions_location_vert_abs (obj1,obj1t,obj2,obj2t,relposition,absp): 
      # templates 

      # 3. A shape is in the horisontal vertical. What is its color?
      #4. A shape is in the horisontal vertical. Is it color or non-color?
      #5. A shape is in the horisontal vertical. Is this color or non-color color?    
	vert_choice = RANDOM.choice('12')
	
	if vert_choice == '1':
		vert1 = 'above'
		vert2 = 'below'       
	elif vert_choice == '2':
		vert1 = 'below'
		vert2 = 'above'
			  
        sentenceOut = [ obj1 + ' ' + VERB[0] + ' ' + absp +'.'+' '+ VERB[2]+' '+ PRONOUN[0]   + ' ' + vert1 + ' '+ DISJUNCTION[0]  +' '+ vert2 +' '+ spacePREPOSITION[1]+' '+obj2t+'?'+' ' +relposition]
		
	return sentenceOut 


def two_objects_questions_size (obj1,obj2,obj2t,relposition,relsize): 
      
	  
        sentenceOut = [ obj1 + ' ' + VERB[0] + ' ' + relposition + ' '+ obj2 +'.'+' '+ VERB[2]+' '+ PRONOUN[0]   + ' ' + COMPSIZE[0] + ' '+ DISJUNCTION[0]  +' '+ COMPSIZE[1] +' '+ DISJUNCTION[1]+' '+obj2t+'?'+' ' +relsize]
		
	return sentenceOut 

def two_objects_questions_size_sameAttribute (sz1,cl1,sh1,obj2,obj2t,relposition,relsize): 
	
      	article = choose_article(cl1)
	  
        sentenceOut = [ VERB[2]+' '+DETERMIN[0] +' '+ cl1 +' ' + sh1  + ' ' + COMPSIZE[0] + ' '+ DISJUNCTION[0] +' '+COMPSIZE[1] +' '+ DISJUNCTION[1]+' '+obj2t+'?'+' ' +relsize,
	article +' '+ cl1 +' ' + sh1 + ' ' + VERB[0] + ' ' + relposition + ' '+ obj2 +'.'+' '+ VERB[2]+' '+ PRONOUN[0]   + ' ' + COMPSIZE[0] + ' '+ DISJUNCTION[0]  +' '+ COMPSIZE[1] +' '+ DISJUNCTION[1]+' '+obj2t+'?'+' ' +relsize]
		
	return sentenceOut 

def two_objects_questions_size_abspos (obj1,obj2,obj2t,abspos,relsize): 
      
	  
        sentenceOut = [ obj1 + ' ' + VERB[0] + ' ' + abspos +'.'+' '+ VERB[2]+' '+ PRONOUN[0]   + ' ' + COMPSIZE[0] + ' '+ DISJUNCTION[0]  +' '+ COMPSIZE[1] +' '+ DISJUNCTION[1]+' '+obj2t+'?'+' ' +relsize]
		
	return sentenceOut 
