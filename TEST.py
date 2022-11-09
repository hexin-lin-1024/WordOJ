from Fetcher import *
# w = WordFetcher()
# print(w.defaultProvider)
# print(w.fetch("apple"))
p = PhraseFetcher()
print(p.fetch("stick *"))
print(p.listProvider())
print(p.provider)