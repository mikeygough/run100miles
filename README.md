## how long does it take to run 100 miles?

i've never been a runner and still don't consider myself one. then, towards the end of college a friend challenged me to run a half marathon (13.1 miles). so i did it.

then, a few weeks later i heard about people who run 100 mile races. i thought that's _impossible_. so in 2018 i decided to run a 100 mile marathon.

i used a gps watch during all my training which stored all my running data. in this project i analyze that data. why not take a look to see how i evolved from never having run more than five miles to running one hundred in a single period (and more than 5,000 along the way)

### notes
* Date also has the time of day... do I usually run in the morning or evening?

* I currently only have rows on days that I ran. For plotting purposes I'd also like to see days I didn't run for identifying rest days or bad streaks where maybe I was sick.

* My first run was April 9th 2018 and my 100 Miler was February 5th 2022. But I wasn't training for the 100 miler on April 9th, I was just training for the Providence half marathon. I can add colored sections to a chart to denote what race I was training for... Providence Half, Kennebunkport Full, Milwaukee Full, Zion 100K, Bandera 100K, Chicago 50M, Rocky Raccoon 100M. It's important to recognize this for calculating an accuracy score as well.

* Add some smoothing, maybe rolling average of 7 day mileage.

* Add jupyter lab widgets for interactions.

* Clean up formatting... Can you output python variables in markdown cells? Or is there a cleaner way to print text and variables togther?

* Incorporate more story... Images.

* Separate file just for beautiful plots.

__Markdown Formatting Guide__
https://www.ibm.com/docs/en/watson-studio-local/1.2.3?topic=notebooks-markdown-jupyter-cheatsheet

### future...
i'm starting to realize that this project should be extensible. what if i turn this notebook into a web app so other runners can upload their exported garmin data and get some neat graphics & such about their running performance? i think i'll do that, after completing my own analysis.

#### reference:

#### virtual environments
Create a Python3 Virtual Environment: 
```python3 -m venv env```

Activate the Virtual Environment:
```source env/bin/activate```

Deactivate the Virtual Environment:
```deactivate```

To Remove a Virtual Environment:
```sudo em -rf venv```

---
#### requirements.txt
Automagically create a requirements.txt file:
```pip3 freeze > requirements.txt```
