#!/usr/bin/env python3
# Copyright 2009-2017 BHG http://bw.org/

import platform
import string

import re
import fileinput


import time
import datetime
from datetime import datetime

def main():
    input_path='../input/'
    output_path='../output/'
    
    input_file_name='log.csv'
    max_session_duration_file_name='inactivity_period.txt'
    #output_fileA_name='sessionStart.txt'
    #output_fileB_name='sessionEnds.txt'
    output_fileC_name='sessionization.txt'
    
    input_file_path_name = input_path + input_file_name
    max_session_duration_file_path_name = input_path+max_session_duration_file_name
    #output_fileA_path_name= output_path + output_fileA_name
    #output_fileB_path_name= output_path + output_fileB_name
    output_fileC_path_name= output_path + output_fileC_name
    
    # get duration from the inactivity_period.txt
    duration_string=retrieve_session_duration(max_session_duration_file_path_name)
    #convert string to int
    max_session_duration=int(duration_string)
    #print('the maximum session duration is',max_session_duration,'s')
    num_of_lines_in_log_file=count_lines_in_log_file(input_file_path_name)
    num_of_lines_in_session_file=count_lines_in_log_file(input_file_path_name)
    #print('the log file has',num_of_lines_in_log_file,'lines')
   
    logFileHandle=get_log_file_handle(input_file_path_name)
    
    
    logFileProcessedMsg=process_log_file_queue(logFileHandle,output_fileC_path_name,max_session_duration,num_of_lines_in_log_file,num_of_lines_in_session_file)
    #writeToSessionizationMsg=
    
    #now sort data in sessions.txt in a chronological order
    sortMsg=sortSessionTXTChronologically(output_fileC_path_name)

#+++++++
def sortSessionTXTChronologically(output_fileC_path_name):
    #load sessions.txt
    #loop through it
    #rearrange if time is out of order
    #save sorted sessions.txt by rewriting the file
    sortMsg=''
    return(sortMsg)
