from dbproject2 import FunctionalDependency, FunctionalDependencyList, Relation, RelationList

# Test different inputs
A = [0]*127
A[65:68] = [1,1,1,] #ABC
B = [0]*127
B[65:69] = [1,1,1,1,] #ABCD
C = [0]*127
C[65:70] = [1,1,1,1,1,] #ABCDE
D = ['X','Y','Z']

r1 = Relation(A)
r2 = Relation(A)
r3 = Relation(B)
r4 = Relation(C)
r5 = Relation(D)

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

fd1 = FunctionalDependency(r1,r3)
fd2 = FunctionalDependency(r2,r4)

print(fd1.toString()) # should return ABC-->ABCD
print(fd2.toString()) # should return ABC-->ABCDE

fdlist = FunctionalDependencyList()
fdlist.insert(fd1)
fdlist.insert(fd2)

print(fdlist.toString()) # should return ['ABC-->ABCD', 'ABC-->ABCDE']

print(fdlist.getFirst().toString()) # should return ABC-->ABCD
print(fdlist.getNext().toString()) # should return ABC-->ABCDE

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