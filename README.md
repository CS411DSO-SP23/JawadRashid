# Jawad_Rashid
Spring 2023 CS 411 Project
Title of application: 
				Comparison of Faculty and Publications among Universities

Purpose:

The purpose of this application is to provide students, researchers and professors context about university faculty, publications and history. A researcher might use this application to view the credibility of a professor by finding out how many publications they have been involved in during a period of time or recently. A Professor looking to join a university may use this application to view the faculty count of their university of choice and view the most productive universities by accessing the top 5/10/15 universities with the most publications per faculty ratio. A student may be interested in using this application to look the publication histogram of a professor they are looking to work with.  


Demo:

https://mediaspace.illinois.edu/media/t/1_gm3ijiku

Installation: I used the academic world dataset

Usage:

Widget One; Input a university name or close to a name such as "California" or "Texas" to receive a bar chart that compares the distinct faculty count from the universities

Widget Two; Input one range of years for example "2001" to "2005" to receive a pie chart that provides the top five university publication counts for that given range.

Widget Three; Enter the name of a professor to receive a histogram of their publication counts throughout their career.

Widget Four; Use the slider which default starts at 10 and ranges to 5 to 15 to display the top publication per faculty ratios within the university data. (Total publication / Faculty Count)

Widget Five; Provide the id, name and photo url to add a new university to the data list, then search the name to find the new university in the list.

Widget Six; Search a university to delete that university  

Design:

The design of the application is divided into six widgets that are each bordered into a specific area of the screen. The front end is created with dash HTMl, and dash bootstrap was used for the components such as search and input buttons. 

Implementation:

I implemented this project using the databases Neo4j, MongoDB and mySQL for the backend and I used Dash Ploty for the frontend. 

Database Techniques:

I used a Null constraint on the university database variable university.name to make sure that value cannot be null so that when a user enter a new university we can display the name in the university data table.

I used indexing on the professor publications histogram to help speed up this specific query because it usually takes a while.

Extra-Credit Capabilities: N/A

Contributions:

I worked alone on this project.
