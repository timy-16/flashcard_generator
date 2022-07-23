from bs4 import BeautifulSoup, Comment
from reverso_context_api import Client
from func_timeout import func_set_timeout, FunctionTimedOut
from dotenv import load_dotenv
import requests
import itertools
import json
import re
import os


def configure():
    load_dotenv()


def getHTMLdocument(url: str):
    response = requests.get(url)
    return response.text


def get_translation(word: str, src_lang: str, target_lang: str):
    # getting one word from the list of requested words to trdefinitionlate
    # list of trdefinitionlations for the given word
    c = Client(src_lang, target_lang)
    translation_raw = list(
        (c.get_translations(word)))
    translation_raw_size = len(
        translation_raw)
    if(translation_raw_size == 0):
        return "<h1 class=\"not-found-h1\">Not Found!</h1>"
    else:
        INITIAL_SHOWED_TRANSLATIONS_NUM = 8
        # wrapping each word in a span tag
        for word in range(0, translation_raw_size):
            translation_raw[word] = f"<span class=\"translation\">{translation_raw[word]}</span>"
            if(word+1 == INITIAL_SHOWED_TRANSLATIONS_NUM):
                translation_raw[word] = f"<span class=\"more-translation\">{translation_raw[word]}"
        translation_raw[translation_raw_size -
                        1] = f"{translation_raw[translation_raw_size -1]}</span><button class=\"more-translation-btn\" onclick=\"showMore()\">Show More</button>"
        # converting a list to a string
        translation = ' '.join(
            [str(elem) for elem in translation_raw])
        return translation


# todo add styles to anki once you handle all exceptions
# print(get_translation("project", "en", "ru"))


def get_video_links(query: str, context_time: int = 8):
    # the link for the website
    # getting the html code of the website
    url = f'https://youglish.com/pronounce/{query}/english/us?'
    html_document = getHTMLdocument(url)
    soup = BeautifulSoup(html_document, 'html.parser')
    # searcing for elements with given parameters
    # dictionary with ids of our videos
    vid_ids = re.findall(r"vid\\\":\\\".+?(?=\\)", html_document)
    start_time = re.findall(r"start\\\":\\\".+?(?=\\)", html_document)
    vid_ids_list = []  # list for ids of our videos
    start_time_list = []  # list for start time of our videos
    for id in vid_ids:
        i = slice(8, len(id))
        id = id[i]
        vid_ids_list.append(id)
    if (len(vid_ids_list) == 0):
        return "\"https://d540vms5r2s2d.cloudfront.net/mad/uploads/mad_blog_5b8e65f4da71a1536058868.jpg\""
    for element in start_time:
        i = slice(10, len(element))
        element = element[i]
        start_time_list.append(element)
    i = 0
    end_time_list = []  # list for end time of the videos
    EXTRA_TIME = 8  # the time that we add/subtract from start/end time
    start_time_list_size = len(start_time_list)
    for j in range(0, start_time_list_size):
        end_time_list.append(str(int(start_time_list[j])+EXTRA_TIME))
        start_time_list[j] = str(int(start_time_list[j]) - EXTRA_TIME)
    vid_links_list = []
    for element in vid_ids_list:
        vid_links_list.append(
            f"\"https://youtube.com/embed/{element}?start={start_time_list[i]}&end={end_time_list[i]}&cc_load_policy=1&cc_lang_pref=en&rel=0\"")
        i += 1
    return ", ".join(vid_links_list)


# print(get_video_links("fine", 0))


@func_set_timeout(4)
def get_example_sentences_init_phase(word: str, src_lang: str, target_lang: str):
    c = Client(src_lang, target_lang)
    example_sentences = []
    example_sentences_list_in = list(itertools.islice(c.get_translation_samples(
        word, cleanup=False), 10))  # requesting example sentences for our words
    example_sentences_list_out = list(
        itertools.chain(*example_sentences_list_in))  # converting a list of tuples into a list of strings
    example_sentences_list_out_size = len(example_sentences_list_out)
    for i in range(0, example_sentences_list_out_size):
        # wrapping in paragraph tag
        example_sentences_list_out[i] = f"<p class=\"context\">{example_sentences_list_out[i]}</p>"
    target_lang_example_counter = 0
    translation_lang_example_counter = 1
    wrapped_sentences_counter = 0
    # merging two elements in a list
    for k in range(0, example_sentences_list_out_size, 2):
        example_sentences.append(
            f"{example_sentences_list_out[target_lang_example_counter]} {example_sentences_list_out[translation_lang_example_counter]}")
        target_lang_example_counter += 2
        translation_lang_example_counter += 2
        # wrapping in html code
        example_sentences[
            wrapped_sentences_counter] = f"<div class=\"inside-container example-sentences\">{example_sentences[wrapped_sentences_counter]}</div>"
        wrapped_sentences_counter += 1
    return ' '.join(example_sentences)


