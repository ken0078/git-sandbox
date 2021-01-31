import os, sys
import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import copy
from . import edit_subtitle


def cv_add_text(font,input_img,input_list,draw):  
    for temp_lst in input_list:
        # テキストを描画（位置、文章、フォント、文字色（BGR+α）を指定）
        draw.text(temp_lst[0], temp_lst[1], font=font, fill=temp_lst[2])
    
    output_img = np.array(input_img)                                 # PIL型の画像をcv2(NumPy)型に変換
    
    return output_img                                     # 文字入りの画像をリターン


def capture_video(video_path):
    cap = cv2.VideoCapture(video_path)

    ret, screen_shot = cap.read()
    cap.release()
    
    return screen_shot


def make_agenda_picture(font_path, font_size,input_img,chapter_list,chapter_initial_list,agenda_path):
    # 画像に文字を入れる関数
    font = ImageFont.truetype(font_path, font_size)     # PILでフォントを定義
    draw = ImageDraw.Draw(input_img)                          # 描画用のDraw関数を用意
        
    print(input_img.size)

    for chapter_num in chapter_list:
        print(chapter_num)
        
        input_agenda_list = []
        for i, c_lst in enumerate(chapter_initial_list):
            if c_lst[0]!='0' and c_lst[0]!= 0:
                message = c_lst[2]

                if str(c_lst[0]) == str(chapter_num):
                    input_agenda_list.append([(10, i * 40 + 20 ),message,(0, 0, 255, 255)])
                else:
                    input_agenda_list.append([(10, i * 40 + 20),message,(0, 0, 0, 255)])
        
        img_mod = cv_add_text(font,input_img,input_agenda_list,draw)

        cv2.imwrite(agenda_path + str(chapter_num) + '.png', img_mod)


def make_memo_picture(font_path, font_size,input_img,memo_text_list):
    # 画像に文字を入れる関数
    font = ImageFont.truetype(font_path, font_size)     # PILでフォントを定義
    draw = ImageDraw.Draw(input_img)                          # 描画用のDraw関数を用意
        
    print(input_img.size)

    input_memo_list = []

    input_memo_list.append([(170,20), '[MEMO]',(0, 0, 0, 255)])

    for i, memo_text in enumerate(memo_text_list):
        input_memo_list.append([(10, i * 40 + 80 ),memo_text,(0, 0, 0, 255)])

    img_mod = cv_add_text(font,input_img,input_memo_list,draw)

    return img_mod
    

def extract_max_area(face_area_list):
        
    max_list = max(face_area_list, key=(lambda x: x[2]*x[3]))
    
    return max_list


def overlayImage(src, overlay, location):
    overlay_height, overlay_width = overlay.shape[:2]

    # 背景をPIL形式に変換
    src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    pil_src = Image.fromarray(src)
    pil_src = pil_src.convert('RGBA')

    # オーバーレイをPIL形式に変換
    overlay = cv2.cvtColor(overlay, cv2.COLOR_BGRA2RGBA)
    pil_overlay = Image.fromarray(overlay)
    pil_overlay = pil_overlay.convert('RGBA')
       

    # 画像を合成
    pil_tmp = Image.new('RGBA', pil_src.size, (255, 255, 255, 0))
    pil_tmp.paste(pil_overlay, location, pil_overlay)
    result_image = Image.alpha_composite(pil_src, pil_tmp)

    # OpenCV形式に変換
    return cv2.cvtColor(np.asarray(result_image), cv2.COLOR_RGBA2BGR)


def detect_face(frame,cascade):
    temp_face_list = []
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
    
    for (x, y, w, h) in face:
        temp_face_list.append((x, y, w, h))
        
    return temp_face_list



