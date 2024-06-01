import random
import nltk

ref = None
tag = None


def init(text, config):
    """
    Setting the common data by tokenizing and pos-tagging.
    """
    global ref
    global tag
    if ref is None:
        ref = refine(text, config).split(" ")
        if config['eng']:
            nltk.download('averaged_perceptron_tagger')
            tag = nltk.pos_tag(ref)
        else:
            nltk.download('averaged_perceptron_tagger_ru')
            tag = nltk.pos_tag(ref, lang="rus")
    return {'ref': ref, 'tag': tag}


def refine(text, config):
    """
    Optional cleanup of the input file.
    Symbols for removal are to be listed in the configuration.
    """
    for i in config['replace']:
        if type(i) is str:
            text = text.replace(i, ' ')
        else:
            text = text.replace(i[0], i[1])
    while '  ' in text:
        text = text.replace('  ', ' ')
    if text[-1] == ' ':
        text = text[0:-1]
    return text


def write(token, last, config):
    """
    It's entire working is a mystery.
    Should build a probability model by connecting grammar to sequence list.
    Checks for coherence and prevents exceeding from the bounds of the generator.
    """
    del last[3:]
    sent = last
    for w in sent:
        if w == '':
            sent.remove('')
    keys = list(token['lang'])
    for tries in range(config['tries']):
        if sent:
            if len(sent) > 3:
                try:
                    index = token['lang'][sent[-3]][2][token['lang'][sent[-3]][0].index(keys.index(sent[-2]))]
                    mask = [(token['lang'][sent[-1]][0][i], token['lang'][sent[-1]][1][i]) for i, t in
                            list(enumerate(token['lang'][sent[-1]][2], 0)) if
                            index in token['gram'][list(token['gram'])[t]]]
                    after = keys[random.choices([p[0] for p in mask], weights=[p[1] for p in mask])[0]]
                except:
                    after = keys[random.choices(token['lang'][sent[-1]][0], weights=token['lang'][sent[-1]][1])[0]]
            else:
                after = keys[random.choices(token['lang'][sent[-1]][0], weights=token['lang'][sent[-1]][1])[0]]
            sent.append(after)
            if after == '.':
                break
    sent = sent[3:]
    return (' '.join(sent).replace(' ,', ',').replace(' .', '.')
            .replace(' ;', ';').replace(' ?', '?').replace(' !', '!'))


def train(ref, tag):
    """
    Constructing the lists.
    As well as refining the data to avoid bloating.
    """
    prob_list = {key: [[], [], []] for key in ref}
    tags_list = {t[1]: [] for t in tag}
    tags_list[None] = []
    for i, t in list(enumerate(tag, 0)):
        prob_list[tag[i - 1][0]][2].append(
            list(tags_list).index(t[1]) if i - 1 > -1 else list(tags_list).index(None))
        prob_list[tag[i - 1][0]][0].append(
            list(prob_list).index(t[0]) if i - 1 > -1 else list(prob_list).index('.'))
        if i - 2 > -1:
            g = list(tags_list).index(tag[i - 2][1])
            if g not in tags_list[t[1]]:
                tags_list[t[1]].append(g)
    for p in list(prob_list):
        temp_word = prob_list[p][0]
        temp_gram = prob_list[p][2]
        prob_list[p][0] = list(set(temp_word))
        prob_list[p][2] = [temp_gram[temp_word.index(g)] for g in prob_list[p][0]]
        prob_list[p][1] = [temp_word.count(s) for s in prob_list[p][0]]
    return prob_list, tags_list
