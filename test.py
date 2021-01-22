#!/usr/bin/python
from z3 import *
# unsat means pass verification
# sat means failed verification

# sat means verification succeed
# unsat means verfication failed
def declassifyBranchCondition(vars, constrain, leakage):
    return  ForAll(vars, Implies(constrain, leakage))

# def declassifyThenBranch(vars, constrain, leakage):
#     return ForAll(vars, Implies(constrain, leakage)) 

# def declassifyElseBranch(vars, constrain, leakage):
#     return ForAll(vars, Implies(constrain, Not(leakage))) 

def check(s):
    if (s.check()):
        print("SAT")
    else:
        print("UNSAT")

x = (Int('x'))
y = (Int('y'))
z = (Int('z'))
inputs = [x,y,z]
constrain = And(z > x, z > y)
s = Solver()
s.add(x > 0)
s.add(y > 0)
s.add(z > 0)
s.add(constrain)
l = x
leakage = l < y
s.push()
s.add(
    If(
        l < y, 
        declassifyBranchCondition(inputs, constrain, leakage), 
        declassifyBranchCondition(inputs, constrain, Not(leakage))))
print(s)
print(s.check())
s.pop(num=1)

s.push()
leakage = l < z
s.add(
    If(l < z, 
    declassifyBranchCondition(inputs, constrain, leakage), 
    declassifyBranchCondition(inputs, constrain, Not(leakage))))
print(s)
print(s.check())
s.pop(num=1)