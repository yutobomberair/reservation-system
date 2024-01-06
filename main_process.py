import pandas as pd
import numpy as np

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate

from main_window import main_window

class main_process(main_window):
    def __init__(self, parent=None):
        super(main_window, self).__init__(parent)
        self.reserve_data = pd.read_csv("./reserve_data/reserve_data.csv") # 予約データを抽出
        self.reserve_data.to_csv("./reserve_data/reserve_data_backup.csv", index=None)
        self.month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        self.time_sel = [str(i+9)+":"+f"{30*j:02}" for i in range(12) for j in range(2)]
        self.room_sel = ["青陽1", "青陽2", "瑠璃", "敷妙", "蓬莱", "残月", "無量庵", "ホール", "直心軒"]
        self.member = ["田中", "菅原", "田辺", "福永", "クリス", "坂井", "川田", "ミルコ"]
        self.member_status = ["確定", "保留", "不可"]

    def processing(self):
        self.set_window(self)
        self.botton_connection()

    def botton_connection(self):
        self.new.clicked.connect(self.new_action) # 新規作成ボタンを押したときのアクション
        self.modified.clicked.connect(self.modified_action) # 編集ボタンを押したときのアクション
        self.delete.clicked.connect(self.delete_action) # 削除ボタンを押したときのアクション
        self.check.clicked.connect(self.check_action) # 詳細確認ボタンを押したときのアクション

    def check_action(self):
        checkbox_status = [int(i.checkState() / 2) for i in self.checkbox]
        if len(self.query_data) == 0:
            self.popup_assertion("予約がありません", "warn")
        elif sum(checkbox_status) == 0:
            self.popup_assertion("予約を選択してください", "warn")
        elif sum(checkbox_status) >= 2:
            self.popup_assertion("2つ以上の予約が選択されています", "warn")
        elif checkbox_status.index(1) >= len(self.query_data):
            self.popup_assertion("選択された位置が誤っています", "warn")
        else:
            self.ind = checkbox_status.index(1)
            self.org_ind = self.query_data.index.tolist()[self.ind]
            look_data = self.query_data.iloc[self.ind]
            Year = look_data["ID"].split("-")[0]
            Month = look_data["ID"].split("-")[1]
            Day = look_data["ID"].split("-")[2]
            Name = look_data["氏名"]
            Kana = look_data["ふりがな"]
            Num = int(look_data["人数"])
            Time = look_data["時間"]
            Room = look_data["部屋"]
            Tel = look_data["連絡先"]
            Remark = look_data["備考"]
            self.date_y_val.setText(Year)
            self.date_m_val.setCurrentIndex(self.month.index(Month))
            self.date_d_val.setText(Day)
            self.name_val.setText(str(Name))
            self.kana_val.setText(str(Kana))
            self.num_val.setText(str(Num))
            self.time_val.setCurrentIndex(self.time_sel.index(Time))
            self.room_val.setCurrentIndex(self.room_sel.index(Room))
            self.tel_val.setText(str(Tel))
            self.remarks_val.setText(str(Remark))
            self.popup_assertion("画面右側に詳細を表示しました", "info")
            self.mod_flag = 1

    def modified_action(self):
        if self.modified_cb.checkState() == 0:
            self.popup_assertion("チェックボックスに印を入れてください", "warn")
        else:
            Year = self.date_y_val.text()
            Month = self.date_m_val.currentText()
            Day = self.date_d_val.text()
            ID = Year + "-" + Month + "-" + Day
            Name = self.name_val.text()
            Kana = self.kana_val.text()
            Num = str(int(self.num_val.text()))
            Time = self.time_val.currentText()
            Room = self.room_val.currentText()
            Tel = self.tel_val.text()
            Remark = self.remarks_val.toPlainText()
            self.reserve_data.iloc[self.org_ind] = [ID, Name, Kana, Num, Time, Room, Tel, Remark]
            self.reserve_data.to_csv("./reserve_data/reserve_data.csv", index=None)
            self.modified_forms()
            if ID == self.selected_date.text():
                self.query_data = self.reserve_data.query("ID==@ID")
                self.namebox[self.ind].setText(Name)
                self.numbox[self.ind].setText(Num)
                self.timebox[self.ind].setText(Time)
                self.roombox[self.ind].setText(Room)
            self.popup_assertion("編集内容を保存しました", "info")
            self.modified_cb.setChecked(False)
            self.mod_flag = 0
    
    def modified_forms(self):
        self.namebox[self.ind].setText("")
        self.numbox[self.ind].setText("")
        self.timebox[self.ind].setText("")
        self.roombox[self.ind].setText("")
        for i in self.checkbox:
            i.setChecked(False)
        self.modified_cb.setChecked(False)

    def new_action(self):
        if self.new_cb.checkState() == 0:
            self.popup_assertion("チェックボックスに印を入れてください", "warn")
        elif self.mod_flag == 1:
            self.popup_assertion("編集ではありませんか？", "warn")
            self.mod_flag = 0
        else:
            Year = self.date_y_val.text()
            Month = self.date_m_val.currentText()
            Day = self.date_d_val.text()
            ID = Year + "-" + Month + "-" + Day
            Name = self.name_val.text()
            Kana = self.kana_val.text()
            Num = str(int(self.num_val.text()))
            Time = self.time_val.currentText()
            Room = self.room_val.currentText()
            Tel = self.tel_val.text()
            Remark = self.remarks_val.toPlainText()
            col = self.reserve_data.columns
            cash = self.reserve_data.to_numpy()
            self.reserve_data = pd.DataFrame(np.vstack((cash, [ID, Name, Kana, Num, Time, Room, Tel, Remark])), columns=col)
            self.reserve_data.to_csv("./reserve_data/reserve_data.csv", index=None)
            self.namebox[len(self.query_data)].setText(Name)
            self.numbox[len(self.query_data)].setText(Num)
            self.timebox[len(self.query_data)].setText(Time)
            self.roombox[len(self.query_data)].setText(Room)
            self.query_data = self.reserve_data.query("ID==@ID")
            self.new_cb.setChecked(False)
            self.popup_assertion("新規登録内容を保存しました", "info")

    def delete_action(self):
        if self.delete_cb.checkState() == 0:
            self.popup_assertion("チェックボックスに印を入れてください", "warn")
        elif self.mod_flag == 0:
            self.popup_assertion("削除する予約を選択してください", "warn")
        else:
            Year = self.date_y_val.text()
            Month = self.date_m_val.currentText()
            Day = self.date_d_val.text()
            ID = Year + "-" + Month + "-" + Day
            self.reserve_data = self.reserve_data.drop(self.reserve_data.index[[self.org_ind]])
            self.reserve_data.to_csv("./reserve_data/reserve_data.csv", index=None)
            self.query_data = self.reserve_data.query("ID==@ID")
            self.modified_forms()
            self.initialize_forms()
            self.mod_flag = 0
            self.delete_cb.setChecked(False)
            self.popup_assertion("削除しました", "info")

    def popup_assertion(self, text, opt): # opt: "warn", "info"
        msg = QMessageBox()
        if opt == "warn":
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("assertion")
            msg.setText("warning!!: " + text)
            x = msg.exec_()
        elif opt == "info":
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("infomation")
            msg.setText("infomation: " + text)
            x = msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_process = main_process()
    main_process.processing()

    main_process.show()
    sys.exit(app.exec_())