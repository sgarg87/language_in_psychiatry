import nltk
import numpy
import read_interview_transcripts
import sys


class NLPFeatures:

    def count_of_pos_tags(self, sent):
        # split text into tokens
        word_tokenized_sent = nltk.word_tokenize(sent)
        # print('word_tokenized_sent', word_tokenized_sent)

        cheryl_vocabulary = numpy.unique(word_tokenized_sent)
        # print(cheryl_vocabulary)
        # print(cheryl_vocabulary.size, len(word_tokenized_sent))

        # obtaining Part of speech tags for tokens
        pos_tags_of_sent = nltk.pos_tag(word_tokenized_sent)
        # print(pos_tags_of_sent)

        pos_tags_only = []
        for curr_tuple in pos_tags_of_sent:
            # print(curr_tuple[1])
            pos_tags_only.append(curr_tuple[1])
        # print(pos_tags_only)

        unique_pos_tags, count_pos_tags = numpy.unique(pos_tags_only, return_counts=True)
        # print(unique_pos_tags.size)
        # print(unique_pos_tags)
        # print(count_pos_tags)

        return unique_pos_tags, count_pos_tags


def example():
    obj = NLPFeatures()

    print('.'*20+' Cheryl text sample '+'.'*20)
    cheryl_sent = "I am enjoying it. No. Yes. I went to the diner this morning to have breakfast." \
                  "The egg omlette was delicious but my coffee was too cold." \
                  "I was sad to have breakfast all by myself."
    print(cheryl_sent)
    unique_pos_tags, count_pos_tags = obj.count_of_pos_tags(sent=cheryl_sent)
    # print(unique_pos_tags.size)
    print(unique_pos_tags)
    print(count_pos_tags)

    print('.'*20+' Sahil text sample '+'.'*20)
    sahil_sent = "Hey Zarina, I am just lying, having fun." \
                 " I didn't go anywhere. I had amazing dinner last night. I had enemies in dinner last night."
    print(sahil_sent)
    unique_pos_tags, count_pos_tags = obj.count_of_pos_tags(sahil_sent)
    # print(unique_pos_tags.size)
    print(unique_pos_tags)
    print(count_pos_tags)


if __name__ == '__main__':
    dir_path = sys.argv[1]

    obj = NLPFeatures()

    read_obj = read_interview_transcripts.ReadInterviewTranscripts()
    text_list = read_obj.read_sentence_sets_from_files_in_dir(dir_path=dir_path)

    for text_from_curr_file in text_list:
        print('................'*3)
        unique_pos_tags, count_pos_tags = obj.count_of_pos_tags(text_from_curr_file)
        print(unique_pos_tags)
        print(count_pos_tags)
