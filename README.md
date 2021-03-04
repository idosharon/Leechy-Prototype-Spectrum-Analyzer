## Leechy Prototype Software

### Setup

1. Install Python 🐍

2.  Use the package manager pip to install selenium and the other packages 📦.

3. Run those commands from the folder:

```bash
sudo mkdir data data/graph data/graph/drunk data/graph/not_drunk \
    data/frames data/frames/drunk data/frames/not_drunk \
    data/sheet expriences
```

```bash
pip install --user -r requirements.txt
```
    
### Imports

```python
import cv2, pickle, xlsxwriter, time, datetime, os, os.path
from imutils import rotate_bound
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from PIL import Image, ImageTk
```

### Get Started

**MAKE SURE KEYBOARD IS ON ENGLISH AND CAPSLOCK ISN'T ON!**
After doing all the setup connect the prototype and run the python script with ```py main.py```. 

### Control The Program

To control the basic things in the software, after putting the finger inside the prototype and seeing the input from the camera on the screen there are several basic commands you can do:
- select the spectrum manually with the mouse.
- "/" - autofind the spectrum.
- "p" - plotting the spectrum (only after locking on it).
- "o" - close the graph.
- "l" - live mode, the graph will always change in real time.
- "k" - save current graph as "not drunk" for comparsion, only at live mode.
- "g" - pause the all program.

### Author

Made by **Leechy** from Ido Sharon, Ori Cohen, Itay Cohen and Nadav Aviran. <br/>
Written in pure python. 🐍

### Copyright License
```
MIT License

Copyright (c) 2020 Ido Sharon

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
