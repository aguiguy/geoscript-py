from java import awt
from java.awt import image
from javax import swing
from geoscript import geom, proj, style 
from org.geotools.geometry.jts import ReferencedEnvelope
from org.geotools.swing import JMapPane,StatusBar
from org.geotools.swing.action import PanAction, ZoomInAction, ZoomOutAction, ResetAction
from org.geotools.map import DefaultMapContext, DefaultMapLayer
from org.geotools.renderer.lite import StreamingRenderer

class MapWindow:

   def __init__(self):
      pass   

   def render(self, layer, style, bounds, size, **options):
      self.map = DefaultMapContext(layer.proj._crs)
      self.map.setAreaOfInterest(bounds)

      self.map.addLayer(DefaultMapLayer(layer._source, style._style()))

      w,h = (size[0], size[1]) 

      hints = {}
      hints [awt.RenderingHints.KEY_ANTIALIASING] = awt.RenderingHints.VALUE_ANTIALIAS_ON
      
      renderer = StreamingRenderer()
      renderer.java2DHints = awt.RenderingHints(hints)

      mappane = JMapPane(renderer, self.map)
      mappane.size = (w,h) 
      mappane.visible = True

      f = Frame(mappane)
      f.setSize(w,h)
      f.setVisible(True)

   def dispose(self):
      if self.map:
         self.map.dispose()

class Frame(swing.JFrame):

   def __init__(self, mappane):
      self.init(mappane)

   def init(self,mappane):
      self.add(mappane,awt.BorderLayout.CENTER)
      self.add(StatusBar(mappane), awt.BorderLayout.SOUTH)
            
      toolBar = swing.JToolBar()
      toolBar.setOrientation(swing.JToolBar.HORIZONTAL)
      toolBar.setFloatable(False)

      cursorToolGrp = swing.ButtonGroup()
      zoomInBtn = swing.JButton(ZoomInAction(mappane))
      toolBar.add(zoomInBtn)
      cursorToolGrp.add(zoomInBtn)

      zoomOutBtn = swing.JButton(ZoomOutAction(mappane))
      toolBar.add(zoomOutBtn)
      cursorToolGrp.add(zoomOutBtn)

      toolBar.addSeparator()

      panBtn = swing.JButton(PanAction(mappane))
      toolBar.add(panBtn)
      cursorToolGrp.add(panBtn)

      toolBar.addSeparator()

      resetBtn = swing.JButton(ResetAction(mappane))
      toolBar.add(resetBtn)

      self.add( toolBar, awt.BorderLayout.NORTH )
