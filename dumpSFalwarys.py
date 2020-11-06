import os
import re 
import pandas as pd

def find_file(path):
    #1.确认要处理的log文件是否存在
    dir_name = os.listdir(path)
    print(dir_name)
    for i in range(len(dir_name)):
        sub_path=os.path.join(path,dir_name[i])
        print(sub_path)
        if os.path.isdir(sub_path):
            sub_fname = os.listdir(sub_path)
            print(sub_fname)
            if 'analysis' not in sub_fname:
                os.makedirs(sub_path+'/analysis')
            if 'log' in sub_fname:
                try:
                    #2.确认log文件存在，进行关键内容的提取
                    if 'dumpSFalwarys.log' in os.listdir(sub_path+'/log'):
                        print('exist')
                        tlist = []
                        alist = []
                        layer1list = []
                        layer0list = []
                        bufferlist = []
                        with open(sub_path+'/log'+'/dumpSFalwarys.log',encoding='utf-8') as f:
                            content = f.read()
                            str_start = "Display 1 HWC layers:"
                            str_end = "Display 0 HWC layers"
                            pat = re.compile(str_start + '(.*?)' + str_end,re.S)
                            keycontent = pat.findall(content)
                            for n in range(len(keycontent)):
                                display_1_layer = int((len(keycontent[n].strip().split('\n'))-4)/3)
                                layer1list.append(display_1_layer)                 

                            str_start_second = "Display 0 HWC layers:"
                            str_end_second = "h/w"
                            second_pat = re.compile(str_start_second + '(.*?)' + str_end_second,re.S)
                            second_keycontent = second_pat.findall(content)
                            for j in range(len(second_keycontent)):
                                display_0_layer = int((len(second_keycontent[j].strip().split('\n'))-4)/3)
                                layer0list.append(display_0_layer)

                            start = "Allocated buffers:" 
                            end = "Total allocated"
                            third_pat = re.compile(start + '(.*?)' + end,re.S)
                            key = third_pat.findall(content)
                            for k in range(len(key)):
                                buffers = int(len(key[k].strip().split('\n')))
                                bufferlist.append(buffers)
                            f.close()

                        with open(sub_path+'/log'+'/dumpSFalwarys.log',encoding='utf-8') as f2:
                            for line in f2.readlines():
                                if line.strip().endswith('CST 2020'):
                                    time = '2020-' + dir_name[i] + ' '  + line.split(" ")[-3]
                                    tlist.append(time)
                                elif line.startswith("Total allocated"):
                                    total_allocated = line.split(":")[-1].strip().split(" ")[0]
                                    alist.append(total_allocated)
                            print(tlist)
                            f2.close()
                        
                        if len(tlist)==len(alist)==len(layer1list)==len(layer0list)==len(bufferlist):
                            dict = {'time':tlist,'total_allocated(KB)':alist,'display_0_layer':layer0list,'display_1_layer':layer1list,'buffers':bufferlist}
                            dataframe = pd.DataFrame(dict)
                            # print(dataframe)
                            dataframe.to_csv(sub_path+'/analysis/dumpSFalwarys.csv', columns=dict.keys())
                        else:
                            num = min(len(tlist),len(alist),len(layer1list),len(layer0list),len(bufferlist))
                            dict1 = {'time':tlist[:num],'total_allocated(KB)':alist[:num],'display_0_layer':layer0list[:num],'display_1_layer':layer1list[:num],'buffers':bufferlist[:num]}
                            dataframe1 = pd.DataFrame(dict1)
                            dataframe1.to_csv(sub_path+'/analysis/dumpSFalwarys.csv',columns=dict1.keys())                       
                except:
                    continue
if __name__ == "__main__":
    find_file('./')