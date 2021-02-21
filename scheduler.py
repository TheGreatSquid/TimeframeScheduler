
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import pytz


PST = pytz.timezone('US/Pacific')
tz_keys = ['US/Central', 'US/Eastern', 'Asia/Seoul', 'Asia/Taipei']
other_tzs = [pytz.timezone(key) for key in tz_keys]


class App (object):
    def __init__(self, root):
        self.root = root
        self.root.geometry('900x500')
        self.root.title('Timeframe Converter')
        friendly_names = ['US: Pacific', 'US: Central', 'US: Eastern', 'Korea', 'Taiwan']
        tz_names = ['US/Pacific', 'US/Central', 'US/Eastern', 'Asia/Taipei', 'Asia/Seoul']
        self.tzs = {friendly: pytz.timezone(name) for friendly, name in zip(friendly_names, tz_names)}
        self.local_zone = friendly_names[0]

        ########### top-level frames ###########
        self.frm_input = tk.Frame(self.root, bg='gray', relief=tk.GROOVE)
        self.frm_input.grid(row=0, column=0, sticky='nsew')
        self.frm_output = tk.Frame(self.root, bg='gray', relief=tk.GROOVE)
        self.frm_output.grid(row=0, column=1, sticky='nsew')

        ######################### labels ########################
        w, h = 15, 1
        title_font = ('Arial', 20)

        self.lbl_start = tk.Label(self.frm_input, text='Start', width=w, height=h, font=title_font)
        self.lbl_start.grid(row=1, column=0)
        self.lbl_end = tk.Label(self.frm_input, text='End', width=w, height=h, font=title_font)
        self.lbl_end.grid(row=3, column=0)

        self.tz_titles = []
        self.tz_lbls = []
        for i in range(4):
            title = tk.Label(self.frm_output, text='', width=w, height=h, font=title_font)
            lbl = tk.Label(self.frm_output, text='', width=1, font=('Arial', 20), justify=tk.CENTER)
            self.tz_titles.append(title)
            self.tz_lbls.append(lbl)
            title.grid(row=2 * i, column=0)
            lbl.grid(row=2 * i + 1, column=0, sticky='nsew')

        ################## buttons & text inputs ###################
        ent_font = ('Arial', 40)
        self.ent_start = tk.Entry(self.frm_input, font=ent_font, width=1, justify=tk.CENTER)
        self.ent_start.insert(0, '00:00')
        self.ent_start.grid(row=1, column=0, sticky='nsew')

        self.ent_end = tk.Entry(self.frm_input, font=ent_font, width=1, justify=tk.CENTER)
        self.ent_end.insert(0, '00:00')
        self.ent_end.grid(row=3, column=0, sticky='nsew')

        self.btn_convert = tk.Button(self.frm_input, text="Convert!", font=title_font, command=self.convert)
        self.btn_convert.grid(row=4, column=0, sticky='nsew')

        self.cmb_current_zone = ttk.Combobox(self.frm_input, values=list(self.tzs.keys()), state='readonly',
                                             font=title_font, width=1)
        self.cmb_current_zone.current(0)
        self.cmb_current_zone.bind('<<ComboboxSelected>>', self.select_zone)
        self.cmb_current_zone.grid(row=0, column=0, sticky='ew')

        ################ configure grids after packing ###############

        self.balance_grid(self.frm_input)
        self.balance_grid(self.frm_output)
        self.balance_grid(self.root)

        self.change_local_zone(self.local_zone)

    def convert(self):
        frame_start, frame_end = self.ent_start.get(), self.ent_end.get()
        st_hr, st_min = map(int, frame_start.split(':'))
        end_hr, end_min = map(int, frame_end.split(':'))

        today = datetime.now(tz=self.tzs[self.local_zone])
        start = today.replace(hour=st_hr, minute=st_min, second=0, microsecond=0)
        end = today.replace(hour=end_hr, minute=end_min, second=0, microsecond=0)

        if end < start:
            end += timedelta(days=1)

        # for i, tz in enumerate(other_tzs):
        #     tz_start, tz_end = [t.astimezone(tz) for t in (start, end)]
        #     tz_frame = ' - '.join(t.strftime('%H:%M') for t in (tz_start, tz_end))
        #     tz_frame += f' ({tz_start.day}, {tz_end.day})'
        #     self.tz_lbls[i]['text'] = tz_frame

        for i in range(4):
            title, lbl = self.tz_titles[i], self.tz_lbls[i]
            tz_start, tz_end = [t.astimezone(self.tzs[title['text']]) for t in (start, end)]
            tz_frame = ' - '.join(t.strftime('%H:%M') for t in (tz_start, tz_end))
            tz_frame += f' ({tz_start.day}, {tz_end.day})'
            lbl['text'] = tz_frame

    def select_zone(self, event):
        new_zone = event.widget.get()
        self.change_local_zone(new_zone)

    def change_local_zone(self, zone):
        other_zones = [name for name in self.tzs.keys() if name != zone]
        self.local_zone = zone

        for widget, name in zip(self.tz_titles, other_zones):
            widget['text'] = name
        for widget in self.tz_lbls:
            widget['text'] = ''

    def balance_grid(self, widget):
        c, r = widget.grid_size()

        for i in range(r):
            widget.rowconfigure(i, weight=1)
        for j in range(c):
            widget.columnconfigure(j, weight=1)


def main():
    root = tk.Tk()
    app = App(root)
    app.root.mainloop()


if __name__ == '__main__': main()
