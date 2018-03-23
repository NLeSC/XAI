import sys
import os
from os.path import *
from math import *

####################################
# Default (global) parameter values#
####################################

# int: Minimum number of n-grams occurence to be retained
# All Ngrams that occur less than n times are removed
# default value: 0

ngram_min_to_be_retained = 0

# real: Minimum ratio n-grams to skip
# (will be chosen among the ones that occur rarely)
# expressed as a ratio of the cumulated histogram
# default value: 0

ngram_min_rejected_ratio = 0

# NB: the n-gram skipping will go on until:
# ( minimal_ngram_count < ngram_min_to_be_retained ) OR ( rejected_ratio <= ngram_min_rejected_ratio)


# int: the 'n' of 'n'-gram
# default value: 2

gram_size = 2


# File name with trinaing data
# (will be used to construct the dictionary)

file_name_train = ''

# 

file_name_valid = ''
file_name_test = ''



# Importing the values from the configuration file
from text_encode_config import *



####################
# GLOBAL VARIABLES #
####################

def globals_init():

    # dictionary of terms for questions, with the corresponding code (int >= 0)
    globals()['questionDICT']={}
    # same as questionDICT for the answers
    globals()['answerDICT']={}
    # list of values and corresponding terms
    globals()['questionDICTinv']=[]
    # list of n-grams of words (in the order of corresponding index)
    globals()['gramLIST']=None
    # list of n-grams of word index (in the order of corresponding index)
    globals()['gramINDEX']=None


    # length of questionDICT (number of words)
    globals()['SIZE_questionDICT']=0
    # length of answerDICT (number of words)
    globals()['SIZE_answerDICT']=0
    # number of n-grams to consider (length of gramLIST or gramINDEX)
    globals()['SIZE_gram']=0

    # maximal number of words in a question
    globals()['NUMBER_WORDS_MAX']=0

    # Number of pixel values in an image
    #globals()['image_size']=None


#++++++++
def set_globals(**glob):
    for key, value in glob.items():
        globals()[key] = value

def read_file_info_from_args(**args):

           globals().update(args)
    
           globals()['SIZE_answerDICT']  = len(answer_words)
           globals()['answerDICT']       = answer_words
    
    
           globals()['NUMBER_WORDS_MAX'] = number_words_max
    
           globals()['questionDICT']     = question_words
           globals()['SIZE_questionDICT']= len(question_words)
    
           globals()['gramLIST']         = gram_list # dict2list(eval('question_keys_'+str(gram_size)+'gram'))
           globals()['SIZE_gram']        = len(gramLIST)

#            string1=string2=''
#            for i in range(gram_size):	   
#                letter="i"+str(i)
#                string1+=letter+","
#                string2+="questionDICT["+letter+"],"
#            string= "[["+string2[0:len(string2)-1]+"] for "+string1[0:len(string1)-1]+" in gramLIST]"
           globals()['gramINDEX'] = gram_index
#--------


def read_file_info(file_info):
           if isfile(file_info) == False:
              print "ERROR: cannot find info file "+file_info
              sys.exit(0)
       
           execfile(file_info,globals())
    
           globals()['SIZE_answerDICT']  = answer_size
           globals()['answerDICTinv']    = answer_words
           globals()['answerDICT']       = dictinv(answer_words)
    
    
           globals()['NUMBER_WORDS_MAX'] = NUMBER_WORDS_MAX
    
           globals()['questionDICTinv']    = question_words
           globals()['questionDICT']     = dictinv(question_words)
           globals()['SIZE_questionDICT']=len(question_words)
    
           globals()['gramLIST']         = dict2list(eval('question_keys_'+str(gram_size)+'gram'))
           globals()['SIZE_gram']        = len(gramLIST)

           string1=string2=''
           for i in range(gram_size):	   
               letter="i"+str(i)
               string1+=letter+","
               string2+="questionDICT["+letter+"],"
           string= "[["+string2[0:len(string2)-1]+"] for "+string1[0:len(string1)-1]+" in gramLIST]"
           globals()['gramINDEX']=eval(string)

	   