#+++++++++++++++++++now define all supporting functions++++++++++++++++++++++++++++++++++++++
def process_log_file_queue(logFileHandle,output_fileC_path_name,max_session_duration,num_of_lines_in_log_file,num_of_lines_in_session_file):
    
    logIp=''
    logDate=''
    logTime=''
    logCik=''
    logAccession=''
    logExtension=''
    logTimeInSecs=0
    logDateTimeStamp='1970-01-01 00:00:00'
    
    startSessionIp=''
    startSessionDate=''
    startSessionTime=''
    startSessionCik=''
    startSessionAccession=''
    startSessionExtension=''
    startSessionTimeInSecs=0
    #stringStartDateTimestamp='0001-010-01 00:00:01'
    
    #EndSessionIp=''
    EndSessionDate=''
    EndSessionTime=''
    EndSessionCik=''
    EndSessionAccession=''
    EndSessionExtension=''
    EndSessionTimeInSecs=0
    #stringEndDateTimestamp='0001-010-01 00:00:01'
    
    ipFound=''
    sessionOver=''
    specific_message=''
    numOfOccurences=0
    
    #InputQueue
    log_file_queue=[]
    #output Queue
    old_session_file_queue=[]
    new_session_file_queue=[]
    log_of_unique_documents=[]
    
    countLogUp=0
    countSessionUp=0
    
    newDuration=0
    #++++++++++++++++++loop through log file line by line++++++++++++++++++++++
    for line in logFileHandle:
        if countLogUp!=0:
            logFileLog_handle=line.rstrip()
            logLineList=logFileLog_handle.split(',')
                        
            logIp=logLineList[0]
            logDate=logLineList[1]
            logYear,logMonth,logDay=int(logDate[0]),int(logDate[1]),int(logDate[2])
            logTime=logLineList[2]
            logTimeList=logTime.split(':')
            logHour,logMin,logSec=int(logTimeList[0]),int(logTimeList[1]),int(logTimeList[2])
            logDateTimeStamp=logDate+' '+logTime
            
            logCik=logLineList[4]
            logAccession=logLineList[5]
            logExtension=logLineList[6]
            #print('startSessionIp,startSessionDate,startSessionTime,startSessionCik,startSessionAccession,startSessionExtension:\n',startSessionIp,startSessionDate,startSessionTime,startSessionCik,startSessionAccession,startSessionExtension)
            logTimeInSecs=getTimeFromDateTimeString(logDateTimeStamp)
            #print('startSessionTimeInSecs',startSessionTimeInSecs)
            
            numberOfIpMatches=0
            #**********************Loop through session file, line by line*************************
            sessionizationFileHandle=get_sessionization_file_handle(output_fileC_path_name)
            LastRecordedSessionsForIP_handle=getLastRecordedSessionsForIP(sessionizationFileHandle,logIp)
            #print('getLastRecordedSessionsForIP_handle: \n',getLastRecordedSessionsForIP_handle)
            
            ipFound=LastRecordedSessionsForIP_handle[0]
            numOfOccurences=LastRecordedSessionsForIP_handle[1]
            listOfOccurences=LastRecordedSessionsForIP_handle[2]
            #print ('was ip found in sessions.txt? ',ipFound,' How many occurences? ',numOfOccurences,'What entries were found?',listOfOccurences)
            
            VeryLastRecordedSessionForIP=[]
            lastRecordedIP=''
            lastRecordedStartDateTimeStamp=''
            lastRecordedEndDateTimeStamp=''
            lastRecordedDuration=''
            lastRecordedDocumentCount=''
            
            if numOfOccurences>0:
                #print ('was ip found in sessions.txt? ',ipFound,' How many occurences? ',numOfOccurences,'What entries were found?',listOfOccurences)
                VeryLastRecordedSessionForIP=retrieveVeryLastRecordedSessionForIP(listOfOccurences,numOfOccurences)
                #print('last recorded session for ip(',logIp,') was: ',VeryLastRecordedSessionForIP[0], 'found after',VeryLastRecordedSessionForIP[1],'iterations.\n')
                lastRecordedEntryData=VeryLastRecordedSessionForIP[0]
                #print('lastRecordedEntryData:',lastRecordedEntryData)
                lastRecordedIP=lastRecordedEntryData[0]
                lastRecordedStartDateTimeStamp=lastRecordedEntryData[1]
                lastRecordedStartDate,lastRecordedStartTime=lastRecordedStartDateTimeStamp.split(' ')
            
                lastRecordedEndDateTimeStamp=lastRecordedEntryData[2]
                #print('lastRecordedEndDateTimeStamp:',lastRecordedEndDateTimeStamp)
                lastRecordedEndDate,lastRecordedEndTime=lastRecordedEndDateTimeStamp.split(' ')
                #print('lastRecordedEndDate:',lastRecordedEndDate)
                lastRecordedEndDateTimeInSeconds=getTimeFromDateTimeString(lastRecordedEndDateTimeStamp)
                #print('lastRecordedEndDateTimeInSeconds:',lastRecordedEndDateTimeInSeconds)
            
                lastRecordedDuration=int(lastRecordedEntryData[3])
            
                lastRecordedDocumentCount=int(lastRecordedEntryData[4])
            else:
                lastRecordedIP=logIp
                lastRecordedStartDateTimeStamp=logDateTimeStamp
                lastRecordedEndDateTimeStamp=logDateTimeStamp
                lastRecordedDuration=0
                lastRecordedDocumentCount=0
                lastRecordedTimeInSecs=logTimeInSecs
                
           #********Now decide if session is new or old********************
            if countLogUp<(num_of_lines_in_log_file-1):
                    #i.e. end of log file not yet reached
                if ipFound=='No':
                    #i.e. this ip is not yet found in session.txt
                    #so it must be a new
                    #increase doc count start and end date the same
                    output_text=logIp+','+logDateTimeStamp+','+logDateTimeStamp+',1,1,\n'
                    writeToFileMsg=writeToSessionsTxtFile(output_fileC_path_name,output_text)
                    #print('no previous session existed, this must be a brand new session')
                    
                elif ipFound=='Yes':
                    #now decide if this is a new session or an old one
                    #i.e the ip from the log.csv file matches one found in session.txt
                    timeElapsed=logTimeInSecs-lastRecordedEndDateTimeInSeconds
                    # print('timeElapsed',timeElapsed)
                    #print('logTimeInSecs',logTimeInSecs)
                    # print('lastRecordedEndDateTimeInSeconds',lastRecordedEndDateTimeInSeconds)
                    
                    if timeElapsed<=max_session_duration:
                        #this line needs to be updated
                        #increase doc count and evaluate duration
                        #startDateTimeStamp is that of previously recorded one
                        
                        #print('last document count: ',lastRecordedDocumentCount)
                        newDocumentCount=str(lastRecordedDocumentCount+1)
                        #print('...newDocumentCount',newDocumentCount)
                        
                        #print('present time in seconds: ',logTimeInSecs)
                        #print('last recorded time in seconds: ',lastRecordedEndDateTimeInSeconds)
                        
                        newDuration=str(logTimeInSecs-lastRecordedEndDateTimeInSeconds+1)
                        
                        newlineData=logIp+','+lastRecordedStartDateTimeStamp+','+logDateTimeStamp+','+newDocumentCount+','+newDocumentCount
                        #print('new line data:',newlineData)
                        oldlineData=lastRecordedIP+','+lastRecordedStartDateTimeStamp+','+lastRecordedEndDateTimeStamp+','+str(lastRecordedDuration)+','+str(lastRecordedDocumentCount)
                        #print('old line data:',oldlineData)
                        updateSessionTxtFileMsg=updateLineInSessions(output_fileC_path_name,oldlineData,newlineData)
                        #print('\n ****+++... still in Session, output_text+++****',newlineData)
                    else:
                        #increase doc count and  duration=1 by default
                        newDuration=str(logTimeInSecs-lastRecordedEndDateTimeInSeconds+1)
                        
                        newDocumentCount=str(lastRecordedDocumentCount+1)
                        output_text=logIp+','+logDateTimeStamp+','+logDateTimeStamp+',1,'+'1,\n'
                        #writeToFileMsg=writeToSessionsTxtFile(output_fileC_path_name,output_text)
                        #print('\n +++***session over, this starts a new session, output_text',output_text)
                        
                else:
                    #error of some kind
                    print('possible error encountered in determining session logic')
            else:
                 #i.e. end of file was reached so session is over by default
                 #New line must be written, start and end date the same
                 newDuration=str(logTimeInSecs-lastRecordedEndDateTimeInSeconds+1)
                 
                 #output_text=logIp+','+logDateTimeStamp+','+logDateTimeStamp+','+str(newDuration)+'1,\n'
                 output_text=logIp+','+logDateTimeStamp+','+logDateTimeStamp+',1,1,\n'
                 writeToFileMsg=writeToSessionsTxtFile(output_fileC_path_name,output_text)
                 #print('\n +++***end of file reached, session is over, output_text***+++',output_text)
                 
            countLogUp=countLogUp+1
        else:
            countLogUp=countLogUp+1
        
        print('****************** line number:',countLogUp,' from log.csv has been analyzed completely!******************')         
    #********????********************
    
    #print('new_session_file_queue: ',new_session_file_queue,'countLogUp',countLogUp)       
    #return not queue     
    logFileHandle.close()
    sessionizationFileHandle.close()
    
    return()
