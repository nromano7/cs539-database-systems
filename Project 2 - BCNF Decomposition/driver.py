from dbproject2 import FunctionalDependency, FunctionalDependencyList, Relation, RelationList

# Read the input file
with open('./test.txt') as f:
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
  if not new_rel.equals(closure):
    completeF.insert(FunctionalDependency(new_rel,closure))
  new_rel = R.powerSetNext()

print("-"*10 + ' Closure of FD ' + "-"*10)
print(completeF.toString())
print("-"*(20+len(' Closure of FD ')))

# compute superkeys
print("-"*10 + ' Superkeys ' + "-"*10)
super_keys = FunctionalDependencyList()
my_fd = completeF.getFirst()
while my_fd is not None:
  lhs = my_fd.getLHS().union(my_fd.getRHS())
  if R.isSubset(lhs):
    super_keys.insert(my_fd)
    print(f"superkey: {my_fd.toString()}")
  my_fd = completeF.getNext()
print("-"*(20+len(' Superkeys ')))

