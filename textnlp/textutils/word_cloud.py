"""
"""

import sys
import os
import logging

import numpy as np

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if proj_path not in sys.path:
    sys.path.insert(1, proj_path)
import textnlp as pkg

logger = logging.getLogger(name=__name__)


def encoded_pairings(encoded_tokens):
    """
    """
    enc_pairs = np.transpose(np.vstack(
            [encoded_tokens[:-1], encoded_tokens[1:]]
        ))
    max_con = np.array([max(x) for x in enc_pairs])
    min_con = np.array([min(x) for x in enc_pairs])
    return np.transpose(np.vstack([min_con, max_con]))


class WordNode():
    """
    """

    def __init__(self, word, word_index):
        """
        """
        self.word = word
        self.w_index = word_index
        self.neighbors = []

    def __repr__(self):
        """
        """
        return f"({self.word}, {self.w_index})"


class WordCloud():
    """
    """

    def __init__(self, dictionary, enum_connections):
        """
        """
        self.dictionary = dictionary
        self.dict_lookup = {word: i for i, word in enumerate(dictionary)}
        self.dict_size = len(dictionary)
        self.graph = [
                WordNode(word, word_index)
                    for word_index, word in enumerate(dictionary)
            ]
        self.connections = enum_connections
        for i in range(self.connections.shape[0]):
            w1 = self.connections[i, 0]
            w2 = self.connections[i, 1]
            try:
                self.graph[w1].neighbors.append(self.graph[w2])
                self.graph[w2].neighbors.append(self.graph[w1])
            except:
                logger.error('w1', w1, 'w2', w2)


    def get_word_relation(self, word1, word2, depth_limit=5):
        """
        """
        try:
            word_ind1 = self.dict_lookup[word1]
        except KeyError as e:
            logger.error(f"{e}")
            word_ind1 = None
        try:
            word_ind2 = self.dict_lookup[word2]
        except KeyError as e:
            logger.error(f"{e}")
            word_ind2 = None
        r_val = None
        paths = []

        if (word_ind1 is not None) and (word_ind2 is not None):
            wn1 = self.graph[word_ind1]
            wn2 = self.graph[word_ind2]
            tree = [[wn1]]
            unique_check = set([word_ind1])

            if word1 == word2:
                r_val = 0
            else:
                depth = 0
                found = False
                end_component = False
                while ((not found)
                       and (not end_component)
                       and (depth < depth_limit)
                ):
                    depth = len(tree) - 1
                    cur_level = tree[depth]
                    next_level = []
                    next_inds = set([])
                    for word_node in cur_level:
                        for neigh in word_node.neighbors:
                            if ((not found)
                                    and neigh.w_index
                                    not in (unique_check | next_inds)
                            ):
                                next_level.append(neigh)
                                next_inds.add(neigh.w_index)
                                if neigh.word == word2:
                                    found = True
                                    next_level = [neigh]
                    if len(next_level) == 0:
                        end_component = True
                    else:
                        tree.append(next_level)
                    unique_check = unique_check | next_inds
                if found:
                    r_val = len(tree) - 1

            if found:
                rev_tree = [[wn2]]
                depth = 0
                found = False
                unique_check = set([word_ind2])
                while ((not found)
                       and (not end_component)
                       and (depth < len(tree))
                ):
                    depth = len(rev_tree) - 1
                    cur_level = rev_tree[depth]
                    next_level = []
                    next_inds = set([])
                    for word_node in cur_level:
                        for neigh in word_node.neighbors:
                            if ((not found)
                                    and neigh.w_index
                                    not in (unique_check | next_inds)
                            ):
                                next_level.append(neigh)
                                next_inds.add(neigh.w_index)
                                if neigh.word == word1:
                                    found = True
                                    next_level = [neigh]
                    rev_tree.append(next_level)
                    unique_check = unique_check | next_inds

            if found:
                paths = []
                for i in range(len(tree)):
                    row = []
                    for node in tree[i]:
                        if node in rev_tree[len(rev_tree)-1-i]:
                            row.append(node)
                    paths.append(row)
        return r_val, paths


if __name__=="__main__":
    pass