#+++++++++++
def updateLineInSessions(output_fileC_path_name,oldlineData,newlineData):
   
    sessionQueue=[]
    
    numOfOccurences=0
    numberOfLinesFromSessionTXT=0
    
    presentLineSessionIp=''
    presentLineStartSessionDateTimeStamp=''
    presentLineEndSessionDateTimeStamp=''
    presentLineSessionDuration=''
    presentLineSessionDocumentCount=''
    
        
    oldlineDataList=oldlineData.split(',')
    oldLineSessionIp=oldlineDataList[0]
    oldLineStartSessionDateTimeStamp=oldlineDataList[1]
    oldLineEndSessionDateTimeStamp=oldlineDataList[2]
    oldLineSessionDuration=oldlineDataList[3]
    oldLineSessionDocumentCount=oldlineDataList[4]
    
    
    newlineDataList=newlineData.split(',')
    newLineSessionIp=newlineDataList[0]
    newLineStartSessionDateTimeStamp=newlineDataList[1]
    newLineEndSessionDateTimeStamp=newlineDataList[2]
    newLineSessionDuration=newlineDataList[3]
    newLineSessionDocumentCount=newlineDataList[4]
    
    
    #print('now searching for old line data line in sessions.txt')
    sessionUpdateHandle=open(output_fileC_path_name,'rt')
    
    for linesession in sessionUpdateHandle:
        sessionFileLog_handle=linesession.rstrip()
        sessionLineList=sessionFileLog_handle.split(',')
        numberOfLinesFromSessionTXT=numberOfLinesFromSessionTXT+1
        
        if sessionLineList!='':
            presentLineSessionIp=sessionLineList[0]
            presentLineStartSessionDateTimeStamp=sessionLineList[1]
            presentLineEndSessionDateTimeStamp=sessionLineList[2]
            presentLineSessionDuration=sessionLineList[3]
            presentLineSessionDocumentCount=sessionLineList[4]
            
            #print('\n comparison txt:oldLineSessionIp==presentLineSessionIp and oldLineStartSessionDateTimeStamp==presentLineStartSessionDateTimeStamp and oldLineEndSessionDateTimeStamp==presentLineEndSessionDateTimeStamp and oldLineSessionDuration==presentLineSessionDuration and oldLineSessionDocumentCount==presentLineSessionDocumentCount\n ')
            #print(oldLineSessionIp+'=='+presentLineSessionIp + ' and '+ oldLineStartSessionDateTimeStamp+'=='+presentLineStartSessionDateTimeStamp + ' and '+ oldLineEndSessionDateTimeStamp+'=='+presentLineEndSessionDateTimeStamp + ' and '+ oldLineSessionDuration+'=='+presentLineSessionDuration + ' and '+ oldLineSessionDocumentCount+'=='+presentLineSessionDocumentCount)
            
            if oldLineSessionIp==presentLineSessionIp and oldLineStartSessionDateTimeStamp==presentLineStartSessionDateTimeStamp and oldLineEndSessionDateTimeStamp==presentLineEndSessionDateTimeStamp and oldLineSessionDuration==presentLineSessionDuration and oldLineSessionDocumentCount==presentLineSessionDocumentCount:
               #print('yaay! I found it')
               if numOfOccurences<0:
                    #matching line found in session.txt
                    #print('now replacing line in sessions.txt and storing updated line to sessionQueue')
                    # print('\n new line data*****:\n',newLineSessionIp,newLineStartSessionDateTimeStamp,newLineEndSessionDateTimeStamp,newLineSessionDuration,newLineSessionDocumentCount)
                    
                    sessionQueue.append([newLineSessionIp,newLineStartSessionDateTimeStamp,newLineEndSessionDateTimeStamp,newLineSessionDuration,newLineSessionDocumentCount])
                    numOfOccurences=numOfOccurences+1
                    
               else:
                    #sessionQueue.append([presentLineSessionIp,presentLineStartSessionDateTimeStamp,presentLineEndSessionDateTimeStamp,presentLineSessionDuration,presentLineSessionDocumentCount])
                    numOfOccurences=numOfOccurences+1
                    sessionQueue.append([newLineSessionIp,newLineStartSessionDateTimeStamp,newLineEndSessionDateTimeStamp,newLineSessionDuration,newLineSessionDocumentCount])
            else :
                #no matching line found in session.txt
                #print('...still looking for line in sessions.txt, storing this line to queue as it is')
                #presentLineSessionIp,presentLineStartSessionDateTimeStamp,presentLineEndSessionDateTimeStamp,presentLineSessionDuration,presentLineSessionDocumentCount
                sessionQueue.append([presentLineSessionIp,presentLineStartSessionDateTimeStamp,presentLineEndSessionDateTimeStamp,presentLineSessionDuration,presentLineSessionDocumentCount])
                numOfOccurences=numOfOccurences+0
                   
        else:
            #print('no line at all was found in session.txt for old line data from log.csv')
            numOfOccurences=numOfOccurences+0
    
    #print('update the whole sessions.txt file using sessionQueue file',sessionQueue)
    
    sessionUpdateHandle.close()
    
    updateMsg=writeQueueToFile(output_fileC_path_name,sessionQueue,numberOfLinesFromSessionTXT)
    
    return(updateMsg)