def get_example_sentences(word: str, src_lang: str, target_lang: str):
    try:
        example_sentences = get_example_sentences_init_phase(
            word, src_lang, target_lang)
        return example_sentences
    except FunctionTimedOut:
        return "<h1 class=\"not-found-h1\">Not Found!</h1>"


# print(get_example_sentences("agonyosijfosifji", "en", "ru"))


def get_image_links(query: str, quantity: int = 1, wrap: bool = True):
    # the link for the website
    # getting the html code of the website
    url = f'https://unsplash.com/s/photos/{query}'
    html_document = getHTMLdocument(url)
    soup = BeautifulSoup(html_document, 'html.parser')
    images = soup.find_all("img", attrs={
        "sizes": "(min-width: 1335px) 416px, (min-width: 992px) calc(calc(100vw - 72px) / 3), (min-width: 768px) calc(calc(100vw - 48px) / 2), 100vw"})
    pre_image_src = []
    for image in images:
        pre_image_src.append(image["src"])
        # wrapping in html code
    pre_image_src_size = len(pre_image_src)
    if(pre_image_src_size == 0):
        return "<div class=\"mySlides\" ><img src=\"https://webhostingmedia.net/wp-content/uploads/2018/01/http-error-404-not-found.png\"class=\"slide-img\" alt=\"\"/></div>"
    else:
        if(wrap):
            for i in range(0, pre_image_src_size):
                pre_image_src[i] = f"<div class=\"mySlides\"><img src=\"{pre_image_src[i]}\"class=\"slide-img\" alt=\"\"/></div>"
        else:
            return pre_image_src[:quantity]
        image_src = ' '.join([str(elem)
                              for elem in pre_image_src[:quantity]])
    return image_src


# print(get_image_links("banana", 19))

# todo mark definitions as a verb, a noun, an adjective etc


def get_definition(query):
    url = f'https://www.britannica.com/dictionary/{query.lower()}'
    html_document = getHTMLdocument(url)
    soup = BeautifulSoup(html_document, 'html.parser')
    all_definition = []
    examples = []
    phrasal_verbs_list = []
    definition = ""
    # for div in soup.findAll('div', {'class': 'sense'}):
    #     for element in div(text=lambda text: isinstance(text, Comment)):
    #         element.extract()
    #         all_definition.append(div)
    for s in soup.findAll('span', {'class': 'def_text'}):
        all_definition.append(s.text)
    # for s in soup.findAll('ul', {'class': 'vis collapsed'}):
    #     examples.append(s)
    # for s in soup.findAll('h2', {'class': 'dre'}):
    #     phrasal_verbs_list.append(s.text)
    if(len(all_definition) == 0):
        return "<h1 class=\"not-found-h1\">Not Found!</h1>"
    else:
        for s in soup.findAll('div', {'class': "vi_content"}):
            examples.append(s.text)
        definition += f"<ul class=\"definition-list\">- {all_definition[0]}"
        examples_num = 3
        if len(examples) > examples_num:
            examples_num = 5
        for example in examples[0:examples_num]:
            definition += f"<li class=\"definition-examples\">{example}</li>"
        definition += "</ul>"
        return definition


# print(get_definition("thug"))


def get_synonyms(query):
    url = f'https://www.thesaurus.com/browse/{query.lower()}'
    html_document = getHTMLdocument(url)
    soup = BeautifulSoup(html_document, 'html.parser')
    synonyms = []
    for s in soup.findAll('a', {'data-linkid': 'nn1ov4'}):
        synonyms.append(s.text)
    if(len(synonyms) == 0):
        return "<h1 class=\"not-found-h1\">Not Found!</h1>"
    else:
        for synonym in range(len(synonyms[0:6])):
            synonyms[synonym] = f"<span class=\"synonym\">{synonyms[synonym]}</span>"
        return ' '.join([str(elem) for elem in synonyms[0:6]])


# print(get_synonyms("allright"))


def get_pronounciation(query: str):
    url = f'https://www.howtopronounce.com/{query}'
    html_document = getHTMLdocument(url)
    soup = BeautifulSoup(html_document, 'html.parser')
    try:
        audio_tag = soup.audio
        audio = audio_tag.attrs["src"]
        return audio
    except AttributeError:
        not_fount_audio = "https://en-audio.howtopronounce.com/15796817165e2807b438b9c.mp3"
        return not_fount_audio