def face_overlay(csv_video_list,rep_img,splited_mp4_path,face_hidden_path):
    for lst in csv_video_list[1:]:    
        cap = cv2.VideoCapture(splited_mp4_path + lst[1])
        ret, frame = cap.read()

        frame_rate = 30
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        writer = cv2.VideoWriter(face_hidden_path  + lst[1], fmt, frame_rate, (width,height))

        cap.release()
        
        # Face Tracking
        cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
        
        cap = cv2.VideoCapture(splited_mp4_path + lst[1])

        lst_num = 0
        
        face_area_list = []
        for i in range(frame_count):
            if i%10 == 0:
                print('write_num:',i/10)
                ret, frame = cap.read()

                temp_face_area_list = detect_face(frame,cascade)
                biggest_face = extract_max_area(temp_face_area_list)
                face_area_list.append(biggest_face)
                
        cap.release()
        
        max_area_face = extract_max_area(face_area_list)
        max_w,max_h = max_area_face[2:4]        
            
        cap = cv2.VideoCapture(splited_mp4_path + lst[1])
        
        read_num = 0
        for i in range(frame_count):
            ret, frame = cap.read()
            
            if i%10 == 0:
                print('read_num:',read_num)
                biggest_face = face_area_list[read_num]
                bx = int(biggest_face[0] + biggest_face[2]/2)        # big_x + big_w/2
                by = int(biggest_face[1] + biggest_face[3]/2)        # big_y + big_h/2
                
                read_num += 1
            
            resized = cv2.resize(rep_img, (max_w,max_h), interpolation = cv2.INTER_AREA)   
            frame = overlayImage(frame, resized, (bx - int(max_w/2), by - int(max_h/2)))

            writer.write(frame)

        writer.release()
        cap.release()

def add_subtitle_video(sub_img,font_path, font_size,csv_video_list,custom_subtitle_list,base_video_path,customized_path,agenda_path,material_path):
    for lst in csv_video_list[1:]:
        
        subtitle_text_list = []
        subtitle_img_list = []
        for c_lst in custom_subtitle_list:
            if c_lst[0] == lst[1]:
                subtitle_text_list.append(c_lst[1])
                subtitle_img_list.append(c_lst[2])
                
        print('subtitle_text_list',subtitle_text_list)
        
        cap = cv2.VideoCapture(base_video_path + lst[1])
        ret, frame = cap.read()
        
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_rate = 30
        frame_list = edit_subtitle.split_frame_code(frame_count, subtitle_text_list,subtitle_img_list)

        print(frame_list)

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

        print('customized_path + lst[1]',customized_path + lst[1])
        writer = cv2.VideoWriter(customized_path + lst[1], fmt, frame_rate, (width,height))

        ret, frame = cap.read()
        cap.release()
        
        cap = cv2.VideoCapture(base_video_path + lst[1])

        count_num = 0
        for i in range(frame_count):
            ret, frame = cap.read()

            time_text_lst = frame_list[count_num]

            temp_subtitle_text = time_text_lst[2]
    

            temp_img = Image.fromarray(sub_img)
            img_w,img_h = temp_img.size    

            
            font = ImageFont.truetype(font_path, font_size)
            draw = ImageDraw.Draw(temp_img) 
            sub_w,sub_h = draw.textsize(temp_subtitle_text,font)

            # overlay agenda img on full sized img
            agenda_img = cv2.imread(agenda_path + lst[0] + '.png', cv2.IMREAD_UNCHANGED)
            resized_agenda_img = cv2.resize(agenda_img, (440,400), interpolation = cv2.INTER_AREA)
            frame = overlayImage(frame, resized_agenda_img, (30, 40))

            # make a subtitle img from a text
            input_list = [[(int((img_w-sub_w)/2),int((img_h-sub_h)/2)),temp_subtitle_text,(255, 255, 255, 255)]]
            img_mod = cv_add_text(font,temp_img,input_list,draw)

            # overlay subtitle img on full sized img
            resized = cv2.resize(img_mod, (1750,160), interpolation = cv2.INTER_AREA)    
            integ_pic = overlayImage(frame, resized, (100,900))


            # overlay insert img on full sized img
            try:
                if time_text_lst[3] != '':
                    temp_insert_img = material_path + time_text_lst[3]
                    insert_img = cv2.imread(temp_insert_img, cv2.IMREAD_UNCHANGED)
            
                    ins_h,ins_w = insert_img.shape[0:2]
                    init_x = 520
                    init_y = 200
                    base_w = 1300
                    base_h = 700

                    opt_w,opt_h,opt_x,opt_y = optimize_size(ins_w,ins_h,base_w,base_h,init_x,init_y)

                    resized_insert = cv2.resize(insert_img, (opt_w,opt_h), interpolation = cv2.INTER_AREA)    
                    integ_pic = overlayImage(integ_pic, resized_insert, (opt_x,opt_y))

                    
            except:
                print("Failed: cannot insert img")

            writer.write(integ_pic)

            if i == (time_text_lst[1]-1):
                count_num += 1


        writer.release()
        cap.release()

