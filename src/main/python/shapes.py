"""
Defines shapes used in circle networks,
Contains Definitions for Circle, GripItem, DirectionGripItem, ConLine and NameItem
"""
import random
from string import ascii_uppercase

from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtGui import QBrush, QColor, QCursor, QPainterPath, QPen
from PyQt5.QtWidgets import (QGraphicsEllipseItem, QGraphicsItem,
                             QGraphicsLineItem, QGraphicsPathItem,
                             QGraphicsTextItem)


class GripItem(QGraphicsPathItem):
    """
    Extends PyQt5's QGraphicsPathItem to create the general structure of the Grabbable points for resizing shapes.
    Takes two parameters, reference item (On which the grip items are to appear) and the grip index
    """
    circle = QPainterPath()
    circle.addEllipse(QRectF(-5, -5, 10, 10))

    def __init__(self, annotation_item, index):
        """
        Extends PyQt5's QGraphicsPathItem to create the general structure of the Grabbable points for resizing shapes.
        """
        super(GripItem, self).__init__()
        self.m_annotation_item = annotation_item
        self.m_index = index

        self.setPath(GripItem.circle)
        self.setPen(QPen(QColor(), -1))  
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)
        self.setZValue(11)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def hoverEnterEvent(self, event):
        """
        defines shape highlighting on Mouse Over
        """
        self.setPen(QPen(QColor("black"), 2))
        self.setBrush(QColor("red"))
        super(GripItem, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        """
        defines shape highlighting on Mouse Leave
        """
        self.setPen(QPen(Qt.transparent))
        self.setBrush(Qt.transparent)   
        super(GripItem, self).hoverLeaveEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Automatically deselects grip item on mouse release
        """
        self.setSelected(False)
        super(GripItem, self).mouseReleaseEvent(event)

    def itemChange(self, change, value):
        """
        Calls movepoint from reference item, with the index of this grip item
        """
        if change == QGraphicsItem.ItemPositionChange and self.isEnabled():
            self.m_annotation_item.movePoint(self.m_index, value)
        return super(GripItem, self).itemChange(change, value)
   
class DirectionGripItem(GripItem):
    """
    Extends grip items for vertical and horizontal directions, with hover events and directional changes
    """
    def __init__(self, annotation_item, direction=Qt.Horizontal, parent=None):
        """
        Extends grip items for vertical and horizontal directions, with hover events and directional changes
        """
        super(DirectionGripItem, self).__init__(annotation_item, parent)
        self._direction = direction

    @property
    def direction(self):
        """
        property that returns the current intended resize direction of the grip item object
        """
        return self._direction
    
    def hoverEnterEvent(self, event):
        """
        Changes cursor to horizontal resize or vertical resize depending on the direction of the grip item on mouse enter
        """
        if self._direction == Qt.Horizontal:
            self.setCursor(QCursor(Qt.SizeHorCursor))
        else:
            self.setCursor(QCursor(Qt.SizeVerCursor))
        super(DirectionGripItem, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        """
        reverts cursor to default on mouse leave
        """
        self.setCursor(QCursor(Qt.ArrowCursor))
        super(DirectionGripItem, self).hoverLeaveEvent(event)

    def itemChange(self, change, value):
        """
        Moves position of grip item on resize or reference circle's position change
        """
        if change == QGraphicsItem.ItemPositionChange and self.isEnabled():
            p = QPointF(self.pos())
            if self.direction == Qt.Horizontal:
                p.setX(value.x())
            elif self.direction == Qt.Vertical:
                p.setY(value.y())
            self.m_annotation_item.movePoint(self.m_index, p)
            return p
        return super(DirectionGripItem, self).itemChange(change, value)

      
class ItemName(QGraphicsTextItem):
    """
    Extends PyQt5's QGraphicsTextItem to be editable name labels for shapes
    """
    def __init__(self, label, index, parent=None):
        """
        Extends PyQt5's QGraphicsTextItem to be editable name labels for shapes
        """
        super(ItemName, self).__init__(label, parent)
        self.m_index = index
        self.setZValue(11)
        self.setDefaultTextColor(Qt.black)
        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.adjustSize()
        self.setTextWidth(-1)
    
    def hoverEnterEvent(self, event):
        """
        set cursor to TextEdit cursor on mouse enter
        """
        self.setCursor(QCursor(Qt.IBeamCursor))
        super(ItemName, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        """
        revert cursor to default on mouse leave
        """
        self.setCursor(QCursor(Qt.ArrowCursor))
        super(ItemName, self).hoverLeaveEvent(event)
    
class ConLine(QGraphicsLineItem):
    """
    Extends PyQt5's QGraphicsLineItem to act as the Connection line between any two circles.
    """
    def __init__(self, cir1, cir2, parent=None):
        """
        Extends PyQt5's QGraphicsLineItem to act as the Connection line between any two circles.
        """
        super(ConLine, self).__init__(cir1.pos().x(), cir1.pos().y(), cir2.pos().x(), cir2.pos().y(), parent=parent)
        self.setZValue(11)
        self.label = f'con{random.choice(ascii_uppercase)}'
        self.ref1 = cir1
        self.ref2 = cir2
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        self.nameItem = None
     
    def setLine(self, x1, y1, x2, y2):
        """
        used to update line on reference item change call this on update_items_positions
        """
        super(ConLine, self).setLine(x1, y1, x2, y2)
        self.updateAlignment()
    
    def addNameItem(self):
        """
        used to add a name item label
        """
        if self.scene() and not self.nameItem:
            nameItem = ItemName(self.label, 1)
            self.scene().addItem(nameItem)
            self.nameItem = nameItem
            
        self.updateAlignment()

    def updateAlignment(self):
        """
        updates alignment along the line on reference circle's position update
        """
        nameItem = self.nameItem
        line = self.line()
        angle = line.angle()
        nameItem.setEnabled(False)
        nameItem.setPos(line.center())
        nameItem.setRotation(180-angle if 90<angle<=270 else -angle)
        nameItem.setEnabled(True)
        
class Circle(QGraphicsEllipseItem):
    """
    Extends PyQt5's QGraphicsEllipseItem to create the basic structure of the circle with given center and radius or random if not provided
    """
    def __init__(self, radius=None, name=None, x=0, y=0, parent=None):
        """
        Extends PyQt5's QGraphicsEllipseItem to create the basic structure of the circle with given center and radius or random if not provided
        """
        super(Circle, self).__init__(parent)
        self.setZValue(11)
        self.m_items = []
        self.lineItems = []
        self.setPen(QPen(Qt.black, 3, Qt.SolidLine))
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self._radius = radius or 50 + random.random() * 200
        self.label = name if name else f'cir{random.choice(ascii_uppercase)}'
        self.setPos(x or random.randint(100, 1000), y or random.randint(100, 600))
        self.update_rect()
        self.addItems()
        self.update_items_positions()

    @property
    def radius(self):
        """
        Property that returns the radius of the circle item
        """
        return self._radius
    

    @radius.setter
    def radius(self, r):
        """
        updates circle properties on radius update
        """
        if r <= 0:
            raise ValueError("radius must be positive")
        self._radius = r
        self.update_rect()
        self.addItems()
        self.addNameItem()
        self.update_items_positions()
  
    def update_rect(self):
        """
        used to set center of circle as the anchor so the shape resizes about it and not the top left corner
        """
        rect = QRectF(0, 0, 2 * self.radius, 2 * self.radius)
        rect.moveCenter(self.rect().center())
        self.setRect(rect)

    def addItems(self):
        """
        adds grip items and the name item to parent
        """
        if self.scene() and not self.m_items:
            for i, (direction) in enumerate(
                (
                    Qt.Vertical,
                    Qt.Horizontal,
                    Qt.Vertical,
                    Qt.Horizontal,
                    Qt.AlignHCenter
                )
            ):
                if i == 4:
                    item = ItemName(self.label, i)
                else:
                    item = DirectionGripItem(self, direction, i)
                self.scene().addItem(item)
                self.m_items.append(item)

        
    def movePoint(self, i, p):
        """
        moves grip items and name label for the circle
        """
        if 0 <= i < min(5, len(self.m_items)):
            item_selected = self.m_items[i]
            lp = self.mapFromScene(p)
            self._radius = (lp - self.rect().center()).manhattanLength()
            k = self.indexOf(lp)
            if k is not None:
                self.m_items = [item for item in self.m_items if not item.isSelected()]
                self.m_items.insert(k, item_selected)
                self.update_items_positions([k])
                self.update_rect()
        

    def update_items_positions(self, index_no_updates=None):
        """
        updates name label, lines, grip items
        """
        index_no_updates = index_no_updates or []
        for i, (item, direction) in enumerate(
            zip(
                self.m_items,
                (
                    Qt.Vertical,
                    Qt.Horizontal,
                    Qt.Vertical,
                    Qt.Horizontal,
                    Qt.AlignCenter,
                ),
            ),
        ):
            item.m_index = i
            if i not in index_no_updates:
                item = self.m_items[i]
                if i != 4:
                    pos = self.mapToScene(self.point(i))
                else: 
                    pos = self.pos() - QPointF(15, 13.5)
                item._direction = direction
                item.setEnabled(False)
                item.setPos(pos)
                item.setEnabled(True)
        for line, ref  in self.lineItems:
            line.setEnabled(False)
            line.setLine(self.pos().x(), self.pos().y(), ref.pos().x(), ref.pos().y())
            line.setEnabled(True)
            
    def indexOf(self, p):
        """
        behaves as an iterator over grip items positions relative to the circle
        """
        for i in range(4):
            if p == self.point(i):
                return i

    def point(self, index):
        """
        yields a list of positions of grip items in a circle
        """
        if 0 <= index < 4:
            return [
                QPointF(0, -self.radius),
                QPointF(self.radius, 0),
                QPointF(0, self.radius),
                QPointF(-self.radius, 0),
            ][index]

    def itemChange(self, change, value):
        """
        Overloads and extends QGraphicsEllipseItem to also update gripitem, label and line positions
        """
        if change == QGraphicsItem.ItemPositionHasChanged:
            self.update_items_positions()
            return
        if change == QGraphicsItem.ItemSceneHasChanged:
            self.addItems()
            self.update_items_positions()
            return
        return super(Circle, self).itemChange(change, value)

    def hoverEnterEvent(self, event):
        """
        Enables highlighting on mouseOver
        """
        self.setBrush(QColor(255, 0, 0, 100))
        super(Circle, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        """
        Clears highlighting on mouse Leave
        """
        self.setBrush(QBrush(Qt.NoBrush))
        super(Circle, self).hoverLeaveEvent(event)
        
    def addLine(self, cir2):
        """
        Adds a line to parent and reference circle when called with reference to another circle taken as an argument 
        """
        line = ConLine(self, cir2)
        self.scene().addItem(line)
        line.addNameItem() 
        self.lineItems.append([line, cir2])
        cir2.lineItems.append([line, self])
