#!/usr/bin/python
from z3 import *

#semantic consequence
def imply(range,lh, rh):
    return ForAll(range, Implies(lh, rh))

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

# def declassifyBranchCondition(s, range, constrain, condition):     
#     return  If( 
#             condition,
#             ForAll(range, Implies(constrain, condition)),
#             ForAll(range, Implies(constrain, Not(condition))))


I = IntVector('I', 8)
# I.append(10)
# I.append(7)
# I.append(8)
# I.append(9)
# I.append(1)
# I.append(5)
n = len(I)
s = Solver()
constrain = And(I[1] > I[2],
                I[2] > I[3],
                I[3] > I[4],
                I[4] > I[5],
                I[5] > I[6],
                I[6] > I[7],
                I[0] > I[1])
inputs = [I[i] for i in range(8)]
def partition(s, arr,low,high): 
    i = ( low-1 )         # index of smaller element 
    pivot = arr[high]     # pivot 
  
    for j in range(low , high): 
        c = declassifyBranchCondition(s, inputs, constrain, arr[j] < pivot)
        if (c == 1):
            print("Branch to Then")
            i = i+1 
            arr[i],arr[j] = arr[j],arr[i] 
        elif ( c == -1):
            print("Branch to Else")
        else:
            print("Verification failed at condition: arr[j] < pivot")
  
    arr[i+1],arr[high] = arr[high],arr[i+1] 
    return ( i+1 ) 
  
# The main function that implements QuickSort 
# arr[] --> Array to be sorted, 
# low  --> Starting index, 
# high  --> Ending index 
  
# Function to do Quick sort 
def quickSort(s, arr,low,high): 
    if low < high: 
  
        # pi is partitioning index, arr[p] is now 
        # at right place 
        pi = partition(s, arr,low,high) 
  
        # Separately sort elements before 
        # partition and after partition 
        quickSort(s, arr, low, pi-1) 
        quickSort(s, arr, pi+1, high) 



#arr = [10, 7, 8, 9, 1, 5] 

quickSort(s,I,0,n-1) 
print ("Sorted array is:") 
for i in range(n): 
    print (I[i])