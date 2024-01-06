import pandas as pd
import numpy as np

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate

class main_window(QWidget):

    def __init__(self):
        super().__init__()
        
    def set_window(self, MainWindow):
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowTitle('reservation system')
        self.set_description()
        self.set_list_reservation_bottons()
        self.set_fillout_form_bottons()
        self.set_calendar()
        self.set_date_bottons()
        self.set_shift_bottons()
        self.mod_flag = 0
        
    def set_description(self):
        self.description1 = QLabel(self)
        self.description1.setText("<font size=5>~このアプリの使い方~</font>")
        self.description1.move(20,10)
        self.description2 = QLabel(self)
        self.description2.setText("<font size=3>1. 検索したい日付をカレンダーから選択してください</font>")
        self.description2.move(20,40)
        self.description3 = QLabel(self)
        self.description3.setText("<font size=3>2. 予約を編集したい場合は左下の画面から1つを選択してください</font>")
        self.description3.move(20,60)
        self.description3 = QLabel(self)
        self.description3.setText("<font size=3>3. 新規作成or予約編集は右画面に必要事項を記入してください</font>")
        self.description3.move(20,80)
        self.description3 = QLabel(self)
        self.description3.setText("<font size=3>4. 画面右下のボタンで変更内容を保存してください</font>")
        self.description3.move(20,100)
    
    def set_calendar(self):
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.move(25, 125)
        self.calendar.resize(580, 370)
        self.calendar.clicked[QDate].connect(self.substract_reservation) # 日付クリックでその日入っている予約を抽出し表示する
        self.selected_date_label = QLabel(self)
        self.selected_date_label.setText("選択中: ") 
        self.selected_date_label.move(30, 510)

    def set_date_bottons(self):
        self.selected_date = QLabel(self)
        self.selected_date.resize(100, 20)
        date = self.calendar.selectedDate()
        ID = date.toString().split(" ")[3] + "-" + date.toString().split(" ")[1] + "-" + date.toString().split(" ")[2]
        self.selected_date.setText(ID) # 日付をラベルにセット
        self.selected_date.move(80, 508)
        self.substract_reservation(date)

    def set_list_reservation_bottons(self):
        self.rlabel0 = QLabel(self)
        self.rlabel1 = QLabel(self)
        self.rlabel2 = QLabel(self)
        self.rlabel3 = QLabel(self)
        self.rlabel0.setText("氏名")
        self.rlabel1.setText("人数")
        self.rlabel2.setText("時間")
        self.rlabel3.setText("部屋")
        self.rlabel0.move(60, 540)
        self.rlabel1.move(200, 540)
        self.rlabel2.move(340, 540)
        self.rlabel3.move(480, 540)

        self.checkbox = [QCheckBox(self) for i in range(9)]
        start = [30, 560]
        for i in self.checkbox:
            i.move(start[0], start[1])
            start[1] += 20

        self.namebox = [QLineEdit(self) for i in range(9)]
        start = [60, 560]
        for i in self.namebox:
            i.move(start[0], start[1])
            start[1] += 20
        
        self.numbox = [QLineEdit(self) for i in range(9)]
        start = [200, 560]
        for i in self.numbox:
            i.move(start[0], start[1])
            start[1] += 20

        self.timebox = [QLineEdit(self) for i in range(9)]
        start = [340, 560]
        for i in self.timebox:
            i.move(start[0], start[1])
            start[1] += 20

        self.roombox = [QLineEdit(self) for i in range(9)]
        start = [480, 560]
        for i in self.roombox:
            i.move(start[0], start[1])
            start[1] += 20
        
        self.new = QPushButton("新規登録", self)
        self.new.move(700, 690)
        self.new.resize(100, 30)
        self.new_cb = QCheckBox(self)
        self.new_cb.clicked.connect(self.cb_initialized_new) # 新規作成, 編集, 削除のチェックボックスはいずれか一つしか選択状態にできない
        self.new_cb.move(670, 695)
        
        self.modified = QPushButton("編集", self)
        self.modified.move(700, 720)
        self.modified.resize(100, 30)
        self.modified_cb = QCheckBox(self)
        self.modified_cb.clicked.connect(self.cb_initialized_mod) # 新規作成, 編集, 削除のチェックボックスはいずれか一つしか選択状態にできない
        self.modified_cb.move(670, 725)

        self.delete = QPushButton("削除", self)
        self.delete.move(700, 750)
        self.delete.resize(100, 30)
        self.delete_cb = QCheckBox(self)
        self.delete_cb.clicked.connect(self.cb_initialized_del) # 新規作成, 編集, 削除のチェックボックスはいずれか一つしか選択状態にできない
        self.delete_cb.move(670, 755)

        self.check = QPushButton("詳細確認", self)
        self.check.move(30, 750)
        self.check.resize(200, 30)

    def cb_initialized_del(self):
        self.modified_cb.setChecked(False)
        self.new_cb.setChecked(False)

    def cb_initialized_new(self):
        self.delete_cb.setChecked(False)
        self.modified_cb.setChecked(False)

    def cb_initialized_mod(self):
        self.delete_cb.setChecked(False)
        self.new_cb.setChecked(False)

    def set_fillout_form_bottons(self):
        self.title_label = QLabel(self)
        self.title_label.move(770, 25)
        self.title_label.setText("<font size=7>登録内容確認フォーム</font>")

        self.date_label = QLabel(self)
        self.name_label = QLabel(self)
        self.num_label = QLabel(self)
        self.time_label = QLabel(self)
        self.room_label = QLabel(self)
        self.tel_label = QLabel(self)
        self.remarks_label = QLabel(self)
        self.shift_label = QLabel(self)
        labels = [self.date_label, self.name_label, self.num_label, self.time_label, self.room_label, self.tel_label, self.remarks_label, self.shift_label]
        label_val = ["日付", "氏名(ふりがな)", "人数", "時間", "部屋", "連絡先", "備考", "シフト"]
        label_start = [670, 80]
        steps = [0, 60, 60, 60, 60, 60, 60, 120]
        for n, i in enumerate(labels):
            label_start[1] += steps[n]
            i.move(label_start[0], label_start[1])
            i.setText("<font size=5>"+label_val[n]+"</font>")

        self.date_y_val = QLineEdit(self)
        self.date_y_val.move(720, 85)
        self.date_tex0 = QLabel(self)
        self.date_tex0.move(850, 87)
        self.date_tex0.setText("年")
        self.date_m_val = self.dec_combbox(self.month)
        self.date_m_val.move(870, 81)
        self.date_tex1 = QLabel(self)
        self.date_tex1.move(947, 87)
        self.date_tex1.setText("月")
        self.date_d_val = QLineEdit(self)
        self.date_d_val.move(965, 85)
        self.date_tex2 = QLabel(self)
        self.date_tex2.move(1093, 87)
        self.date_tex2.setText("日")
        self.name_val = QLineEdit(self)
        self.name_val.move(815, 145)
        self.kana_tex0 = QLabel(self)
        self.kana_tex0.move(950, 145)
        self.kana_tex0.setText("(")
        self.kana_val = QLineEdit(self)
        self.kana_val.move(960, 145)
        self.kana_tex0 = QLabel(self)
        self.kana_tex0.move(1087, 145)
        self.kana_tex0.setText(")")
        self.num_val = QLineEdit(self)
        self.num_val.move(720, 205)
        self.num_tex0 = QLabel(self)
        self.num_tex0.move(850, 207)
        self.num_tex0.setText("名")
        self.time_val = self.dec_combbox(self.time_sel)
        self.time_val.move(720, 259)
        self.room_val = self.dec_combbox(self.room_sel)
        self.room_val.move(720, 319)
        self.tel_val = QLineEdit(self)
        self.tel_val.move(750, 381)
        self.remarks_val = QTextEdit(self)
        self.remarks_val.setPlaceholderText("")
        self.remarks_val.move(720, 439)
        self.remarks_val.resize(400, 100)

    def set_shift_bottons(self):
        self.shift_bottons = []
        for i in range(len(self.member)):
            self.shift_bottons.append([QLabel(self), self.dec_combbox(self.member_status)])
        x_cnt = 0
        y_cnt = 0
        start = [700, 595]
        step_x = 0
        step_y = 0
        for n, i in enumerate(self.shift_bottons):
            i[0].setText(self.member[n])
            i[0].move(start[0] + step_x, start[1] + step_y)
            i[1].move(start[0] + 35 + step_x, start[1] - 5 + step_y)
            x_cnt += 1
            step_x = 120 * x_cnt
            if x_cnt == 4:
                x_cnt = 0
                y_cnt += 1
                step_x = 0
                step_y = 30 * y_cnt

    def dec_combbox(self, items):
        vtypebox = QComboBox(self)
        for i in items:
            vtypebox.addItem(i)
        return vtypebox

    def initialize(self):
        # 初期化
        for i in range(len(self.namebox)):
            self.namebox[i].setText("")
            self.numbox[i].setText("")
            self.timebox[i].setText("")
            self.roombox[i].setText("")
        self.new_cb.setChecked(False)
        self.modified_cb.setChecked(False)
        for i in self.checkbox:
            i.setChecked(False)
        self.name_val.setText("")
        self.kana_val.setText("")
        self.num_val.setText("")
        self.time_val.setCurrentIndex(self.time_sel.index("9:00"))
        self.room_val.setCurrentIndex(self.room_sel.index("青陽1"))
        self.tel_val.setText("")
        self.remarks_val.setText("")

    def initialize_forms(self):
        for i in self.checkbox:
            i.setChecked(False)
        self.name_val.setText("")
        self.kana_val.setText("")
        self.num_val.setText("")
        self.time_val.setCurrentIndex(self.time_sel.index("9:00"))
        self.room_val.setCurrentIndex(self.room_sel.index("青陽1"))
        self.tel_val.setText("")
        self.remarks_val.setText("")
            
    def substract_reservation(self, date):
        self.initialize()
        # クリックされた日付をラベルにセット
        ID = date.toString().split(" ")[3] + "-" + date.toString().split(" ")[1] + "-" + date.toString().split(" ")[2]
        self.selected_date.setText(ID)
        self.query_data = self.reserve_data.query("ID==@ID")
        self.date_y_val.setText(date.toString().split(" ")[3])
        self.date_m_val.setCurrentIndex(self.month.index(date.toString().split(" ")[1]))
        self.date_d_val.setText(date.toString().split(" ")[2])
        if len(self.query_data) != 0:
            for i in range(len(self.query_data)):
                self.namebox[i].setText(str(self.query_data["氏名"].tolist()[i]))
                self.numbox[i].setText(str(int(self.query_data["人数"].tolist()[i])))
                self.timebox[i].setText(str(self.query_data["時間"].tolist()[i]))
                self.roombox[i].setText(str(self.query_data["部屋"].tolist()[i]))
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = main_window()

    main_window.show()
    sys.exit(app.exec_())