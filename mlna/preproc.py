from googletrans import Translator
from rapidfuzz import fuzz
from langdetect import detect
import pandas as pd
import spacy
import re



nlp = spacy.load("en_core_web_md")


def find_sign_index (text):
    """
    Gets a string and returns the index of the first occurance of the signs that mark a sentence [. ! ?] in the string.
    """
    match = re.search(r"[.!?]", text)
    if match:
        return match.start()
    else:
        return None



def apply_user_dict(text, user_dict):
    """
    Replaces the keys of a user-defined dictionary with their values in a long text.
    """
    for key, value in user_dict.items():
        if key in text:
            text= text.replace(key, value)
    return text



def translate_long_text (text):
    """
    Translates long texts into English. This function was developed because the Translator model does not translate
    texts that are longer than 5000 characters. So this function devides the input text into chunks of 4000
    characters, translates them and puts them together again.
    """
    source= detect(text)
    translator = Translator()
    translation= ''

    while True:
        if len(text) <= 4000:
            translation += translator.translate(text, src=source, dest="en").text
            break
        else:
            fun_text= text[:4000] + "<placeholder>" + text[4000:]
            ph_index= fun_text.index("<placeholder>")
            rest= text[ph_index:]
            sign_index= find_sign_index(rest)
            if sign_index==None:
                cut_index= ph_index
            else:
                cut_index= ph_index + sign_index
            cut_index= ph_index + sign_index
            chunk= text[:cut_index]
            translation += translator.translate(chunk, src=source, dest="en").text + ". "
            text = text.replace(chunk, "", 1)

    translation= translation.replace("..", ".")
    translation = re.sub(r'[\u200b-\u200f\u202a-\u202e]', ' ', translation)

    return translation



def sent_tokenize (eng_text, user_dict=None):
    """
    Sentence-tokenizes a text that is in English. I did not use NLTK's sentence tokenizer, becauase it cannot recognize
    sentences when there is no space between the full stop at the end of the sentence and the next word.
    """
    if user_dict:
        eng_text_1= apply_user_dict(eng_text, user_dict)
        eng_text= apply_user_dict(eng_text_1, user_dict)

    eng_sentences= [sentence.strip() + '.' for sentence in re.split(r'[.!?]', eng_text) if sentence.strip()]

    return eng_sentences



def trans_sent_tokenize (text, user_dict=None):
    """
    Translates the input text to English if it is not already in English. Then sentence-tokenizes the resulting
    English text. It returns a tuple of the original language of the text and a list of the tokenized English sentences.
    """
    language= detect(text)

    if language != 'eng':
        eng_text= translate_long_text(text)
        eng_sentences= sent_tokenize(eng_text, user_dict)
    else:
        eng_sentences= sent_tokenize(text, user_dict)

    return eng_sentences



def extract_entities (text, text_id, entity_tags, user_ents=None, user_dict=None):
    """
    This function receives a whole text, translates it to English (if it is not already in English) and
    sentence-tokenizes it. It then extracts the desired entities that are given as a list and stored in
    entity_tags. It also extracts all desired words by the user, stored in user_ents, from the text. It finally stores
    all of the entities and words in a dictionary with the following keys: 'text_id', 'sentences', 'entities'.
    """
    eng_sentences = trans_sent_tokenize(text, user_dict)
    entities = []

    for sent in eng_sentences:
        sent_entities=[]
        sent_doc = nlp(sent)
        for ent in sent_doc.ents:
            if ent.label_ in entity_tags:
                # doing some text cleaning, but could be removed later:
                entity = ent.text.strip()
                if "'s" in entity:
                    cutoff = entity.index("'s")
                    entity = entity[:cutoff]
                if "’s" in entity:
                    cutoff = entity.index("’s")
                    entity = entity[:cutoff]
                if "ʿ" in entity:
                    entity.replace("ʿ", "")
                # end of text cleaning
                if entity != "":
                    sent_entities.append(entity)
        seen = set()
        sent_entities= [x for x in sent_entities if not (x in seen or seen.add(x))]

        # adding the words defined by the user as fixed entities to the entity list:
        if user_ents:
            funny_sent= sent
            for ent in sent_entities:
                funny_sent.replace(ent, str(sent_entities.index(ent)))
            funny_sent_words= [x.lower() for x in sent.split()]
            source_index= 0
            for i in range(len(funny_sent_words)):
                if funny_sent_words[i]=='1':
                    source_index=i
                    break
            for word in user_ents:
                if word.lower() in funny_sent_words:
                    # word_index = index of each single word provided by the user within the original sentence:
                    word_index=funny_sent_words.index(word.lower())
                    if word_index <= source_index:
                        sent_entities.insert(0, word)
                    else:
                        sent_entities.append(word)

        entities.append(sent_entities)

    ent_dict= {'text_id': text_id,
               'sentences': eng_sentences,
               'entities': entities
                }


    return ent_dict



def group_similar_ents(text_df, entity_tags, user_ents=None, user_dict=None, threshold=80):
    """
    Finds similar entities using fuzzy matching. It will be used in the user_dict function in the user_input module to
    suggest similar dictionary keys to the user.
    """
    # helper function that creates groups of similar entities:
    def find_group(groups, ent):
        for group in groups:
            if any(fuzz.ratio(ent, member) >= threshold for member in group):
                return group
        return None

    groups = []

    for i, row in text_df.iterrows():
        text= row['full_text']
        text_id= row['text_id']

        ent_lists= extract_entities (text, text_id, entity_tags, user_ents, user_dict)['entities']

        for ent_list in ent_lists:
            if len(ent_list)>0:
                for ent in ent_list:
                    group = find_group(groups, ent)
                    if group:
                        if ent not in group:
                            group.append(ent)
                    else:
                        groups.append([ent])

    groups = [group for group in groups if len(group) >= 2]

    return groups
