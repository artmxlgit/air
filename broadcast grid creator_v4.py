import datetime, time
import os
import subprocess
import pprint, re
import random
import string
import codecs
from tkinter import *
from colorama import Fore, Back, Style
from colorama import init
init()
random.seed(datetime.datetime.now())

def randomString(stringLength=8): # случайное название
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def randomOrder_key(element):
    return random.random()

def getLength(filename): # Узнать длинну видео
    result = subprocess.Popen(["ffprobe", "-i", filename],stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    A = (result.stdout.readlines())
    B = re.findall('Duration: (\d\d:\d\d:\d\d)', str(A))
    C = B[0].split(':')
    TIME = datetime.timedelta(hours=int(C[0]), minutes=int(C[1]), seconds=int(C[2]))
    return TIME


class Main():

    def __init__(self):
        self.Play_list = []
        self.air = [] # эфир
        self.intro = [] # заставка
        self.air_add = []
        self.air_old = []
        self.read_dir_to_filling_base() # база наполнения канала
        self.read_air_add()
        self.read_intro_add()
        self.Sort_rand()
        self.read_air_old()

        path = 'D:\\AIR\\air_fresh'
        Video = os.listdir(path); VP = path + '\\' + Video[0]
        Len = getLength(VP)
        for h in (7,10,12,15,19,21):
            self.air.append({'name':VP, 'start':datetime.timedelta(hours=h), 'len':Len, 'block':'', 'logo':''}) # air

        path = 'D:\\AIR\\museum'
        Video = os.listdir(path); VP = path + '\\' + Video[0]
        Len = getLength(VP)
        for h in (13,16,20):
            self.air.append( {'name':VP, 'start':datetime.timedelta(hours=h), 'len':Len, 'block':'', 'logo':''} ) # old_string


        path = 'D:\\AIR\\region'
        Video = os.listdir(path); VP = path + '\\' + Video[0]
        Len = getLength(VP)
        for h in (9,11,14,18,22):
            self.air.append( {'name':VP, 'start':datetime.timedelta(hours=h), 'len':Len, 'block':'air_region_and_old', 'logo':''} )


    def read_dir_to_filling_base(self):
        path = 'D:\\AIR\\channel_filling' # наполнение кананала
        files = os.listdir(path)
        self.filling_base = []
        for i in files:
            name = path + '\\' + i
            self.filling_base.append( { 'name':name, 'len':getLength(name) } )

    def read_air_old(self):
        path = 'D:\\AIR\\air_old'
        Video = os.listdir(path)
        for i in Video:
            name = path + '\\' + i
            self.air_old.append( {'name':name, 'len':getLength(name), 'logo':'repeat'} )


    def read_air_add(self):
        path = 'D:\\AIR\\quadrocopter'
        files = os.listdir(path)
        for i in files:
            name = path + '\\' + i
            self.air_add.append({ 'name':name, 'len':getLength(name) })

    def read_intro_add(self):
        path = 'D:\\AIR\\intro'
        files = os.listdir(path)
        for i in files:
            name = path + '\\' + i
            self.intro.append({ 'name':name, 'len':getLength(name) })


    def save_list(self): # 06:00:00:00	00:00:00:00	
        file = codecs.open("D:\\AIR\\air.playlist", "w", "utf-8")
        Z = ''
        self.Play_list.reverse()
        for i in self.Play_list:
            Z += i
        
        file.write(Z)
        file.close()


    def Create_random_Basa(self): # создать случайную базу видео. Пустышка
        self.BASA = {}
        for i in range(30):
            name = randomString(8) + '.mp4'
            Time = datetime.timedelta(hours=random.randint(0,1), minutes=random.randint(0,10), seconds=random.randint(0,59), microseconds=0)
            self.filling_base[name] = Time
    

    def Show_BASA(self): # показать базу
        pprint.pprint(self.filling_base)


    def Show_playlist(self):
        listbox.delete('1.0', END)
        self.Play_list.reverse()
        for i in self.Play_list:
            listbox.insert(1.0, i)


    def Sort(self): # сортировать по возрастанию длительности видео
        #s = {k: v for k, v in sorted(self.filling_base.items(), key=lambda item: item[1])}
        self.filling_base.sort()

    def Sort_rand(self):
        random.shuffle(self.filling_base)

    def Del_by_time(self):
        print('del')
        for n, i in enumerate(self.air):
            s = (i['start'])
            if s == self.cur_time: 
                del self.air[n]
                break

    def Add_to_Play_list(self, video, Bl='', Logo=''): # начало, длинна, название, блок, лого
        '''
        Добавить видео в готовый плейлист
        '''
        S = self.cur_time
        N = video['name']
        L = video['len']
        if Bl: B = f'<eob>_{Bl}_<eob>'
        else: B = Bl
        if "#" in N: Logo='old_string' # если в названиее символ "#" - добавить лого
        if "%" in N: Logo='repeat' # повторы
        pl = '	{0}			{1}	00:00:00:00	'.format(Logo, B) # лого и блок
        u = 'UTF8'
        STR = f'{S}:00	{L}:00	{u}{N}{pl}{L}:00\n' #.format(S, L, N, pl)
        print(Back.BLACK + '  '*5, N, L)
        self.Play_list.append(STR)
        self.cur_time += L


    def find_from_filling(self, need_time):
        '''
        Поиск видео под свободно место из файлов заполнения
        '''
        result = None
        
        for x, f in enumerate(self.filling_base):
            mini = need_time - datetime.timedelta(minutes=1)
            if (f['len'] < need_time) and (f['len'] > mini):
                result = f
                print(f['len'], need_time)

        if not result: print('!!!')
        print(Back.YELLOW + ' + Добивка:', result)
        
        return result



    def check_old(self, block):
        if block == 'air_region_and_old': # добавить второй файл после
            n = self.air_old[0]
            #print(n)
            self.Add_to_Play_list(n, '', 'repeat')


    def air_check(self):
        '''
        Вставить видео по времени (Выпуск)
        '''
        next_video = self.filling_base[0]
        next_time = next_video['len'] + self.cur_time

        for air in self.air:
            if next_time > air['start']: # если время больше времени Выпуска
                
                need_time = air['start'] - self.cur_time # шаг назад
                print(Back.RED +'    need_time: ', need_time)

                
                video = self.find_from_filling(need_time)
                if video: self.Add_to_Play_list(video,'','')


                self.cur_time = air['start']
                self.Play_list.append('{0}:00	00:00:00:00	\n'.format(self.cur_time)) # якорь
                #if n['len'] > datetime.timedelta(minutes=59): # если видео больше 1 часа
                    #n['len'] = datetime.timedelta(minutes=59)

                self.Add_to_Play_list(air, air['block'], air['logo']) # поставить на эфир
                self.Del_by_time() # удалить из списка на эфир
                self.check_old(air['block']) # добавить второй файл после
                intro = random.choice(self.intro)
                self.Add_to_Play_list(intro,'','') # добавить в плейлист заставка

                break


    def Start(self):
        '''
        Основной цикл. Начало
        '''
        self.cur_time = datetime.timedelta(hours=0)
        
        while True:
            print(Back.BLUE + '- Время:', self.cur_time) 
            intro = random.choice(self.intro)
            self.Add_to_Play_list(intro,'','') # добавить в плейлист заставка

            if len(self.air) > 0: self.air_check() # проверка на время зфира

            next_video = self.filling_base.pop(0)
            self.Add_to_Play_list(next_video,'logo_24') # добавить в плейлист

            if self.cur_time > datetime.timedelta(hours=23): break # закончить плейлист

            if len(self.filling_base) == 0: # повторить список заново
                self.read_dir_to_filling_base() 
                next_video = self.filling_base.pop(0)
            print('   '*10)


M = Main()

root = Tk()
root.geometry('1200x500')

listbox = Text(root,height=25,font='Arial 9')
listbox.pack(fill=X)

A = Button(root, text='Создать', command=M.Start); A.pack(side=LEFT)
b = Button(root, text='Заполнить лист', command=M.Show_playlist); b.pack(side=LEFT)
c = Button(root, text='Сохранить лист', command=M.save_list); c.pack(side=LEFT)
#D = Button(root, text='Сохранить лист', command=M.save_list); c.pack(side=LEFT)

root.mainloop()
