# The past projects of Henry Gann

I have included below a summary of the various languages that I have used and an overview of the projects these langauges have been used to complete

# Personal Projects #

### Text Editor ###

I have made a text editor using Tkinter in Python. This includes the ability to save and open files. It is a fairly barebones text editor.

### Birthday Countdown webpage  ###

I used HTML, CSS and JS to produce a countdown timer to my birthday (9th March).

### Center Of Mass Calculator ###
Ensure that when this is run, that it is run through a webserver. Otherwise a CORS error will prevent your scripts from running.

This allows you to insert components with a mass and an X,Y,Z COM position and it will display the total mass and the current cumulative COM. To edit an item, search for the item using the edit menu and it will autofill the current properties.

### BlackJack ###
Using Python, I have implemented Blackjack using the command line. To run this, navigate to the Blackjack folder and enter ```py blackjack.py``` into the terminal. Note that this variation of blackjack has the dealer stand on soft 17.

### Git API ###
This uses the command line to ask a user for an owner and the name of a repository. Then it counts all the current pull requests for that repo.
##### How to run #####
1. Clone the repo
2. Begin a terminal session and navigate to the directory of the clone
3. Enter ```npm install``` to install the dependencies
4. Enter ```node API.js``` to run the program

* Note that this requires Node.js and npm to be installed 

# University Work #

### C ### 

I have used C to perform multiprocessing tasks. The featured files use a merge sort and insertion sort hybrid. I have applied various methods of multiprocessing to speed up this sorting process. I have used 8 threads, where each thread has been assigned a part of the datablock to sort.
I have also used the Unix 'Fork' function to generate 8 processes. In one method, I am sorting different parts of the data block and using pipes to send the sorted data back to the parent process. In another, I have allocated the data block as shared memory between the processes.

*Please note that I used 8 processes and threads because my CPU had 8 logical processors.*

### C++ ### 

Using Object-Oriented Programming, I implemented linked-lists to help simulate lanes of traffic. This involved using inheritance, polymorphism and other important OOP concepts.

### R ###

I have used R to perform basic data wrangling as well as data analysis. This was done largely through the 'Tidyverse' library which allows data to be sorted and presented tidily. This analysis involve two-sample t-testing and ANOVA analysis.

### Python ###

Python has been my most frequently used language. I have used python for a large number of purposes. These include implementing Dijkstra's greedy shortest path algorithm, data wrangling using Pandas and implementing a file system in Main Memory using FUSE (Not shown in the repository). 

I used Dijkstra's algorithm in a large project which involved finding the shortest route couriers would have to take when delivering medication to retirement. This is the under the 'GreedyShortestPath'.

### Websites ### 

I have included 2 websites. The first was for an assignment. We needed to generate a website for a group called 'Book Program Discussion' and provide a registration form that can be opened with the 'Register Now' button. This had to work with the widths 1920-900px. The registration form looks weird at large widths due to time constraints on the project. It also required the use of the dark-green colour that is prominent throughout much of the page. This website incorporates HTML, CSS and Javascript.

The other item is a webapp for the Auckland University Muay Thai club (Martial Art). I am the 2021 Web developer in charge of maintaining and updating the website. The website uses React as well as CSS and has a Firebase server that contains data for all the members. I am not the sole contributor to this project, but I have added pages and performed maintenance on the webapp.
