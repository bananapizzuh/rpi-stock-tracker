I just found out that the site-maintainer has made a script that is more functional than this. [the repo](https://github.com/camerahacks/rpilocator-rss-feed)

# RPI Stock Tracker
A python script to email you when there's an update to the [rpilocator rss feed](rpilocator.com). You must schedule and run the script yourself.

## Pre-requesites
- python 3 (I don't know the minimum version)
- pip

## How to use
Install all the dependencies with:  
```pip install -r requirements.txt```  
Either create a file named 'config.toml' in the directory of the script or run it once to generate the file.
The config file should like this:
```
[gmail]
recipent = ""
username = ""
password = ""
    
[parameters]
vendors = []
country = ""
categories = []
```
You must fill out the gmail section (or else there would be no point in the script) and it is optional to fill out the parameters section. (WIP)

## Todo 
- Error handling
- Figure out more about rpilocator's rss feed
