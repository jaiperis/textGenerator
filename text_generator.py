# importing stuff
from nltk.util import ngrams
from nltk.tokenize import WhitespaceTokenizer
from collections import Counter
import random


# opening file
# f = open("GOT.txt", "r", encoding="utf-8")
file = input("Enter file: ")
f = open(file, "r", encoding="utf-8")
corpus = ' '.join(f.readlines())
f.close()


# tokenization and n-gram
ws = WhitespaceTokenizer()
tokens = ws.tokenize(corpus)
trigram_list = list(ngrams(tokens, 3))
trigram_counter = Counter(trigram_list)


# function for getting words (receiving head as list)
def population_weights(head):
    pop_weights = [[], []]
    for trigram in trigram_counter:
        guess_head = [trigram[0], trigram[1]]
        if head == guess_head:
            pop_weights[0].append(trigram[2])
            pop_weights[1].append(trigram_counter[trigram])
    return pop_weights


# select tail (receiving head as list)
def tail_choice(head):
    arguments = population_weights(head)
    return random.choices(arguments[0], arguments[1])


# finds out if a sentence is ended too soon
def dead_end(head):
    arguments = population_weights(head)
    pop = arguments[0]
    pop_string = ' '.join(pop)
    count = pop_string.count('.') + pop_string.count('?') + pop_string.count('!')
    if count == len(pop):
        return True
    return False


# outputting sentence (receiving head as list)
def sentence(head):
    sent = [head[0], head[1]]
    head_list = head
    endings = ['.', '?', '!']
    # body of sentence with no end
    while len(sent) < 5:
        new_word = tail_choice(head_list)[0]
        trigram = [head_list[0], head_list[1], new_word]
        if new_word[-1] in endings:
            if dead_end(head_list):
                return -1, -1
            head_list = head
            sent = [head[0], head[1]]
        elif trigram_check(trigram, trigram_list):
            sent.append(new_word)
            head_list = [head_list[1], new_word]
    # sentence continued till end
    while True:
        new_word = tail_choice(head_list)[0]
        trigram = [head_list[0], head_list[1], new_word]
        # end sentence and return it joined
        if new_word[-1] in endings and trigram_check(trigram, trigram_list):
            sent.append(new_word)
            return ' '.join(sent)
        elif trigram_check(trigram, trigram_list):
            sent.append(new_word)
        head_list = [head_list[1], new_word]


# first word
def first_word(leads):
    endings = ['.', '?', '!']
    while True:
        attempt = random.choice(leads)
        word1, word2 = attempt[0], attempt[1]
        if (word1[0].isupper() and word1[-1] not in endings) and (word2[0].isupper() and word2[-1] not in endings):
            return attempt  # returns head as list


# make a list of trigram heads
def trigram_heads(trigrams):
    heads_list = []
    for trigram in trigrams:
        head = [trigram[0], trigram[1]]
        heads_list.append(head)
    # returns list of heads list
    return heads_list


# check trigrams to make sure they come from the list (incomplete)
def trigram_check(trigram, tri_list):
    trigram_t = tuple(trigram)
    if trigram_t in tri_list:
        return True
    return False


heads = trigram_heads(trigram_list)
trigram_head = first_word(heads)
iterations = 0

while iterations < 10:
    line = sentence(trigram_head)
    if line == -1:
        trigram_head = first_word(heads)
        continue
    print(line)
    iterations += 1
    trigram_head = first_word(heads)


