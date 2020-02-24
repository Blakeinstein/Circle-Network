# FOSSEE-PYTHON ##
A desktop application to draw a network of circles using PyQt.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
[![Run on Repl.it](https://repl.it/badge/github/Blakeinstein/Circle-Network)](https://repl.it/github/Blakeinstein/Circle-Network)
![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
[![python-camelCase-style](https://img.shields.io/badge/code%20style-camelCase-brightgreen.svg?style=flat)](https://wiki.c2.com/?CamelCase)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Motivation
Built for the screening phase of the FOSSEE program under Python.
 
## Screenshots
> Main window
<p align="center><img width="95%" src="https://i.imgur.com/HCvPV7f.png"></p>
> Canvas with circles (output saved with program)
<p align="center"><img width=95% src="https://i.imgur.com/nujzcwA.png"></p>
> pdf output
<p align="center"><img width=95% src="https://i.imgur.com/5f5eibS.png"></p>
<p align="center"><img width=95% src="https://i.imgur.com/anGmaEm.png"></p>

## Tech/framework used

#### Built with
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)
- [FBS](https://build-system.fman.io/)

## Features ####
> 1. Create random colored circles in the Canvas area on clicking the "Add" button.
> 2. The circles have the following properties:
>    1. They get added to random places on the canvas.
>    2. They have a text label which the user can modify at any time.
> 3. The added circles can be repositioned in the Canvas area.
> 4. The added circles can be deleted from the Canvas area.
> 5. Two circles can be connected using a black line.Two or more circles can simply be selected to connected them, the lines have a text label which the user can modify at any time.
> 6. A pdf report can be generated displaying the connection between different circles on clicking the "Generate Report" button.
> 7. An image file as png can be saved of whatever is displayed in the canvas area on clicking the "Save" button.

## Code overview #

> #### src/main/python/main.py
> Implements the main window with the toolbar using QHBoxLayout, and the canvas using QGraphicsScene on a QDialog

> #### src/main/python/shapes.py
> Implements the shapes to be drawn on canvas, the Circle using QGraphicsEllipseItem, the connection line using QGraphicsLineItem, the name label using QGraphicsTextItem and grip items using QGraphicsPathItem

## Installation
#### clone this repository by running
```bash
git clone https://github.com/Blakeinstein/Circle-Network.git
```
or by simply pressing the Clone or Download button and using your own preferred way of obtaining a working copy of the repository
#### requirements can be installed using
```bash
pip install -r requirements.txt
```
#### Then run using
```bash
fbs run
```
## API Reference

The QtForPython docs were used to implement the program, one can reference them here 
- [QtForPython](https://doc.qt.io/qtforpython/contents.html)
The docs for Qt for C++ library can be found here
- [Qt](https://doc.qt.io/)

## How to use?

- To add a circle, Press the **add** button to add a new circle. a
- To delete a circle, Press the **Del** or the **Backspace** key on your keyboard with the circle selected
- To add a connection, Select two or more circles then press **Space** to add connections
- To change any label, simply **click** on any text to enter edit mode.
- Click on **save** or **generate report** to save canvas as png or generate a report in pdf format, the files are saved as Output.png and Output.pdf respectively

## Afternote and credits
Apart from the screening phase requirement, this project was a really valuable experience, and I have learnt so much while building this
Additionally, I would like to thank [@eyllanesc](https://stackoverflow.com/users/6622587/eyllanesc) over at stack overflow for helping me resolve a few minor issues with PyQt

## License and Ownership

MIT © [Blaine](https://github.com/Blakeinstein/)

![Rishikesh Anand](https://img.shields.io/badge/%20-Rishikesh_Anand-blueviolet)

[![181210041](https://img.shields.io/badge/18120041-%40nitdelhi.ac.in-9cf?style=for-the-badge&logo=Gmail)](mailto:181210041@nitdelhi.ac.in)
