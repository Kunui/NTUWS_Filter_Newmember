# NTUWS Filter Newmember
## Introduction
The modules are developed for processing and cleaning the data which generated by the Web Survey platform of National Taiwan University. It's designed to filter the members of the platform who has filled in the "Welcome Questionnaire" and their recommenders were the interviewers recruited by NTUWS in 2023. The filtered members' list would be compared to the "General members" file, which recorded the detail information of the whole members. 
Users could get the result of each of members merely recommended by interviewers and the key features of them such as "age" or "area" etc. It enables users to track the successful samples each interviewers got and also evaluate their performance.
## Methods and Functions
There are many different methods below the main module class "admember()". The 5 important functions are: 
* "get_filter()"
* "get_problem()"
* "duplicate_number()"
* "sample_merge()"
* "interviewers_performance()"
### get_filter()
This is the major method below "admember()". The function would return the two objects: "**wqs**" and "**tts**", representing the filtered data of "welcome questionnaire samples" and "total members samples" respectively. The first one "wqs" is a pandas.dataframe which processed by the "Welcome Questionnaire" file based on the "recommenders" column, only the samples who recommended by interviewers would selected from the origin data. Similar to "wqs", the second one "tts" is data frame type too. It's selected from the "General members" file, based on the "phone" column which is consistent with the same numbers of the "phone" column in "wqs", "tts" is undoubtedly the data of members the interviewers acquired in "General members" file.
Both of these two objects are defined as the **arguments** of following methods.
### get_problem(wqs, tts)
Both "wqs" and "tts" are the arguments of this function. By comparing each numbers of "phone" within the two data frames, users could filter the numbers exist in "wqs" but not in "tts". (It means such samples are **problematic**) The return type is a data frame.
### duplicate_number(wqs)
There's only one argument "wqs". This function would count the frequency of each numbers of "phone" in "wqs", and then return a data frame that shows all the numbers of which frequency are more than one. 
### sample_merge(wqs, tts)
The two arguments are "wqs" and "tts". This function would filter out the samples who have duplicate and problematic "phone" numbers in "wqs", those left behind and "tts" would be merged into a new data frame. The result shows the entire qualified and successful samples every interviewers have recommended to become the new members.
### interviewers_performance(wqs, tts)
There're also two arguments "wqs" and "tts". This function would count the members based on the specific values of "age" and "city" columns. The **elder** people and **non Great Taipei area** residents are the target samples. Interviewers could fit the bill only when the members they recommended whose age is over 50 and not living in Great Taipei. It would return a table that shows the amount of target samples and general samples respectively each interviewers finally acquired so far.
## Running
In addition to running the codes by editing the script file, the modules also support running by GUI. 
### Main Program
Clone the whole file of this repository, make a new directory which is upper the project folder and then create a "main\.py" file to run the modules. The codes within "main" should be:
>import os  
>os.chdir(os.path.dirname(\_\_file\_\_))    
>from filtmem.filter_member_gui import filmem_gui   
>filmem_gui().mainloop()    
### Select the files
There're three key files users have to select to run the modules. Click the "Open File" buttons on the window, select the right files according to the labels above the entries placed in the same row with the buttons. Each entries would show the path of the file selected.
### Print out the Tables and Image
Users have to type the date in "Samples' Date" entry. The three check buttons on the window could export the tables of **duplicate samples**, the **problematic samples** and the **successful samples**. It's optional for users to get the tables, it could export partial not all tables, depending on which check buttons users finally click. The modules would also print out the image of the counted result of how many target and general samples the interviewers had got whether users clicked any check button or not.
## Version
* **v1.01** 07/23/2023
The first committed and released version. The basic function is export interviews' performance image.
* **v1.02** 07/25/2023
Added GUI script file, the codes could be run by GUI. The steps are simplified, just select the files and click "OK" button to execute the modules.
* **v1.11** 07/30/2023
The added function is edit the method of the modules, so that it could export the tables of three kinda samples, could show **duplicate samples**, the **problematic samples** and the **successful samples**.
