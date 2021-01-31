import os, sys

from janome.tokenizer import Tokenizer

def split_text(input_text,t):
    text_list = []
    total_num = 0
    temp_text = ''
    temp_block = ''
    tokens_temp = t.tokenize(input_text)
    tokens_len = max([i for i, token in enumerate(tokens_temp)]) + 1
    
    tokens = t.tokenize(input_text)
    
    for i, token in enumerate(tokens):
        token_speech = token.part_of_speech.split(',')
        print(total_num,token)
        total_num += len(token.surface)
        
        if (token_speech[1] == '空白'):
#             print('*空白')
            pass
        elif (token.surface in ['です','ます','だ','である','か','た']):
                temp_text = temp_text + temp_block + token.surface
                text_list.append(temp_text)
#                 print("　　",temp_text)
                
                temp_text = ''
                temp_block = ''
                total_num = len(temp_block)   

        elif (token_speech[0] == '助詞'):
            if total_num < 13:
#                 print('*助詞, 動詞, 10 < ')
                temp_block = temp_block + token.surface
                temp_text = temp_text + temp_block
                temp_block = ''
                
            elif total_num >= 13:
#                 print('*助詞, 動詞, 10> ',temp_text)
                temp_text = temp_text + temp_block + token.surface
                text_list.append(temp_text)
#                 print("　　",temp_text)
                
                temp_text = ''
                temp_block = ''
                total_num = len(temp_block)   
        else:
            temp_block = temp_block + token.surface
#             print('*else')
            
        if (i == (tokens_len-1)):
            temp_text = temp_text + temp_block
            
            if temp_text != '':
                text_list.append(temp_text)
            
            
#             print("　　",temp_text)

            
    return text_list

def split_text_memo(input_text,t):
    text_list = []
    tokens_temp = t.tokenize(input_text)
    integ_text = ''

    tokens_len = max([i for i, token in enumerate(tokens_temp)]) + 1
    
    tokens = t.tokenize(input_text)
    
    for i, token in enumerate(tokens):
        
        if len(integ_text + token.surface) > 15:
            text_list.append(integ_text)
            integ_text = token.surface
            
        else:
            integ_text = integ_text + token.surface
            
        if i == tokens_len  - 1:
            text_list.append(integ_text)
            
    return text_list



def split_frame_code_memo(frame_count,text_list,img_list,memo_list):
    time_frame_list = []
    text_num = len(text_list)
    
    for i in range(0,text_num,1):
        if i < text_num - 1:
            time_frame_list.append([int(frame_count/text_num) * i ,int(frame_count/text_num) * (i+1),text_list[i],img_list[i],memo_list[i]])
        elif i == text_num - 1:
            time_frame_list.append([int(frame_count/text_num) * i ,frame_count,text_list[i],img_list[i],memo_list[i]])
        
    return time_frame_list

def split_frame_code(frame_count,text_list,img_list):
    time_frame_list = []
    text_num = len(text_list)
    
    for i in range(0,text_num,1):
        if i < text_num - 1:
            time_frame_list.append([int(frame_count/text_num) * i ,int(frame_count/text_num) * (i+1),text_list[i],img_list[i]])
        elif i == text_num - 1:
            time_frame_list.append([int(frame_count/text_num) * i ,frame_count,text_list[i],img_list[i]])
        
    return time_frame_list