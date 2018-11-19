Each folder in current folder presents different user ID (except "_Hrates"). Each of the folders include the following files:
* "user-id"-phase-new.dat -> this is the phase of the signal, from which the breathing and heartbeats can be extracted;
* "user-id"-time-new.dat -> comes along with the previous file - this includes the time samples for each of the above phase samples;
* "user-id"-primary.txt -> all the clicks and keywords entered in the application to collect current cognitive load. The application that outputs this file is not included in this repository;
* "user-id"-primary-extract.txt -> from the above file only the relevant features are extracted, such as *task ID, user ID, task label, task complexity, start time (in Unix epoch time), time on task (in ms), number of correct answers, number of incorrect answers, number of all correct answers, TLX (from NASA-TLX questionnaire), finished task boolean value*
