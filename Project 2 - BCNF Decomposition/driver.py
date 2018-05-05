from dbtools import FunctionalDependency, FunctionalDependencyList, Relation, RelationList

# Read the input file
with open('./test2.txt') as f:
  fdlist = FunctionalDependencyList()
  is_first_line = True
  for line in f:
    if is_first_line: 
      # read relation from first line
      A = line.strip().split(' ')
      R = Relation(A)
      is_first_line = False
    else:
      # create list of functional dependencies from remaining lines
      lhs = Relation(line.split('->')[0].strip().split())
      rhs = Relation(line.split('->')[1].strip().split())
      fdlist.insert(FunctionalDependency(lhs,rhs))

print("-"*10 + ' File Read ' + "-"*10)
print('R = ' + R.toString())
print('FD = ' + fdlist.toString())
print("-"*(20+len(' File Read ')))

# compute complete list of functional dependencies
completeF = FunctionalDependencyList()
new_rel = R.powerSetFirst()
while new_rel is not None:
  closure = fdlist.closure(new_rel)
  # print(f'{closure.toString()}')
  if not new_rel.equals(closure):
    completeF.insert(FunctionalDependency(new_rel,closure))
    # print(f'{completeF.toString()}')
  new_rel = R.powerSetNext()

print("-"*10 + ' Closure of FD ' + "-"*10)
[print(f.toString()) for f in completeF]
print("-"*(20+len(' Closure of FD ')))

# compute superkeys
print("-"*10 + ' Superkeys ' + "-"*10)
superkeys = FunctionalDependencyList()
compF = FunctionalDependencyList()
[compF.insert(f) for f in completeF]
my_fd = compF.getFirst()
while my_fd is not None:
  lhs = my_fd.getLHS().union(my_fd.getRHS())
  if R.isSubset(lhs):
    superkeys.insert(my_fd)
    print(f"superkey: {my_fd.toString()}")
  my_fd = compF.getNext()
print("-"*(20+len(' Superkeys ')))

# compute keys
print("-"*10 + ' Keys ' + "-"*10)
keys = RelationList()
my_fd = superkeys.getFirst()
previous = len(R.toString())
while my_fd is not None:
  lhs = my_fd.getLHS()
  if len(lhs.toString()) <= previous:
    keys.insert(lhs)
    print(f'key: {lhs.toString()}')
    previous = len(lhs.toString())
  my_fd = superkeys.getNext()
print("-"*(20+len(' Keys ')))

# find all bcnf violations
print("-"*10 + ' BCNF Violations ' + "-"*10)
compF = FunctionalDependencyList()
[compF.insert(f) for f in completeF]
violations = FunctionalDependencyList()
fd = compF.getFirst()
while fd is not None:
  if fd.BCNFviolation(R):
    violations.insert(fd)
    print(f"BCNF Violation: {fd.toString()}")
  fd = compF.getNext()
if len(violations) == 0:
  print(None)
print("-"*(20+len(' BCNF Violations ')))

# BCNF decomposition
db = RelationList()
s = []
s.append(R)
isEmpty = False
while len(s) > 0:
  a = s.pop()
  violation = False
  f = fdlist.getFirst()
  while ((not violation) and (f is not None)):
    if f.BCNFviolation(a):
      violation = True
    else:
      f = fdlist.getNext()			
  if (not violation):
    print(a.toString())
    print(f'--- inserted --- ({a.toString()})')
    db.insert(a)
  elif (f is not None):
    # X = f.getLHS()
    # Y = completeF.closure(X) - X
    # XY = X.union(Y)
    # Z = a - XY
    # XZ = X.union(Z)
    # s.append(XY)
    # s.append(XZ)
    x = f.getLHS()
    y = f.getRHS().intersect(a)
    xy = x.union(y)
    s.append(xy)
    s.append(a - f.getRHS())
    print("--------------------------")
    print(f'R = {a.toString()}')
    print(f'{x.toString()} -> {y.toString() if (y is not None) else None}')
    print([i.toString() for i in s])
    print("--------------------------")

print("------------- Tables in BCNF ----------------")
print(db.toString())
print("---------------------------------------------")