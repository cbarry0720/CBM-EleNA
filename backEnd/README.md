#backEnd
main.py contains all the code that gets locations from front end react and returns the best path.

python version should be 3.x.x

in python enviroment run the command below

```
pip install -r requirments.txt 
```
this will install all the necessary python packages

To run unit tests, from CBM_EleNA route directory
command: 
```
python -m coverage run -m pytest 
```
To see coverage: 
```
python -m coverage html 
```
This will create html coverage directory, and the index will show line coverage which can be opened up in the browser

To Run Back end Application:
From CMB_EleNa root Directory
```
python -m flask --app backend/elenaBackend --debug run
```
