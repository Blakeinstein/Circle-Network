# FOSSEE-PYTHON ##
A desktop application to draw a network of circles using PyQt.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
[![Run on Repl.it](https://repl.it/badge/github/Blakeinstein/Circle-Network)](https://repl.it/github/Blakeinstein/Circle-Network)
![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
[![python-camelCase-style](https://img.shields.io/badge/code%20style-camelCase-brightgreen.svg?style=flat)](https://wiki.c2.com/?CamelCase)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Motivation
Built for the screening phase of the FOSSEE program under Python.
 
## Screenshots

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

## Code Example #

####src/main/python/main.py
> Implements the main window with the toolbar using QHBoxLayout, and the canvas using QGraphicsScene on a QDialog

####src/main/python/shapes.py
> Implements the shapes to be drawn on canvas, the Circle using QGraphicsEllipseItem, the connection line using QGraphicsLineItem, the name label using QGraphicsTextItem and grip items using QGraphicsPathItem

## Installation

#### requirements can be installed using ##
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
The standard docs for C++ library of Qt can be found here
- [Qt](https://doc.qt.io/)

## How to use?


## Contribute

Let people know how they can contribute into your project. A [contributing guideline](https://github.com/zulip/zulip-electron/blob/master/CONTRIBUTING.md) will be a big plus.

## Credits
Give proper credits. This could be a link to any repo which inspired you to build this project, any blogposts or links to people who contrbuted in this project. 

#### Anything else that seems useful

## License
A short snippet describing the license (MIT, Apache etc)

MIT © [Blaine](https://github.com/Blakeinstein/)