def write_file_info(file_info):

	   FID_info = open(file_info,"w")
           FID_info.write("image_size="+str(image_size)+"\n")
           FID_info.write("\nanswer_size = "+str(SIZE_answerDICT)+"\n")
           FID_info.write("answer_words="+repr(dictinv(answerDICT))+"\n")
           FID_info.write("\n# onehot encoding:\n")
	   FID_info.write("NUMBER_WORDS_MAX="+str(NUMBER_WORDS_MAX)+"\n")
           FID_info.write("question_size_onehot = "+str(SIZE_questionDICT*NUMBER_WORDS_MAX)+"\n")
   	   FID_info.write("question_words="+repr(dictinv(questionDICT))+"\n")
           FID_info.write("\n# "+str(gram_size)+"-gram encoding:\n")
           FID_info.write("question_size_"+str(gram_size)+"gram  = "+str(SIZE_gram)+"\n")
           FID_info.write("question_keys_"+str(gram_size)+"gram="+repr(list2dict(gramLIST))+"\n")
           FID_info.close()

def append_file_info(file_info):
	   FID_info = open(file_info,"a")
           FID_info.write("\n# "+str(gram_size)+"-gram encoding:\n")
           FID_info.write("question_size_"+str(gram_size)+"gram  = "+str(SIZE_gram)+"\n")
           FID_info.write("question_keys_"+str(gram_size)+"gram="+repr(list2dict(gramLIST))+"\n")
           FID_info.close()

#######################
# Auxiliary functions #
#######################

#######################
# String manipulators #
# To avoid strange things in the sentences (double spaces, spaces before point...)


def format_line(line):
    return line.rsplit('\n')[0]

def read_questionAnswer(line):
    if not line:
        return '', ''
    p=line.replace(",", " ").replace("  "," ").replace("  "," ").replace("  "," ").replace(" .",".").split("?")
    return "".join(p[0:len(p)-1]),p[len(p)-1] 

def format_answer(answer):
    return answer.replace(" ","").split(".")[0].split()[0]

def format_word(word):
    return word.lower().split('.')[0].strip()


#####################
# File manipulators #
# File(s) will contain question encoding and/or answer encoding

def open_1or2files(file1,file2):
    FID1 = open(file1, 'w')
    if file1 == file2:
       FID2=FID1
    else:
       FID2 = open(file2, 'w')
    return FID1,FID2

def write_question_answer(questionCODE,answerCODE,FID_question,FID_answer):
   FID_question.write(list2string(questionCODE))
   if FID_question != FID_answer:
      FID_question.write("\n")
   else:
      FID_question.write("  ")
   FID_answer.write(list2string(answerCODE)+"\n")

def write_image_question_answer(imageSTRING,questionCODE,answerCODE,FID_out_amat,FID_out_libsvm):
   FID_out_amat.write(imageSTRING)
   FID_out_amat.write("  ")
   FID_out_amat.write(list2string(questionCODE))
   FID_out_amat.write("  ")
   FID_out_amat.write(list2string(answerCODE)+"\n")

def close_1or2files(FID1,FID2):
    FID1.close()
    if FID1 != FID2:
       FID2.close()

####################################
# List and dictionary manipulators #

def list2string(mylist):
    return " ".join([str(y) for y in mylist])   

def minimum(mylist):
    MIN=mylist[0]
    index_min=[0]
    for i in range(1,len(mylist)):
        if mylist[i] == MIN:
	   index_min.append(i)
	elif mylist[i] < MIN:
	   index_min=[i]
    return MIN,index_min

def list2dict(mylist):
    mydict={}
    for i in range(len(mylist)):
        mydict[i]=' '.join([str(x) for x in mylist[i]])
    return mydict
    
def dict2list(mydict):
    mylist=['']*len(mydict)
    for i in mydict:
        mylist[int(i)]=mydict[i].split()
    return mylist
    
