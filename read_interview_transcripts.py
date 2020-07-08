import glob
import textract
import numpy as np


class ReadInterviewTranscripts:
    def __init__(self):
        pass

    def read_word_file_text(self, filename):
        print(filename)
        text = textract.process(filename)
        return text

    def extract_content_from_utterance(self, utterance):
        if '\t' in utterance:
            utterance_split = utterance.split('\t')
            utterance_split = [x for x in utterance_split if x.strip()]
            assert len(utterance_split) == 2, utterance_split
            return utterance_split[1]
        else:
            return None

    def __read_interviewee_sentences_from_word_file__(self, word_file):

        assert word_file.endswith('.docx') or word_file.endswith('.doc')
        # print('word_file', word_file)

        text = self.read_word_file_text(filename=word_file)
        text = text.strip()
        # print(text)
        if not isinstance(text, str):
            text = str(text, 'utf-8')
        assert isinstance(text, str)

        dialogue_utterances = text.split('\n')
        # print('len(dialogue_utterances)', len(dialogue_utterances))

        sentences = []
        is_patient_else_therapist = None

        for curr_utterance in dialogue_utterances:
            curr_utterance = curr_utterance.strip()

            if not curr_utterance:
                continue

            # print(curr_utterance)

            content_from_utterance = None
            if curr_utterance.startswith('Primary Interviewer ') \
                    or curr_utterance.startswith('Primary Interviewer:') \
                    or curr_utterance.startswith('S1 '):
                is_patient_else_therapist = False
            elif curr_utterance.startswith('Subject ') \
                    or curr_utterance.startswith('Subject:') or curr_utterance.startswith('S2 '):
                is_patient_else_therapist = True
                content_from_utterance = self.extract_content_from_utterance(utterance=curr_utterance)
                # print('-' * 10)
                # print(curr_utterance)
                # print(content_from_utterance)
            else:
                # from previous iteration
                if (is_patient_else_therapist is not None) and is_patient_else_therapist:
                    content_from_utterance = curr_utterance
                is_patient_else_therapist = None

            # print(is_patient_else_therapist)

            if content_from_utterance is not None:
                sentences.append(content_from_utterance)

        sentences = np.array(sentences)

        return sentences

    def read_sentence_sets_from_files_in_dir(
            self,
            # where your files are located
            dir_path,
    ):
        files_names_in_dir = glob.glob(dir_path+'/*.docx') + glob.glob(dir_path+'/*.doc')
        files_names_in_dir = [curr_file for curr_file in files_names_in_dir if '~$' not in curr_file]

        sentence_sets_from_files = []
        for curr_file in files_names_in_dir:
            sentences_from_curr_file = self.__read_interviewee_sentences_from_word_file__(curr_file)
            sentences_from_curr_file = ' '.join(sentences_from_curr_file)
            sentence_sets_from_files.append(sentences_from_curr_file)

        return sentence_sets_from_files
