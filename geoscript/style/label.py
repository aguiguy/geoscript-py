from geoscript.style import util
from geoscript.style.symbolizer import Symbolizer
from geoscript.style.font import Font
from geoscript.style.halo import Halo
from org.geotools.styling import TextSymbolizer

class Label(Symbolizer):
  """
  Symbolizer for labelling a geometry. 

  The ``property`` argument specifies the field or attribute with which to generate
  labels from.

  >>> Label('foo')
  Label(property=foo)
  """

  def __init__(self, property):
    Symbolizer.__init__(self)
    self.property = property
    self._font = None
    self._halo = None
    self._placement = None
    self.options = {}

  def font(self, font):
    """
    Sets the font for this label. The ``font`` argument is a string describing the
    font attributes. See :class:`Font <geoscript.style.font.Font>` for supported 
    syntax.

    >>> label = Label('foo').font('italic bold 12px "Times New Roman"')
    """

    self._font = Font(font)
    return self

  def halo(self, fill=None, radius=None):
    """
    Generates a halo for this label.  

    The ``fill`` and ``radius`` arguments specify the :class:`Fill` and radius to 
    use for the halo.
   
    >>> from geoscript.style import Fill
    >>> label = Label('foo').halo(Fill('#ffffff'), 2)
    """
    self._halo = Halo(fill, radius)
    return self

  def point(self, anchor=(0.5,0.5), displace=(0,0), rotate=0):
    """
    Sets the label placement relative to a point. 

    The ``anchor`` argument is a tuple that specifies how the label should be 
    anchored along an xy axis relative to the geometry being labeled. Allowable
    values range from (0,0) to (1,1) ordered from the bottom left corner to the top
    right corner of the label. 

    The ``displacement`` argument is a tuple that specifies how the label should be
    displaced along an xy axis. 

    The ``rotate`` argument specifies in degrees the angle at which to rotate the 
    label. 

    >>> label = Label('foo').point((0.5,0), (0,5))
    """
    f = self.factory
    ap = f.createAnchorPoint(self._literal(anchor[0]), self._literal(anchor[1]))
    dp = f.createDisplacement(self._literal(displace[0]), self._literal(displace[1]))
    self._placement = f.createPointPlacement(ap, dp, self._literal(rotate))
    return self

  def linear(self, offset=0, gap=None, igap=None, align=False, follow=False, 
             displace=None, repeat=None):
    """
    Sets the label placement relative to a line. 

    The ``offset`` argument specifies the perpindicular distance from the line at
    which to position the label. 

    The ``align`` argument specifies whether to align the label along the line. The
    ``follow`` argument specifies whether to curve the label in order to force it
    to follow the line. 
    
    >>> label = Label('foo').linear(align=True, follow=True)
    """
    f = self.factory
    lp = f.createLinePlacement(self._literal(offset))
    lp.setAligned(align)
    #lp.setRepeated(repeat)
    if gap:   
      lp.setGap(self._literal(gap))
    if igap:
      lp.setInitialGap(self._literal(gap))
    self._placement = lp

    self.options = {"followLine": follow}
    if displace:
      self.options['maxDisplacement'] = displace
    if repeat:
      self.options['repeat'] = repeat
    return self

  def _prepare(self, rule):
    syms = util.symbolizers(rule, TextSymbolizer)
    for sym in syms:
      self._apply(sym)

  def _apply(self, sym):
    sym.setLabel(self.factory.filter.property(self.property))

    if self._font:
      self._font._apply(sym)
    if self._halo:
      self._halo._apply(sym)

    if self._placement:
      sym.setLabelPlacement(self._placement)

    for k,v in self.options.iteritems(): 
	  sym.getOptions()[k] = str(v)

  def __repr__(self):
    return self._repr('property')
