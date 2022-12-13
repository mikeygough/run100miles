# RUN 100 MILES
#### Video Demo: xxx

## about this project...

sometime in 2018 a friend challenged me to run a half-marathon; 13.1 miles. i was not a runner. i had never run more than 5 miles in my life. so i started training and just before college graduation i finished my first race.

then something weird happened. i heard about ultra-marathons, races longer than the marathon. the most tantalizing of which is the 100-miler. _‘that’s impossible’_ i thought. __so i made it my goal to run one__.

i trained for nearly four years. 850 hours spent running. more than 5,500 training miles.

when race day finally came, it took me almost 29 hours to finish. i walked the last 10 miles. but i finished. 

big goals take time and sacrifice and i’m lucky to have the chance to chase something so fun and arbitrary.

i wore a running watch during most of my training and recently transformed this data into a science project. that project lives here. 

see for yourself how i went from not-a-runner to 100-mile-finisher. 

***

#### stack...

run100miles uses real training data from a gps watch i used while training. the data was exported from my garmin connect profile 
(https://connect.garmin.com/signin).

to clean and format the data i used python in a jupyter lab environment. those data wrangling files are called *1-loading_and_cleaning.ipynb* and *2-processing.ipynb*. after cleaning and filtering, i exported a final *numeric_data.csv*.

to build a dynamic dashboard i used the plotly & dash python framework. plotly is a stand-alone library for generating beautiful graphics. dash is its web-partner that lets you publish these dashboards and style them with html and css. 

bootstrap and node styling are implemented help from the dash_bootstrap_components and dash_mantine_components libraries.

application code is written in *app.py*. to launch the web app run ```python3 app.py``` and visit the local host url.

***

#### five tips on running your first ultra...

1. __run (a lot)__. i ran more than 5,000 miles before i ran my first hundred. this included a half marathon, two marathons and three smaller ultras (one 50 mile race & two 100 kilometer races).

2. __stretch (as much as you can)__. injury prevention is critical. if you hurt yourself you can't train and you won't get any closer to finishing that race! yoga, foam rolling & various cross-training helps.

3. __eat cleanly__. the science is mixed on what's the best diet for ultra-running. my advice is to try and avoid grease, alcohol and highly processed foods. you also want to learn how to eat _while_ running. it's painful to go 100 miles on only gels and goos (though you can use them intermittenly). i enjoyed whole foods like cheese quesadillas, onigiri and fruits during long runs.

4. __find a friend__. 850 hours spent running alone can be beautiful or brutal, it depends on the day. running commitments keep you consistent, entertained and can make you a better runner if you choose the right partner. you also want a crew when running your ultras. i'm forever indebted to my girlfriend for this. her support and crewing from my first to my final ultra made things much better for me.

5. most importantly, __enjoy the process__. life is everything between your birth and your death. so enjoy the days of good weather. and enjoy the days of bad weather. enjoy the muscle soreness. enjoy the sense of accomplishment running 30 miles on saturday morning. then, enjoy a beer knowing you have to run 20 miles the next day. enjoy finding consistency. enjoy the process of going from not-a-runner to 100-mile-finisher.

***

#### reference...

#### virtual environments
Create a Python3 Virtual Environment: 
```python3 -m venv env```

Activate the Virtual Environment:
```source env/bin/activate```

Deactivate the Virtual Environment:
```deactivate```

To Remove a Virtual Environment:
```sudo em -rf venv```

#### requirements.txt
Automagically create a requirements.txt file:
```pip3 freeze > requirements.txt```

#### markdown formatting guide
https://www.ibm.com/docs/en/watson-studio-local/1.2.3?topic=notebooks-markdown-jupyter-cheatsheet
