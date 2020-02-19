import random
from string import ascii_uppercase

from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtGui import QColor, QCursor, QPainterPath, QPen, QBrush

from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPathItem, QGraphicsEllipseItem


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

class Circle(QGraphicsEllipseItem):
    
    def __init__(self, radius=None, name=None, x=0, y=0, parent=None):
        super(Circle, self).__init__(parent)
        self.setZValue(11)
        self.m_items = []

        self.setPen(QPen(Qt.black, 2, Qt.SolidLine))

        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        self.setAcceptHoverEvents(True)

        self.setCursor(QCursor(Qt.PointingHandCursor))

        self._radius = radius or 50 + random.random() * 300
        self.label = name if name else f'cir{random.choice(ascii_uppercase)}'
        self.setPos(x or random.randint(0, 300), y or random.randint(0, 450))
        self.update_rect()
        self.add_grip_items()
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
        self.add_grip_items()
        self.update_items_positions()

    def update_rect(self):
        rect = QRectF(0, 0, 2 * self.radius, 2 * self.radius)
        rect.moveCenter(self.rect().center())
        self.setRect(rect)

    def add_grip_items(self):
        if self.scene() and not self.m_items:
            for i, (direction) in enumerate(
                (
                    Qt.Vertical,
                    Qt.Horizontal,
                    Qt.Vertical,
                    Qt.Horizontal,
                )
            ):
                item = DirectionGripItem(self, direction, i)
                self.scene().addItem(item)
                self.m_items.append(item)

    def movePoint(self, i, p):
        if 0 <= i < min(4, len(self.m_items)):
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
                ),
            ),
        ):
            item.m_index = i
            if i not in index_no_updates:
                pos = self.mapToScene(self.point(i))
                item = self.m_items[i]
                item._direction = direction
                item.setEnabled(False)
                item.setPos(pos)
                item.setEnabled(True)

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
            self.add_grip_items()
            self.update_items_positions()
            return
        return super(Circle, self).itemChange(change, value)

    def hoverEnterEvent(self, event):
        self.setBrush(QColor(255, 0, 0, 100))
        super(Circle, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(QBrush(Qt.NoBrush))
        super(Circle, self).hoverLeaveEvent(event)