def dictinv(mydict):
    mydictinv={}
    for abc in mydict:
        mydictinv[mydict[abc]]=abc
    return mydictinv




########################################
# Listing all possible words in a file #
########################################

def create_dictionary(files_name):

    NUMBER_WORDS_MAX=globals()['NUMBER_WORDS_MAX']
    indice_question=0
    indice_answer = 0

    for file_name in files_name:
        print "Reading "+file_name+" to make the dictionnary"

        FID = open(file_name, 'r')
        for line in FID:
            question, answer = read_questionAnswer(line)
            words=question.split()
            if len(words)>NUMBER_WORDS_MAX:
               NUMBER_WORDS_MAX=len(words)
            for word in words:
                word_standard=format_word(word)
                if questionDICT.has_key(word_standard)==False:
                   questionDICT[word_standard]=indice_question
	           questionDICTinv.append(word_standard)
	           indice_question+=1
        
            answer = format_answer(answer)
            if answerDICT.has_key(answer)==False:
               answerDICT[answer]=indice_answer
	       indice_answer+=1
        FID.close()
    
    globals()['questionDICT']=questionDICT
    globals()['questionDICTinv']=questionDICTinv
    globals()['answerDICT']=answerDICT
    globals()['SIZE_questionDICT']=len(questionDICT)
    globals()['SIZE_answerDICT']=len(answerDICT)
    globals()['NUMBER_WORDS_MAX']=NUMBER_WORDS_MAX

    print "Maximal number of words in the question: "+str(NUMBER_WORDS_MAX)
    print "Number of words in the dictionary for questions: "+str(SIZE_questionDICT)
    print "      ''                    ''           answers: "+str(SIZE_answerDICT)



#++++++++
def create_dictionary_from_text_stream(text_stream):

    NUMBER_WORDS_MAX=globals()['NUMBER_WORDS_MAX']
    indice_question=0
    indice_answer = 0

    for lines in text_stream:
        for line in [l for l in lines.split("\n") if l]:
            question, answer = read_questionAnswer(line)
            words=question.split()
            if len(words)>NUMBER_WORDS_MAX:
               NUMBER_WORDS_MAX=len(words)
            for word in words:
                word_standard=format_word(word)
                if questionDICT.has_key(word_standard)==False:
                   questionDICT[word_standard]=indice_question
	           questionDICTinv.append(word_standard)
	           indice_question+=1
        
            answer = format_answer(answer)
            if answerDICT.has_key(answer)==False:
               answerDICT[answer]=indice_answer
	       indice_answer+=1
    
    globals()['questionDICT']=questionDICT
    globals()['questionDICTinv']=questionDICTinv
    globals()['answerDICT']=answerDICT
    globals()['SIZE_questionDICT']=len(questionDICT)
    globals()['SIZE_answerDICT']=len(answerDICT)
    globals()['NUMBER_WORDS_MAX']=NUMBER_WORDS_MAX

    return (questionDICT, answerDICT, NUMBER_WORDS_MAX)

#--------




#################################
# Converting a list of sentence #
# into list of bits             #
#################################

def answer_int_encoding(answer):
    if not answer:
        return [len(answerDICT)]
    answer = format_answer(answer)
    return [answerDICT[answer]]

def answer_onehot_encoding(answer):
    answerCODE=[0]*SIZE_answerDICT
    if answer:
        answerCODE[answer_int_encoding(answer)]=1
    return answerCODE

#++++++++
def question_int_encoding(question):

        questionCODE=[SIZE_questionDICT]*NUMBER_WORDS_MAX
	
	# Encoding each word
	indice=0
        for word in question.split():
            word_standard=format_word(word)
	    if questionDICT.has_key(word_standard):
      	       questionCODE[indice]=questionDICT[word_standard]
	    indice+=1

	return questionCODE
#--------

def question_onehot_encoding(question):

        questionCODE=([0]*SIZE_questionDICT)*NUMBER_WORDS_MAX
	
	# Encoding each word
	indice=0
        for word in question.split():
            word_standard=format_word(word)
	    if questionDICT.has_key(word_standard):
      	       questionCODE[indice+questionDICT[word_standard]]=1
	    indice+=SIZE_questionDICT

	return questionCODE

