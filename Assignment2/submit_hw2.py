

### The only things you'll have to edit (unless you're porting this script over to a different language) 
### are at the bottom of this file.

import urllib
import urllib2
import hashlib
import random
import email
import email.message
import email.encoders
import StringIO
import sys
import os

""""""""""""""""""""
""""""""""""""""""""

class NullDevice:
  def write(self, s):
    pass

def submit():   
  print '==\n== [sandbox] Submitting Solutions \n=='
  
  (login, password) = loginPrompt()
  if not login:
    print '!! Submission Cancelled'
    return
  
  print '\n== Connecting to Coursera ... '

  # Part Identifier
  (partIdx, sid) = partPrompt()

  # Get Challenge
  (login, ch, state, ch_aux) = getChallenge(login, sid) #sid is the "part identifier"
  if((not login) or (not ch) or (not state)):
    # Some error occured, error string in first return element.
    print '\n!! Error: %s\n' % login
    return

  # Attempt Submission with Challenge
  ch_resp = challengeResponse(login, password, ch)
  try:
    (result, string) = submitSolution(login, ch_resp, sid, output(partIdx), \
                                  source(partIdx), state, ch_aux)
  
    print '== %s' % string.strip()
  except:
    print
    print 'Submission Failure from error',str(sys.exc_info()[0])
    print 'The error can be caused by a too large output file, or some unexpected output preventing the submission.'
    print 'Please submit parta/b_websubmission.txt(generated by this scripts) online.'
    print 'Please compare your answer with our sample output on instruction.'

# =========================== LOGIN HELPERS - NO NEED TO CONFIGURE THIS =======================================

def loginPrompt():
  """Prompt the user for login credentials. Returns a tuple (login, password)."""
  (login, password) = basicPrompt()
  return login, password


def basicPrompt():
  """Prompt the user for login credentials. Returns a tuple (login, password)."""
  login = raw_input('Login (Email address): ')
  password = raw_input('One-time Password (from the assignment page. This is NOT your own account\'s password): ')
  return login, password

def partPrompt():
  print 'Hello! These are the assignment parts that you can submit:'
  counter = 0
  for part in partFriendlyNames:
    counter += 1
    print str(counter) + ') ' + partFriendlyNames[counter - 1]
  partIdx = int(raw_input('Please enter which part you want to submit (1-' + str(counter) + '): ')) - 1
  return (partIdx, partIds[partIdx])

def getChallenge(email, sid):
  """Gets the challenge salt from the server. Returns (email,ch,state,ch_aux)."""
  url = challenge_url()
  values = {'email_address' : email, 'assignment_part_sid' : sid, 'response_encoding' : 'delim'}
  data = urllib.urlencode(values)
  req = urllib2.Request(url, data)
  response = urllib2.urlopen(req)
  text = response.read().strip()

  # text is of the form email|ch|signature
  splits = text.split('|')
  if(len(splits) != 9):
    print 'Badly formatted challenge response: %s' % text
    return None
  return (splits[2], splits[4], splits[6], splits[8])

def challengeResponse(email, passwd, challenge):
  sha1 = hashlib.sha1()
  sha1.update("".join([challenge, passwd])) # hash the first elements
  digest = sha1.hexdigest()
  strAnswer = ''
  for i in range(0, len(digest)):
    strAnswer = strAnswer + digest[i]
  return strAnswer 
  
def challenge_url():
  """Returns the challenge url."""
  return "https://class.coursera.org/" + URL + "/assignment/challenge"

def submit_url():
  """Returns the submission url."""
  return "https://class.coursera.org/" + URL + "/assignment/submit"

