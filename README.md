# Vehicle-hail-dent-detection

This is the software part of the hail detection system, and should be used along with the hardware system. This is the software installation guide for MAC. 

## Getting Started
Download this folder to your desktop, then start terminal to type in the following commands. 
```
cd Desktop/Vehicle-hail-dent-detection/
```

### Installing

Install virtual environment for python3

```
python3 -m venv env
```
Start virtual environment
```
source env/bin/activate
```
install dependencies
```
pip install -r requirements.txt
```

### Running
```
python3 Simpler.py
```
Assuming there are already 23 raw images copied over from raspberry pi, the program should run with no problem. Click through the buttons. After the last step, go to the folder and open detected.jpg for a clearer result.
