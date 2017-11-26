# cs170


### Running the program (type these commands exactly)
If running in an instructional machine:
* ```tmux```
* ``` cd cs170```
* ``` ipython3```
* ``` %run exponential_solution.py```
* ```cd phase2_inputs_2/inputs50```
* ```supervisor_multithreaded()``` 
* ```Ctrl-b```
* ```d (Don't have the control key held)``` 
The terminal can now be shut down. To return to the program and to view state use:
* ```ssh <the machine>```
* ```tmux attach```
You can now exit the procedure using the same commands: 
* ```Ctrl-b```
* ```d (Don't have the control key held)``` 


### Pushing solutions 
* ```cd out to cs170 directory```
* ``` git checkout -b inputs<num>_<your_name_here>``` EG ``` git checkout -b inputs20_jared```
* ``` git add .```
* ``` git commit -m "commit message"``` 
* ``` git push origin inputs_<your_name_here> ``` EG ```git push origin inputs20_jared```

#### If you aren't running in an instructional machine just remove the tmux commands 
* ``` cd cs170```
* ``` ipython3```
* ``` %run exponential_solution.py```
* ```cd phase2_inputs_2/inputs50```
* ```supervisor_multithreaded()``` 
