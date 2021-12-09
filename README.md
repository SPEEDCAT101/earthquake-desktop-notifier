# earthquake-desktop-notifier
Finds earthquakes in the US states of Alaska, Hawaii, California, Oregon and Washington and then delivers a notification to your desktop when a new one appears.

NOTICE: In order for this to work, you must edit the Directory1.txt file to reflect a location in which the logs will be stored.
NOTICE2: You must be running Windows 10 or Windows 11 for this to work, as those are the only systems I know how to issue notifications on.

This project uses information from the US Geological Survey to get near live information on earthquakes.  It covers all US states (you must edit the .py to include the other 45 states).   Several libraries may need to be installed, such as win10toast (used to issue notifications to your desktop)
https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson is where you can get a json of all the US earthquakes in the past week.

How To Run

Download the Directory1.txt, delaytime.txt, Earthquake Notifier.py, and Untitled.ico.  Make sure they're in the same folder, and you can open the .py in IDLE and run it.  Feel free to use a different .ico, this one I made as a stop gap.  The .ico is only seen on the notifications.  I reccomend you use Python 3 to run this, it may also work under Python 2 but I doubt it.
