import random
from string import ascii_uppercase

from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtGui import QBrush, QColor, QCursor, QPainter, QPainterPath, QPen
from PyQt5.QtWidgets import (QGraphicsEllipseItem, QGraphicsItem,
                             QGraphicsLineItem, QGraphicsPathItem,
                             QGraphicsTextItem)


class GripItem(QGraphicsPathItem):
    circle = QPainterPath()
    circle.addEllipse(QRectF(-5, -5, 10, 10))

    def __init__(self, annotation_item, index):
        super(GripItem, self).__init__()
        self.m_annotation_item = annotation_item
        self.m_index = index

        self.setPath(GripItem.circle)
        self.setPen(QPen(QColor(),-1))  
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)
        self.setZValue(11)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def hoverEnterEvent(self, event):
        self.setPen(QPen(QColor("black"), 2))
        self.setBrush(QColor("red"))
        super(GripItem, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setPen(QPen(Qt.transparent))
        self.setBrush(Qt.transparent)   
        super(GripItem, self).hoverLeaveEvent(event)

    def mouseReleaseEvent(self, event):
        self.setSelected(False)
        super(GripItem, self).mouseReleaseEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange and self.isEnabled():
            self.m_annotation_item.movePoint(self.m_index, value)
        return super(GripItem, self).itemChange(change, value)
   
class DirectionGripItem(GripItem):
    def __init__(self, annotation_item, direction=Qt.Horizontal, parent=None):
        super(DirectionGripItem, self).__init__(annotation_item, parent)
        self._direction = direction

    @property
    def direction(self):
        return self._direction
    
    def hoverEnterEvent(self, event):
        if self._direction == Qt.Horizontal:
            self.setCursor(QCursor(Qt.SizeHorCursor))
        else:
            self.setCursor(QCursor(Qt.SizeVerCursor))
        super(DirectionGripItem, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))
        super(DirectionGripItem, self).hoverLeaveEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange and self.isEnabled():
            p = QPointF(self.pos())
            if self.direction == Qt.Horizontal:
                p.setX(value.x())
            elif self.direction == Qt.Vertical:
                p.setY(value.y())
            self.m_annotation_item.movePoint(self.m_index, p)
            return p
        return super(DirectionGripItem, self).itemChange(change, value)

      
class itemName(QGraphicsTextItem):
    def __init__(self, label, index, parent=None):
        super(itemName, self).__init__(label, parent)
        self.m_index = index
        self.setZValue(11)
        self.setDefaultTextColor(Qt.black)
        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.adjustSize()
        self.setTextWidth(-1)
    
    def hoverEnterEvent(self, event):
        self.setCursor(QCursor(Qt.IBeamCursor))
        super(itemName, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))
        super(itemName, self).hoverLeaveEvent(event)
    
class conLine(QGraphicsLineItem):
    def __init__(self, cir1, cir2, parent=None):
        super(conLine, self).__init__(cir1.pos().x(), cir1.pos().y(), cir2.pos().x(), cir2.pos().y(), parent=parent)
        self.setZValue(11)
        self.label = f'con{random.choice(ascii_uppercase)}'
        self.ref1 = cir1
        self.ref2 = cir2
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        self.nameItem = None
     
    def setLine(self, x1, y1, x2, y2):
        super(conLine, self).setLine(x1, y1, x2, y2)
        self.updateAlignment()
    
    def addNameItem(self):
        if self.scene() and not self.nameItem:
            nameItem = itemName(self.label, 1)
            self.scene().addItem(nameItem)
            self.nameItem = nameItem
            
        self.updateAlignment()

    def updateAlignment(self):
        nameItem = self.nameItem
        line = self.line()
        angle = line.angle()
        nameItem.setEnabled(False)
        nameItem.setPos(line.center())
        nameItem.setRotation(180-angle if 90<angle<=270 else -angle)
        nameItem.setEnabled(True)
        
class Circle(QGraphicsEllipseItem):
    
    def __init__(self, radius=None, name=None, x=0, y=0, parent=None):
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
        return self._radius
    

    @radius.setter
    def radius(self, r):
        if r <= 0:
            raise ValueError("radius must be positive")
        self._radius = r
        self.update_rect()
        self.addItems()
        self.addNameItem()
        self.update_items_positions()
  
    def update_rect(self):
        rect = QRectF(0, 0, 2 * self.radius, 2 * self.radius)
        rect.moveCenter(self.rect().center())
        self.setRect(rect)

    def addItems(self):
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
                    item = itemName(self.label, i)
                else:
                    item = DirectionGripItem(self, direction, i)
                self.scene().addItem(item)
                self.m_items.append(item)

        
    def movePoint(self, i, p):
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
        for line,ref  in self.lineItems:
            line.setEnabled(False)
            line.setLine(self.pos().x(), self.pos().y(), ref.pos().x(), ref.pos().y())
            line.setEnabled(True)
            
    def indexOf(self, p):
        for i in range(4):
            if p == self.point(i):
                return i

    def point(self, index):
        if 0 <= index < 4:
            return [
                QPointF(0, -self.radius),
                QPointF(self.radius, 0),
                QPointF(0, self.radius),
                QPointF(-self.radius, 0),
            ][index]

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            self.update_items_positions()
            return
        if change == QGraphicsItem.ItemSceneHasChanged:
            self.addItems()
            self.update_items_positions()
            return
        return super(Circle, self).itemChange(change, value)

    def hoverEnterEvent(self, event):
        self.setBrush(QColor(255, 0, 0, 100))
        super(Circle, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(QBrush(Qt.NoBrush))
        super(Circle, self).hoverLeaveEvent(event)
        
    def addLine(self, cir2):
        line = conLine(self, cir2)
        self.scene().addItem(line)
        line.addNameItem() 
        self.lineItems.append([line, cir2])
        cir2.lineItems.append([line, self])