# print(get_pronounciation("whateadgver"))
################################# NOT USED #######################################


def get_definition_data(word: str):
    app_id = "9517819b"
    app_key = os.getenv('api_key_cambridge')
    language = 'en-us'
    word_id = word
    url = f'https://od-api.oxforddictionaries.com/api/v2/entries/{language}/{word_id.lower()}'
    r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})
    if(r.ok):
        d = json.dumps(r.json())
        data = json.loads(d)
        return (d, data)
    else:
        return -1
    # todo work on raising exceptions rather, or better yet hack them))) but please work instead on youutbe examples, they are more important than this
    # print("code {}\n".format(r.status_code))
    # print("text \n" + r.text)
    # print(json.dumps(r.json()))


# print(get_definition_data("haul"))


def get_pronounciation_cambridge(word: str):
    data_init = get_definition_data(word)
    if(data_init != -1):
        data = get_definition_data(word)[1]
        pronunciation = data['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][1]['audioFile']
        return pronunciation
    else:
        print("Error Oxford Pronunciation")
        return get_pronounciation(word)


# print(get_pronounciation_cambridge('sever'))


def get_definition_dict(word: str):
    # shortcutting variable
    data = get_definition_data(word)[1]
    in_lex_entry = data['results'][0]['lexicalEntries']
    definition = {}
    definition_with_example = {}
    defenition_without_examples = []
    for i in range(len(in_lex_entry)):  # geting all possible part of speech for exact word
        part_of_speech = in_lex_entry[i]['lexicalCategory']['id']
        # shortcutting variable
        in_senses = in_lex_entry[i]['entries'][0]['senses']
        for k in range(len(in_senses)):
            definition_key = in_senses[k]['definitions'][0]
            for_searching_ex = in_senses[k]
            if 'examples' in for_searching_ex:
                example = in_senses[k]['examples'][0]['text']
                definition_with_example[definition_key] = example
            else:
                defenition_without_examples.append(definition_key)
                definition_with_example = dict.fromkeys(
                    defenition_without_examples)
        definition[part_of_speech] = definition_with_example

    # print(json.dumps(definition, sort_keys=False, indent=4))
    return definition


# print(get_definition_dict('haul'))


def get_definition_cambridge(word: str):
    definition = []
    definitino_dict = get_definition_dict(word)
    for word_type in definitino_dict:
        definition.append('<li class="word-type">')
        definition.append(f'{word_type}')
        definition.append('<ul class="word-type-def-list">')
        for uses in definitino_dict[word_type]:
            definition.append('<li class="word-def">')
            definition.append(f'-{uses}')
            definition.append(
                '<ul class="word-def-examples">')
            if isinstance(definitino_dict[word_type][uses], list):
                for ex in definitino_dict[word_type][uses]:
                    definition.append(
                        f'<li class="word-def-example">{ex}</li>')
            definition.append(
                f'<li class="word-def-example">{definitino_dict[word_type][uses]}</li>')
            definition.append('</ul>')
            definition.append('</li>')
        definition.append('</ul>')
        definition.append('</li>')

    return ''.join(definition)


def get_synonyms_cambridge(query):
    init_data = get_definition_data(query)
    d = init_data[0]
    data = init_data[1]
    # shortcutting variable
    in_lex_entry = data['results'][0]['lexicalEntries']
    # getting_definitions(in_lex_entry)

    synonym_list = []
    for i in range(len(in_lex_entry)):  # geting all possible part of speech for exact word
        # shortcutting variable
        in_senses = in_lex_entry[i]['entries'][0]['senses']
        for j in range(len(in_senses)):
            for_searching_synonyms = in_senses[j]
            if 'synonyms' in for_searching_synonyms:
                synonym = in_senses[j]['synonyms'][0]['text']
                synonym_list.append(synonym)
    for synonym in range(len(synonym_list)):
        synonym_list[synonym] = f"<span class=\"synonym\">{synonym_list[synonym]}</span>"
    return ' '.join([str(elem) for elem in synonym_list])


def get_pharasal_verbs(word):
    # shortcutting variable
    data_raw = get_definition_data(word)
    d = data_raw[0]
    data = data_raw[1]
    in_lex_entry = data['results'][0]['lexicalEntries']
    phrasal_verbs_list = []
    pv = 'phrasalVerbs'
    if pv in d:
        for i in range(len(in_lex_entry[0]['phrasalVerbs'])):
            phrasal_verbs_list.append(
                in_lex_entry[0]['phrasalVerbs'][i]['text'])
        return phrasal_verbs_list
    else:
        message = 'None'
        return message


def main():
    configure()
