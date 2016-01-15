
replacement = { "noun" : None, "verb" : None, "adjective" : None }

for key in replacement:
    replacement[key] = raw_input("Type in a(n) "+key+" : ")

story = """noun, I just verbed a noun, and I am adjective"""
words = story.split()

for i in range(0, len(words)):
    for key in replacement:
        if key in words[i]:
            words[i] = words[i].replace(key, replacement[key])

print " ".join(words)