def submitSolution(email_address, ch_resp, sid, output, source, state, ch_aux):
  """Submits a solution to the server. Returns (result, string)."""
  source_64_msg = email.message.Message()
  source_64_msg.set_payload(source)
  email.encoders.encode_base64(source_64_msg)

  output_64_msg = email.message.Message()
  output_64_msg.set_payload(output)
  email.encoders.encode_base64(output_64_msg)
  values = { 'assignment_part_sid' : sid, \
             'email_address' : email_address, \
             'submission' : output_64_msg.get_payload(), \
             'submission_aux' : source_64_msg.get_payload(), \
             'challenge_response' : ch_resp, \
             'state' : state \
           }
  url = submit_url()  
  data = urllib.urlencode(values)
  req = urllib2.Request(url, data)
  response = urllib2.urlopen(req)
  string = response.read().strip()
  result = 0
  return result, string

## This collects the source code (just for logging purposes) 
def source(partIdx):
  # open the file, get all lines
  f = open(sourceFiles[partIdx])
  src = f.read() 
  f.close()
  return src



############ BEGIN ASSIGNMENT SPECIFIC CODE - YOU'LL HAVE TO EDIT THIS ##############

__author__ = 'linkuo'
import os
import subprocess
import shutil
import datetime
import time

class student:
    def __init__(self, p, uni='', pin=''):
        self.uni=uni
        self.pin=pin
        self.accuracy=[float(0)]*11
        self.rawgrade=[]
        self.leverage=[5,10,5,5,10,5,5,20,5]
        self.grade=float(0)
        self.address='/home/'+uni+'/hidden/'+pin+'/Homework1/'
        self.lateday=0
        self.partIdx = p
    def setaccuracy(self,i,x):
        self.accuracy[i]=x
    def accuracy2grade(self):
        for question in self.accuracy[:9]:
            if question>=0.95:
                self.rawgrade.append(float(1))
            elif question>=0.85:
                self.rawgrade.append(float(0.9))
            elif question>=0.65:
                self.rawgrade.append(float(0.8))
            elif question>=0.35:
                self.rawgrade.append(float(0.5))
            elif question>=0.30:
                self.rawgrade.append(float(0.3))
            else:
                self.rawgrade.append(0.0)
        
        if self.partIdx == 0:
            for item in zip(self.rawgrade[:4],self.leverage[:4]):
                self.grade=self.grade+item[0]*item[1]
            if self.accuracy[9] == 1:
                self.grade += 15
        else:
            for item in zip(self.rawgrade[4:],self.leverage[4:]):
                self.grade=self.grade+item[0]*item[1]
            if self.accuracy[10] == 1:
                self.grade += 15
            
        
    '''
    def get_lateday(self,duedate):
        try:
            lastm=(datetime.date.fromtimestamp(os.path.getmtime(self.address+'solutionsA.py'))-duedate).days
        except:
            lastm=0
        try:
            if lastm<(datetime.date.fromtimestamp(os.path.getmtime(self.address+'solutionsB.py'))-duedate).days:
                lastm=(datetime.date.fromtimestamp(os.path.getmtime(self.address+'solutionsB.py'))-duedate).days
        except:
            lastm=0
        if lastm<0:
            lastm=0
        self.lateday=lastm
    '''
    def get_runningtime(self,starttime,endtime,i):
        finaltime=(endtime-starttime)/60
        if i==1:
            if finaltime<=5:
                self.setaccuracy(9,float(1))
        if i==2:
            if finaltime<=25:
                self.setaccuracy(10,float(1))
