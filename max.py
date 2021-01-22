from z3 import *

x = Int("x")
y = Int("y")
z = Int("z")
l = Int("l")
constrain = And(z > x, z > y)
inputs = [x,y,z]



# Define verification function
def imply(range,lh, rh):
    return ForAll(range, Implies(lh, rh))


# 1.push track point
# 2.check constrain==>then_branch_condition
# 3.check constrain==>else_branch_condition
# 4.if no implication sat, verification failed
def declassifyBranchCondition(s, range, constrain, condition):   
    s.push()
    s.add(imply(range, constrain, condition))
    then_branch = s.check()
    s.pop(num=1)
    if (then_branch == sat):
        return 1

    s.push()
    s.add(imply(range, constrain, Not(condition)))
    else_branch = s.check()
    s.pop(num=1)
    if (else_branch == sat):
        return -1

    return 0  

def declassifyValue(s, range, constrain, value):
    s.push()
    s.add(imply(range, constrain, value))
    c = s.check()
    if ( c == sat ):
        return value 
    else:
        print("Verification falied at condition: ", value)
        return None
# raw max function
# def max(x,y,z):
#     l = x 
#     if ( l < y ):
#         l =  y 
#     if ( l < z ):
#         l = z
#     return l

# verified max function
def max(x,y,z):
    l = x
    c = declassifyBranchCondition(s, inputs, constrain, l < y)
    if (c == 1):
        l = y 
    elif ( c == -1):
        pass
    else:
        print("Verification failed at condition: l = y ")

    c = declassifyBranchCondition(s, inputs, constrain, l < z)
    if (c == 1):
        l = z 
    elif ( c == -1):
        pass
    else:
        print("Verification failed at condition: l = z ")
    return l

s = Solver()
s.add(x > 0)
s.add(y > 0)
s.add(z > 0)
l = max(x,y,z)
l = 20
l = declassifyValue(s, inputs, constrain,l == 20)
print(l)

