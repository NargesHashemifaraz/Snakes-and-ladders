# -*- coding: utf-8 -*-
"""Q_learning.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CVBWKI5vhLd-yMgzZLsv5_FoBI2HSzN9
"""

#RUN EVERY TIME
dimension = int(input())
last_s = (dimension ** 2 ) - 1
Q_state = []
for i in range (0, dimension ** 2) :
    Q_state.append([0, 0, 0, 0])

Q_state[1-1] = [0, 0]
Q_state[2-1] = [0, 0, 0]
Q_state[last_s-1] = [0, 0, 0]
Q_state[last_s] = [last_s + 1 + dimension] #reward = D^2 + D

print(Q_state)

import ast

# Input string snakes
input_string = input('snakes')
input_tuples = ast.literal_eval(input_string)
snakes = [[x-1 for x in t] for t in input_tuples]

print(snakes)

# Input string ladders
input_string = input('ladders')
input_tuples = ast.literal_eval(input_string)
ladders = [[x-1 for x in t] for t in input_tuples]

print(ladders)
print(type(ladders[0][0]))

dragon = int(input())-1

genie = int(input())-1

phoenix = int(input())-1

dimond = int(input())-1

print(dragon, type(dragon))
print(genie, type(genie))
print(phoenix, type(phoenix))
print(dimond, type(dimond))

#RUN EVERY TIME
R = -1 #reward or punish ment for every R(s, a, s')
L = 1  #becuase we punish for every extra move we can set lanbda to 1

n = 0.1 #number of times game has been played we start with about 0
alpha = 1.0 / n
print(alpha)

epsilon = 0.5 #probiblity for doing arbitary move
noise = 0.2

converge = False

having_dimond = False

import random


def chose_action(loc):
  max_index = Q_state[loc].index(max(Q_state[loc]))
  random_float = random.random()
  if random_float > epsilon :
    return max_index
  else :
    return random.randint(0, len(Q_state[loc])-1) #returns the index of the action chosen

x=32
print(Q_state[x-1])
print(chose_action(x-1))

def find_index_of_number_in_first_element(main_list, target):
    for i, sublist in enumerate(main_list):
        if sublist[0] == target:
            return i
    return None

def loc_finaler(loc):

  global having_dimond
  changed = True

  while changed :
    changed = False

    if loc == dimond :
      having_dimond = True

    #snakes
    index = find_index_of_number_in_first_element(snakes, loc)
    if index is not None:
      loc = snakes[index][1]
      changed = True
    #ladders
    index = find_index_of_number_in_first_element(ladders, loc)
    if index is not None:
      loc = ladders[index][1]
      changed = True

    if loc == dimond :
      having_dimond = True

    if (loc == dragon) and (having_dimond == False):
      loc = 0
      changed = True

    if (loc == dragon) and (having_dimond == True):
      having_dimond = False

    if (loc == phoenix) :
      loc = loc - (loc  % dimension ) + dimension -1
      changed = True

    if (loc == genie) :#333333333333333333333333333333333333333333333333333333
      yekan = (loc+1) % dimension
      dahgan = loc+1 - yekan
      if (dimension - dahgan) % 2 == 1:
        loc = last_s - dimension + yekan
      else:
        yekan = dimension+1 - yekan
        loc = last_s - dimension + yekan

      changed = True

  return loc

x=52
print(loc_finaler(x-1)+1)

def find_next_loc(loc , action):
  if loc == 0:####
    next_loc = loc + action + 1

  elif loc == 1:###

    random_float = random.random()
    if random_float < noise :
      if action == 0:
        action = 1
      elif action == 1:
        action = 0

    if action == 0:
      next_loc = loc - 1
    else:
      next_loc = loc + action

  elif loc == last_s - 1:###

    random_float = random.random()
    if random_float < noise :
      if action == 1:
        action = 2
      elif action == 2:
        action = 1

    if action == 2:
      next_loc = loc + 1
    else:
      next_loc = loc + action - 2





  else:####

    random_float = random.random()
    if random_float < noise :
      action = 3 - action


    next_loc = loc + action
    if action < 2 : # its backward
      next_loc += -2
    else: #its forward
      next_loc += -1


  next_loc = loc_finaler(next_loc)
  return(next_loc)

x=99  #loc
a=2  #act
print(find_next_loc(x-1,a)+1)  #result

#RUN EVERY TIME
while not converge : #we replay the game

  loc = 0 #our agent's location
  n += 1
  alpha = 1.0 / n
  having_dimond = False
  max_update = 0

  while loc < (dimension ** 2) - 1 :
    action = chose_action(loc)
    new_loc = find_next_loc(loc, action)
    sample = R + L * max(Q_state[new_loc])
    #print(loc, action)
    if abs(alpha *(sample - Q_state[loc][action]) ) > max_update :
      max_update = abs(sample - Q_state[loc][action])

    Q_state[loc][action] = (1 - alpha) * Q_state[loc][action] + alpha * sample
    loc = new_loc

  if max_update < 0.05 :
    converge = True
    print('converged')

print(Q_state)


#best bath
best_path = []
loc = 0
epsilon = 0.0 #eliminating probiblity for doing arbitary move
noise = 0.0

while loc < (dimension ** 2) - 1 :
  action = chose_action(loc)
  best_path.append([loc+1,action])#   2backwards -> 1backward -> 1forward -> 2forwards
  loc = find_next_loc(loc, action)

print(best_path)
print(n)

'''
exp
 for node 1 : 0: 1forward, 1: 2forwards
 doe node 36 : 0: 1backward, 1: 2backwards, 2: 1forward, 3: 2forwards
 for node 99 : 0: 1forward
'''