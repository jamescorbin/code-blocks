"""
"""

import sys
import os
import logging

import numpy as np

sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))
import __init__ as pkg

logger = logging.getLogger(name=__name__)


class WordNode():
    """
    """

    def __init__(self, word, word_ind):
        """
        """
        self.word = word
        self.word_ind = word_ind
        self.neighbors = []

    def __repr__(self):
        """
        """
        return f"{self.word}\t{self.word_ind}"


class WordCloud():
    """
    """

    def __init__(self, dictionary, enum_connections):
        """
        """
        self.dictionary = dictionary
        self.dict_lookup = {word: i for i, word in enumerate(dictionary)}
        self.dict_size = len(dictionary)
        self.graph = [WordNode(word, word_ind) for
                      word_ind, word in enumerate(dictionary)]
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
        word_ind1 = self.dict_lookup[word1]
        word_ind2 = self.dict_lookup[word2]
        wn1 = self.graph[word_ind1]
        wn2 = self.graph[word_ind2]
        tree = [[wn1]]
        unique_check = set([word_ind1])
        r_val = None

        if word1 == word2:
            r_val = 0
        else:
            depth = 0
            found = False
            end_component = False
            while ((not found)
                   and (not end_component)
                   and (depth < depth_limit)):
                depth = len(tree) - 1
                cur_level = tree[depth]
                next_level = []
                next_inds = set([])
                for word_node in cur_level:
                    for neigh in word_node.neighbors:
                        if ((not found)
                                and neigh.word_ind
                                not in (unique_check | next_inds)):
                            next_level.append(neigh)
                            next_inds.add(neigh.word_ind)
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
                   and (depth < len(tree))):
                depth = len(rev_tree) - 1
                cur_level = rev_tree[depth]
                next_level = []
                next_inds = set([])
                for word_node in cur_level:
                    for neigh in word_node.neighbors:
                        if ((not found)
                                and neigh.word_ind
                                not in (unique_check | next_inds)):
                            next_level.append(neigh)
                            next_inds.add(neigh.word_ind)
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
    import argparse
    parser = argparse.ArgumentParser(
            description="Counts unique words in Project Gutenburg text.")
    parser.add_argument("--pairings_file")
    parser.add_argument("--dictionary_pt", metavar="dict")
    args = parser.parse_args()

    dic_fn = args.dictionary_pt
    pairs_fn = args.pairings_file

    with open(dic_fn, 'r') as f:
        dictionary = [x.strip() for x in f]
    with open(pairs_fn, 'rb') as f:
        pairs = np.load(f, allow_pickle=True)

    words = [("man", "head"), ("conscious", "space")]
    for w1, w2 in words:
        wc = WordCloud(dictionary, pairs)
        d, paths = wc.get_word_relation(w1, w2)
        logger.info(f"WC get word relation {w1}-{w2}: {d}")
        logger.info(paths)