#Grader Class
#When initialize, will take inputs of gold standard files, and convert them into the format they should be.
#for transition and emission probabilities, the gold standard will be stored in dictionary where the ngrams or word/tags as the key, and the log-probability as the value
#for probability of sentences, the probabilities will be stored as a list of number in the order of sentences
#convertdict() and convertnum() convert the line of files to dictionary and number lists
#gradenum(), gradedic() and gradepos() functions will take the students' output files as input. And calculate the percentage of similarity of the student's file and the gold standard.
#setaccuracy() function will take the index of questions and the percentage of similarity as input and set the students' accuracy attribute.
#grade() function calls gradenum(), gradedic() and gradepos() functions and setaccuracy(), to set all accuracies for the current student
class grader:
    gradefiles=['A1.txt','A2.uni.txt','A2.bi.txt','A2.tri.txt','A3.txt','Sample1_scored.txt','Sample2_scored.txt','B2.txt','B3.txt','B4.txt','B5.txt','B6.txt']
    Gold=['A1_GS.txt','A2_GS.uni.txt','A2_GS.bi.txt','A2_GS.tri.txt','A3_GS.txt','Sample1_GS_scored.txt','Sample2_GS_scored.txt','B2_GS.txt','B3_GS.txt','B4_GS.txt','Brown_tagged_dev.txt','Brown_tagged_dev.txt']
    goldstandard=[]
    
    gradefiles = [ 'output/'+f for f in gradefiles]
    Gold =['data/GS/'+f for f in Gold]
    def __init__(self):
        for item in self.Gold:
            file=open(item,'r')
            self.goldstandard.append(file.readlines())
            file.close()
        self.goldstandard[0]=self.convertdict(self.goldstandard[0])
        self.goldstandard[7]=self.convertdict(self.goldstandard[7])
        self.goldstandard[9]=self.convertdict(self.goldstandard[9])
        self.goldstandard[1]=self.convertnum(self.goldstandard[1])
        self.goldstandard[2]=self.convertnum(self.goldstandard[2])
        self.goldstandard[3]=self.convertnum(self.goldstandard[3])
        self.goldstandard[4]=self.convertnum(self.goldstandard[4])
        self.goldstandard[5]=self.convertnum(self.goldstandard[5])
        self.goldstandard[6]=self.convertnum(self.goldstandard[6])
    def convertdict(self,file):
        dict={}
        for line in file:
            try:
                dict[line.rsplit(' ',1)[0]]=float(line.strip().rsplit(' ',1)[1])
            except:
                continue
        return dict
    def convertnum(self,file):
        list=[]
        for line in file:
            try:
                list.append(float(line.strip()))
            except:
                list.append(float(0))
        return list
    def grade(self,currentstudent):
        #print 'grading',currentstudent.uni
        try:
            currentstudent.setaccuracy(0,self.gradedict(0))
        except:
            print 'error on ',currentstudent.uni,0

        try:
            currentstudent.setaccuracy(4,self.gradedict(7))
        except:
            print 'error on ',currentstudent.uni,4

        try:
            currentstudent.setaccuracy(6,self.gradedict(9))
        except:
            print 'error on ',currentstudent.uni,6

        try:
            currentstudent.setaccuracy(2,self.gradenum(4))
        except:
            print 'error on ',currentstudent.uni,2

        try:
            currentstudent.setaccuracy(5,self.gradepos(8))
        except:
            print 'error on ',currentstudent.uni,5

        score=float(0)
        try:
            score=float(self.gradepos(10))-float(0.933249946254)
            if score >=float(0):
                score=1
            else:
                score=abs(self.gradepos(10))/float(0.933249946254)
        except:
            print 'error on ',currentstudent.uni,7

        currentstudent.setaccuracy(7,score)

        score=float(0)
        try:
             score=float(self.gradepos(11))-float(0.879985146677)
             if score >=float(0):
                 score=1
             else:
                 score=abs(self.gradepos(11))/float(0.879985146677)
        except:
            print 'error on ',currentstudent.uni,8
        currentstudent.setaccuracy(8,score)

        score=float(0)
        try:
            score=(self.gradenum(1)+self.gradenum(2)+self.gradenum(3))/3
        except:
            print 'error on ',currentstudent.uni,1
        currentstudent.setaccuracy(1,score)

        score=float(0)
        try:
            score=(self.gradenum(5)+self.gradenum(6))/2
        except:
            print 'error on ',currentstudent.uni,3
        currentstudent.setaccuracy(3,score)

    def gradedict(self,i):
        score=float(0)
        wrong=float(0)
        sum=float(0)
        try:
            files=open(self.gradefiles[i],'r')
            lines=files.readlines()
            files.close()
            lines=self.convertdict(lines)
            for item in self.goldstandard[i]:
                try:
                    if self.goldstandard[i][item]!=0:
                        wrong+= min(abs(float(lines[item]-self.goldstandard[i][item])/float(self.goldstandard[i][item])),1)
                        sum+= 1
                    else:
                        wrong+= min(abs(float(lines[item]-self.goldstandard[i][item])),1)
                        sum+=1
                except:
                    wrong+=1
                    sum+= 1
            try:
                score=float(sum-wrong)/float(sum)
                return score
            except:
                print "error on",i
        except IOError:
            return score

    def gradenum(self,i):
        score=float(0)
        wrong=float(0)
        sum=float(0)
        try:
            files=open(self.gradefiles[i],'r')
            lines=files.readlines()
            files.close()
            lines=self.convertnum(lines)
            for j in range(0,len(self.goldstandard[i])):
                try:
                    if self.goldstandard[i][j]!=0:
                        wrong+= min(abs(float(lines[j]-self.goldstandard[i][j])/float(self.goldstandard[i][j])),1)
                        sum+= 1
                    else:
                        wrong+= min(abs(float(lines[j]-self.goldstandard[i][j])),1)
                        sum+=1
                except:
                    wrong+=1
                    sum+= 1
            try:
                score=float(sum-wrong)/float(sum)
                return score
            except:
                print "error on",i
        except IOError:
            return score

    def gradepos(self,i):
        score=float(0)
        try:
            files=open(self.gradefiles[i],'r')
            lines=files.readlines()
            files.close()
            num_correct = 0
            total = 1
            for user_sent, correct_sent in zip(lines, self.goldstandard[i]):
                user_tok = user_sent.split()
                correct_tok = correct_sent.split()
                if len(user_tok) != len(correct_tok):
                    continue
                for u, c in zip(user_tok, correct_tok):
                    if u == c:
                        num_correct += 1
                    total += 1
            score = float(num_correct) / total
            return score
        except IOError:
            return score


