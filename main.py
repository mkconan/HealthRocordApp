import os
import datetime
import csv

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd

record_file_path = "./health.csv"
health_data_columns = ["date", "feeling_level", "sleeping_time", "body_weight"]
if not os.path.isfile(record_file_path):
    with open(record_file_path, mode="w") as f:
        writer = csv.writer(f)
        writer.writerow(health_data_columns)
        print("記録ファイルが作成されました")


class Application(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):

        ttk.Label(self, text="今日の気分は？").grid(column=0, row=0, pady=5)

        self.radio_value = tk.IntVar(value=0)
        for level in range(-5, 5 + 1):
            ttk.Radiobutton(self, text=f"{level}", variable=self.radio_value, value=level).grid(
                column=5 + level + 1,
                row=0,
                padx=3,
            )

        ttk.Label(self, text="今日の睡眠時間は？").grid(column=0, row=1, pady=5)
        hours_list = [i for i in range(0, 12 + 1)]
        minutes_list = [i for i in range(0, 60, 15)]

        self.hour_box = ttk.Combobox(
            self, height=len(hours_list), width=2, justify="center", values=hours_list, state="readonly"
        )
        self.hour_box.grid(column=1, row=1)
        ttk.Label(self, text="時間").grid(column=2, row=1)

        self.minute_box = ttk.Combobox(
            self, height=len(minutes_list), width=2, justify="center", values=minutes_list, state="readonly"
        )
        self.minute_box.grid(column=3, row=1)
        ttk.Label(self, text="分").grid(column=4, row=1)

        ttk.Label(self, text="今日の体重は？").grid(column=0, row=2, padx=5)
        self.body_weight_box = ttk.Entry(self, width=4)
        self.body_weight_box.grid(column=1, row=2)
        ttk.Label(self, text="kg").grid(column=2, row=2)

        ttk.Button(self, text="保存", width=3, command=self.save_data).grid(column=0, row=3, pady=5)

    def save_data(self):
        feeling_level = self.radio_value.get()

        try:
            hour = int(self.hour_box.get())
            minute = int(self.minute_box.get())
            sleeping_time = f"{hour:02d}h{minute:02d}m"
        except ValueError:
            messagebox.showinfo("入力エラー", "睡眠時間を入力してください")
            return

        try:
            body_weight = float(self.body_weight_box.get())
        except ValueError:
            messagebox.showinfo("入力エラー", "体重を半角数字で入力してください")
            return

        df = pd.read_csv(record_file_path)
        recored_today_list = is_already_record(df)

        if True in recored_today_list.values:  # すでに保存されていた場合
            # 本日分のデータを取得し、削除する
            already_record_index = [i for i, x in enumerate(recored_today_list) if x == True]
            df.drop(df.index[already_record_index], inplace=True)

        today_df = pd.DataFrame([[get_today(), feeling_level, sleeping_time, body_weight]], columns=health_data_columns)
        df = pd.concat([df, today_df])

        df.to_csv(record_file_path, index=False)
        ret = messagebox.askyesno("保存完了", "保存できました！\n画面を閉じますか？")
        if ret == True:
            self.quit()


def get_today():
    dt_now = datetime.datetime.now()
    return f"{dt_now.year}-{dt_now.month:02d}/{dt_now.day:02d}"


def is_already_record(df):
    return df["date"].isin([get_today()])


def main():
    root = tk.Tk()

    dt_now = datetime.datetime.now()
    root.title(f"健康記録アプリ({get_today()})")

    # ディスプレイの中央にウインドウを配置する
    window_width, window_height = 800, 600
    screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    center_x, center_y = (screen_width - window_width) // 2, (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    app = Application(root)
    app.mainloop()


if __name__ == "__main__":
    main()
