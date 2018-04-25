from itertools import chain, combinations
from numpy import array

class Relation:
  """The Relation class gives an object representing a relation between a set of attributes."""

  _ASCII_TABLE = [chr(i) for i in range(127)]

  def __init__(self,A):
    self.A = A

  def toString(self):
    """Returns a string representation of the Relation instance."""
    bool_index = array(self.A).astype(bool)
    relation_string = array(self._ASCII_TABLE)[bool_index]
    return ''.join(relation_string)
  
  def equals(self,r):
    """Returns True if Relation instance equals Relation argument 'r', False otherwise."""
    if not isinstance(r,Relation):
      raise TypeError('Inappropriate argument type')
    return self.A == r.A

  def contains(self,c):
    """Returns True if Relation contains character argument 'c', False otherwise."""
    if not isinstance(c,str):
      raise TypeError('Inappropriate argument type')
    relation_string = self.toString()
    relation_contains_c = c in relation_string
    return relation_contains_c

  def isSubset(self,r):
    """Returns True if Relation is a subset of the Relation argument 'r', False otherwise."""
    if not isinstance(r,Relation):
      raise TypeError('Inappropriate argument type')
    relation_is_subset = set(self.toString()).issubset(set(r.toString()))
    return relation_is_subset

  @property
  def powerset(self):
    relation_string = self.toString()
    relation_elements = list(relation_string)
    c = chain.from_iterable(combinations(relation_elements, r) for r in range(1,len(relation_elements)+1))
    powerset = [''.join(i) for i in c]
    return powerset

  def powerSetFirst(self):
    """Returns string representation of the first element in the power set of the Relation."""
    return self.powerset[0]
    
  def powerSetNext(self):
    """Returns string representation of the next element in the power set of the Relation."""
    try:
      return next(self._powerset)
    except AttributeError:
      self._powerset = (i for i in self.powerset)
      return next(self._powerset)
    
  def union(self,r):
    """Returns the union of the Relation instance and the Relation argument 'r'."""
    if not isinstance(r,Relation):
      raise TypeError('Inappropriate argument type')
    r1 = set(self.toString())
    r2 = set(r.toString())
    union = ''.join(sorted(r1.union(r2)))
    return union

  def intersect(self,r):
    """Returns the intersection of the Relation instance and the Relation argument 'r'."""
    if not isinstance(r,Relation):
      raise TypeError('Inappropriate argument type')
    r1 = set(self.toString())
    r2 = set(r.toString())
    intersection = ''.join(sorted(r1.intersection(r2)))
    return intersection

#TODO: methods have to return relation object

# Testing
A = [0]*127
A[65:68] = [1,1,1,] #ABC
B = [0]*127
B[65:69] = [1,1,1,1,] #ABCD
C = [0]*127
C[65:70] = [1,1,1,1,1,] #ABCDE

r1 = Relation(A)
r2 = Relation(A)
r3 = Relation(B)
r4 = Relation(C)

print(r1.toString()) # should return ABC
print(r2.toString()) # should return ABC
print(r3.toString()) # should return ABCD
print(r4.toString()) # should return ABCDE

print(r1.equals(r2)) # should return True
print(r2.equals(r1)) # should return True
print(r3.equals(r1)) # should return False
print(r1.equals(r3)) # should return False

print(r2.contains('A')) # should return True
print(r2.contains('D')) # should return False
print(r3.contains('D')) # should return True
print(r4.contains('E')) # should return True

print(r1.isSubset(r2)) # should return True
print(r2.isSubset(r3)) # should return True
print(r3.isSubset(r2)) # should return False
print(r3.isSubset(r4)) # should return True


class FunctionalDependency:
  """The FunctionalDependency class gives an object that represents a functional dependency of two relations."""
  
  def __init__(self,r1,r2):
    if not isinstance(r1,Relation) or not isinstance(r2,Relation):
      raise TypeError('Inappropriate argument type')
    self.lhs = r1
    self.rhs = r2

  def toString(self):
    """Returns a string representation of the FunctionalDependency instance."""
    fd_string = f'{self.lhs.toString()}-->{self.rhs.toString()}'
    return fd_string

  def BCNFviolation(self,r):
    if not isinstance(r,Relation):
      raise TypeError('Inappropriate argument type')
    pass 

  def getLHS(self):
    """Returns the Relation instance on the left hand side of the functional dependency."""
    return self.lhs

  def getRHS(self):
    """Returns the Relation instance on the right hand side of the functional dependency."""
    return self.rhs

fd1 = FunctionalDependency(r1,r3)
fd2 = FunctionalDependency(r2,r4)

print(fd1.toString()) # should return ABC-->ABCD
print(fd2.toString()) # should return ABC-->ABCDE

class FunctionalDependencyList(list):
  """A list of FunctionalDependency objects."""

  def toString(self):
    """Returns a string representation of all FunctionalDependency objects."""
    fdlist_string = str(sorted([item.toString() for item in self]))
    return fdlist_string

  def insert(self,f):
    """Inserts a FunctionalDependency into the FunctionalDependencyList."""
    if not isinstance(f,FunctionalDependency):
      raise TypeError('Inappropriate argument type')
    self.append(f)

  def getFirst(self):
    """Returns the first FunctionalDependency object in the list."""
    return self.pop(0)

  def getNext(self):
    """Returns the next FunctionalDependency object in the list."""
    return self.pop(0)

  def closure(self,r):
    if not isinstance(r,Relation):
      raise TypeError('Inappropriate argument type')
    pass

fdlist = FunctionalDependencyList()
fdlist.insert(fd1)
fdlist.insert(fd2)

print(fdlist.toString()) # should return ['ABC-->ABCD', 'ABC-->ABCDE']

print(fdlist.getFirst().toString()) # should return ABC-->ABCD
print(fdlist.getNext().toString()) # should return ABC-->ABCDE

class RelationList(list):
  """A list of Relation objects."""
  
  def toString(self):
    """Returns a string representation of all Relation objects."""
    rlist_string = str(sorted([item.toString() for item in self]))
    return rlist_string

  def insert(self,r):
    """Inserts a FunctionalDependency into the FunctionalDependencyList."""
    if not isinstance(r,Relation):
      raise TypeError('Inappropriate argument type')
    self.append(r)

  def getFirst(self):
    """Returns the first Relation object in the list."""
    return self.pop(0)

  def getNext(self):
    """Returns the next Relation object in the list."""
    return self.pop(0)


rlist = RelationList()
rlist.insert(r1)
rlist.insert(r2)
rlist.insert(r3)
rlist.insert(r4)

print(rlist.toString()) # should return ['ABC', 'ABC', 'ABCD', 'ABCDE']

print(rlist.getFirst().toString()) # should return ABC
print(rlist.getNext().toString()) # should return ABC
print(rlist.getNext().toString()) # should return ABCD
print(rlist.getNext().toString()) # should return ABCDE
