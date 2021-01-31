import csv
from . import edit_subtitle

def write_dict_to_csv(video_sub_list,video_data_csv,splited_mp4_path):
    with open(splited_mp4_path + video_data_csv, 'w') as f:
        writer = csv.DictWriter(f, ['chapter', 'video_name', 'subtitle'], extrasaction='ignore')
        writer.writeheader()
        
        for lst in video_sub_list:
            writer.writerow(lst)


def write_subtitle_list_to_csv(t,csv_video_list,splited_subtitle_path):
    with open(splited_subtitle_path + 'subtitle.csv', 'w') as f:
        writer = csv.writer(f)

        for lst in csv_video_list[1:]:
            subtitle_text_list = edit_subtitle.split_text(lst[2],t)
            
            for s_text in subtitle_text_list:
                writer.writerow([lst[1],s_text,"",""])

def read_subtitle_list_from_csv(splited_subtitle_path):
    custom_subtitle_list = []

    with open(splited_subtitle_path +  'subtitle.csv') as f:
        reader = csv.reader(f)
        custom_subtitle_list = [x for x in reader]

    return custom_subtitle_list
