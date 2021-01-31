from google.cloud import storage
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import io
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/k/Documents/credential/quickstart-1562668836216-a6140e0c14c1.json'

def sample_recognize(local_file_path,language_code,sample_rate_hertz):

    client = speech_v1.SpeechClient()

    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
        "encoding": 'FLAC',
    }

    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    response = client.recognize(config, audio)

    for result in response.results:
        alternative = result.alternatives[0]
    
    return alternative.transcript



def label_audio(sound_list,language_code,sample_rate_hertz):

    chapter_num = 0

    for lst in sound_list:
    #     print(lst['flac_path'])
        letter_limit = 10
        
        try:
            stt_text = sample_recognize(lst['flac_path'],language_code,sample_rate_hertz)
        #         print(stt_text)

            if (('chapter' in stt_text) or('Chapter' in stt_text)  or('チャプター' in stt_text)) and (len(stt_text) <13):
                chapter_num += 1
                lst['status'] = 'chapter'
                lst['chapter'] = chapter_num
                print(lst['chapter'],lst['status'],stt_text)

            if (len(stt_text) < letter_limit) and ('開始' in stt_text):            
                lst['status'] = 'start'
                lst['chapter'] = chapter_num
                lst['text'] = ''
                print(lst['chapter'],lst['status'],stt_text)

            elif (len(stt_text) < letter_limit) and ('終了' in stt_text): 
                lst['status'] = 'end'
                lst['chapter'] = chapter_num
                lst['text'] = ''
                print(lst['chapter'],lst['status'],stt_text)

            elif (len(stt_text) < letter_limit) and ('削除' in stt_text): 
                lst['status'] = 'delete'
                lst['chapter'] = chapter_num
                lst['text'] = ''
                print(lst['chapter'],lst['status'],stt_text)

            else:
                lst['status'] = 'text'    
                lst['chapter'] = chapter_num
                lst['text'] = stt_text
                print(lst['chapter'],lst['status'],stt_text)

        except:
            print('no voice')
            lst['text'] = ''
            lst['chapter'] = 0
            lst['status'] = 'silent'

    return sound_list
    