#################################
# Converting a list of sentence #
# into n-grams                  #
#################################

def question_gram_encoding(question):

    gramINDEX=globals()['gramINDEX']
    if gramINDEX==None:
       create_defaultINDEX(gram_size)
    gramINDEX=globals()['gramINDEX']
    gramLIST =globals()['gramLIST']
    SIZE_gram=globals()['SIZE_gram']
    
    questionCODE=[0]*SIZE_gram
    	
    # Encoding each word
    words=question.split()
    for i in range(len(words)-gram_size+1):
	    mygram=[]
	    word_list=''
	    for j in range(gram_size):
                word_standard=format_word(words[i+j])
		word_list+=word_standard+' '
		if questionDICT.has_key(word_standard) == False:
		   break
		mygram.append(questionDICT[word_standard])
	    if mygram in gramINDEX:
     	       questionCODE[gramINDEX.index(mygram)]+=1
	    else:
               print "WARNING: '"+word_list+"' was not found in the " + str(gram_size) + " gram dictionary."

    return questionCODE

#++++++++

def gramINDEX_helper(size, n):
    if size == 1:
        return [[i] for i in xrange(n)]
    else:
        sublists = gramINDEX_helper(size - 1, n)
        answer = []
        for i in xrange(n):
            answer += [[i] + x for x in sublists]
        return answer

#--------


def create_defaultINDEX(gram_size):
    #xxxxxxxx
    # Construction of default index: all ngrams considered...
#    string0=string1=string2=""
#    for i in range(gram_size):	   
#        letter="i"+str(i)
#        string0+=" for "+letter+" in range(SIZE_questionDICT)"
#        string1+=letter+","
#        string2+="questionDICTinv["+letter+"],"
#    string1= "[["+string1[0:len(string1)-1]+"]"+string0+"]"
#    gramINDEX=eval(string1)
#++++++++
    gramINDEX = gramINDEX_helper(gram_size, SIZE_questionDICT)
#--------
#xxxxxxxx
      # examples :
      # n=1 => gramINDEX = [[0], [1], [2], [3]
      # n=2 => gramINDEX = [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [1, 3], [2, 0], [2, 1], [2, 2], [2, 3], [3, 0], [3, 1], [3, 2], [3, 3]]
#    string2= "[["+string2[0:len(string2)-1]+"]"+string0+"]"
#    gramLIST=eval(string2)
#++++++++
    gramLIST=[[questionDICTinv[i] for i in l] for l in gramINDEX]
#--------
   
    globals()['gramLIST']=gramLIST
    globals()['gramINDEX']=gramINDEX
    globals()['SIZE_gram']=len(gramLIST)


def create_gramINDEX(gram_size, file_in):
    create_defaultINDEX(gram_size)    
    gramINDEX=globals()['gramINDEX']
    gramLIST =globals()['gramLIST']
    SIZE_gram=globals()['SIZE_gram']
    
    FID_in = open(file_in, 'r')
    cumulCODES=[0]*SIZE_gram
    for line in FID_in:
        question, answer = read_questionAnswer(line)
	words=question.split()
        for i in range(len(words)-gram_size+1):
	    mygram=[]
	    word_list=''
	    for j in range(gram_size):
                word_standard=format_word(words[i+j])
		word_list+=word_standard+' '
		mygram.append(questionDICT[word_standard])
	    
	    if mygram in gramINDEX:
     	       cumulCODES[gramINDEX.index(mygram)]+=1
	    else:
               print "ERROR... '"+word_list+"' was not listed in the default dictionary"
	       print "Probably "+file_in+" was not the file used to build de dictionary -- with the function create_dictionary() --"
	       sys.exit(1)
    FID_in.close()


    cumulMIN=sum(cumulCODES)*1.0*ngram_min_rejected_ratio
    cumulREJECTED=0.0
    
    i=cumulCODES.index(min(cumulCODES))
    cumulREJECTED+=cumulCODES[i]
    while (cumulCODES[i] < ngram_min_to_be_retained) | (cumulREJECTED <= cumulMIN):
	  
	  #print "discarding "+str(gramLIST[i])
	  gramINDEX = gramINDEX[0:i]+gramINDEX[i+1:SIZE_gram]
	  gramLIST  = gramLIST[0:i]+gramLIST[i+1:SIZE_gram]
	  cumulCODES= cumulCODES[0:i]+cumulCODES[i+1:SIZE_gram]
	  SIZE_gram-=1
	  
          i=cumulCODES.index(min(cumulCODES))
          cumulREJECTED+=cumulCODES[i]
        
    globals()['gramLIST']=gramLIST
    globals()['gramINDEX']=gramINDEX
    globals()['SIZE_gram']=len(gramLIST)

