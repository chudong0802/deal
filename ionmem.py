import re 
import pandas as pd
import os

def find_file(path):
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
                    if 'ionmemalways.log' in os.listdir(sub_path+'/log'):
                        print('exist')
                        tlist = []
                        slist = []
                        total_list = []
                        string = '2020-' + dir_name[i] + ' '
                        with open(sub_path+'/log'+'/ionmemalways.log',encoding='utf-8') as f:
                            content = f.read()
                            str_start = '          client'
                            str_end = 'orphaned allocations'
                            pat = re.compile(str_start + '(.*?)' +str_end,re.S)
                            keycontent = pat.findall(content)
                            for i in range(len(keycontent)):
                                word = keycontent[i].strip().split("\n")
                                for j in range(len(word)):
                                    if '  surfaceflinger' in word[j]:
                                        slist.append(word[j].split(" ")[-1])
                            f.close()
                        with open(sub_path+'/log'+'/ionmemalways.log',encoding='utf-8') as f2:   
                            for line in f2.readlines():
                                if line.strip().endswith('CST 2020'):
                                    time = string +line.split(" ")[-3]
                                    tlist.append(time)
                                elif line.startswith('          total'):
                                    total_size = int(line.split(" ")[-1])
                                    total_list.append(total_size)
                        print(tlist)
                        f2.close()

                        if len(tlist)==len(slist)==len(total_list):
                            dict = {'time':tlist,'surfaceflinger_size(Byte)':slist,'total_size(Byte)':total_list}
                            dataframe = pd.DataFrame(dict)
                            dataframe.to_csv(sub_path+'/analysis/ionmemalways.csv', columns=dict.keys())
                        else:
                            num = min(len(tlist),len(slist),len(total_list))
                            dict1 = {'time':tlist[:num],'surfaceflinger_size(Byte)':slist[:num],'total_size(Byte)':total_list[:num]}
                            dataframe1 = pd.DataFrame(dict1)
                            dataframe1.to_csv(sub_path+'/analysis/ionmemalways.csv',columns=dict1.keys())    
                except:
                    continue
if __name__ == "__main__":
    find_file('./')