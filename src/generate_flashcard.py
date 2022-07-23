from csv import writer
from . import apis

# todo get better pronunciation files
# todo improve advanced vocabulary too(This is the first thing you should do actually. Add youtube examples, synonyms, translation and reverso context examples)
# todo maybe you can make some part where you try to make a sentence with the word that you're trying to learn and then AI checks whether this is the correct way to use that word
# todo fix the bug where where you have to press next button for youtube video to show up
# todo fix the bug in reverso context examples where prev button doesn't work and another bug where you have to tap on that block with examples in order to minimize it
# todo fix the bug with multiple images in flashcards
# todo get images from istock using headers user agents or something(beautiful soup has this as it turns out)
# todo fix the bug with complementary colors in ankidroid
# todo change design a little
# todo add examples from movies and series(you can first get subtitles from the most popular movies and TV shows on opensubtitles.com and then add them for now. For example you can say like Captain America: add image, and for the word DAY you can add -I can do this all <em>day</em>. Once you've done that you can go on and find timestamps and somehow find movies and series online and record that piece of the movie where he says that with a little bit of context in between of course. If you're able to do that then you can call yourself a real webscraper)
# todo improve the algorithm(Work on time comlexity, try to evaluate first(that's where discrete math comes in handy))
# todo implement AI for picking the right images (I honestly have no idea how you can pull this off)
# todo add a restart button for youtube videos(technically you've already done that, the moment you change src attribute of iframe it restarts the video on its own)
# todo add a pronounciation for reverso context examples(there you can use their own pronunciation or you can make TTS do that for you)
# todo make GUI(It should be the last thing you do, because I honestly couldn't care less about this. No matter how selfish it may sound, I'm doing this for myself and I don't need GUI)


def generate_flashcard(src_file: str, dest_file: str, des_words_num: int = 5, src_lang: str = "en", target_lang: str = "ru"):
    try:
        with open(src_file, 'r') as f:  # opening the file with words
            data = f.read()  # getting words as a string
            # splitting our words in the string and putting them in a list
            words_list_in = data.split()
            words_num = len(words_list_in)  # calculating the number of words
            if des_words_num > words_num:  # if we requested to translate more words than there are in our file with words
                # equating des_words_num to the number of words we currently have in the file with words
                des_words_num = words_num
            # list of words that we need to translate
            words_list_out = words_list_in[:des_words_num]
    except FileNotFoundError:
        print("Source File Is Not Found!")
        return 0
    for i in range(0, des_words_num):
        flashcard = []
        imgages = apis.get_image_links(words_list_out[i], 10)
        pronounciation = apis.get_pronounciation_cambridge(words_list_out[i])
        definition = apis.get_definition(words_list_out[i])
        synonyms = apis.get_synonyms(words_list_out[i])
        translation = apis.get_translation(
            words_list_out[i], src_lang, target_lang)
        context = apis.get_example_sentences(
            words_list_out[i], src_lang, target_lang)
        youtube_videos = apis.get_video_links(words_list_out[i])
        flashcard.extend(
            [imgages, words_list_out[i], pronounciation, definition, synonyms, translation, youtube_videos, context])
    # appending context to the csv file
        with open(dest_file, 'a', encoding='utf-8', newline='') as csv_file:
            writer_object = writer(csv_file)
            writer_object.writerow(flashcard)
    with open(src_file, 'w') as f:
        words_list_in = words_list_in[des_words_num:]
        for word in words_list_in:
            f.write("%s " % word)
    if des_words_num == 1:
        print('\n1 Flashcard Has Been Created!')
    else:
        print(f"\n{des_words_num} flashcards have been created!")
    with open('../my_stuff/my_vocabulary.csv', 'r', encoding="utf-8") as f_in:
        rowcount = 0
        for row in f_in:
            rowcount += 1
    print(f"Flashcards To Import: {rowcount}")
    print(f"Untranslated Words Left: {len(words_list_in)}")


def clear_csv_file(src_file):
    with open(src_file, 'w+') as f:
        f.truncate(0)
    print("The File Has Been Successfully Cleared!")

# generate_flashcard('worjoids.txt', 'vocabulary.csv', 'en', 'ru', 1)
