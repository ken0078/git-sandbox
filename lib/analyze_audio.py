from pydub import utils
from pydub import AudioSegment
from pydub.silence import split_on_silence

def classify_chunk(chunksize,seconds_threshold,db_threshold,converted_monoral_mp3):
    sound = AudioSegment.from_mp3(converted_monoral_mp3) 
    myAudioChunks = utils.make_chunks(sound,chunksize)

    x = []
    y = []
    time_code_list = []

    start_code = 0.0
    end_code = 0.0

    voice_count = 0.0
    silent_count = 0.0


    for i, audioChunks in enumerate(myAudioChunks):
        time_code = round((i+1) * (chunksize/1000), 2)
        loudness = audioChunks.dBFS
        y.append(loudness)
        x.append(i+1)
        
        if loudness > db_threshold:
            if voice_count ==0.0:
                start_code = round(time_code - 0.1,2)
            
            end_code = time_code
            silent_count = 0.0
            voice_count = round(voice_count + 0.1,2)
            
            print (time_code, round(loudness,2),"Status: Voice, Voice Count:",voice_count)

        else:
            silent_count = round((silent_count + chunksize/1000),2)
            
            if silent_count < seconds_threshold:
                print(time_code, round(loudness,2) , "Status: In Silence, Silent Count:",silent_count)
                
            elif silent_count >= seconds_threshold  and silent_count < seconds_threshold + 0.1:
                print(time_code, round(loudness,2) , "Status: Silent End, Silent Count:",silent_count)
                
                end_code = end_code + 0.3
                time_code_list.append([round(start_code,2),round(end_code,2)])
                voice_count = 0.0
                
            elif silent_count >= seconds_threshold + 0.1:
                print(time_code, round(loudness,2), "Status: No Count, Silent Count:", silent_count)            
            
        if (i == len(myAudioChunks)-1) and (voice_count != 0.0) :
            time_code_list.append([start_code,end_code])

    return time_code_list


def split_audio(time_code_list,converted_monoral_mp3,splited_mp3_path):

    sound = AudioSegment.from_file(converted_monoral_mp3, format="mp3")

    sound_list = []
    for i,lst in enumerate(time_code_list):
        temp_sound = sound[lst[0]*1000:lst[1]*1000]

        temp_sound_name = splited_mp3_path + "temp_output"+ str(i) + ".mp3"

        sound_list.append({'time_code':lst,'sound_path':temp_sound_name})
        temp_sound.export(temp_sound_name, format="mp3")
        
    return sound_list