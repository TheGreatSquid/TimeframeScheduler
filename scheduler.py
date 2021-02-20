
import tkinter as tk
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

        ########### top-level frames ###########
        self.frm_input = tk.Frame(self.root, bg='gray', relief=tk.GROOVE)
        self.frm_input.grid(row=0, column=0, sticky='nsew')
        self.frm_output = tk.Frame(self.root, bg='gray', relief=tk.GROOVE)
        self.frm_output.grid(row=0, column=1, sticky='nsew')

        ######################### labels ########################
        w, h = 15, 1
        title_font = ('Arial', 20)

        self.lbl_start = tk.Label(self.frm_input, text='Start', width=w, height=h, font=title_font)
        self.lbl_start.grid(row=0, column=0)
        self.lbl_end = tk.Label(self.frm_input, text='End', width=w, height=h, font=title_font)
        self.lbl_end.grid(row=2, column=0)

        self.tz_titles = []
        self.tz_lbls = []
        for i, title in enumerate(['Central', 'Eastern', 'Korea', 'Taiwan']):
            title = tk.Label(self.frm_output, text=title, width=w, height=h, font=title_font)
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

        ################ configure grids after packing ###############

        self.balance_grid(self.frm_input)
        self.balance_grid(self.frm_output)
        self.balance_grid(self.root)

    def convert(self):
        frame_start, frame_end = self.ent_start.get(), self.ent_end.get()
        st_hr, st_min = map(int, frame_start.split(':'))
        end_hr, end_min = map(int, frame_end.split(':'))

        today = datetime.now(tz=PST)
        start = today.replace(hour=st_hr, minute=st_min, second=0, microsecond=0)
        end = today.replace(hour=end_hr, minute=end_min, second=0, microsecond=0)

        if end < start:
            end += timedelta(days=1)

        for i, tz in enumerate(other_tzs):
            tz_start, tz_end = [t.astimezone(tz) for t in (start, end)]
            tz_frame = ' - '.join(t.strftime('%H:%M') for t in (tz_start, tz_end))
            tz_frame += f' ({tz_start.day}, {tz_end.day})'
            self.tz_lbls[i]['text'] = tz_frame

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