def add_tutrial_video(back_img,sub_img,font_path, font_size,csv_video_list,custom_subtitle_list,base_video_path,customized_path,agenda_path,material_path,memo_img,memo_out_img,t):
    background_img = cv2.imread(back_img)
    width = int(background_img.shape[1])
    height = int(background_img.shape[0])
    # print(background_img.shape[0:2])

    memo_text_img_out = make_memo_picture(font_path, 27,memo_out_img,[''])
    memo_text_img_out_resized = cv2.resize(memo_text_img_out, (300,540), interpolation = cv2.INTER_AREA)

    for lst in csv_video_list[1:]:
        subtitle_text_list = []
        subtitle_img_list = []
        subtitle_memo_list = []
        for c_lst in custom_subtitle_list:
            # print(lst,c_lst,)
            if c_lst[0] == lst[1]:
                subtitle_text_list.append(c_lst[1])
                subtitle_img_list.append(c_lst[2])
                subtitle_memo_list.append(c_lst[3])

        print('subtitle_text_list',subtitle_text_list)
        
        cap = cv2.VideoCapture(base_video_path + lst[1])
        ret, frame = cap.read()
        
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_rate = 30
        frame_list = edit_subtitle.split_frame_code_memo(frame_count, subtitle_text_list,subtitle_img_list,subtitle_memo_list)

        # print(frame_list)
        ret, frame = cap.read()
        cap.release()

        fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        writer = cv2.VideoWriter(customized_path + lst[1], fmt, frame_rate, (width,height))
        

        cap = cv2.VideoCapture(base_video_path + lst[1])

        count_num = 0
        for i in range(frame_count):
            ret, frame = cap.read()

            time_text_lst = frame_list[count_num]
            temp_subtitle_text = time_text_lst[2]
    
            temp_img = Image.fromarray(sub_img)
            img_w,img_h = temp_img.size    
            
            font = ImageFont.truetype(font_path, font_size)
            draw = ImageDraw.Draw(temp_img) 
            sub_w,sub_h = draw.textsize(temp_subtitle_text,font)
            

            # overlay agenda img on full sized img
            agenda_img = cv2.imread(agenda_path + lst[0] + '.png', cv2.IMREAD_UNCHANGED)
            resized_agenda_img = cv2.resize(agenda_img, (300,270), interpolation = cv2.INTER_AREA)
            bg_agnd = overlayImage(background_img, resized_agenda_img, (30, 30))

            # overlay memo img on full sized img
            input_text = time_text_lst[4]
            
            if input_text != '':
                memo_font = 27
                memo_text_list = edit_subtitle.split_text_memo(input_text,t)
                print('input_text',input_text)
                copy_memo_img = copy.deepcopy(memo_img)
                memo_text_img = make_memo_picture(font_path, memo_font,copy_memo_img,memo_text_list)
                resized_memo_text_img = cv2.resize(memo_text_img, (300,540), interpolation = cv2.INTER_AREA)
            else:
                resized_memo_text_img = memo_text_img_out_resized
            
            bg_agnd_memo = overlayImage(bg_agnd, resized_memo_text_img, (30, 320))

            # make & overlay a subtitle img from a text
            input_list = [[(int((img_w-sub_w)/2),int((img_h-sub_h)/2)),temp_subtitle_text,(255, 255, 255, 255)]]
            img_mod = cv_add_text(font,temp_img,input_list,draw)
            resized = cv2.resize(img_mod, (1540,140), interpolation = cv2.INTER_AREA)    
            bg_agnd_sub = overlayImage(bg_agnd_memo, resized, (350,910))



            # overlay insert img on full sized img
            # try:
            if time_text_lst[3] != '':
                temp_insert_img = material_path + time_text_lst[3]
                insert_img = cv2.imread(temp_insert_img, cv2.IMREAD_UNCHANGED)
        
                ins_h,ins_w = insert_img.shape[0:2]
                init_x = 350
                init_y = 30
                base_w = 1540
                base_h = 866

                opt_w,opt_h,opt_x,opt_y = optimize_size(ins_w,ins_h,base_w,base_h,init_x,init_y)

                resized_insert = cv2.resize(insert_img, (opt_w,opt_h), interpolation = cv2.INTER_AREA)    
                integ_pic = overlayImage(bg_agnd_sub, resized_insert, (opt_x,opt_y))
                
            else:
                # overlay main img on full sized img
                resized_frame = cv2.resize(frame, (1540,866), interpolation = cv2.INTER_AREA)
                integ_pic = overlayImage(bg_agnd_sub, resized_frame, (350, 30))                

                    
            # except:
                # print("Failed: cannot insert img")

            writer.write(integ_pic)

            if i == (time_text_lst[1]-1):
                count_num += 1


        writer.release()
        cap.release()



