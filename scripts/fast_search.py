"""BM25 shortlist over research passages. Standard library only; no model calls.

Fast search narrows the library before Jev judges each candidate, following the
documented shortlist-then-rerank pattern. Ranking is lexical: it finds shared
words, not meaning, so the shortlist is deliberately generous.
"""
from collections import Counter
import math
import re

STOP = set('''a an and are as at be but by can could do does for from has have how i if in into is it its
me my of on or our so than that the their them then there these they this to too use using want was we
what when where which while who why will with would you your jev typesafe'''.split())
WORD = re.compile(r'[a-z0-9]+')


def stem(word):
    for suffix in ('ing', 'ies', 'ed', 'es', 's'):
        if len(word) > len(suffix)+3 and word.endswith(suffix):
            return word[:-len(suffix)] + ('y' if suffix == 'ies' else '')
    return word


def tokens(text):
    return [stem(w) for w in WORD.findall(text.lower()) if w not in STOP and len(w) > 1]


class Index:
    def __init__(self, rows, k1=1.2, b=0.75, title_weight=3):
        self.rows, self.k1, self.b = rows, k1, b
        # Titles name the project or pattern; weight them so a matching case outranks passing mentions.
        self.terms = [Counter(tokens(r['text']) + tokens(r['title'])*title_weight) for r in rows]
        self.lengths = [sum(t.values()) for t in self.terms]
        self.average = sum(self.lengths)/max(len(rows), 1)
        frequency = Counter(term for t in self.terms for term in t)
        n = len(rows)
        self.idf = {term: math.log(1+(n-f+.5)/(f+.5)) for term, f in frequency.items()}

    def scores(self, query):
        query = set(tokens(query))
        result = []
        for terms, length in zip(self.terms, self.lengths):
            norm = self.k1*(1-self.b+self.b*length/self.average)
            result.append(sum(self.idf[q]*terms[q]*(self.k1+1)/(terms[q]+norm) for q in query if q in terms))
        return result

    def shortlist(self, query, limit, per_document=2):
        """Top passages, capped per document so one long guide cannot fill the list."""
        ranked = sorted(zip(self.scores(query), range(len(self.rows))), key=lambda x: (-x[0], x[1]))
        chosen, seen = [], Counter()
        for score, i in ranked:
            if score <= 0 or len(chosen) == limit:
                break
            path = self.rows[i]['path']
            if seen[path] < per_document:
                seen[path] += 1
                chosen.append({**self.rows[i], 'lexical': round(score, 4)})
        return chosen