#++++++++
def create_gramINDEX_from_text_stream(gram_size, text_stream):
    create_defaultINDEX(gram_size)
    gramINDEX=globals()['gramINDEX']
    gramLIST =globals()['gramLIST']
    SIZE_gram=globals()['SIZE_gram']
    
    cumulCODES=[0]*SIZE_gram
    for line in text_stream:
        question, answer = read_questionAnswer(line)
	words=question.split()
        for i in range(len(words)-gram_size+1):
	    mygram=[]
	    word_list=''
	    for j in range(gram_size):
                word_standard=format_word(words[i+j])
		word_list+=word_standard+' '
		mygram.append(questionDICT[word_standard])
	    
	    if mygram in gramINDEX:
     	       cumulCODES[gramINDEX.index(mygram)]+=1
	    else:
               print "ERROR... '"+word_list+"' was not listed in the default dictionary"
	       print "Probably a different text stream was used to build el dictionary -- with the function create_dictionary() --"
	       sys.exit(1)


    cumulMIN=sum(cumulCODES)*1.0*ngram_min_rejected_ratio
    cumulREJECTED=0.0
    
    #++++++++
#    temp = [x for x in zip(cumulCODES, xrange(len(cumulCODES))) if x[0] > 0.0]
    temp = zip(cumulCODES, xrange(len(cumulCODES)))
    temp.sort()

    i = 0
    cumulREJECTED+=temp[i][0]

    while (temp[i][0] < ngram_min_to_be_retained) | (cumulREJECTED <= cumulMIN):
#	  print "discarding "+str(gramLIST[temp[i][1]])
	  gramINDEX[temp[i][1]] = None
	  gramLIST[temp[i][1]]  = None
#	  cumulCODES[temp[i][1]] = None
	  SIZE_gram-=1
          i = i + 1
          if i == len(temp):
              raise "We're not keeping anything? How swell."
          cumulREJECTED+=temp[i][0]
    #--------

    gramINDEX = [x for x in gramINDEX if x is not None]
    gramLIST = [x for x in gramLIST if x is not None]

#     cumulMIN=sum(cumulCODES)*1.0*ngram_min_rejected_ratio
#     cumulREJECTED=0.0
    
#     i=cumulCODES.index(min(cumulCODES))
#     cumulREJECTED+=cumulCODES[i]

#     while (cumulCODES[i] < ngram_min_to_be_retained) | (cumulREJECTED <= cumulMIN):
	  
# 	  print "discarding "+str(gramLIST[i])
# 	  gramINDEX = gramINDEX[0:i]+gramINDEX[i+1:SIZE_gram]
# 	  gramLIST  = gramLIST[0:i]+gramLIST[i+1:SIZE_gram]
# 	  cumulCODES= cumulCODES[0:i]+cumulCODES[i+1:SIZE_gram]
# 	  SIZE_gram-=1
#           i=cumulCODES.index(min(cumulCODES))
#           cumulREJECTED+=cumulCODES[i]
        
    globals()['gramLIST']=gramLIST
    globals()['gramINDEX']=gramINDEX
    globals()['SIZE_gram']=len(gramLIST)

    return (gramLIST, gramINDEX)
