++++++++++++++++++This is the help file for this Edgaranalyzer+++++++++++++++++++
++++++The project is still lacking one function to arrange the output in chronological order+++++++++++++++++
++++++Paths+++++++
++For this program to work, the following file directories and file names need to be specified correctly
input_path='../input/'
output_path='../output/'
    
input_file_name='log.csv'
max_session_duration_file_name='inactivity_period.txt'
output_fileC_name='sessionization.txt'

++They are set for the program to run from the /src/ folder with input in  /input/ and output stored in /output/
++If you wish to have this tested under the folder: /insight_testsuite/ please change as desired

++++++++++++++++++++++++++++++++Successful running+++++++++++++++++++
++The program spits out a message at the end of the each analyzed line from the log.csv file
++such as:
****************** line number: 1  from log.csv has been analyzed completely!******************
****************** line number: 2  from log.csv has been analyzed completely!******************
****************** line number: 3  from log.csv has been analyzed completely!******************
****************** line number: 4  from log.csv has been analyzed completely!******************
****************** line number: 5  from log.csv has been analyzed completely!******************
****************** line number: 6  from log.csv has been analyzed completely!******************
****************** line number: 7  from log.csv has been analyzed completely!******************
****************** line number: 8  from log.csv has been analyzed completely!******************
****************** line number: 9  from log.csv has been analyzed completely!******************
****************** line number: 10  from log.csv has been analyzed completely!******************
****************** line number: 11  from log.csv has been analyzed completely!******************

+++for the example log.csv given, the solution without sorting was...
+++
000.00.000.00a,1970-01-01 00:00:01,1970-01-01 00:00:01,1,1,
107.23.85.jfd,2017-06-30 00:00:00,2017-06-30 00:00:03,4,4,
108.91.91.hbc,2017-06-30 00:00:01,2017-06-30 00:00:01,1,1,
106.120.173.jie,2017-06-30 00:00:02,2017-06-30 00:00:02,1,1,
107.178.195.aag,2017-06-30 00:00:02,2017-06-30 00:00:04,2,2,
108.91.91.hbc,2017-06-30 00:00:04,2017-06-30 00:00:04,1,1,

+++The line: 
+++000.00.000.00a,1970-01-01 00:00:01,1970-01-01 00:00:01,1,1,
+++is like a default entry which is required so that the session.txt is never empty

#other tests have not been performed as a result of time constraints
