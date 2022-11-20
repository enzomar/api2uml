import enum

"""
- Association
Bicicle (*) ----- (0..1) Owner

Bycicle
type: object
  owner: string
  or 
  owner: 
    type: object
    $ref: Owner


- Aggregation
Bycile < >------- (0..2) Wheel

Bycicle
type: object
  wheels:
    type: array
      items: 
        $ref: Wheel

- Composition
Bycicle <#>------ (0..1) FramePart

Bycicle
type: object
$ref: FramePart
other: ...


"""
class LinkType(object):
  ASSO = 1
  AGG = 2
  COMP = 3


class Link(object):
  def __init__(self):
    self.desc = str()
    self.origin = None
    self.dest = None
    self.type = None #LinkType

  
  def set(self, origin, dest, type_ = None):
    self.origin = origin
    self.dest = dest
    self.type = type_


  def __str__(self):
    return "{0} {1} {2}: {3}".format(self.origin, 
      self.type, self.dest, self.desc)

  def __hash__(self):
      return hash(str(self))

  def __eq__(self,other):
      return str(self) == str(other)


