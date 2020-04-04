#レコーディングダイエットアプリ
import json, os, textwrap, re
import tkinter as tk

import matplotlib.pyplot as plt#
import matplotlib.ticker as ticker#
from matplotlib.dates import date2num#
from matplotlib.dates import DateFormatter#

from tkinter import messagebox as mbox
from time import strftime
from datetime import datetime

class AppBase(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        header_frame = tk.Frame(self)
        header_frame.pack()
        self.header_label = tk.Label(header_frame)
        self.header_label.pack(side='left', anchor='center')
        self.menu_btn = tk.Button(header_frame, text='メニューに戻る')
        self.pack()
        
    def userentry_widgets(self):
        self.userentry_frame = tk.LabelFrame(self,\
            text='各項目を入力してください')
        tk.Label(self.userentry_frame, text='名前', anchor='e').grid(row=0, column=0)
        self.name = tk.Entry(self.userentry_frame, width=10)
        self.name.grid(row=0, column=1, columnspan=2)
        gender_frame = tk.Frame(self.userentry_frame)
        tk.Label(gender_frame, text='性別', anchor='e').pack(side='left')
        self.gender_iv = tk.IntVar()
        self.gender_dict = {0:'女性', 1:'男性'}
        self.gender_iv.set(0)
        for i,j in self.gender_dict.items():
            rb = tk.Radiobutton(gender_frame, value=i,
                                text=j, variable=self.gender_iv)
            rb.pack(side='left')
        gender_frame.grid(row=0, column=4, columnspan=4)
        tk.Label(self.userentry_frame, text='生年月日', anchor='e').grid(row=1, column=0)
        self.birthday = tk.Entry(self.userentry_frame, width=10)
        self.birthday.insert(0, '1970/01/01')
        self.birthday.grid(row=1, column=1, columnspan=2)
        tk.Label(self.userentry_frame, text='身長', anchor='e').grid(row=1, column=3)
        self.height = tk.Entry(self.userentry_frame, width=5)
        self.height.grid(row=1, column=4)
        tk.Label(self.userentry_frame, text='cm', anchor='w').grid(row=1, column=5)
        tk.Label(self.userentry_frame, text='体重', anchor='e').grid(row=1, column=6)
        self.weight = tk.Entry(self.userentry_frame, width=5)
        self.weight.grid(row=1, column=7)
        tk.Label(self.userentry_frame, text='kg', anchor='w').grid(row=1, column=8)
        tk.Label(self.userentry_frame, text='目標体重', anchor='e').grid(row=2, column=6)
        self.goal = tk.Entry(self.userentry_frame, width=5)
        self.goal.grid(row=2, column=7)
        tk.Label(self.userentry_frame, text='kg', anchor='e').grid(row=2, column=8)
        self.userentry_btn = tk.Button(self.userentry_frame, text='上記の内容で登録する')
        self.userentry_btn.grid(row=3, column=0, columnspan=9, sticky='ew')
        self.userentry_frame.pack()
        
    def menu_widgets(self):
        self.menu_frame = tk.Frame(self)
        tk.Label(self.menu_frame, text='＜レコーディングダイエット＞\n　メニューを選択して下さい').grid(row=0, column=0, columnspan=5)
        self.meal_btn = tk.Button(self.menu_frame,\
            text='食 事 を\n記録する', command=self.meal_widgets)
        self.motion_btn = tk.Button(self.menu_frame,\
            text='運 動 を\n記録する', command=self.motion_widgets)
        self.data_btn = tk.Button(self.menu_frame,\
            text='記録確認\n（修正）', command=self.data_totalization)
        self.meal_btn.grid(row=1, column=0, padx=2)
        self.motion_btn.grid(row=1, column=1)
        self.data_btn.grid(row=1, column=2, padx=2)
        self.userselect_btn = tk.Button(self.menu_frame, text='ユーザー選択に戻る')
        self.userselect_btn.grid(row=2, column=0, columnspan=3, sticky='ew', padx=2, pady=2)
        self.menu_frame.pack()
    
    #---食品登録関連---
    def meal_widgets(self):#レコーディング用・カロリー登録用ウィジェット
        self.menu_frame.pack_forget()
        self.menu_btn.config(command=lambda:self.return_menu(self.meal_frame))
        self.menu_btn.pack(side='right', anchor='e', padx=10)
        self.meal_frame = tk.LabelFrame(self, text='食事の記録(食品データは追加されません)　※ * 印の項目は入力必須です')
        self.recwidget_frame = tk.Frame(self.meal_frame)
        tk.Label(self.recwidget_frame, text='*日付', anchor='e').grid(row=0, column=0, sticky='we')
        self.date = tk.Entry(self.recwidget_frame, width=10)
        self.date.insert(0, strftime('%Y/%m/%d'))
        self.date.grid(row=0, column=1, sticky='we')
        tk.Label(self.recwidget_frame, text='*時間', anchor='e').grid(row=0, column=3, sticky='we')#, columnspan=2)
        self.time = tk.Entry(self.recwidget_frame, width=5)#リストボックスにする？
        self.time.insert(0, strftime('%H:%M'))
        self.time.grid(row=0, column=4, columnspan=2, sticky='we')
        tk.Label(self.recwidget_frame, text=' 体重', anchor='e').grid(row=0, column=6, columnspan=3, sticky='we')
        self.weight =  tk.Entry(self.recwidget_frame, width=5)
        self.weight.grid(row=0, column=9, sticky='we')
        tk.Label(self.recwidget_frame, text='kg', anchor='w').grid(row=0, column=10, sticky='we')
        tk.Label(self.recwidget_frame, text='*品名', anchor='e').grid(row=2, column=0, sticky='we')
        self.food =  tk.Entry(self.recwidget_frame)
        self.food.grid(row=2, column=1, columnspan=10, sticky='we')
        tk.Label(self.recwidget_frame, text=' *総カロリー', anchor='e').grid(row=2, column=11, columnspan=2, sticky='we')
        self.calorie =  tk.Entry(self.recwidget_frame, width=5)
        self.calorie.grid(row=2, column=13, columnspan=2, sticky='we')
        tk.Label(self.recwidget_frame, text='kcal', anchor='w').grid(row=2, column=15, sticky='we')
        self.rec_btn = tk.Button(self.recwidget_frame, text='食事内容を\n記録する', command=self.recording_meal)
        self.rec_btn.grid(row=2, column=16, columnspan=4, sticky='we', ipadx=2)
        tk.Label(self.recwidget_frame,\
            text='※既存のデータから食品を選択する場合、一番下の\n「登録した食品を組み合わせて新規の食品データを作る」から指定して下さい',\
                justify='left', fg='blue').grid(row=3, column=0, columnspan=20, sticky='we')
        self.meal_frame.pack()
        self.recwidget_frame.grid(row=0, column=0, columnspan=30, sticky='we')
        
        self.register_frame = tk.LabelFrame(self.meal_frame,
                                            text='食品データを新規登録する　※ * 印の項目は入力必須です')
        tk.Label(self.register_frame, fg='blue',\
            text='品目を選んで品名とカロリーを入力して下さい\n'\
                +'(品目は上書きで追加可能、登録済みの品名は内容を更新します)',\
                    justify='left').grid(row=0, column=0, columnspan=10, sticky='we')
        tk.Label(self.register_frame, text='*品 目 ', anchor='e').grid(row=1, column=0, sticky='we')
        self.item = tk.Spinbox(self.register_frame, values=[i for i in self.cal.keys()], width=10)
        self.item.grid(row=1, column=1, sticky='we')# columnspan=3,入れると矢印出ねえ
        tk.Label(self.register_frame, text='*品 名 ', anchor='e').grid(row=1, column=2, sticky='we')
        self.itemfood =  tk.Entry(self.register_frame, width=35)
        self.itemfood.grid(row=1, column=3, columnspan=4, sticky='we')
        tk.Label(self.register_frame, text='*カロリー', anchor='e').grid(row=2, column=0, sticky='we')
        self.unit_cal =  tk.Entry(self.register_frame, width=5)#1単位あたりのカロリー
        self.unit_cal.grid(row=2, column=1, sticky='we')
        tk.Label(self.register_frame, text='kcal(1g当たり)　　一食分の量', anchor='e').grid(row=2, column=2, columnspan=3, sticky='we')
        self.intake =  tk.Entry(self.register_frame, width=5)#摂取量
        self.intake.grid(row=2, column=5, sticky='we')
        tk.Label(self.register_frame, text='g', anchor='w').grid(row=2, column=6, sticky='we')
        tk.Label(self.register_frame, text='備考').grid(row=3, column=0, sticky='we')
        self.remarks =  tk.Entry(self.register_frame)#備考欄
        self.remarks.grid(row=3, column=1, columnspan=6, sticky='we')
        self.reg_btn = tk.Button(self.register_frame,\
            text='食品データを\n登録する', command=self.registar_food)
        self.reg_btn.grid(row=3, column=7, columnspan=4, sticky='we')
        self.register_frame.grid(row=1, column=0, columnspan=20, sticky='we')
        
        self.combo_frame = tk.LabelFrame(self.meal_frame,\
            text='登録した食品を組み合わせて新規の食品データを作る')
        self.combo_frame.grid(row=2, column=0, columnspan=20, sticky='we')
        tk.Label(self.combo_frame, fg='blue',\
             text='操作方法： 品目を選ぶ ⇒「この品目から選択」を押す ⇒ 品名を選ぶ ⇒ 摂取量を入力\n'\
                 +'　※選択した品名の1食分の量等を確認する場合は、下の「備考を取得する」を押してください\n'\
                 +'⇒「この内容を入力する」を押す(入力中の食品は下に表示されます)\n'\
                 +'　※入力中の食品を取り消す場合は同じ操作で「この内容を削除する」を押してください\n'\
                 +'⇒ 組み合わせる食品をすべて選択したら、一番下の「上記の内容で転記する」を押す\n'\
                 +'　※[食事の記録]及び[食品データを新規登録する]の品名、カロリー欄等に内容を転記します',\
                 justify='left').grid(row=0, column=0, columnspan=30, sticky='we')
        self.combo_dict = {}
        self.combo_item = tk.Spinbox(self.combo_frame,\
            values=[i for i in self.cal.keys()], width=10)
        self.combo_item.grid(row=1, column=1, sticky='we')
        tk.Button(self.combo_frame, text='この品目\nから選択',\
            command=self.disp_combo_food).grid(row=1, column=2, sticky='we')
        
    def disp_combo_food(self):
        self.combo_food = tk.Spinbox(self.combo_frame, width=14,\
            values=[i for i in self.cal[self.combo_item.get()].keys()])
        self.combo_food.grid_forget()#他の品目を選んでいた場合
        self.combo_food.grid(row=1, column=3, sticky='we')
        tk.Label(self.combo_frame, text='摂取量',\
            anchor='e').grid(row=1, column=4, sticky='we')
        self.conbo_gram = tk.Entry(self.combo_frame, width=5)
        self.conbo_gram.grid(row=1, column=5, sticky='we')
        tk.Label(self.combo_frame,text='g', anchor='w')\
            .grid(row=1, column=6, sticky='we')
        self.combo_entbtn = tk.Button(self.combo_frame,\
            text='この内容を\n入力する', command=self.add_to_combo)
        self.combo_entbtn.grid(row=1, column=7, columnspan=2, sticky='we')#, ipadx=3)
        self.combo_delbtn = tk.Button(self.combo_frame,\
            text='入力中から\n削除する', command=self.delete_combo)
        self.combo_delbtn.grid(row=1, column=9, columnspan=2, sticky='we')#, ipadx=3)
        self.combo_footer = tk.Frame(self.combo_frame)
        remarks_label_frame = tk.LabelFrame(self.combo_footer,\
            text='上記の食品に登録された備考を確認する')
        self.remarks_label = tk.Label(remarks_label_frame)#, anchor='e')
        self.remarks_label.pack(side='left')
        remarks_label_frame.pack(fill='x')
        tk.Button(remarks_label_frame, text='備考を取得する',\
            command=self.get_remarks).pack(side='right')
        combo_label_frame = tk.LabelFrame(self.combo_footer,\
            text='現在入力中の食品')
        combo_label_frame.pack(fill='x')
        combo_text = textwrap.wrap(','.join(i+j[0]+'g:'+str(j[1])+'kcal'\
                 for i,j in self.combo_dict.items()), 65)
        self.combo_label = tk.Label(combo_label_frame, fg='red',\
            text='\n'.join(combo_text)\
                if self.combo_dict else '何も入力されていません')
        self.combo_label.pack()
        self.combo_regbtn = tk.Button(self.combo_footer,\
            text='上記の内容で転記する', command=self.posting_combo)
        self.combo_regbtn.pack(fill='x')
        self.combo_footer.grid(row=2, column=0, columnspan=20, sticky='we')
    #---食品登録関連ここまで---

    #---運動登録関連---
    def motion_widgets(self):
        self.menu_frame.pack_forget()
        self.menu_btn.config(command=lambda:self.return_menu(self.motion_frame))
        self.menu_btn.pack(side='right', anchor='e', padx=10)
        self.motion_frame = tk.LabelFrame(self, text='運動の記録　※ * 印の項目は入力必須です')
        tk.Label(self.motion_frame, fg='blue',\
             text='操作方法： 日付と運動時間を入力 ⇒　活動内容を選択\n'\
                 +'⇒「活動内容から動作を選ぶ」を押す ⇒ 動作を選択\n'\
                 +'⇒ 頑張り度を選択 ⇒「カロリー計算」を押す\n'\
                 +'　※消費カロリーは体重を使って計算します。なるべく入力してください\n'\
                 +'　　(体重の入力がなければ、同日又は直近の日の平均体重が選択されます)\n'\
                 +'⇒ 計算結果に問題がなければ、「この内容で記録する」を押す',\
                 justify='left').grid(row=0, column=0, columnspan=30, sticky='we')
        tk.Label(self.motion_frame, text=' *日付', anchor='e').grid(row=1, column=0, sticky='we')
        self.m_date = tk.Entry(self.motion_frame, width=10)
        self.m_date.insert(0, strftime('%Y/%m/%d'))
        self.m_date.grid(row=1, column=1, sticky='we')
        tk.Label(self.motion_frame, text=' *運動時間', anchor='e').grid(row=1, column=2, columnspan=4, sticky='we')
        self.m_time = tk.Entry(self.motion_frame, width=5)
        self.m_time.grid(row=1, column=6, sticky='we')
        tk.Label(self.motion_frame, text='分　', anchor='w').grid(row=1, column=7, sticky='we')
        tk.Label(self.motion_frame, text='体重', anchor='w').grid(row=1, column=8, sticky='we')
        self.m_weight =  tk.Entry(self.motion_frame, width=5)
        self.m_weight.grid(row=1, column=9, sticky='we')
        tk.Label(self.motion_frame, text='kg', anchor='w').grid(row=1, column=10, sticky='we')
        radio_frame = tk.Frame(self.motion_frame)
        tk.Label(radio_frame, text='活動内容：', anchor='w').pack(side='left')
        self.motion_iv = tk.IntVar()
        self.motion_dict = {0:'運動', 1:'生活'}
        self.motion_iv.set(0)
        for i,j in self.motion_dict.items():
            rb = tk.Radiobutton(radio_frame, value=i,
                                text=j, variable=self.motion_iv)
            rb.pack(side='left')
        radio_frame.grid(row=2, column=0, columnspan=4, sticky='we')
        tk.Button(self.motion_frame, text='活動内容から動作を選ぶ',\
            command=self.disp_activity).grid(row=2, column=4, columnspan=4, sticky='we')
        self.motion_frame.pack()
    
    def disp_activity(self):
        tk.Label(self.motion_frame, text='*動作', anchor='e').grid(row=3, column=0, sticky='we')
        self.activity = tk.Spinbox(self.motion_frame,\
            values=[i for i in self.mets[self.motion_dict[self.motion_iv.get()]].keys()], width=15)
        self.activity.grid(row=3, column=1, columnspan=3, sticky='we')
        tk.Label(self.motion_frame, text=' *頑張り度', anchor='e').grid(row=3, column=4, columnspan=2, sticky='we')
        self.work_dict = {'最弱(×0.7)':0.7, '弱い(×0.8)':0.8, 'やや弱い(×0.9)':0.9,\
            '普通(×1)':1, 'やや強い(×1.2)':1.2, '強い(×1.4)':1.4, '最強(×1.6)':1.6}
        self.work = tk.Spinbox(self.motion_frame,\
            values=[i for i in self.work_dict.keys()], width=10)
        self.work.grid(row=3, column=6, columnspan=2, sticky='we')
        tk.Button(self.motion_frame, text='カロリー計算',\
            command=self.burn_cal_culc).grid(row=3, column=8, columnspan=2, sticky='we')
        self.burn_frame = tk.LabelFrame(self.motion_frame, text='計算結果')
        self.burn_btn = tk.Button(self.burn_frame, text='この内容で記録する')
        self.burn_btn.pack(side='right')
        self.burn_label = tk.Label(self.burn_frame, anchor='e', fg='red')
        self.burn_label.pack(side='right', fill='x')

    def data_widgets(self):#閲覧するデータの期間を指定し、修正等も可能にする
        self.menu_frame.pack_forget()
        self.menu_btn.config(command=lambda:self.return_menu(self.data_frame))
        self.menu_btn.pack(side='right', anchor='e', padx=10)
        self.data_frame = tk.LabelFrame(self, text='データメニューを選択してください')
        self.graph_btn = tk.Button(self.data_frame, text='データをグラフ化', command=self.disp_graph)
        self.graph_btn.grid(row=0, rowspan=2, column=0, columnspan=5, sticky='ewsn')
        self.fix_btn = tk.Button(self.data_frame, text='データを修正する')
        self.fix_btn.grid(row=0, rowspan=2, column=5, columnspan=5, sticky='ewsn')
        self.data_frame.pack()
    
class RecordingDiet(AppBase):
    def __init__(self, master=None):
        super().__init__(master)
        self.user_exist()
    
    #userdata確認関連
    def user_exist(self):
        if os.path.exists('userdata.json'):
            self.open_menu()
        else:
            self.header_label.config(text='個人データを登録します')
            self.userentry_widgets()
            self.userentry_btn.config(command=lambda:self.make_userdata())
            
    def open_menu(self):#userdetaがあればmenuを開く
        self.user = self.load_json('userdata.json')
        self.mets = self.load_json('METsdatabase.json')
        self.cal = self.load_json('caloriedatabase.json')
        self.header_label.config(text=f'{self.user["user"]["name"]}さん、ようこそ')
        self.menu_widgets()
    
    def return_menu(self, frame):
        self.open_menu()
        self.menu_btn.pack_forget()    
        frame.pack_forget()
            
    def make_userdata(self):
        name = self.name.get()
        gender = self.gender_iv.get()
        birthday = self.birthday.get()
        height = self.height.get()
        weight = self.weight.get()
        goal = self.goal.get()
        if all([name, birthday, height, weight, goal]):# str(gender)※必ず選択されるので不要
            try:
                birthday = datetime.strptime(birthday,'%Y/%m/%d').strftime('%Y/%m/%d')#不正な日付か
                if birthday > datetime.now().strftime('%Y/%m/%d'):#生まれている人か
                    raise KeyError
            except:
                mbox.showerror('エラー', '日付が不正です！')
                return
            
            keys = ['name', 'gender', 'birthday', 'height', 'weight', 'goal']
            values = [name, gender, birthday, float(height), float(weight), float(goal)]
            d = {'user':{k:v for k,v in zip(keys, values)}}
            self.write_json('userdata.json', d)#(f'{name}data.json', d)※userを複数作成する場合
            self.userentry_frame.pack_forget()
            self.open_menu()
        else:
            mbox.showerror('エラー', '入力漏れがあります！')
    
    def get_age(self, x):#年齢を基礎代謝計算に用いるため必要
        today = int(time.today().strftime('%Y%m%d'))
        birthday = int(datetime.strptime(x,'%Y/%m/%d').strftime('%Y%m%d'))
        return int((today - birthday)/10000)

    #JSON関連        
    def write_json(self, jsonfile, dictionary):
        with open(jsonfile, 'w')as f:
            json.dump(dictionary, f)#, ensure_ascii=False, sort_keys=True)
    
    def load_json(self, jsonfile):
        with open(jsonfile, 'r')as f:
            return json.load(f)
    
    #食品登録関連
    def get_remarks(self):
        item = self.combo_item.get()
        food = self.combo_food.get()
        remarks = self.cal[item][food][1]
        txt = remarks if remarks != '' else '備考は登録されていません'
        self.remarks_label.config(text=textwrap.wrap(txt, 40))

    def add_to_combo(self):
        gram = self.conbo_gram.get()
        key = self.combo_food.get()
        cal = self.cal[self.combo_item.get()][key][0]
        if all([gram, key]):
            self.remarks_label.config(text='')
            self.combo_dict[key] = [gram, int(float(gram)*float(cal))]
            combo_text = textwrap.wrap(','.join(i+j[0]+'g:'+str(j[1])+'kcal'\
                for i,j in self.combo_dict.items()), 65)
            self.combo_label.config(text='\n'.join(combo_text))
        else:
            mbox.showerror('エラー', '入力漏れがあります！')
        
    def delete_combo(self):
        try:
            target = self.combo_food.get()
            delete = self.combo_dict.pop(target)
            mbox.showinfo('削除完了', f'組み合わせから\n{target}{delete[0]}g:{delete[1]}kcalを削除しました')
            combo_text = textwrap.wrap(','.join(i+j[0]+'g:'+str(j[1])+'kcal'\
                 for i,j in self.combo_dict.items()), 65)
            self.combo_label.config(text='\n'.join(combo_text)\
                 if self.combo_dict else '何も入力されていません')
        except:
            mbox.showerror('エラー', 'その食品はありません！')
    
    def posting_combo(self):
        if self.combo_dict:
            remarks = ','.join(i+str(j[0])+'g' for i,j in self.combo_dict.items())
            totalgram = sum(int(i[0]) for i in self.combo_dict.values())
            totalcal = sum(int(i[1]) for i in self.combo_dict.values())
            unitcal = round(totalcal/totalgram, 2)
            self.food.delete(0, 'end')
            self.food.insert(0, remarks)
            self.calorie.delete(0, 'end')
            self.calorie.insert(0, totalcal)
            self.unit_cal.delete(0, 'end')
            self.unit_cal.insert(0, unitcal)
            self.intake.delete(0, 'end')
            self.intake.insert(0, totalgram)
            self.remarks.delete(0, 'end')
            self.remarks.insert(0, remarks)
            self.combo_dict.clear()
            self.combo_label.config(text='何も入力されていません')
            self.conbo_gram.delete(0, 'end')
        else:
            mbox.showerror('エラー', '何も入力されていません！')
    
    def recording_meal(self):#食事記録('get')
        date = self.date.get()#必須項目
        time = self.time.get()#必須項目
        food = self.food.get()#必須項目
        calorie = self.calorie.get()#必須項目
        if not all([date, time, food, calorie]):
            mbox.showerror('エラー', '入力漏れがあります！')
            return
        try:#日時を0埋めに直す
            date = datetime.strptime(date, '%Y/%m/%d').strftime('%Y/%m/%d')#不正な日付か
            time = datetime.strptime(time, '%H:%M').strftime('%H:%M')#不正な時間か
            if date > datetime.now().strftime('%Y/%m/%d'): 
                raise KeyError
        except:
            mbox.showerror('エラー', '日時が不正です！')
            return
        if date in self.user:#日付があるか
            if 'get' in self.user[date]:#食事入力があるか
                if time in self.user[date]['get']:#時間があるか
                    if not food in self.user[date]['get'][time]:#食事重複なし
                        self.user[date]['get'][time][food] = int(calorie)
                    else:#食事が重複
                        mbox.showerror('エラー', 'そのデータは既に登録済みです')
                        return
                else:#時間、食事なし
                    value = {food : int(calorie)}
                    self.user[date]['get'][time] = value
            else:#食事入力なし
                value = {time : {food : int(calorie)}}
                self.user[date]['get'] = value
        else:#日付、食事、時間なし(新規登録)
            value = {'get': {time : {food : int(calorie)}}}
            self.user[date] = value
        
        weight = self.weight.get()#体重はdate['weight']のリスト内へ入れる
        if weight:#体重入力あり
            if 'weight' in self.user[date]:
                self.user[date]['weight'].append(float(weight))
            else:#体重登録なし(新規登録)
                self.user[date]['weight'] = [float(weight)]
        self.write_json('userdata.json', self.user)
        u = self.load_json('userdata.json')#DEBUG
        self.food.delete(0, 'end')
        self.calorie.delete(0, 'end')
        self.weight.delete(0, 'end')
        print(f'\n{u}')#DEBUG

    def registar_food(self):#食品データ登録
        item = self.item.get()#必須項目
        food = self.itemfood.get()#必須項目
        cal = self.unit_cal.get()#必須項目
        if not all([item, food, cal]):
            mbox.showerror('エラー', '入力漏れがあります！')
            return
        
        remarks = self.remarks.get()#備考
        intake = f'1食{self.intake.get()}g' if self.intake.get() else ''#1食分の量(備考に追記)
        if item in self.cal:#品目があるか
            if food in self.cal[item]:#品名があるか
                answer = mbox.askokcancel('登録前確認',\
                    f'既に登録済みの品名です。上書きしますか？\n\n食 品 名：{food}\n'\
                    +'\n'.join(f'1g当たり：{i}kcal' if isinstance(i,float)\
                     else f' 備　考 ：{i}' for i in self.cal[item][food]))
                if answer:#上書きする
                    self.cal[item][food] = [float(cal), f'{remarks}、{intake}']
                else:#上書きしない
                    return
            else:#品名がない(新規登録)
                self.cal[item][food] = [float(cal),f'{remarks}、{intake}']    
        else:#品目がない(新規登録)
            self.cal[item] = {food : [float(cal),f'{remarks}、{intake}']}

        self.write_json('caloriedatabase.json', self.cal)
        c = self.load_json('caloriedatabase.json')#DEBUG
        print(f'{c}')#DEBUG OK
    
    #運動登録関連
    def burn_cal_culc(self):
        date = self.m_date.get()#必須
        weight = self.m_weight.get()#無ければ他から取ってこさせる
        mets = self.mets[self.motion_dict[self.motion_iv.get()]][self.activity.get()]#動作
        work = self.work_dict[self.work.get()]
        time = self.m_time.get()#ここでは判定だけに用いる
        try:#日を0埋めに直す
            date = datetime.strptime(date, '%Y/%m/%d').strftime('%Y/%m/%d')#不正な日付か
            if date > datetime.now().strftime('%Y/%m/%d'): 
                raise KeyError
        except:
            mbox.showerror('エラー', '日付が不正です！')
            return

        index = sorted(self.user['daily_total'])#平均体重存在確認用
        if not weight:#体重入力無し
            if not date in self.user:#この日の体重データがない
                if not index:#平均体重データもない
                    weight = self.user['user']['weight']#開始時の体重で計算
                else:#平均体重データはある
                    weight = self.user['daily_total'][index[-1]][0]#直近の平均体重で計算
            else:#この日の体重データがある
                lst = self.user[date]['weight']
                weight = round(sum(lst)/len(lst), 1)#この日の平均体重で計算
        else:#体重入力がある場合
            weight = float(weight)#浮動小数点数に変換

        if all([mets, weight, time, work]):
            self.burn_cal = int(mets * float(weight) * int(time)/60 * work * 1.05)
            self.burn_label.config(text=f'{self.activity.get()}{time}分(体重{weight}kgで計算)\n頑張り度：{self.work.get()}\n消費カロリー：{self.burn_cal}kcal')
            self.burn_btn.config(command=self.recording_motion)
            self.burn_frame.grid(row=4, rowspan=3, column=0, columnspan=10, sticky='wesn')
            self.burn_weight = weight
        else:
            mbox.showerror('エラー', '入力漏れがあります！')
    
    def recording_motion(self):#運動記録('burn')
        date = datetime.strptime(self.m_date.get(), '%Y/%m/%d').strftime('%Y/%m/%d')#必須項目
        motion = f'{self.activity.get()}{self.m_time.get()}分'#必須項目
        lst = [self.work.get(), self.burn_weight, self.burn_cal]#
        if date in self.user:#日付があるか
            if 'burn' in self.user[date]:#運動入力があるか
                if not motion in self.user[date]['burn']:#運動重複なし
                    self.user[date]['burn'][motion] = lst
                else:#運動が重複
                    mbox.showerror('エラー', 'そのデータは既に登録済みです')
                    return
            else:#運動入力なし
                self.user[date]['burn'] = {motion : lst}
        else:#日付、運動なし(新規登録)
            self.user[date] = {'burn': {motion : lst}}
        
        weight = self.m_weight.get()#体重はdate['weight']のリスト内へ入れる
        if weight:#体重入力あり
            if 'weight' in self.user[date]:
                self.user[date]['weight'].append(float(weight))
            else:#体重登録なし(新規登録)
                self.user[date]['weight'] = [float(weight)]
        self.write_json('userdata.json', self.user)
        u = self.load_json('userdata.json')#DEBUG
        self.burn_frame.grid_forget()
        self.m_time.delete(0, 'end')
        self.m_weight.delete(0, 'end')
        print(f'\n{u}')#DEBUG
    
    #データ集計・修正関連
    def data_totalization(self):#self.user['daily_total'][日付]]内の各リストに日計データを差し込む
        #毎回データをすべて再集計する(登録済みの内容を消す)
        self.user['daily_total'].clear()

        #self.user['daily_total'][日付] = [ave_weight, total_burn, total_get]の辞書内リスト形式で定義
        #   ※特定の要素がなければ0(体重の場合は前日と同じ値)を挿入する
        for k,v in self.user.items():
            #print(k,v)#DEBUG
            if re.match('\d{4}/\d{2}/\d{2}', k):#kが日付のものだけ集計する
                self.user['daily_total'][k] = []
                if 'weight' in v:#体重データがある
                    ave_weight = round(sum(v['weight'])/len(v['weight']), 1)
                    #print(round(sum(v['weight'])/len(v['weight']), 1))#DEBUG OK
                elif all((i for i in self.user['daily_total'].values())):#体重データはないが平均体重がある
                    index = sorted(self.user['daily_total'])
                    ave_weight = self.user['daily_total'][index[-2]][0]#前の平均体重
                else:#その日の体重データも平均体重も無い
                    ave_weight = self.user['user']['weight']#開始時の体重を平均体重とする
                self.user['daily_total'][k].append(ave_weight)#リスト[0]に追加

                if 'burn' in v:#burn(運動)がある
                    total_burn = sum(lst[-1] for motion,lst in v['burn'].items())
                    #print(total_burn)#DEBUG OK
                else:#運動がない
                    total_burn = 0
                self.user['daily_total'][k].append(total_burn)#リスト[1]に追加
                
                if 'get' in v:#get(食事)がある
                    gets = [[cal for cal in food_cal.values()]for time,food_cal in v['get'].items()]
                    total_get = sum(sum(cal) for cal in gets)
                    #print(total_get)#DEBUG OK
                else:#食事がない
                    total_get = 0
                self.user['daily_total'][k].append(total_get)#リスト[2]に追加
        #データ書き込み
        self.write_json('userdata.json', self.user)
        u = self.load_json('userdata.json')#DEBUG
        print(u)#DEBUG OK
        self.data_widgets()
    
    def disp_graph(self):
        days = [datetime.strptime(i,'%Y/%m/%d') for i in sorted(self.user['daily_total'])]
        weights = []
        burns = []
        gets = []
        for lst in self.user['daily_total'].values():
            weights.append(lst[0])
            burns.append(lst[1])
            gets.append(lst[2])
        #print(f'days:{days}\nweights:{weights}\nburns{burns}\ngets{gets}')#DEBUG OK
        fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=(9, 6))
        ax1.plot(days, weights, label='Weight')
        ax2.plot(days, burns, label='Burned_calorie', color='r')
        ax3.plot(days, gets, label='Intaked_calorie', color='g')
        ax1.set_title('Recording Diet Graph')
        ax3.set_xlabel('Days')
        ax1.set_ylabel('Weight')
        ax2.set_ylabel('Burned calorie')
        ax3.set_ylabel('Intaked calorie')
        plt.xticks(days, rotation=90, size='small')
        new_xticks = date2num(days)
        ax1.xaxis.set_major_locator(ticker.FixedLocator(new_xticks))
        ax1.xaxis.set_major_formatter(DateFormatter('%Y/%m/%d'))
        ax2.xaxis.set_major_locator(ticker.FixedLocator(new_xticks))
        ax2.xaxis.set_major_formatter(DateFormatter('%Y/%m/%d'))
        ax3.xaxis.set_major_locator(ticker.FixedLocator(new_xticks))
        ax3.xaxis.set_major_formatter(DateFormatter('%Y/%m/%d'))
        fig.tight_layout()#表示範囲の自動修正
        plt.grid(True)
        plt.legend()#線の名前を表示
        plt.show()

root = tk.Tk()
root.title("Let's レコーディングダイエット")
root.geometry('500x600+400+300')
app = RecordingDiet(root)
app.mainloop()