#--------

##########################
# Writing the outputFile #
##########################

def encode_line(line_txt):

   line_txt=format_line(line_txt)
   question, answer = read_questionAnswer(line_txt)
	
   answerCODE=answer_int_encoding(answer)
   questionCODE=question_gram_encoding(question)
   return answerCODE, questionCODE


def amat_write_fromimg(file_img,file_txt,coding_types,files_amat_out):

    number_codings=len(coding_types)
    if number_codings != len(files_amat_out):
       print "ERROR: coding_types AND files_amat_out MUST HAVE same length IN amat_write"


    FID_txt=open(file_txt, 'r')
    nsamples=0	
    while len(FID_txt.readline())>1:
	nsamples+=1
    FID_txt.close()

    print "Processing "+str(nsamples)+" samples..."

    FID_img=open(file_img, 'r')
    FID_txt=open(file_txt, 'r')
    FIDs_out=[0]*number_codings
    for i in range(number_codings):
        FIDs_out[i] = open(files_amat_out[i]+'.amat', 'w')

    
    isample=0
    for line_img in FID_img:
        line_img=format_line(line_img)    
        line_txt=format_line(FID_txt.readline())
	question, answer = read_questionAnswer(line_txt)
	if len(line_txt.replace(" ","")) == 0:
	   print "ERROR: missing line in "+file_txt
	   sys.exit(69)
	
	answerCODE=answer_int_encoding(answer)
        for i in range(number_codings):
            questionCODE=coding_types[i](question)
    	    if isample == 0: # Write the heading, before the first image
               globals()['image_size']=len(line_img.split())
               FIDs_out[i].write("#size: "+str(nsamples)+" "+str( image_size + len(questionCODE) + len(answerCODE) )+"\n")
               FID_vmat = open(files_amat_out[i]+'.vmat', 'w')
	       FID_vmat.write('AutoVMatrix(\n')
               FID_vmat.write('specification="'+files_amat_out[i]+'.amat"\n')
               FID_vmat.write('inputsize = '+str( image_size + len(questionCODE) )+',\n')
               FID_vmat.write('targetsize = 1,\n')
               #FID_vmat.write('targetsize = '+str( len(answerCODE) )+',\n')
               FID_vmat.write('weightsize = 0,\n')
               FID_vmat.write(')')
	       
            FIDs_out[i].write(line_img)
            FIDs_out[i].write("    ")
            FIDs_out[i].write(list2string(questionCODE))
            FIDs_out[i].write("  ")
            FIDs_out[i].write(list2string(answerCODE)+"\n")
        isample=1


    if len(FID_txt.readline().replace(" ","")) != 0:
       print "ERROR: missing line in "+file_img
       sys.exit(69)
	    
    FID_img.close()    
    FID_txt.close()    
    for i in range(number_codings):
        FIDs_out[i].close()


