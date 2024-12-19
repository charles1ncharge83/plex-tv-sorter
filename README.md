# TVSorter3 

### TVSorter3 was originally a Python2 project that I began when I first began using PLEX Media Server almost a decade ago.  I am not a programmer or software engineer by any stretch of the imagination but I had a problem that I wanted to solve and this has been working for me for a long time.

This is a very simple command line utility that does simple things to sort TV show files into a PLEX friendly directory/folder structure: 

    + First it looks at a staging directory
    + It then analyzes the staging directory to look for video files
    + It then loops through the identified video files and breaks the filenames into digestible pieces
    + Once it has broken the filenames up into pieces, it loops through each of the files to sort
    + Sorting looks to see if the TV show already has a base and season directory in the target PLEX TV media directory
    + If the directories for the TV show or season do not already exist it will prompt to create them
    + If the directories do exist it will automatically sort the files 

### Basic (Common) Usage:
```
$ tvsorter3.py -d /staging_directory/unsorted/ -t /target_directory/tv/ -sv --auto 
```
In the above example, you give it the staging directory where your TV files are located and then provide it with the target directory where you store your TV shows for your PLEX library.  