#+++++++++++
def writeQueueToFile(output_fileC_path_name,sessionQueue,numberOfLinesFromSessionTXT):
    #print('*****now writing sessionQueue',sessionQueue,' to session.txt not appending I hope:',)
    countLines=0
    output_text=''
    
    file_handle3=open(output_fileC_path_name,'wt')
    #if append doesn't work, use newDataQueue to create a new file with old data as well
    
    while countLines<numberOfLinesFromSessionTXT:
        lineHandle=sessionQueue[countLines]
        if countLines==0:
            output_text=lineHandle[0]+','+lineHandle[1]+','+lineHandle[2]+','+lineHandle[3]+','+lineHandle[4]+',\n'
            #print('output text is now',output_text)
        else:
            #print('line handle is: ',lineHandle)
            output_text=output_text+lineHandle[0]+','+lineHandle[1]+','+lineHandle[2]+','+lineHandle[3]+','+lineHandle[4]+',\n'
            #print('output text is now',output_text)
        
        countLines=countLines+1
                
    file_handle3.write(output_text)
    file_handle3.close()
    
    #print('output text is: ',output_text)
    
    if file_handle3!=False:
        return('written to successfully to file')
    else:
        return('unable to write to file')

#+++++++++++
def writeToSessionsTxtFile(output_fileC_path_name,output_text):
    file_handle2=open(output_fileC_path_name,'at')
    #if append doesn't work, use newDataQueue to create a new file with old data as well
    file_handle2.write(output_text)
    file_handle2.close()
    if file_handle2!=False:
        return('written to successfully to file')
    else:
        return('unable to write to file')
