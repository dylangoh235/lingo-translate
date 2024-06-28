from lingo_suggestion.suggestion import synonym_suggestion

suggestor = synonym_suggestion("llama2_7b")
term = suggestor.suggestion("sex", True, 0, "what you wanna do my man? i don't need a baby right now, i just want to get a sleep.")

print(term)