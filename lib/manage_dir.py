import os, sys
import datetime

def make_videoname_path(folder_path,video_name):
    try:
        target_folder  = folder_path +'2_splited_audio/a_splited_mp3/' + video_name +'/'
        os.mkdir(target_folder)
    except:
     print("Error: cannot make the path >> " + target_folder)
        
    try:
        target_folder  = folder_path +'2_splited_audio/b_converted_flac/' + video_name +'/'
        os.mkdir(target_folder)
    except:
        print("Error: cannot make the path >> " + target_folder)

        
    try:
        target_folder  = folder_path +'3_generated_video_and_subtitle/a_splited_video/' + video_name +'/'
        os.mkdir(target_folder)
    except:
        print("Error: cannot make the path >> " + target_folder)

    try:
        target_folder  = folder_path +'3_generated_video_and_subtitle/c_generated_agenda/' + video_name +'/'
        os.mkdir(target_folder)
    except:
        print("Error: cannot make the path >> " + target_folder)

    try:
        target_folder  = folder_path +'3_generated_video_and_subtitle/d_0_customized/' + video_name +'/'
        os.mkdir(target_folder)
    except:
        print("Error: cannot make the path >> " + target_folder)

    try:
        target_folder  = folder_path +'material/' + video_name +'/'
        os.mkdir(target_folder)
    except:
        print("Error: cannot make the path >> " + target_folder)

    try:
        target_folder  = folder_path +'3_generated_video_and_subtitle/d_1_customized/' + video_name +'/'
        os.mkdir(target_folder)
    except:
        print("Error: cannot make the path >> " + target_folder)

    try:
        target_folder  = folder_path +'3_generated_video_and_subtitle/e_extracted_audio/' + video_name +'/'
        os.mkdir(target_folder)
    except:
        print("Error: cannot make the path >> " + target_folder)

    try:
        target_folder  = folder_path +'3_generated_video_and_subtitle/f_custom_video_with_audio/' + video_name +'/'
        os.mkdir(target_folder)
    except:
        print("Error: cannot make the path >> " + target_folder)

    try:
        target_folder  = folder_path +'3_generated_video_and_subtitle/g_0_initial_video/' + video_name +'/'
        os.mkdir(target_folder)
    except:
        print("Error: cannot make the path >> " + target_folder)

    try:
        target_folder  = folder_path +'3_generated_video_and_subtitle/g_1_initial_video/' + video_name +'/'
        os.mkdir(target_folder)
    except:
        print("Error: cannot make the path >> " + target_folder)

    try:
        target_folder  = folder_path +'3_generated_video_and_subtitle/g_2_initial_video/' + video_name +'/'
        os.mkdir(target_folder)
    except:
        print("Error: cannot make the path >> " + target_folder)

    try:
        target_folder  = folder_path +'3_generated_video_and_subtitle/h_all_material/' + video_name +'/'
        os.mkdir(target_folder)
    except:
        print("Error: cannot make the path >> " + target_folder)

    try:
        target_folder  = folder_path +'3_generated_video_and_subtitle/i_integrated_video/' + video_name +'/'
        os.mkdir(target_folder)
    except:
        print("Error: cannot make the path >> " + target_folder)


def make_timestamp_path(path_name):
    dt_now = datetime.datetime.now()
    now_text = dt_now.strftime('%Y_%m%d_%H%M_%S')
    
    path_name_mod = path_name + '/' + now_text + '/'
    
    try:
        os.mkdir(path_name_mod)
        print("Succeeded: "+ path_name_mod)
    except:
        print("Failed: "+ path_name_mod)

    return path_name_mod   
    
    
    