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
    d.clone = lambda : clone_datum_string (d)
    d.reclaim = lambda : reclaim_datum_string (d)    
    d.srepr = lambda : srepr_datum_string (d)
    d.raw = lambda : raw_datum_string (d)    
    d.kind = lambda : "string"
    return d

def clone_datum_string (d):
  d = new_datum_string (d.data)
  return d

def reclaim_datum_string (src):
  pass

def srepr_datum_string (d):
  return d.data

def raw_datum_string (d):
  return bytearray (d.data,'UTF-8')



def new_datum_bang ():
    p = Datum ()
    p.data = True
    p.clone = lambda : clone_datum_bang (p)
    p.reclaim = lambda : reclaim_datum_bang (p)
    p.srepr = lambda : srepr_datum_bang ()
    p.raw = lambda : raw_datum_bang ()    
    p.kind = lambda : "bang"
    return p

def clone_datum_bang (d):
    return new_datum_bang ()


def reclaim_datum_bang (d):
    pass

def srepr_datum_bang ():      
    return "!"

def raw_datum_bang ():
    return []



def new_datum_tick ():      
    p = new_datum_bang ()
    p.kind = lambda : "tick"
    p.clone = lambda : new_datum_tick ()
    p.srepr = lambda : srepr_datum_tick ()
    p.raw = lambda : raw_datum_tick ()
    return p


def srepr_datum_tick ():
    return "."


def raw_datum_tick ():      
    return []


def new_datum_bytes (b):      
    p = Datum ()
    p.data = b[:]
    p.clone = clone_datum_bytes
    p.reclaim = lambda : reclaim_datum_bytes (p)
    p.srepr = lambda : srepr_datum_bytes (b)
    p.raw = lambda : raw_datum_bytes (b)
    p.kind = lambda : "bytes"
    return p


def clone_datum_bytes (src):      
    p = Datum ()
    p = src
    p.data = src.clone ()
    return p


def reclaim_datum_bytes (src):      
    pass


def srepr_datum_bytes (d):
    return d.data.decode ('utf-8')


def raw_datum_bytes (d):
    return d.data



def new_datum_handle (h):
    return new_datum_int (h)

def new_datum_int (i):      
    p = Datum ()
    p.data = i
    p.clone = lambda : clone_int (i)
    p.reclaim = lambda : reclaim_int (i)
    p.srepr = lambda: srepr_datum_int (i)
    p.raw = lambda : raw_datum_int (i)
    p.kind = lambda : "int"
    return p


def clone_int (i):      
    p = Datum ()
    p = new_datum_int (i)
    return p


def reclaim_int (src):      
    pass

def srepr_datum_int (i):
  return str (i)

def raw_datum_int (i):      
    return i
