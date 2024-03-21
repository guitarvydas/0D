class Datum:
  def __init__(self):
    self.data = None
    self.clone = None
    self.reclaim = None
    self.srepr = None
    self.kind = None
    self.raw = None

def new_datum_string (s):
    d = Datum ()
    d.data = s
    d.clone = clone_datum_string
    d.reclaim = reclaim_datum_string    
    d.srepr = srepr_datum_string    
    d.raw = raw_datum_string    
    d.kind = "string"
    return d

def clone_datum_string (src):
  d = Datum ()
  d = src
  return d

def reclaim_datum_string (src):
  pass

def srepr_datum_string (d):
  return d.srepr ()

def raw_datum_string (d):
  return d.data



def new_datum_bang ():
    p = Datum ()
    p.data = true
    p.clone = clone_datum_bang
    p.reclaim = reclaim_datum_bang
    p.srepr = srepr_datum_bang    
    p.raw = raw_datum_bang    
    p.kind = "bang"
    return p

def clone_datum_bang (src):      
    return new_datum_bang ()


def reclaim_datum_bang (src):      
    pass

def srepr_datum_bang (src):      
    return "!"

def raw_datum_bang (src):      
    return "!"



def new_datum_tick ():      
    p = new_datum_bang ()
    p.kind = "tick"
    p.clone = new_datum_tick
    p.raw = raw_datum_tick
    return p


def srepr_datum_tick (src):      
    return "."


def raw_datum_tick (src):      
    return "."


def new_datum_bytes (b):      
    p = Datum ()
    p.data = b.clone ()
    p.clone = clone_datum_bytes
    p.reclaim = reclaim_datum_bytes
    p.srepr = srepr_datum_v
    p.raw = raw_datum_bytes
    p.kind = "bytes"
    return p


def clone_datum_bytes (src):      
    p = Datum ()
    p = src
    p.data = src.clone ()
    return p


def reclaim_datum_bytes (src):      
    pass


def srepr_datum_v (src):      
    return src.asString ()


def raw_datum_bytes (src):      
    return src.data



def new_datum_handle (h):
    p = Datum ()
    p.data = h
    p.clone = clone_handle
    p.reclaim = reclaim_handle
    p.srepr = srepr_datum_v
    p.raw = raw_datum_handle
    p.kind = "handle"
    return p

def clone_handle (src):      
    p = Datum ()
    p = src
    return p


def reclaim_handle (src):      
    pass


def raw_datum_handle (src):      
    return src

def new_datum_int (i):      
    p = Datum ()
    p.data = i
    p.clone = clone_int
    p.reclaim = reclaim_int
    p.srepr = srepr_datum_v
    p.raw = raw_datum_int
    p.kind = "int"
    return p


def clone_int (src):      
    p = Datum ()
    p = src
    p.data = src.data
    return p


def reclaim_int (src):      
    pass


def raw_datum_int (src):      
    return src.data
