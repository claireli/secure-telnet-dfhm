import math
# sieve of eratos thenes

# input, ceiling which is max given limit
# this algo will mark non-primes (composite) starting from 2 to ... limit

def delete_multiples(candidates, x): 
  # x = 2
  # every xth number in the list after x by counting up from x in increments of x 
  eliminate=[]
  for i in range(0,len(candidates)):
    # 2,4,6,8,10,12,14,...30
    if candidates[i]%x==0:
      
      print(candidates[i],"MULTIPLE OF ", x, " MARKED FOR ELIMINATION")
      eliminate.append(i)
  for d in eliminate:
    candidates.pop
    
  return candidates
  

def erato(n,digit_len_key):
  print(f"Range would be from 2 to {n}")
  print(f"but since the user specified a key of digit-length {digit_len_key}")

  sieve_floor = 10**digit_len_key 

  print(f"we will start from {sieve_floor}")

  # generate a list of consecutive int from 2 to n
  candidates=[]
  for x in range(sieve_floor, n+1):
    candidates.append(x)  
  
  print(candidates)

  p = sieve_floor
  for k in range(2,n):
    #print("MULTIPLES OF ", p)
    for i in (p*k for p in range(p, int((n/2)+1))):
      if(i>n):
        break
      #print("ELIMINATE ", i)
      try:
        candidates.remove(i)
      except:
        continue

  print(candidates)

erato(3000,3)
