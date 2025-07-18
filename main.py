import heapq
import json
class TrieNode:
 def __init__(self):
    self.children = {}
    self.is_end = False
    self.frequency = 0
class Trie:
    def __init__(self):
        self.root = TrieNode()
    def insert(self, word, frequency):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.frequency = frequency
    def _dfs(self, node, prefix, result):
        if node.is_end:
            result.append((node.frequency, prefix))
        for char, child in node.children.items():
            self._dfs(child, prefix + char, result)
    def autocomplete(self, prefix, k):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        result = []
        self._dfs(node, prefix, result)
        top_k = heapq.nlargest(k, result)
        return [word for _, word in top_k]
    def levenshtein_distance(s1, s2):
        m, n = len(s1), len(s2)
        dp = [[0] * (n+1) for _ in range(m+1)]
        for i in range(m+1):
            for j in range(n+1):
                if i == 0:
                    dp[i][j] = j
                elif j == 0:
                    dp[i][j] = i
                elif s1[i-1] == s2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
        return dp[m][n]
    def spell_check(dictionary, word, k):
        distances = []
        for entry in dictionary:
            dist = levenshtein_distance(word, entry['word'])
            distances.append((dist, entry['word']))
        distances.sort()
        return [w for _, w in distances[:k]]
    def main():
        with open("input.json") as f:
            data = json.load(f)
        trie = Trie()
        dictionary = data['dictionary']
        for item in dictionary:
            trie.insert(item['word'], item['frequency'])
        autocomplete_results = trie.autocomplete(data['autocomplete_prefix'], data['top_k'])
        spellcheck_results = spell_check(dictionary, data['misspelled_word'], data['top_k'])
        output = {
            "autocomplete_suggestions": autocomplete_results,
            "spell_check_suggestions": spellcheck_results
        }
        print(json.dumps(output, indent=2))
    if __name__ == "__main__":
        main()