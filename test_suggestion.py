from lingo_suggestion.suggestion import synonym_suggestion

suggestor = synonym_suggestion("llama2_13b")
term = suggestor.suggestion(0, True, 0, "what you wanna do my man? i don't need a baby right now, i just want to get a sleep.")

print(term)