def amat_write_fromamat(file_amat,file_txt,coding_types,files_amat_out):

    number_codings=len(coding_types)
    if number_codings != len(files_amat_out):
       print "ERROR: coding_types AND files_amat_out MUST HAVE same length IN amat_write"


    FID_txt=open(file_txt, 'r')
    nsamples=0	
    while len(FID_txt.readline())>1:
	nsamples+=1
    FID_txt.close()
    
    print "Processing "+str(nsamples)+" samples..."


    FID_img=open(file_amat, 'r')
    FID_txt=open(file_txt, 'r')
    FIDs_out=[0]*number_codings
    for i in range(number_codings):
        FIDs_out[i] = open(files_amat_out[i]+'.amat', 'w')

    
    isample=0
    for line_img in FID_img:
        line_img=format_line(line_img)  
	if line_img[0]=="#":
	   continue
	line_img=" ".join(line_img.split()[0:image_size])
        line_txt=format_line(FID_txt.readline())
	if len(line_txt.replace(" ","")) == 0:
	   print "ERROR: missing line in "+file_txt
	   sys.exit(69)
	question, answer = read_questionAnswer(line_txt)
	
	answerCODE=answer_int_encoding(answer)
        for i in range(number_codings):
            questionCODE=coding_types[i](question)
    	    if isample == 0: # Write the heading, before the first image
               FIDs_out[i].write("#size: "+str(nsamples)+" "+str( image_size + len(questionCODE) + len(answerCODE) )+"\n")
               FID_vmat = open(files_amat_out[i]+'.vmat', 'w')
	       FID_vmat.write('AutoVMatrix(\n')
               FID_vmat.write('specification="'+files_amat_out[i]+'.amat"\n')
               FID_vmat.write('inputsize = '+str( image_size + len(questionCODE) )+',\n')
               FID_vmat.write('targetsize = 1,\n')
               #FID_vmat.write('targetsize = '+str( len(answerCODE) )+',\n')
               FID_vmat.write('weightsize = 0,\n')
               FID_vmat.write(')')
	       
            FIDs_out[i].write(line_img)
            FIDs_out[i].write("    ")
            FIDs_out[i].write(list2string(questionCODE))
            FIDs_out[i].write("  ")
            FIDs_out[i].write(list2string(answerCODE)+"\n")
        isample=1

    if len(format_line(FID_txt.readline()).replace(" ","")) != 0:
       print "ERROR: missing line in "+file_amat
       sys.exit(69)
	    
    FID_img.close()    
    FID_txt.close()    
    for i in range(number_codings):
        FIDs_out[i].close()



       
####################################
############### MAIN ###############
####################################

if __name__ == "__main__":

    #if len(sys.argv) > 2:
    #    print "Usage: " + sys.argv[0] + " <configFileFID>"
    #    sys.exit(1)
    #elif  len(sys.argv) == 1:
    #    file_name_train='questions'
    #else:
    #    file_name_train=sys.argv[1]
	
    globals_init()

    #if len(files_path+'/'+file_name_train_amat):
    #   globals()['image_size']=image_size
    #   amat_write=amat_write_fromamat
    #   FILES=[[files_path+'/'+file_name_train_amat,files_path+'/'+file_name_train_txt, files_path+'/'+file_name_train_out],
    #          [files_path+'/'+file_name_valid_amat,files_path+'/'+file_name_valid_txt, files_path+'/'+file_name_valid_out],
    #	      [files_path+'/'+file_name_test_amat, files_path+'/'+file_name_test_txt,  files_path+'/'+file_name_test_out]]
    #else:
    
    amat_write=amat_write_fromimg
    FILES=[[files_path+'/'+file_name_train_img,files_path+'/'+file_name_train_txt, files_path+'/'+file_name_train_out],
              [files_path+'/'+file_name_valid_img,files_path+'/'+file_name_valid_txt, files_path+'/'+file_name_valid_out],
	      [files_path+'/'+file_name_test_img, files_path+'/'+file_name_test_txt,  files_path+'/'+file_name_test_out]]

    if file_info == None or len(file_info) == 0:
       create_dictionary([files_path+'/'+file_name_train_txt])
       create_gramINDEX(gram_size, files_path+'/'+file_name_train_txt)
    else:
       read_file_info(files_path+'/'+file_info)
       

    for file_names in FILES:
     
     file_name_img=file_names[0]
     file_name_txt=file_names[1]
     file_name_root=file_names[2]
     
     if len(file_name_img):

	file_info=file_name_root+".info"
	file_out_onehot = file_name_root+'.onehot'
	file_out_ngram  = file_name_root+'.'+str(gram_size)+'gram'
	if isfile(file_out_onehot+'.amat'):
	   append_file_info(file_info)
	   amat_write(file_name_img,file_name_txt,[question_gram_encoding],[file_name_root+'.'+str(gram_size)+'gram'])
	else:
	   write_file_info(file_info)
	   amat_write(file_name_img,file_name_txt,[question_onehot_encoding,question_gram_encoding],[file_out_onehot,file_out_ngram])
	   
	
        os.system('chmod g+r '+ file_name_root + ".*")
