from collections import deque
import argparse
parser = argparse.ArgumentParser()
item = parser.add_mutually_exclusive_group()
parser.add_argument('wordlist', nargs='+', type=str, help='The words that user give us')
item.add_argument('-v', '--vessel', action='store_true', help='If user puts -v s1 and s2 get printed')
parser.add_argument("textfile", type=str, help='The name of the file')
user_input = parser.parse_args()
substrings = user_input.wordlist #Read search terms
inverted_substrings = [substring[::-1] for substring in substrings] #inverting each substring
filename = user_input.textfile #Read the content of example.txt
with open(filename, 'r') as f:
    text = f.read().replace('\n', '')
    t = [text]
text_length = len(text)
pmin = min(inverted_substrings, key=len)
pmin = len(pmin) #Find the shortest length of the search term
trie = {} #trie creation
counter = 0
for term in inverted_substrings:
    current_node = 0  # Start from the beginning for each string
    for i, letter in enumerate(term):
        if current_node in trie and letter in trie[current_node]:
            current_node = trie[current_node][letter]
        else:
            counter += 1
            if current_node not in trie:
                trie[current_node] = {}
            trie[current_node][letter] = counter  # Add new node to current_node
            current_node = counter
    trie[current_node] = {} # Add the node that is not connected with others

#r_t creation
def r_t(inverted_substrings,pmin):
    concatenated_string = ''.join(inverted_substrings)
    unique_letters = ''.join(set(concatenated_string)) #Extract unique letters from the concatenated string
    min_positions = {letter: float('inf') for letter in unique_letters}
    for letter in unique_letters:  #Iterate through each letter in the unique_letters
     for j, word in enumerate(inverted_substrings):  #Iterate through each word in the inverted_substrings
        if letter in word:
            index = word.index(letter) #Find the index of the first occurrence of the letter in the word
            min_positions[letter] = min(min_positions[letter], index + 1) #Update the minimum position for the letter if necessary
    alphabet = [chr(i) for i in range(ord('a'), ord('z')+1)]
    rt = {letter: pmin+1 for letter in alphabet}
    for letter, index in min_positions.items(): #Update the "rt" dictionary with the minimum positions
        rt[letter] = index
    return (rt)

#failurecreation
def failure():
    failure = [0] * (len(trie))  # Initialize failure array
    visited = [False] * (len(trie))  # Initialize visited list
    queue = deque()
    for letter in trie[0]:
        next_node = trie[0][letter]
        queue.append(next_node)
        failure[next_node] = 0
        visited[next_node] = True
    while queue:
        parent_node = queue.popleft()
        for letter, child_node in trie[parent_node].items():
            queue.append(child_node)
            u = failure[parent_node]
            while u != 0 and letter not in trie[u]:
                u = failure[u]
            if letter in trie[u]:
             failure[child_node] = trie[u][letter]
            else:
                failure[child_node] = 0
            visited[child_node] = True
    return (failure)

#set1creation
def set_1(failure):
    set1 = [set() for _ in range(len(failure))] #Initialize set1
    for i, element in enumerate(failure):
        if element!=0:
          set1[element].add(i)
    
    set1 = [0 if len(s) == 0 else s for s in set1] #Set 0 where set is empty
    return (set1)

#set2creation
def set_2(set1):
    set2 = [set() for _ in range(len(set1))]
    for i, elements in enumerate(set1):
        if elements != 0:
            for element in elements:
                if element in trie and not trie[element]:
                    set2[i].add(element)
    set2 = [0 if len(s) == 0 else s for s in set2] #Set 0 where set is empty
    return (set2)

#Calculate the depth
def depth(node_to_find):
    if node_to_find not in trie:
        return -1  # Node not found in the trie
    queue = deque([(0, 1)])  # Start with root node and depth 1
    visited = set()
    while queue:
        current_node, depth = queue.popleft()
        visited.add(current_node)
        if current_node == node_to_find:
            return depth
        for child in trie.get(current_node, {}).values():
            if child not in visited:
                queue.append((child, depth + 1))

    return -1 #Node not found in the trie


def s1(set1):
    s_1 = [0] * len(set1)
    for u in trie:
     if u==0:
         s_1[u] = 1
     else: 
         elements = set1[u]
         if isinstance(elements, set): #find the set which contains nodes
            min_difference = float('inf')
            for element in elements:
                depth_parent = depth(u)
                depth_child = depth(element)
                k = depth_child - depth_parent
                min_difference = min(min_difference, k)
            s_1[u] = min(pmin,min_difference)
         else: # if the set value is 0
             s_1[u] = pmin
    return (s_1)


def s2(set2):
    s_2 = [0] * len(set2)
    for u in trie:
      if u==0:
         s_2[u] = pmin
      else: 
         elements = set2[u]
         if isinstance(elements, set): #find the set which contains nodes
            min_difference = float('inf')
            for element in elements:
                depth_parent = depth(u)
                depth_child = depth(element)
                k = depth_child - depth_parent
                min_difference = min(min_difference, k)
            s_2[u] = min(s_2[parent(u)],min_difference)
         else: # if the set value is 0
             s_2[u] = s_2[parent(u)]
    return (s_2)

#Find the parent of node u
def parent(u): 
    for node, edges in trie.items():
        if u in edges.values():
            return node


def commentz_walter():
 i = pmin - 1
 j  = 0
 u = 0
 m = ""
 q = []
 letter = text[i-j]
 while i < text_length:
    while letter in trie[u]: # HasChild 
      u = trie[u][letter] #GetChild
      j+=1
      m +=letter
      letter = text[i-j]
      if not trie[u]:
        q.append((m[::-1],i-j+1))
    failure_table = failure()
    set1 = set_1(failure_table)
    rt = r_t(inverted_substrings,pmin)
    set2 = set_2(set1)
    s_1 = s1(set1)
    s_2 = s2(set2)
    if j > i:
      j = i
    s = min(s_2[u], max(s_1[u],rt[letter] - j - 1))
    i = i + s
    j = 0
    u = 0
    m = ""
    if i < text_length:
        letter = text[i - j]
 if user_input.vessel:
     for i in range(len(set1)):
      print(f"{i}: {s_1[i]},{s_2[i]}")      
 for word, position in q:
    print(f"{word}: {position}")
 
commentz_walter() 