#++++++++++
def retrieveVeryLastRecordedSessionForIP(listOfOccurences,numOfOccurences):
    iterationsPossible=0
    VeryLastRecordedSessionForIP=[]
   
    while iterationsPossible<numOfOccurences:
        #print('\n looping through occurences:', listOfOccurences[iterationsPossible])
        if iterationsPossible==(numOfOccurences-1):
          VeryLastRecordedSessionForIP=listOfOccurences[iterationsPossible]
          
        else:
            VeryLastRecordedSessionForIP=listOfOccurences[iterationsPossible]
        iterationsPossible=iterationsPossible+1
    
    iterationsMade=iterationsPossible

    return(VeryLastRecordedSessionForIP,iterationsMade)
#++++++++++
def getLastRecordedSessionsForIP(sessionizationFileHandle,logIp):
    startSessionIp=''
    startSessionDate=''
    startSessionTime=''
    startSessionCik=''
    startSessionAccession=''
    startSessionExtension=''
    startSessionTimeInSecs=0
    #stringStartDateTimestamp='1970-01-01 00:00:01'
    
    #EndSessionIp=''
    EndSessionDate=''
    EndSessionTime=''
    EndSessionCik=''
    EndSessionAccession=''
    EndSessionExtension=''
    EndSessionTimeInSecs=0
    #stringEndDateTimestamp='1970-01-01 00:00:01'
    
    numOfOccurences=0
    listOfOccurences=[]
    ipFound=''
    
    
    for linesession in sessionizationFileHandle:
        sessionFileLog_handle=linesession.rstrip()
        sessionLineList=sessionFileLog_handle.split(',')
        #print('session line retrieved:',sessionLineList)
        
        if sessionLineList!='':
            startSessionIp=sessionLineList[0]
            
            startSessionDateTimeStamp=sessionLineList[1]
            startSessionDateTimeStamp_List=startSessionDateTimeStamp.split(' ')
            startSessionDate=startSessionDateTimeStamp_List[0]
            startSessionTime=startSessionDateTimeStamp_List[1]
            #startSessionCik=''
            #startSessionAccession=''
            #startSessionExtension=''
            if startSessionDate!='' and startSessionTime !='':
                startSessionTimeInSecs=getTimeFromDateTimeString(startSessionDateTimeStamp)
            else:
                print('empty date time string')
            
            EndSessionDateTimeStamp=sessionLineList[2]
            EndSessionDateTimeStamp_List=startSessionDateTimeStamp.split(' ')
            #EndSessionIp=''
            EndSessionDate=EndSessionDateTimeStamp_List[0]
            EndSessionTime=EndSessionDateTimeStamp_List[1]
            #EndSessionCik=''
            #EndSessionAccession=''
            #EndSessionExtension=''
            if EndSessionDate!='' and EndSessionTime !='':
                #print('EndSessionDateTimeStamp',EndSessionDateTimeStamp)
                EndSessionTimeInSecs=getTimeFromDateTimeString(EndSessionDateTimeStamp)
            else:
                print('empty date time string')
            
            recordedSessionDuration=sessionLineList[3]
            recordedNumOfDocsAccessedInSession=sessionLineList[4]
            
            if logIp==startSessionIp:
                #session found
                numOfOccurences=numOfOccurences+1
                listOfOccurences.append([startSessionIp,startSessionDateTimeStamp,EndSessionDateTimeStamp,recordedSessionDuration,recordedNumOfDocsAccessedInSession])
            
            elif logIp!=startSessionIp:
                #no session found
                numOfOccurences=numOfOccurences+0
            else:
                #ipFound='No'
                numOfOccurences=numOfOccurences+0
       
        else:
            #print('no line found in session.txt for ip from log.csv')
            ipFound='No'
            numOfOccurences=numOfOccurences+0
            #listOfOccurences.append(['000.00.000.00a','0001-01-01 00:00:01','0001-01-01 00:00:01','1','1'])
            #numOfOccurences=numOfOccurences+1
    
    if numOfOccurences>=1:
        ipFound='Yes'
        
    else:
        ipFound='No'
    
    return(ipFound,numOfOccurences,listOfOccurences)
        
    
