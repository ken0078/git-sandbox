import subprocess
import re
pattern_1 = re.compile(r'.mp4')

def delete_mp4(input_text):
    output_text = re.sub(pattern_1,'', input_text)
    
    return output_text

# convert MOV(iPhone camera defalut) to mp4
def convert_MOV_to_mp4(folder_path,video_name):
    default_mov = folder_path + '1_full_size_data/a_input_MOV/' + video_name +  '.MOV'
    converted_mp4 = folder_path + '1_full_size_data/b_converted_mp4/' + video_name + '.mp4'

    try:
        cmd = "ffmpeg -i {} -vf fps=30 -vsync 1 {}".format(default_mov, converted_mp4)
        resp = subprocess.check_output(cmd, shell=True)
        print("Succeeded: converted mp4 was generated")
    except:
        print("Failed: mp4 was not generated")
        
    return converted_mp4



# convert mp4 to stereo mp3
def convert_mp4_to_stereo_mp3(folder_path,video_name,converted_mp4):
    converted_stereo_mp3 = folder_path + '1_full_size_data/c_converted_mp3/' + video_name + '.mp3'

    try:
        cmd = "ffmpeg -i  {} {}".format(converted_mp4,converted_stereo_mp3)
        resp = subprocess.check_output(cmd, shell=True)
        print("Succeeded: stereo mp3 was generated")
    except:
        print("Failed: stereo mp3 was not generated")

    return converted_stereo_mp3
        


# convert stereo mp3 to monoral mp3
def convert_stereo_mp3_to_monoral_mp3(folder_path,video_name,converted_stereo_mp3):
    converted_monoral_mp3 = folder_path + '1_full_size_data/c_converted_mp3/' + video_name +'_monoral' +'.mp3'

    try:
        cmd = "ffmpeg -i {} -ac 1 {}".format(converted_stereo_mp3,converted_monoral_mp3)
        resp = subprocess.check_output(cmd, shell=True)
        print("Succeeded: monoral mp3 was generated")
    except:
        print("Failed: monoral mp3 was not generated")

    return converted_monoral_mp3

    # convert mp4 to stereo mp3
def convert_mp4_to_stereo_mp3_2(folder_path,video_name,converted_mp4):
    converted_stereo_mp3 = folder_path + video_name + '.mp3'

    try:
        cmd = "ffmpeg -i  {} {}".format(converted_mp4,converted_stereo_mp3)
        resp = subprocess.check_output(cmd, shell=True)
        print("Succeeded: stereo mp3 was generated")
    except:
        print("Failed: stereo mp3 was not generated")

    return converted_stereo_mp3
        


# convert stereo mp3 to monoral mp3
def convert_stereo_mp3_to_monoral_mp3_2(folder_path,video_name,converted_stereo_mp3):
    converted_monoral_mp3 = folder_path +  video_name +'_monoral' +'.mp3'

    try:
        cmd = "ffmpeg -i {} -ac 1 {}".format(converted_stereo_mp3,converted_monoral_mp3)
        resp = subprocess.check_output(cmd, shell=True)
        print("Succeeded: monoral mp3 was generated")
    except:
        print("Failed: monoral mp3 was not generated")

    return converted_monoral_mp3


# convert monoral mp3 to flac
def convert_monoral_mp3_to_flac(sound_list,converted_flac_path):
    
    for i,lst in enumerate(sound_list):
        flac_name = converted_flac_path  + "temp_output" + str(i) +".flac"
        cmd = "ffmpeg -i {} -vn -ar 16000 -acodec flac -f flac {}".format(lst['sound_path'], flac_name)
        resp = subprocess.check_output(cmd, shell=True)
        
        lst['flac_path'] = flac_name
    
    return sound_list

def split_mp4(sound_list,converted_mp4,video_name,splited_mp4_path):

    for i,lst in enumerate(sound_list):
        temp_mp4_name = splited_mp4_path + video_name + "_output"+ str(i) + ".mp4"
        cmd = "ffmpeg -ss {} -to {} -i {} {}".format(lst['timecode'][0], lst['timecode'][1],converted_mp4,  temp_mp4_name)
        resp = subprocess.check_output(cmd, shell=True)
        lst['video_path'] = temp_mp4_name
        lst['video_name'] = video_name + "_output"+ str(i) + ".mp4"

    return sound_list

def convert_mp4_to_stereo_mp3_second(csv_video_list,splited_mp4_path,audio_path):
    for lst in csv_video_list[1:]:
        output_mp4 = splited_mp4_path + lst[1]
        output_mp3 = audio_path + delete_mp4(lst[1]) + '.mp3'
        
        # print(output_mp3)

        cmd = "ffmpeg -i {} {}".format(output_mp4, output_mp3)
        resp = subprocess.check_output(cmd, shell=True)



def add_mp3_to_customized_mp4(csv_video_list,chapter_list,customized_path,audio_path,custom_audio_path):
    for chapter_num in chapter_list:    
        for lst in csv_video_list[1:]:
            if lst[0] == str(chapter_num):
                custom_mp4 = customized_path + lst[1]
                output_mp3 = audio_path + delete_mp4(lst[1]) + '.mp3'
                integrated_mp4 = custom_audio_path + lst[1]

                cmd = "ffmpeg -i {}  -i {} {}".format(custom_mp4, output_mp3, integrated_mp4)
                resp = subprocess.check_output(cmd, shell=True)
                

def add_mp3_to_initial_mp4(bgm_mp3,chapter_initial_list,chapter_initial_path,chapter_initial_audio_path):
    for lst in chapter_initial_list:
        if lst[0]!='0' and lst[0]!=0:
            chapter_num = str(lst[0])

            no_audio_mp4 = chapter_initial_path + chapter_num + '.mp4'
            integrated_mp4 = chapter_initial_audio_path + chapter_num + '.mp4'

            cmd = "ffmpeg -i {} -i {} -shortest {}".format(no_audio_mp4, bgm_mp3, integrated_mp4)
            resp = subprocess.check_output(cmd, shell=True)    
    

def convert_mp4_to_fps30(chapter_initial_list,chapter_initial_audio_path,chapter_initial_converted_path):
    for lst in chapter_initial_list:
        if lst[0]!='0' and lst[0]!=0:
            chapter_num = str(lst[0])

            converted_mp4 = chapter_initial_converted_path + chapter_num + '.mp4'
            integrated_mp4 = chapter_initial_audio_path + chapter_num + '.mp4'

            cmd = "ffmpeg -i {} -vf fps=30 -vsync 1 {}".format(integrated_mp4,converted_mp4)
            resp = subprocess.check_output(cmd, shell=True)  