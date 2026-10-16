"""Authoring-only Qt path stroker: GTK3 symbolic loaders discard SVG strokes.

PySide6 is needed only to regenerate sources. The committed filled SVG artwork
builds and installs using Python's standard library alone.
"""
from PySide6.QtCore import QByteArray, QRectF, Qt
from PySide6.QtGui import QPaintDevice, QPaintEngine, QPainter, QPainterPath, QPainterPathStroker
from PySide6.QtSvg import QSvgRenderer


class OutlineEngine(QPaintEngine):
    def __init__(self):
        super().__init__(QPaintEngine.PaintEngineFeature.AllFeatures)
        self.outline = QPainterPath()

    def begin(self, device):
        return True

    def end(self):
        return True

    def type(self):
        return QPaintEngine.Type.User

    def updateState(self, state):
        self.pen = state.pen()
        self.brush = state.brush()
        self.transform = state.transform()

    def drawPath(self, path):
        filled = QPainterPath()
        if self.brush.style() != Qt.BrushStyle.NoBrush and self.brush.color().alpha() > 0:
            filled = path
        if self.pen.style() != Qt.PenStyle.NoPen and self.pen.color().alpha() > 0:
            stroker = QPainterPathStroker()
            stroker.setWidth(self.pen.widthF())
            stroker.setCapStyle(self.pen.capStyle())
            stroker.setJoinStyle(self.pen.joinStyle())
            stroker.setMiterLimit(self.pen.miterLimit())
            filled = filled.united(stroker.createStroke(path))
        self.outline = self.outline.united(self.transform.map(filled))

    def drawPolygon(self, points, mode):
        path = QPainterPath()
        if not points:
            return
        path.moveTo(points[0])
        for point in points[1:]:
            path.lineTo(point)
        if mode != QPaintEngine.PolygonDrawMode.PolylineMode:
            path.closeSubpath()
        self.drawPath(path)

    def drawEllipse(self, rect):
        path = QPainterPath()
        path.addEllipse(QRectF(rect))
        self.drawPath(path)

    def drawRects(self, rects):
        for rect in rects:
            path = QPainterPath()
            path.addRect(QRectF(rect))
            self.drawPath(path)


class OutlineDevice(QPaintDevice):
    def __init__(self):
        super().__init__()
        self.engine = OutlineEngine()

    def paintEngine(self):
        return self.engine

    def metric(self, kind):
        return {QPaintDevice.PaintDeviceMetric.PdmWidth: 16, QPaintDevice.PaintDeviceMetric.PdmHeight: 16,
                QPaintDevice.PaintDeviceMetric.PdmDpiX: 96, QPaintDevice.PaintDeviceMetric.PdmDpiY: 96,
                QPaintDevice.PaintDeviceMetric.PdmPhysicalDpiX: 96, QPaintDevice.PaintDeviceMetric.PdmPhysicalDpiY: 96,
                QPaintDevice.PaintDeviceMetric.PdmDepth: 32, QPaintDevice.PaintDeviceMetric.PdmDevicePixelRatio: 1,
                QPaintDevice.PaintDeviceMetric.PdmDevicePixelRatioScaled: 65536}.get(kind, 0)


def outline(svg):
    device = OutlineDevice()
    renderer = QSvgRenderer(QByteArray(svg.encode()))
    if not renderer.isValid():
        raise ValueError("Cannot outline invalid symbolic SVG")
    painter = QPainter(device)
    renderer.render(painter, QRectF(0, 0, 16, 16))
    painter.end()
    path = device.engine.outline.simplified()
    if path.isEmpty():
        raise ValueError("Symbolic artwork has no filled outline")
    commands, i = [], 0
    while i < path.elementCount():
        el = path.elementAt(i)
        if el.isMoveTo():
            commands.append(f"M{el.x:.4f} {el.y:.4f}")
        elif el.isLineTo():
            commands.append(f"L{el.x:.4f} {el.y:.4f}")
        elif el.isCurveTo():
            b, c = path.elementAt(i + 1), path.elementAt(i + 2)
            commands.append(f"C{el.x:.4f} {el.y:.4f} {b.x:.4f} {b.y:.4f} {c.x:.4f} {c.y:.4f}")
            i += 2
        i += 1
    return ''.join(commands)