#++++++++++
def getTimeFromDateTimeString(startSessionDateTimeStamp):
    #2017-06-30 00:00:00
    #stringDateTime='' + date_str +' ' + time_str
    #format = "%Y-%m-%d %H:%M:%S"
    #dt = datetime.datetime.strptime(stringDateTime,format)
    #timeInSecs=dt.toordinal()
    
    #date_time_stamp="1970-01-01 00:00:00"
    #date_time_stamp=date_str+' '+time_str
    format = "%Y-%m-%d %H:%M:%S"
    #print('date_time_stamp:',startSessionDateTimeStamp)
    
    d=datetime.strptime(startSessionDateTimeStamp,format)
    #print('d: ',d)
    #print('d tuple: ',d.timetuple())
    timeInSeconds=time.mktime(d.timetuple())
    #print('timeInSeconds: ',timeInSeconds)
    return(timeInSeconds)
#++++++++++    
def get_sessionization_file_handle(output_fileC_path_name):
    sessionizationFileHandle=open(output_fileC_path_name,'rt')
    return(sessionizationFileHandle)
#++++++++++
def get_log_file_handle(input_file_path_name):
    log_file_handle=open(input_file_path_name,'rt')
    return(log_file_handle)
#++++++++++
def count_lines_in_log_file(input_file_path_name):    
    file_handle=open(input_file_path_name,'rt')
    lineCounter=0
    for line in file_handle:
        lineCounter=lineCounter+1
    file_handle.close()
    return(lineCounter)
#++++++++++
def retrieve_session_duration(inactivity_file_name):
    t=open(inactivity_file_name)
    for line in t:
        if line!='':
            duration_string=line.rstrip()
            t.close()
            return (duration_string)
        else:
            #print('end of file reached')
            duration_string='0'
            t.close()
            return (duration_string)
        
#+++++++++++++++++++++++++++++++end+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == '__main__':main()
