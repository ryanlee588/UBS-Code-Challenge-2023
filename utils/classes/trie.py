"""
File containing Implementations of Trie and TrieNode classes used for getting the completions
"""

class TrieNode:

  def __init__(self):
    self.children = {}
    self.is_end_of_word = False


class Trie:

  def __init__(self):
    self.root = TrieNode()

  def insert(self, word):
    """
    Inserting a word into the Trie
    """
    node = self.root
    for char in word:
      if char not in node.children:
        node.children[char] = TrieNode()
      node = node.children[char]
    node.is_end_of_word = True

  def get_completion(self, prefix):
    """
    Given a prefix, get the completed word including prefix in a Trie
    """
    node = self.root
    for char in prefix:
      if char not in node.children:
        return []
      node = node.children[char]

    completions = []
    self._find_completions(node, prefix, completions)
    return completions

  def _find_completions(self, node, current_prefix, completions):
    """
    Auxilary function to recursively get completed word in a Trie
    """
    if node.is_end_of_word:
      completions.append(current_prefix)

    for char, child_node in node.children.items():
      self._find_completions(child_node, current_prefix + char, completions)
