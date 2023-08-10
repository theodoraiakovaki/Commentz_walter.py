# Commentz_walter.py

# Commentz-Walter Algorithm Implementation

This repository contains a Python script that implements the Commentz-Walter algorithm for substring searching. The Commentz-Walter algorithm is used to efficiently find all occurrences of a list of substrings in a given text.

## Usage

The script can be executed with different options to control its behavior. The algorithm expects a list of search terms, a text file containing the input text, and an optional flag for printing additional information.


## How it Works

The script implements the Commentz-Walter algorithm, a substring search algorithm. It reads the provided search terms and the input text, then constructs a trie data structure for efficient substring matching.

Trie Creation: The script constructs a trie data structure based on the inverted search terms. This trie helps in quickly matching substrings within the text.

Failure Function: The failure function is computed to handle mismatches and efficiently backtrack in the trie.

Set Creation: Sets (set1 and set2) are created to store relevant nodes in the trie, which aid in substring search calculations.

Depth Calculation: The depth of nodes in the trie is calculated for further calculations.

Commentz-Walter Algorithm: The core algorithm iterates through the text while matching substrings using the trie and applying the sets and depth information.

Printing Results: The algorithm prints the positions of found substrings.


## Options and Output
If you include the -v or --vessel flag, additional information about the sets and substrings will be printed.
