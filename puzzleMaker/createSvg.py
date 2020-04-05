
"""
    SVG file writer module:
        svgFile() -> file writer class 
        svgGroup() -> create a group of object (to apply common translation/rotation/opacity)

        Styles:
        svgFill() -> fill options
        svgStroke() -> line/stroke options

        Objects (need style(s) and are file/group.write(<object>)):
        svgRectangle
        svgCircle
        svgPolyline
        svgPath
"""

from dataclasses import dataclass, field

@dataclass
class svgFile():
    fileName: str
    size: tuple = (500,500)
    title: str = 'SVG'
    description: str = 'My SVG'

    def __enter__(self):
        self.fileHdl = open(self.fileName, 'w')
        self.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- basic SVG header -->\n')
        self.write(f'<svg width="{self.size[0]}" height="{self.size[1]}" xmlns="http://www.w3.org/2000/svg">\n')
        self.write(f'<title>{self.title}</title>\n')
        self.write(f'<desc>{self.description}</desc>\n')
        return self

    def write(self, obj):
        self.fileHdl.write(str(obj))

    def __exit__(self, type, value, tb):
        #Add footer to SVG file
        self.write('</svg>\n')
        # headerTemplate = self.env.get_template("footerTemplate")
        # self.fileHdl.write(headerTemplate.render())

        self.fileHdl.close()

@dataclass
class svgGroup():
    parent: type(svgFile)
    rotate: float = 0
    translate: tuple = (0,0)
    opacity: float = 1.0

    def __enter__(self):
        #group header
        self.write(f'<g opacity="{self.opacity}" transform="translate({self.translate[0]},{self.translate[1]}) rotate({self.rotate})">\n')
        return self

    def write(self, obj):
        self.parent.write(obj)

    def __exit__(self, type, value, tb):
        #close group when object is deleted
        self.write('</g>\n')

#For fill & stroke attributes: https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Fills_and_Strokes
#For possible colors : https://developer.mozilla.org/en-US/docs/Web/CSS/color_value#Color_keywords
#   'red'/'green'/'#<0-f = R><0-f = G><0-f = B>'/...
@dataclass
class svgFill():
    color: str = None
    opacity: float = None

    def __str__(self):
        if self.color is None:
            res = ' fill="none"'
        else:
            res = f' fill="{self.color}"'
            if self.opacity is not None:
                res += f' fill-opacity="{self.opacity}"'
        return res

@dataclass
class svgStroke():
    #todo: stroke-linecap / stroke-linejoin / stroke-dasharray
    color: str = None
    width: float = None

    def __str__(self):
        res = ''
        if self.color is not None:
            res = f' stroke="{self.color}"'
            if self.width is not None:
                res += f' stroke-width="{self.width}"'
        return res

@dataclass
class svgRectangle():
    x: float
    y: float
    width: float
    height: float
    fill: type(svgFill) = field(default_factory=svgFill)
    stroke: type(svgStroke) = field(default_factory=svgStroke)

    def __str__(self):
        res = f'<rect x="{self.x}" y="{self.y}" width="{self.width}" height="{self.height}"'
        res += str(self.fill) + str(self.stroke) + '/>\n'
        return res

@dataclass
class svgCircle():
    cx: float
    cy: float
    r: float
    fill: type(svgFill) = field(default_factory=svgFill)
    stroke: type(svgStroke) = field(default_factory=svgStroke)

    def __str__(self):
        res = f'<circle cx="{self.cx}" cy="{self.cy}" r="{self.r}"'
        res += str(self.fill) + str(self.stroke) + '/>\n'
        return res

#See https://www.w3.org/TR/SVG/shapes.html#PolylineElement
# points is a list of abs coo : [(x1,y1), (x2,y2), (x3,y3) ...]
@dataclass
class svgPolyline():
    points: list
    fill: type(svgFill) = field(default_factory=svgFill)
    stroke: type(svgStroke) = field(default_factory=svgStroke)

    def __str__(self):
        pStr = ''.join([str(x)+','+str(y)+' ' for x,y in self.points])
        res = f'<polyline points="{pStr}" '
        res += str(self.fill) + str(self.stroke) + '/>\n'
        return res

#See https://www.w3.org/TR/SVG/paths.html for d parameter format
#  Capital = abs coo, Lower case = relative move from last point
#  M/m -> move no trace
#  L/l <x> <y> -> straight line to (x,y)
#  C/c <x1> <y1> <x2> <y2> <x> <y> -> bezier from previous using (x1,x2) ctl to (x,y) point using (x2,y2) ctl
#  S/s           <x2> <y2> <x> <y> -> snooth from previous to (x,y) point using (x2,y2) ctl
#  Z/z -> close path
@dataclass
class svgPath():
    d: float
    fill: type(svgFill) = field(default_factory=svgFill)
    stroke: type(svgStroke) = field(default_factory=svgStroke)

    def __str__(self):
        dStr = ''.join([str(x)+' ' for x in self.d])
        res = f'<path d="{dStr}" '
        res += str(self.fill) + str(self.stroke) + '/>\n'
        return res


if __name__ == "__main__":
    #Example on how to use the module:

    #Create a file 
    with svgFile('test.svg', (600,500)) as s:

        #Create 2 fill/stroke styles
        fill = svgFill('red', 0.8)
        stroke = svgStroke('black',5)

        #Write a polyline
        s.write(svgPolyline([(80,50), (100,20), (30,40), (58,12)], stroke=stroke))

        #In a group
        with svgGroup(s, translate=(250,250), rotate=45) as g:

            #Create a bunch of objects
            for x in range(0,200,60):
                s.write(svgRectangle(x, 0, 20, 30, stroke=stroke))
                s.write(svgCircle(x+20, 40, 5, fill=fill))

                pathData = ['M', x, 50, 'l', 20, 30, 'l', -40, 0, 'z']
                s.write(svgPath(pathData, stroke=stroke, fill=fill))

