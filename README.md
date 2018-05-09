# database-systems
Project repository for Rutgers CS539 Database Systems Implementation Spring.

# Content
#### [Online Flight Reservation System](https://github.com/nromano7/database-systems/tree/master/Project%201%20-%20Online%20Flight%20Reservation%20System)  

Design and implement a relational database system to support the operations of an online travel reservation system that will allow
customers to use the web to browse/search the contents of your database and to make flight reservations over the web.

Built using: [Django](https://docs.djangoproject.com/en/2.0/), [MySQL](https://www.mysql.com/), [Bootstrap](http://getbootstrap.com/)

![screenshot](https://github.com/nromano7/database-systems/blob/master/Project%201%20-%20Online%20Flight%20Reservation%20System/screenshots/landing_page.PNG)

#### [BCNF Decomposition](https://github.com/nromano7/database-systems/tree/master/Project%202%20-%20BCNF%20Decomposition)  

Write a program, using an object oriented programming language, that takes as input a file with a relation (set of attributes R) and a set of functional dependencies and satisfies the following use cases:
1. Return all non-trivial functional dependencies that can be obtained from the ones in the file (the closure of the set of functional dependencies, F+)
1. Determine the functional dependencies which are BCNF violations and return the result.
1. Performs the BCNF decomposition of a given relation and a set of functional dependencies using the algorithm discussed in class and return the resulting tables in BCNF.

Implemented in Python. Sample code from dbtools.py :

```python
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



```