def evaluate_solutions(partIdx):
    gradernow=grader()
    for item in ['dummy']:
        currentstudent= student(partIdx)

        #running the student's scripts and get the running time
        strattime=time.time()
        try:
            subprocess.check_call(" python solutionsA.py",shell=True)
        except:
            print 'solutionsA failed',currentstudent.uni
        endtime=time.time()
        currentstudent.get_runningtime(strattime,endtime,1)
        strattime=time.time()
        try:
            subprocess.check_call(" python solutionsB.py",shell=True)
        except:
            print 'solutionsB failed',currentstudent.uni
        endtime=time.time()
        currentstudent.get_runningtime(strattime,endtime,2)
        #grading current student, this process will generate a list of accuracies for each question
        gradernow.grade(currentstudent)
        #transfer the accuracies to the final grade
        currentstudent.accuracy2grade()

        print 'Your accuracy',
        if partIdx == 0:
            print currentstudent.accuracy[:4]
        else:
            print currentstudent.accuracy[4:9]
        print 'Your grade', currentstudent.grade

        return currentstudent.grade

# Make sure you change this string to the last segment of your class URL.
# For example, if your URL is https://class.coursera.org/pgm-2012-001-staging, set it to "pgm-2012-001-staging".
URL = 'nlpintro-001'

# the "Identifier" you used when creating the part
partIds = ['hw1parta', 'hw1partb']
                     
# used to generate readable run-time information for students
partFriendlyNames = ['Part A - Language Model', 'Part B - Part of Speech Tagging'] 


# source files to collect (just for our records)
#sourceFiles = ['sampleStudentAnswer.py', 'sampleStudentAnswer.py', 'sampleStudentAnswer.py']
sourceFiles = ['solutionsA.py', 'solutionsB.py']             


def output(partIdx):
  outputString = 'nlpfromumich'*100
  outputString += str(int(round(evaluate_solutions(partIdx))))
  return outputString

submit()
