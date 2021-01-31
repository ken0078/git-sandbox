
def classify_chapter(sound_list, initial_in_ch_flag = False):

    video_list = []
    subtitles_list = []
    chapter_list = []
    temp_video = []
    temp_sub = []
    in_ch_flag = initial_in_ch_flag

    temp_video = []
    temp_sub = []
    temp_chapters = []

    chapter = 0
    for i, lst in enumerate(sound_list):
        
        if lst['status'] == 'start':
    #         print(temp_sub)
            chapter = lst['chapter']
            in_ch_flag = True
            temp_video = []
            temp_sub = []
            temp_chapters = []
            
            
        elif (lst['status'] == 'text') and (in_ch_flag == True):
            temp_video.append(lst['time_code'])
            temp_sub.append(lst['text'])
            temp_chapters.append(chapter)
            
        elif (lst['status'] == 'end') and (in_ch_flag == True):
            print(temp_sub)
            chapter_list.extend(temp_chapters)
            video_list.extend(temp_video)
            subtitles_list.extend(temp_sub)

    video_sub_list = []

    for i, video_code in enumerate(video_list):
        # print(i)
        video_sub_list.append({'timecode':video_code,'subtitle':subtitles_list[i],'chapter':chapter_list[i]})
    
            
    return     video_sub_list
    
        
def classify_chapter_wihout_startend(sound_list, initial_in_ch_flag = False):

    video_list = []
    subtitles_list = []
    chapter_list = []
    temp_video = []
    temp_sub = []
    in_ch_flag = initial_in_ch_flag

    temp_video = []
    temp_sub = []
    temp_chapters = []

    chapter = 0
    for i, lst in enumerate(sound_list):
        if (lst['status'] == 'text') and (in_ch_flag == True):
            print(lst)
            chapter_list.append(lst['chapter'])
            video_list.append(lst['time_code'])
            subtitles_list.append(lst['text'])            



    video_sub_list = []

    for i, video_code in enumerate(video_list):
        # print(i)
        video_sub_list.append({'timecode':video_code,'subtitle':subtitles_list[i],'chapter':chapter_list[i]})
    
            
    return     video_sub_list
    