def optimize_size(ins_w,ins_h,base_w,base_h,init_x,init_y):

    if ins_h * base_w <= ins_w * base_h:
        opt_w = base_w
        opt_h = ins_h * base_w / ins_w
        opt_x = init_x
        opt_y = init_y + (base_h - opt_h)/2


    else:
        opt_h = base_h
        opt_w = ins_w * base_h / ins_h
        opt_y = init_y
        opt_x = init_x + (base_w - opt_w)/2
        print("insert:",ins_w,ins_h)
        print("base:",base_w,base_h)
        print("opt:" ,int(opt_w),int(opt_h),int(opt_x),int(opt_y))    


    
    return int(opt_w),int(opt_h),int(opt_x),int(opt_y)




def make_init_video(font_path,font_size,mask_img,chapter_initial_path, chapter_initial_list,base_video_path):
    for lst in chapter_initial_list:
        if lst[0]!='0' and lst[0]!= 0:
            chapter_num = str(lst[0])
            input_video = base_video_path + lst[1]
            input_text = lst[2]

            font = ImageFont.truetype(font_path, font_size)     # Text font definition
            temp_img = Image.fromarray(mask_img)                          # cv2(NumPy)型の画像をPIL型に変換
            draw = ImageDraw.Draw(temp_img)                          # 描画用のDraw関数を用意
            img_w,img_h = temp_img.size
            
            w,h = draw.textsize(input_text,font)

            # Overlay text（position、text、font、font color(BGRα)）
            input_list = [[((img_w-w)/2,(img_h-h)/2),input_text,(255, 255, 255, 255)]]

            print(input_list)
            img_mod = cv_add_text(font,temp_img,input_list,draw)              # 画像に文字を入れる関数を実行

            src1 = capture_video(input_video)
            src2 = cv2.cvtColor(np.asarray(img_mod), cv2.COLOR_BGRA2BGR)

            src2_mod = cv2.resize(src2 , (src1.shape[1],src1.shape[0]))
            print(src2_mod.shape[0:2])

            pic_list = []
            for i in range(0,10,1):
                temp_pic = cv2.addWeighted(src1, (0.55 - i*0.05), src2_mod, (0.55 + i*0.05), 0)
                pic_list.append(temp_pic)


            fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
            video  = cv2.VideoWriter(chapter_initial_path + chapter_num +'.mp4', fourcc, 30.0, (pic_list[0].shape[1], pic_list[0].shape[0]))

            pic_num = len(pic_list)
            for i in range(0,pic_num*2+10,1):
                if pic_num > i: 
                    for j in range(0,3,1):
                        video.write(pic_list[i])            
                elif (i >= pic_num) and (pic_num + 10 >i):
                    for j in range(0,3,1):
                        video.write(pic_list[-1])
                else:
                    for j in range(0,3,1):
                        video.write(pic_list[pic_num * 2 + 9 - i])

            video.release()



