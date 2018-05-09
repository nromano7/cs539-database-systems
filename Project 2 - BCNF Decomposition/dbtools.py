from itertools import chain, combinations
from numpy import array

class Relation:

  """
  The Relation class returns an object representing a relation between a set of attributes.
  
  To initialize a Relation object, provide a list as input to the Relation class. The list can either be:

  (1) a vector of attributes labels from A-Z (e.g. ['A','B','C']) or 
  (2) a binary vector with value 1 at the ASCII code index of each attribute (e.g. someList[65] = 1 indicates attribute with label 'A')

  Example Usage:

  A = ['A','B',C]
  R = Relation(A)

  A = [0]*127 
  A[65:68] = [1,1,1,] # equivalent to ['A','B','C']
  R = Relation(A)

  """

  _ASCII_TABLE = [chr(i) for i in range(127)]

  def __init__(self,A):
    if isinstance(A[0],str):
      # for relation as string vector
      binaryA =  [0]*len(self._ASCII_TABLE)
      index = [Relation._ASCII_TABLE.index(i) for i in A]
      for i in index:
        binaryA.__setitem__(i,1)
      self.A = binaryA
    else:
      # for relation as binary vector
      self.A = A

  def toString(self):

    """
    Returns a string representation of the Relation instance.
    """

    bool_index = array(self.A).astype(bool)
    relation_string = array(self._ASCII_TABLE)[bool_index]
    return ''.join(relation_string)
  
  def equals(self,r):

    """
    Returns True if Relation instance equals Relation argument 'r', False otherwise.
    """

    if not isinstance(r,Relation):
      raise TypeError('Inappropriate argument type')
    return self.A == r.A

  def contains(self,c):

    """
    Returns True if Relation contains character argument 'c', False otherwise.
    """

    if not isinstance(c,str):
      raise TypeError('Inappropriate argument type')
    relation_string = self.toString()
    relation_contains_c = c in relation_string
    return relation_contains_c

  def isSubset(self,r):

    """
    Returns True if Relation is a subset of the Relation argument 'r', False otherwise.
    """

    if not isinstance(r,Relation):
      raise TypeError('Inappropriate argument type')
    relation_is_subset = set(self.toString()).issubset(set(r.toString()))
    return relation_is_subset

  @property
  def powerset(self):
    relation_string = self.toString()
    relation_elements = list(relation_string)
    c = chain.from_iterable(combinations(relation_elements, r) for r in range(1,len(relation_elements)+1))
    powerset = RelationList()
    for i in c:
      powerset.insert(Relation(i))
    return powerset

  def powerSetFirst(self):

    """
    Returns the first element in the power set of the Relation.
    """

    try:
      return next(self._powerset)
    except AttributeError:
      self._powerset = (i for i in self.powerset)
      return next(self._powerset)
    except StopIteration:
      return None
    
  def powerSetNext(self):

    """
    Returns the next element in the power set of the Relation.
    """

    try:
      return next(self._powerset)
    except AttributeError:
      self._powerset = (i for i in self.powerset)
      return next(self._powerset)
    except StopIteration:
      return None
    
  def union(self,r):

    """
    Returns a new Relation objct which is the union of the Relation instance and the Relation argument 'r'.
    """
    if r is None:
      return self

    if not isinstance(r,Relation):
      raise TypeError('Inappropriate argument type')

    r1 = set(self.toString())
    r2 = set(r.toString())
    union = ''.join(sorted(r1.union(r2)))
    return Relation(list(union))

  def intersect(self,r):

    """
    Returns a new Relation object which is the intersection of the Relation instance and the Relation argument 'r'.
    """

    if not isinstance(r,Relation):
      raise TypeError('Inappropriate argument type')
    r1 = set(self.toString())
    r2 = set(r.toString())
    intersection = ''.join(sorted(r1.intersection(r2)))
    if intersection == '':
      return None
    return Relation(list(intersection))

  def __sub__(self,r):

    """
    Returns the set difference between two relations.
    """

    if not isinstance(r,Relation):
      raise TypeError('Inappropriate argument type')
    r1 = set(self.toString())
    r2 = set(r.toString())
    difference = r1 - r2
    if not difference:
      difference = set(self.toString())
    return Relation(list(difference))


class FunctionalDependency:

  """
  The FunctionalDependency class returns an object that represents a functional dependency of two relations.

  To initialize a FunctionalDependency object, provide two valid Relation objects.

  Example usage:

  AB, C  = ['A','B'], ['C']
  r1, r2 = Relation(AB), Relation(C)
  fd = FunctionalDependency(r1,r2)

  """
  
  def __init__(self,r1,r2):
    if not isinstance(r1,Relation) or not isinstance(r2,Relation):
      raise TypeError('Inappropriate argument type')
    self.lhs = r1
    self.rhs = r2

  def toString(self):

    """
    Returns a string representation of the FunctionalDependency instance.
    """

    fd_string = f'{self.lhs.toString()}-->{self.rhs.toString()}'
    return fd_string

  def BCNFviolation(self,r):

    """ 
    Returns True if Functional Dependency is a BCNF violation for given Relation, False otherwise.
    """

    if not isinstance(r,Relation):
      raise TypeError('Inappropriate argument type')
    
    if not r.isSubset(self.getLHS().union(self.getRHS())):
      return True

    return False
    

  def getLHS(self):

    """
    Returns the Relation object on the left hand side of the functional dependency.
    """

    return self.lhs

  def getRHS(self):

    """
    Returns the Relation object on the right hand side of the functional dependency.
    """

    return self.rhs


class FunctionalDependencyList(list):

  """
  A class for creating a list of FunctionalDependency objects.
  """

  def toString(self):

    """
    Returns a string representation of all FunctionalDependency objects.
    """

    fdlist_string = str(sorted([item.toString() for item in self]))
    return fdlist_string

  def insert(self,f):

    """
    Inserts a FunctionalDependency object into the FunctionalDependencyList.
    """

    if not isinstance(f,FunctionalDependency):
      raise TypeError('Inappropriate argument type')
    self.append(f)

  def getFirst(self):

    """
    Returns the first FunctionalDependency object in the list.
    """

    try:
      return self.pop(0)
    except IndexError:
      return None

  def getNext(self):

    """
    Returns the next FunctionalDependency object in the list.
    """

    try:
      return self.pop(0)
    except IndexError:
      return None

  def closure(self,r):

    """
    Returns a new Relation object which is the closure for the set of Functional Dependencies.
    """

    if not isinstance(r,Relation):
      raise TypeError('Inappropriate argument type')

    closure = r
    diff = True
    while diff:
      previous = closure
      for fd in self:
        lhs = fd.getLHS()
        if lhs.isSubset(closure):
          previous = closure
          rhs = fd.getRHS()
          closure = closure.union(rhs) #- r
      if closure.equals(previous):
        diff = False
    return closure - r


class RelationList(list):

  """
  A list of Relation objects.
  """
  
  def toString(self):

    """
    Returns a string representation of all Relation objects.
    """

    rlist_string = str(sorted([item.toString() for item in self]))
    return rlist_string

  def insert(self,r):

    """
    Inserts a Relation object into the RelationList.
    """

    if not isinstance(r,Relation):
      raise TypeError('Inappropriate argument type')
    self.append(r)

  def getFirst(self):

    """
    Returns the first Relation object in the list, or None if one does not exist.
    """

    try:
      return self.pop(0)
    except IndexError:
      return None

  def getNext(self):

    """
    Returns the next Relation object in the list, or None if one does not exist.
    """

    try:
      return self.pop(0)
    except IndexError:
      return None

