from tkinter import *
from bs4 import BeautifulSoup
import requests
import getpass
import sqlite3 as s3
import datetime
import time as t
import re


class StartScreen:
    def __init__(self):
        root.title("Task Manager")
        root.resizable(False, False)
        main_frame.config(bg="#333")
        self.tool = Tools(main_frame)
        self.now = datetime.datetime.now()

        self.main_frame = Frame(main_frame, bg="#333")
        self.main_frame.grid(row=0, padx=40, pady=(20, 30))

        username = getpass.getuser()
        welcome_label = Label(self.main_frame, text="Welcome, %s" % username, font=(
            'Arial', 17), bg="#333", fg="#efefef")

        welcome_label.grid(row=0, pady=(0, 10))

        month_dict = {1: 'January',
                      2: 'February',
                      3: 'March',
                      4: 'April',
                      5: 'May',
                      6: 'June',
                      7: 'July',
                      8: 'August',
                      9: 'September',
                      10: 'October',
                      11: 'November',
                      12: 'December'}

        date_label = Label(self.main_frame, text="%s %s %s" % (
            self.now.day, month_dict[self.now.month], self.now.year), font=('Arial', 15), bg="#333", fg="#efefef")
        date_label.grid(row=1, pady=(0, 20))

        try:
            res = requests.get(r"https://www.brainyquote.com/quote_of_the_day")
            soup = BeautifulSoup(res.text, 'html.parser')
            element = element = str(soup.find_all('a', {'class': 'oncl_q'}))
            quote = re.findall(r'alt=\"(.+?)\"', element)[0]
        except Exception as e:
            quote = "No Internet Connection"

        totd_label = Label(self.main_frame, text="Quote of the Day", font=(
            'Arial', 17), bg="#333", fg="#efefef")
        quote_label = Label(self.main_frame, text="%s" %
                            quote, font=('Arial', 15), bg="#333", fg="#efefef")

        totd_label.grid(row=2)
        quote_label.grid(row=3, pady=(0, 20))

        root.update_idletasks()
        self.tool.center(root)


class ToDoList:
    def __init__(self):
        root.title('To-Do List')
        root.resizable(False, False)
        self.now = datetime.datetime.now()
        self.tool = Tools(root)
        self.db = Database(r"./taskmanager.db")

        main_frame.config(bg="#333")
        main_frame.grid(row=0)
        # self.master.resizable(False, False)

        # Main Frame =======================================
        self.main_frame = Frame(main_frame, bg="#333")
        self.main_frame.grid(row=0, column=0, padx=30, pady=(10, 10))

        # Left Frame
        left_frame = Frame(self.main_frame, bg="#333")
        left_frame.grid(row=0, padx=(0, 20), sticky=N)

        year_label = Label(left_frame, text="%s Resolutions" % str(
            self.now.year), font=('Helvetica', 17, 'bold'), bg="#333", fg="#efefef")
        self.yearlies_listbox = Listbox(left_frame, width=30, height=24, font=(
            'Arial', 15), justify=CENTER, exportselection=False)

        self.yearlies_listbox.bind('<<ListboxSelect>>', self.select_yearlies)

        year_label.grid(row=0, pady=(0, 10))
        self.yearlies_listbox.grid(row=1, pady=(0, 20))

        # Center Frame =======================================
        center_frame = Frame(self.main_frame, bg="#333")
        center_frame.grid(row=0, column=1, padx=(0, 20), sticky=N)

        dailies_label = Label(center_frame, text="Dailies", font=(
            'Helvetica', 17, 'bold'), bg="#333", fg="#efefef")
        self.dailies_listbox = Listbox(center_frame, width=38, height=22, font=(
            'Arial', 15), justify=CENTER, exportselection=False)

        self.dailies_listbox.bind('<<ListboxSelect>>', self.select_dailies)
        self.dailies_listbox.bind('<Double-Button-1>', self.remove_task)

        dailies_label.grid(row=0, pady=(0, 10))
        self.dailies_listbox.grid(row=1, pady=(0, 20))

        task_button_frame = Frame(center_frame, bg="#333")
        width = 9
        font_size = 12
        add_button = Button(task_button_frame, text="Add",
                            width=width, font=('Helvetica', font_size))
        edit_button = Button(task_button_frame, text="Edit",
                             width=width, font=('Helvetica', font_size))
        remove_button = Button(
            task_button_frame, text="Remove", width=width, font=('Helvetica', font_size))
        clear_button = Button(task_button_frame, text='Clear All',
                              width=width, font=('Helvetica', font_size))

        add_button.bind('<Button-1>', self.add_task)
        edit_button.bind('<Button-1>', self.rename_task)
        remove_button.bind('<Button-1>', self.remove_task)
        clear_button.bind('<Button-1>', self.clear_task)

        task_button_frame.grid(row=2)
        padding = 23
        add_button.grid(row=0, column=0, padx=(0, padding))
        edit_button.grid(row=0, column=1, padx=(0, padding))
        remove_button.grid(row=0, column=2, padx=(0, padding))
        clear_button.grid(row=0, column=3)

        # Right Frame =====================================
        right_frame = Frame(self.main_frame, bg="#333")
        right_frame.grid(row=0, column=2, sticky=N)

        # Goal
        goal_frame = Frame(right_frame, bg="#333")
        goal_frame.grid(row=0, pady=(0, 20))

        goals_listbox_width = 32
        goals_label = Label(goal_frame, text="Goals", font=(
            'Helvetica', 17, 'bold'), bg="#333", fg="#efefef")
        self.goals_listbox = Listbox(goal_frame, width=goals_listbox_width, height=18, font=(
            'Arial', 15), justify=CENTER, exportselection=False)

        self.goals_listbox.bind('<<ListboxSelect>>', self.select_goals)

        goals_label.grid(row=0, pady=(0, 10))
        self.goals_listbox.grid(row=1)

        deadline_label = Label(goal_frame, text="Deadline", font=(
            'Helvetica', 17, 'bold'), bg="#333", fg="#efefef")
        self.deadline_listbox = Listbox(
            goal_frame, width=45 - goals_listbox_width, height=18, font=('Arial', 15), justify=CENTER)

        deadline_label.grid(row=0, column=1, pady=(0, 10))
        self.deadline_listbox.grid(row=1, column=1)

        # Task Info
        task_info_frame = Frame(right_frame, bg="#333")

        # create text widget
        self.task_info = Text(task_info_frame, width=43,
                              height=7, font=('Helvetica', 12))
        task_info_frame.grid(row=2, columnspan=2)
        self.task_info.grid(row=0, sticky=N+W)

        # create a Scrollbar and associate it with txt
        scrollbar = Scrollbar(task_info_frame, command=self.task_info.yview)
        scrollbar.grid(row=0, column=1, padx=(0, 20), sticky='nsew')
        self.task_info['yscrollcommand'] = scrollbar.set

        info_button_frame = Frame(task_info_frame, bg="#333")
        save_info_button = Button(
            info_button_frame, text="Save", width=width, font=('Helvetica', font_size))
        clear_info_button = Button(
            info_button_frame, text="Clear", width=width, font=('Helvetica', font_size))
        self.save_indicator_label = Label(info_button_frame, text="", font=(
            'Helvetica', 12, 'bold'), bg="#333", fg="#efefef")

        save_info_button.bind('<Button-1>', self.save_task_info)
        clear_info_button.bind('<Button-1>', self.clear_task_info)

        info_button_frame.grid(row=0, column=2, sticky=N)
        save_info_button.grid(row=0, pady=(0, 20))
        clear_info_button.grid(row=2, pady=(0, 12))
        self.save_indicator_label.grid(row=3)

        root.update_idletasks()
        self.tool.center(root)

        self.initialize()

    def initialize(self):
        self.yearlies_listbox.delete(0, END)
        self.dailies_listbox.delete(0, END)
        self.goals_listbox.delete(0, END)
        self.deadline_listbox.delete(0, END)

        self.yearlies_listbox.insert(END, '')
        self.dailies_listbox.insert(END, '')
        self.goals_listbox.insert(END, '')
        self.deadline_listbox.insert(END, '')

        # Yearlies
        self.db.raw_execute(
            "SELECT taskName FROM yearList ORDER BY taskId ASC")
        all_tasks = self.db.fetchall()
        task_list = []
        for task in all_tasks:
            task_list.append(str(task[0]))

        for task in task_list:
            self.yearlies_listbox.insert(END, self.tool.from_database(task))
            self.yearlies_listbox.insert(END, '')

        # Dailies
        self.db.raw_execute(
            "SELECT taskName FROM dailiesList ORDER BY taskId ASC")
        all_tasks = self.db.fetchall()
        task_list = []
        for task in all_tasks:
            task_list.append(str(task[0]))

        for task in task_list:
            self.dailies_listbox.insert(END, self.tool.from_database(task))
            self.dailies_listbox.insert(END, '')

        # Goals
        self.db.raw_execute(
            "SELECT taskName, deadline FROM goalsList ORDER BY taskId ASC")
        all_tasks = self.db.fetchall()
        task_list = []
        for task in all_tasks:
            if len(task) > 0:
                task_list.append(task)

        for task in task_list:
            self.goals_listbox.insert(END, self.tool.from_database(task[0]))
            self.goals_listbox.insert(END, '')

            # Deadlines
            self.deadline_listbox.insert(END, self.tool.from_database(task[1]))
            self.deadline_listbox.insert(END, '')

    def select_yearlies(self, event=""):
        self.goals_listbox.selection_clear(0, END)
        self.dailies_listbox.selection_clear(0, END)
        self.task_info.delete(1.0, END)
        self.list_id = 0
        task_info = ''

        try:
            self.task_id = self.yearlies_listbox.curselection()[0]
            task_name = self.yearlies_listbox.get(self.task_id)
            self.db.select('taskInfo', 'taskInfo', "taskName = '%s' AND listId = 0" % (
                self.tool.to_database(task_name)))

            task_info = self.db.fetchone()[0]
            self.task_info.insert(END, task_info)
        except Exception as e:
            pass

        self.save_indicator_label.config(text="")

    def select_dailies(self, event=""):
        self.goals_listbox.selection_clear(0, END)
        self.yearlies_listbox.selection_clear(0, END)
        self.task_info.delete(1.0, END)
        self.list_id = 1
        task_info = ''

        try:
            self.task_id = self.dailies_listbox.curselection()[0]
            task_name = self.dailies_listbox.get(self.task_id)
            self.db.select('taskInfo', 'taskInfo', "taskName = '%s' AND listId = 1" % (
                self.tool.to_database(task_name)))

            task_info = self.db.fetchone()[0]
            self.task_info.insert(END, task_info)
        except Exception as e:
            pass

        self.save_indicator_label.config(text="")

    def select_goals(self, evenet=""):
        self.dailies_listbox.selection_clear(0, END)
        self.yearlies_listbox.selection_clear(0, END)
        self.task_info.delete(1.0, END)
        self.list_id = 2
        task_info = ''

        try:
            self.task_id = self.goals_listbox.curselection()[0]
            task_name = self.goals_listbox.get(self.task_id)
            self.db.select('taskInfo', 'taskInfo', "taskName = '%s'AND listId = 2" % (
                self.tool.to_database(task_name)))
            task_info = self.db.fetchone()[0]
            self.task_info.insert(END, task_info)
        except Exception as e:
            pass

        self.save_indicator_label.config(text="")

    def add_task(self, event=""):
        self.add_task_popup = Toplevel(self.main_frame)
        self.add_task_popup.title("Add Task")
        self.tool.center(self.add_task_popup)
        self.add_task_popup.config(bg="#333")

        self.center_frame = Frame(self.add_task_popup, bg="#333")
        add_yearlies_button = Button(
            self.center_frame, text="Yearlies", width=10)
        add_dailies_button = Button(
            self.center_frame, text="Dailies", width=10)
        add_goals_button = Button(self.center_frame, text="Goals", width=10)

        add_yearlies_button.bind('<Button-1>', self.add_yearlies)
        add_dailies_button.bind('<Button-1>', self.add_dailies)
        add_goals_button.bind('<Button-1>', self.add_goals)

        self.center_frame.grid(row=0, padx=20, pady=20)
        add_yearlies_button.grid(row=0, column=0, padx=(0, 30))
        add_dailies_button.grid(row=0, column=1, padx=(0, 30))
        add_goals_button.grid(row=0, column=2)

    def add_yearlies(self, event=""):
        self.center_frame.grid_forget()
        self.add_task_popup.title("Add Yearly Task")

        add_yearlies_label = Label(self.add_task_popup, text="Enter Yearly Name",
                                   bg="#333", foreground="#efefef", font=('Arial', 13))
        self.add_yearlies_entry = Entry(
            self.add_task_popup, width=40, justify=CENTER)
        add_yearlies_button = Button(
            self.add_task_popup, text="Add Yearly", width=18)

        self.add_yearlies_entry.bind('<Return>', self.add_yearlies_to_app)
        add_yearlies_button.bind('<Button-1>', self.add_yearlies_to_app)

        add_yearlies_label.pack(pady=10)
        self.add_yearlies_entry.pack(padx=20)
        add_yearlies_button.pack(padx=50, pady=(12, 10))

        self.add_task_popup.resizable(False, False)

    def add_yearlies_to_app(self, event=""):
        task_name = self.add_yearlies_entry.get()
        self.add_yearlies_entry.delete(0, END)
        self.add_task_popup.destroy()

        self.db.select('yearList', 'MAX(taskId)')
        max_id = self.db.fetchone()[0]

        if len(task_name) > 0:
            if max_id == None:
                self.db.insert('yearList', 'taskId, taskName',
                               " 1, '%s'" % (self.tool.to_database(task_name)))
            else:
                self.db.insert('yearList', 'taskId, taskName', "%d, '%s'" % (
                    max_id+1, self.tool.to_database(task_name)))

        self.initialize()

    def add_dailies(self, event=""):
        self.center_frame.grid_forget()
        self.add_task_popup.title("Add Daily Task")

        add_dailies_label = Label(self.add_task_popup, text="Enter Daily Name",
                                  bg="#333", foreground="#efefef", font=('Arial', 13))
        self.add_dailies_entry = Entry(
            self.add_task_popup, width=40, justify=CENTER)
        add_dailies_button = Button(
            self.add_task_popup, text="Add Daily", width=18)

        self.add_dailies_entry.bind('<Return>', self.add_dailies_to_app)
        add_dailies_button.bind('<Button-1>', self.add_dailies_to_app)

        add_dailies_label.pack(pady=10)
        self.add_dailies_entry.pack(padx=20)
        add_dailies_button.pack(padx=50, pady=(12, 10))

        self.add_task_popup.resizable(False, False)

    def add_dailies_to_app(self, event=""):
        task_name = self.add_dailies_entry.get()
        self.add_dailies_entry.delete(0, END)
        self.add_task_popup.destroy()

        self.db.select('dailiesList', 'MAX(taskId)')
        max_id = self.db.fetchone()[0]

        if len(task_name) > 0:
            if max_id == None:
                self.db.insert('dailiesList', 'taskId, taskName',
                               " 1, '%s'" % (self.tool.to_database(task_name)))
            else:
                self.db.insert('dailiesList', 'taskId, taskName', "%d, '%s'" % (
                    max_id+1, self.tool.to_database(task_name)))

        self.initialize()

    def add_goals(self, event=""):
        self.center_frame.grid_forget()
        self.add_task_popup.title("Add Goals")

        width = 40
        add_goals_label = Label(self.add_task_popup, text="Enter Goal Name",
                                bg="#333", foreground="#efefef", font=('Arial', 13))
        self.add_goals_entry = Entry(
            self.add_task_popup, width=width, justify=CENTER)
        add_deadline_label = Label(self.add_task_popup, text="Enter Deadline Date",
                                   bg="#333", foreground="#efefef", font=('Arial', 13))
        self.add_deadline_entry = Entry(
            self.add_task_popup, width=width, justify=CENTER)

        add_goals_button = Button(
            self.add_task_popup, text="Add Goal", width=18)

        self.add_goals_entry.bind('<Return>', self.add_goals_to_app)
        add_goals_button.bind('<Button-1>', self.add_goals_to_app)

        add_goals_label.pack(pady=10)
        self.add_goals_entry.pack(padx=20)
        add_deadline_label.pack(pady=10)
        self.add_deadline_entry.pack()
        add_goals_button.pack(padx=50, pady=(15, 10))

        self.add_task_popup.resizable(False, False)

    def add_goals_to_app(self, event=""):
        task_name = self.add_goals_entry.get()
        deadline = self.add_deadline_entry.get()
        # self.add_task_entry.delete(0, END)
        self.add_task_popup.destroy()

        self.db.select('goalsList', 'MAX(taskId)')
        max_id = self.db.fetchone()[0]

        if len(task_name) > 0:
            if max_id == None:
                self.db.insert('goalsList', 'taskId, taskName, deadline', " 1, '%s', '%s'" % (
                    self.tool.to_database(task_name), self.tool.to_database(deadline)))
            else:
                self.db.insert('goalsList', 'taskId, taskName, deadline', "%d, '%s', '%s'" % (
                    max_id+1, self.tool.to_database(task_name), self.tool.to_database(deadline)))

        self.initialize()

    def rename_task(self, event):
        if self.list_id == 0:
            self.rename_task_popup = Toplevel(self.main_frame)
            self.rename_task_popup.title("Rename Yearly Task")
            self.tool.center(self.rename_task_popup)
            self.rename_task_popup.config(bg="#333")

            picked_task_index = self.task_id
            task_name = self.yearlies_listbox.get(picked_task_index)

            width = len(task_name) + (len(task_name) // 3)
            if width < 30:
                width = 30

            rename_yearly_label = Label(self.rename_task_popup, text="Rename %s to" %
                                        task_name, bg="#333", foreground="#efefef", font=('Arial', 13))
            self.rename_yearly_entry = Entry(
                self.rename_task_popup, width=width, justify=CENTER)
            self.rename_yearly_entry.insert(0, task_name)
            rename_yearly_button = Button(
                self.rename_task_popup, text="Rename Yearly", width=20)

            self.rename_yearly_entry.bind('<Return>', self.rename_task_to_app)
            rename_yearly_button.bind('<Button-1>', self.rename_task_to_app)

            rename_yearly_label.pack(padx=20, pady=10)
            self.rename_yearly_entry.pack()
            rename_yearly_button.pack(padx=50, pady=(12, 10))

            self.rename_task_popup.resizable(False, False)

        elif self.list_id == 1:
            self.rename_task_popup = Toplevel(self.main_frame)
            self.rename_task_popup.title("Rename Daily Task")
            self.tool.center(self.rename_task_popup)
            self.rename_task_popup.config(bg="#333")

            picked_task_index = self.task_id
            task_name = self.dailies_listbox.get(picked_task_index)

            width = len(task_name) + (len(task_name) // 3)
            if width < 30:
                width = 30

            rename_daily_label = Label(self.rename_task_popup, text="Rename %s to" %
                                       task_name, bg="#333", foreground="#efefef", font=('Arial', 13))
            self.rename_daily_entry = Entry(
                self.rename_task_popup, width=width, justify=CENTER)
            self.rename_daily_entry.insert(0, task_name)

            rename_daily_button = Button(
                self.rename_task_popup, text="Rename Daily", width=20)

            self.rename_daily_entry.bind('<Return>', self.rename_task_to_app)
            rename_daily_button.bind('<Button-1>', self.rename_task_to_app)

            rename_daily_label.pack(padx=20, pady=10)
            self.rename_daily_entry.pack()
            rename_daily_button.pack(padx=50, pady=(12, 10))

            self.rename_task_popup.resizable(False, False)

        elif self.list_id == 2:
            self.rename_task_popup = Toplevel(self.main_frame)
            self.rename_task_popup.title("Rename Daily Task")
            self.tool.center(self.rename_task_popup)
            self.rename_task_popup.config(bg="#333")

            task_name = self.goals_listbox.get(self.task_id)
            deadline = self.deadline_listbox.get(self.task_id)

            width = len(task_name) + (len(task_name) // 3)
            if width < 30:
                width = 30

            rename_goals_label = Label(
                self.rename_task_popup, text="Enter Goal Name", bg="#333", foreground="#efefef", font=('Arial', 13))
            self.rename_goals_entry = Entry(
                self.rename_task_popup, width=width, justify=CENTER)
            self.rename_goals_entry.insert(END, task_name)
            rename_deadline_label = Label(
                self.rename_task_popup, text="Enter Deadline Date", bg="#333", foreground="#efefef", font=('Arial', 13))
            self.rename_deadline_entry = Entry(
                self.rename_task_popup, width=width, justify=CENTER)
            self.rename_deadline_entry.insert(END, deadline)

            rename_goals_button = Button(
                self.rename_task_popup, text="Rename Goal", width=18)

            self.rename_goals_entry.bind('<Return>', self.rename_task_to_app)
            rename_goals_button.bind('<Button-1>', self.rename_task_to_app)

            rename_goals_label.pack(pady=10)
            self.rename_goals_entry.pack(padx=20)
            rename_deadline_label.pack(pady=10)
            self.rename_deadline_entry.pack()
            rename_goals_button.pack(padx=50, pady=(15, 10))

            self.rename_task_popup.resizable(False, False)

    def rename_task_to_app(self, event):
        picked_task_index = self.task_id

        if self.list_id == 0:
            task_name = self.yearlies_listbox.get(picked_task_index)
            renamed_task_name = self.rename_yearly_entry.get()

            if len(renamed_task_name) > 0:
                self.db.update('yearList', "taskName = '%s'" % self.tool.to_database(
                    renamed_task_name), "taskName = '%s'" % self.tool.to_database(task_name))
                self.db.update('taskInfo', "taskName = '%s'" % self.tool.to_database(
                    renamed_task_name), "taskName = '%s' AND listId = 0" % self.tool.to_database(task_name))

        elif self.list_id == 1:
            task_name = self.dailies_listbox.get(picked_task_index)
            renamed_task_name = self.rename_daily_entry.get()

            if len(renamed_task_name) > 0:
                self.db.update('dailiesList', "taskName = '%s'" % self.tool.to_database(
                    renamed_task_name), "taskName = '%s'" % self.tool.to_database(task_name))
                self.db.update('taskInfo', "taskName = '%s'" % self.tool.to_database(
                    renamed_task_name), "taskName = '%s' AND listId = 1" % self.tool.to_database(task_name))

        elif self.list_id == 2:
            task_name = self.goals_listbox.get(picked_task_index)
            renamed_task_name = self.rename_goals_entry.get()

            deadline = self.rename_deadline_entry.get()

            if len(renamed_task_name) > 0:
                self.db.update('goalsList', "taskName = '%s', deadline = '%s'" % (self.tool.to_database(
                    renamed_task_name), self.tool.to_database(deadline)), "taskName = '%s'" % self.tool.to_database(task_name))
                self.db.update('taskInfo', "taskName = '%s'" % self.tool.to_database(
                    renamed_task_name), "taskName = '%s' AND listId = 2" % self.tool.to_database(task_name))

        self.initialize()

        self.rename_task_popup.destroy()

    def remove_task(self, event):
        picked_task_index = self.task_id

        if self.list_id == 0:
            task_name = self.yearlies_listbox.get(picked_task_index)
        elif self.list_id == 1:
            task_name = self.dailies_listbox.get(picked_task_index)
        elif self.list_id == 2:
            task_name = self.goals_listbox.get(picked_task_index)

        if len(task_name) >= 1:
            self.remove_task_popup = Toplevel(self.main_frame)
            self.remove_task_popup.title("Remove Task")

            self.remove_task_popup.config(bg="#333")

            remove_task_label = Label(self.remove_task_popup, text="Are you sure you would like to remove %s?" %
                                      task_name, bg="#333", foreground="#efefef", font=('Arial', 13))

            remove_task_button_frame = Frame(self.remove_task_popup, bg="#333")
            remove_task_button_yes = Button(
                remove_task_button_frame, text="Yes", width=10)
            remove_task_button_no = Button(
                remove_task_button_frame, text="No", width=10)

            remove_task_button_yes.bind('<Button-1>', self.remove_task_yes)
            remove_task_button_no.bind('<Button-1>', self.remove_task_no)

            remove_task_label.grid(
                row=0, column=0, padx=(10, 10), pady=(10, 10))
            remove_task_button_frame.grid(row=1, column=0, pady=(0, 15))
            remove_task_button_yes.grid(row=0, column=0, padx=(0, 20))
            remove_task_button_no.grid(row=0, column=1)

            self.tool.center(self.remove_task_popup)

            self.remove_task_popup.resizable(False, False)

    def remove_task_yes(self, event):
        picked_task_index = self.task_id

        if self.list_id == 0:
            task_name = self.yearlies_listbox.get(picked_task_index)

            self.yearlies_listbox.delete(picked_task_index)
            self.yearlies_listbox.delete(picked_task_index)

            self.db.delete('yearList', "taskName = '%s'" %
                           self.tool.to_database(task_name))
            self.db.delete('taskInfo', "taskName = '%s' AND listId = 0" % (
                self.tool.to_database(task_name)))
            self.task_info.delete(1.0, END)

        elif self.list_id == 1:
            task_name = self.dailies_listbox.get(picked_task_index)

            self.dailies_listbox.delete(picked_task_index)
            self.dailies_listbox.delete(picked_task_index)

            self.db.delete('dailiesList', "taskName = '%s'" %
                           self.tool.to_database(task_name))
            self.db.delete('taskInfo', "taskName = '%s' AND listId = 1" % (
                self.tool.to_database(task_name)))
            self.task_info.delete(1.0, END)

        elif self.list_id == 2:
            task_name = self.goals_listbox.get(picked_task_index)

            self.goals_listbox.delete(picked_task_index)
            self.goals_listbox.delete(picked_task_index)

            self.db.delete('goalsList', "taskName = '%s'" %
                           self.tool.to_database(task_name))
            self.db.delete('taskInfo', "taskName = '%s' AND listId = 2" % (
                self.tool.to_database(task_name)))
            self.task_info.delete(1.0, END)

        self.initialize()
        self.remove_task_popup.destroy()

    def remove_task_no(self, event):
        self.remove_task_popup.destroy()

    def clear_task(self, event=""):
        self.clear_task_popup = Toplevel(self.main_frame)
        self.clear_task_popup.title("Clear Task")
        self.tool.center(self.clear_task_popup)
        self.clear_task_popup.config(bg="#333")

        self.center_frame = Frame(self.clear_task_popup, bg="#333")
        clear_yearlies_button = Button(
            self.center_frame, text="Yearlies", width=10)
        clear_dailies_button = Button(
            self.center_frame, text="Dailies", width=10)
        clear_goals_button = Button(self.center_frame, text="Goals", width=10)

        clear_yearlies_button.bind('<Button-1>', self.clear_yearlies)
        clear_dailies_button.bind('<Button-1>', self.clear_dailies)
        clear_goals_button.bind('<Button-1>', self.clear_goals)

        self.center_frame.grid(row=0, padx=20, pady=20)
        clear_yearlies_button.grid(row=0, column=0, padx=(0, 30))
        clear_dailies_button.grid(row=0, column=1, padx=(0, 30))
        clear_goals_button.grid(row=0, column=2)

    def clear_yearlies(self, event=""):
        self.db.delete('yearList')
        self.db.delete('taskInfo', 'listId = 0')
        self.initialize()
        self.clear_task_popup.destroy()

    def clear_dailies(self, event=""):
        self.db.delete('dailiesList')
        self.db.delete('taskInfo', 'listId = 1')
        self.initialize()
        self.clear_task_popup.destroy()

    def clear_goals(self, event=""):
        self.db.delete('goalsList')
        self.db.delete('taskInfo', 'listId = 2')
        self.initialize()
        self.clear_task_popup.destroy()

    def save_task_info(self, event=""):

        task_info = self.task_info.get(1.0, END)

        if self.list_id == 0:
            task_name = self.yearlies_listbox.get(self.task_id)
            task_name = self.tool.to_database(task_name)

            self.db.delete('taskInfo', "EXISTS (SELECT * FROM taskInfo WHERE taskName = '%s' AND listId = 0) AND taskName = '%s' AND listId = 0;"
                           % (task_name, task_name))
            self.db.insert('taskInfo', "listId, taskName, taskInfo",
                           "0, \"%s\", \"%s\"" % (task_name, task_info))

        elif self.list_id == 1:
            task_name = self.dailies_listbox.get(self.task_id)
            task_name = self.tool.to_database(task_name)

            self.db.delete('taskInfo', "EXISTS (SELECT * FROM taskInfo WHERE taskName = '%s' AND listId = 1) AND taskName = '%s' AND listId = 1;"
                           % (task_name, task_name))
            self.db.insert('taskInfo', "listId, taskName, taskInfo",
                           "1, \"%s\", \"%s\"" % (task_name, task_info))

        elif self.list_id == 2:
            task_name = self.goals_listbox.get(self.task_id)
            task_name = self.tool.to_database(task_name)

            self.db.delete('taskInfo', "EXISTS (SELECT * FROM taskInfo WHERE taskName = '%s' AND listId = 2) AND taskName = '%s' AND listId = 2;"
                           % (task_name, task_name))
            self.db.insert('taskInfo', 'listId, taskName, taskInfo',
                           "2, \"%s\", \"%s\"" % (task_name, task_info))

        self.save_indicator_label.config(text="Saved!")

    def clear_task_info(self, event=""):
        self.task_info.delete(1.0, END)
        self.save_indicator_label.config(text="Cleared!")


class DayPlanner:
    def __init__(self):
        self.now = datetime.datetime.now()
        self.tool = Tools(main_frame)
        self.db = Database(r"./taskmanager.db")

        month_dict = {1: 'January',
                      2: 'February',
                      3: 'March',
                      4: 'April',
                      5: 'May',
                      6: 'June',
                      7: 'July',
                      8: 'August',
                      9: 'September',
                      10: 'October',
                      11: 'November',
                      12: 'December'}

        # self.main_frame.title('Day Planner For %s %s %s' % (self.now.day, month_dict[self.now.month], self.now.year))
        root.title('Day Planner')
        main_frame.config(bg="#333")
        root.resizable(False, False)
        main_frame.grid(row=0)

        # Main Frame ============================================================

        self.main_frame = Frame(main_frame, bg="#333")
        self.main_frame.grid(row=0, column=0, padx=30, pady=(10, 10))

        # Top Frame ============================================================

        # Left Frame ====================
        left_frame = Frame(self.main_frame, bg="#333")
        hour_time_label = Label(left_frame, text='Hour', font=(
            'Helvetica', 17, 'bold'), bg="#333", fg="#efefef")
        activity_label = Label(left_frame, text='Overview', font=(
            'Helvetica', 17, 'bold'), bg="#333", fg="#efefef")

        self.hour_listbox = Listbox(
            left_frame, width=5, height=24, font=('Arial', 16), justify=CENTER)
        self.overview_listbox = Listbox(left_frame, width=50, height=24, font=(
            'Arial', 16), justify=CENTER, exportselection=False)

        for i in range(0, 24):
            self.hour_listbox.insert(END, i)

        self.overview_listbox.bind(
            '<<ListboxSelect>>', self.change_activity_list)

        left_frame.grid(row=0, pady=(0, 20))
        hour_time_label.grid(row=0, column=0, pady=(0, 10), sticky=W)
        activity_label.grid(row=0, column=1, pady=(0, 10))
        self.hour_listbox.grid(row=1, column=0, padx=(0, 20), sticky=W)
        self.overview_listbox.grid(row=1, column=1, padx=10)

        # Right Frame ===================
        right_frame = Frame(self.main_frame, bg="#333")
        minute_time_label = Label(right_frame, text='Min', font=(
            'Helvetica', 17, 'bold'), bg="#333", fg="#efefef")
        minute_activity_label = Label(right_frame, text='Activities', font=(
            'Helvetica', 17, 'bold'), bg="#333", fg="#efefef")

        self.minute_listbox = Listbox(
            right_frame, width=5, height=12, font=('Arial', 16), justify=CENTER)
        self.activity_listbox = Listbox(right_frame, width=30, height=12, font=(
            'Arial', 16), justify=CENTER, exportselection=False)

        for i in range(0, 61, 5):
            self.minute_listbox.insert(END, i)

        self.activity_listbox.bind('<<ListboxSelect>>', self.change_task_info)

        right_frame.grid(row=0, column=1, padx=(0, 0), pady=(0, 20), sticky=N)
        minute_time_label.grid(row=0, column=0, pady=(0, 10))
        minute_activity_label.grid(row=0, column=1, pady=(0, 10))
        self.minute_listbox.grid(row=1, column=0, padx=(20, 20))
        self.activity_listbox.grid(row=1, column=1, padx=10)

        # Bottom Frame ==========================================================

        button_frame = Frame(right_frame, bg="#333")
        self.add_button = Button(
            button_frame, text='Add', width=8, height=1, font=('Helvetica', 14))
        self.rename_button = Button(
            button_frame, text='Rename', width=8, height=1, font=('Helvetica', 14))
        self.remove_button = Button(
            button_frame, text='Remove', width=8, height=1, font=('Helvetica', 14))
        clear_button = Button(button_frame, text='Clear All',
                              width=8, height=1, font=('Helvetica', 14))

        self.add_button.bind('<Button-1>', self.add_task)
        self.rename_button.bind('<Button-1>', self.rename_task)
        self.remove_button.bind('<Button-1>', self.remove_task)
        clear_button.bind('<Button-1>', self.clear_task)

        self.task_info_label = Label(right_frame, text='Activity: ', font=(
            'Helvetica', 17, 'bold'), bg="#333", fg="#efefef")
        self.task_info = Text(right_frame, width=41,
                              height=6, font=('Helvetica', 14))
        save_frame = Frame(right_frame, bg="#333")
        self.save_button = Button(
            save_frame, text='Save Info', width=8, height=1, font=('Helvetica', 14))
        self.save_indicator_label = Label(save_frame, text="", font=(
            'Helvetica', 14), bg="#333", fg="#efefef")

        self.save_button.bind('<Button-1>', self.save_task_info)

        self.add_button.config(state=DISABLED)
        self.rename_button.config(state=DISABLED)
        self.remove_button.config(state=DISABLED)
        self.save_button.config(state=DISABLED)

        button_frame.grid(row=2, pady=(30, 0), columnspan=2)
        self.add_button.grid(row=0, column=0, padx=(0, 20))
        self.rename_button.grid(row=0, column=1, padx=(0, 20))
        self.remove_button.grid(row=0, column=2, padx=(0, 20))
        clear_button.grid(row=0, column=3)

        self.task_info.grid(row=3, columnspan=2, pady=(30, 0))
        save_frame.grid(row=4, columnspan=2, pady=(20, 0))
        self.save_button.grid(row=0, padx=(0, 20))
        self.save_indicator_label.grid(row=0, column=1)

        root.update_idletasks()
        self.tool.center(root)

        self.initialize()

    def initialize(self):
        self.db.raw_execute(
            "SELECT DISTINCT hourIndex FROM activityList ORDER BY hourIndex ASC")
        hours = self.db.fetchall()

        for i in range(0, 24):
            self.overview_listbox.insert(i, '')

        for hour in hours:
            tasks_in_hour_list = []
            self.db.raw_execute(
                "SELECT taskName FROM activityList WHERE hourIndex = %d ORDER BY minIndex ASC" % (hour))
            tasks = self.db.fetchall()

            for task in tasks:
                tasks_in_hour_list.append(self.tool.from_database(task[0]))
            overview_name = ', '.join(tasks_in_hour_list)

            self.overview_listbox.delete(hour)
            self.overview_listbox.insert(hour, overview_name)

    def change_activity_list(self, event):
        self.activity_listbox.config(state=NORMAL)
        self.add_button.config(state=DISABLED)
        self.rename_button.config(state=DISABLED)
        self.remove_button.config(state=DISABLED)
        self.save_button.config(state=DISABLED)
        self.task_info.delete(1.0, END)

        self.hour_id = self.overview_listbox.curselection()[0]
        self.hour_listbox.activate(self.hour_id)

        for i in range(0, 12):
            self.activity_listbox.insert(i, '')

        self.db.raw_execute(
            "SELECT minIndex, taskName FROM activityList WHERE hourIndex = %d ORDER BY minIndex ASC" % (self.hour_id))
        activities = self.db.fetchall()

        for min_index, taskName in activities:
            self.activity_listbox.delete(min_index)
            self.activity_listbox.insert(
                min_index, self.tool.from_database(taskName))

        self.save_indicator_label.config(text="")

    def change_task_info(self, event=""):
        self.add_button.config(state=NORMAL)
        self.rename_button.config(state=NORMAL)
        self.remove_button.config(state=NORMAL)
        self.save_button.config(state=NORMAL)

        self.minute_id = self.activity_listbox.curselection()[0]
        self.minute_listbox.activate(self.minute_id)
        try:
            self.task_info.delete(1.0, END)

            self.db.select('activityInfo', 'taskInfo', 'hourIndex = %d AND minIndex = %d' % (
                self.hour_id, self.minute_id))
            task_info = self.db.fetchone()[0]
            self.task_info.insert(END, task_info)

            self.save_indicator_label.config(text="")
        except Exception as e:
            pass

    def save_task_info(self, event=""):
        try:
            task_info = self.task_info.get(1.0, END)

            self.db.delete('activityInfo', 'EXISTS (SELECT * FROM activityInfo WHERE hourIndex = %d AND minIndex = %d) AND hourIndex = %d AND minIndex = %d;'
                           % (self.hour_id, self.minute_id, self.hour_id, self.minute_id))
            self.db.insert('activityInfo', 'hourIndex, minIndex, taskInfo', "%d, %d, '%s'" % (
                self.hour_id, self.minute_id, task_info))

            self.save_indicator_label.config(text="Saved!")
        except Exception as e:
            pass

    def add_task(self, event=""):
        try:
            selected_index = self.minute_id
            if selected_index is not None:
                self.activity_listbox.config(state=DISABLED)
                task_name_on_list = self.activity_listbox.get(selected_index)

                self.add_task_popup = Toplevel(self.main_frame)
                self.add_task_popup.title("Add Task")
                self.tool.center(self.add_task_popup)
                self.add_task_popup.config(bg="#333")

                add_task_label = Label(self.add_task_popup, text="Enter Task Name",
                                       bg="#333", foreground="#efefef", font=('Arial', 13))
                self.add_task_entry = Entry(
                    self.add_task_popup, width=30, justify=CENTER)
                add_task_button = Button(
                    self.add_task_popup, text="Add Task", width=18)

                self.add_task_entry.bind('<Return>', self.add_task_to_app)
                add_task_button.bind('<Button-1>', self.add_task_to_app)

                add_task_label.pack(pady=10)
                self.add_task_entry.pack()
                add_task_button.pack(padx=50, pady=(12, 10))

                self.add_task_popup.resizable(False, False)

        except Exception as e:
            print(e)

    def add_task_to_app(self, event):
        task_name = self.add_task_entry.get()
        self.add_task_entry.delete(0, END)
        self.add_task_popup.destroy()

        selected_index = self.minute_id
        task_name_on_list = self.activity_listbox.get(selected_index)

        self.activity_listbox.config(state=NORMAL)

        if task_name_on_list == '' and len(task_name) > 0:
            self.activity_listbox.delete(selected_index)
            self.activity_listbox.insert(selected_index, task_name)
            self.db.insert('activityList', 'hourIndex, minIndex, taskName', "%d, %d, '%s'" %
                           (int(self.hour_id), int(selected_index), self.tool.to_database(task_name)))

        self.initialize()

    def rename_task(self, event):
        try:
            self.activity_listbox.config(state=DISABLED)
            selected_index = self.minute_id
            task_name = self.activity_listbox.get(selected_index)

            self.rename_task_popup = Toplevel(self.main_frame)
            self.rename_task_popup.title("Rename Task")
            self.tool.center(self.rename_task_popup)
            self.rename_task_popup.config(bg="#333")

            rename_task_label = Label(self.rename_task_popup, text="Rename %s to" %
                                      task_name, bg="#333", foreground="#efefef", font=('Arial', 13))
            self.rename_task_entry = Entry(
                self.rename_task_popup, text=task_name, width=30, justify=CENTER)
            self.rename_task_entry.insert(0, task_name)
            rename_task_button = Button(
                self.rename_task_popup, text="Rename Task", width=20)

            self.rename_task_entry.bind('<Return>', self.rename_task_to_app)
            rename_task_button.bind('<Button-1>', self.rename_task_to_app)

            rename_task_label.pack(pady=10)
            self.rename_task_entry.pack()
            rename_task_button.pack(padx=50, pady=(12, 10))

            self.rename_task_popup.resizable(False, False)
        except:
            pass

    def rename_task_to_app(self, event):
        selected_index = self.minute_id
        task_name = self.activity_listbox.get(selected_index)
        renamed_task_name = self.rename_task_entry.get()

        self.activity_listbox.config(state=NORMAL)

        self.activity_listbox.delete(selected_index)
        self.activity_listbox.insert(selected_index, renamed_task_name)

        self.db.update('activityList', "taskName = '%s'" % self.tool.to_database(renamed_task_name),
                       "hourIndex = %d AND  minIndex = %d" % (self.hour_id, int(selected_index)))

        self.rename_task_popup.destroy()
        self.initialize()

    def remove_task(self, event):
        try:
            self.activity_listbox.config(state=DISABLED)
            selected_index = self.minute_id
            task_name = self.activity_listbox.get(selected_index)

            if len(task_name) >= 1:
                self.remove_task_popup = Toplevel(self.main_frame)
                self.remove_task_popup.title("Remove Task")
                self.tool.center(self.remove_task_popup)
                self.remove_task_popup.config(bg="#333")

                remove_task_label = Label(self.remove_task_popup, text="Are you sure you would like to remove %s?" %
                                          task_name, bg="#333", foreground="#efefef", font=('Arial', 13))

                remove_task_button_frame = Frame(
                    self.remove_task_popup, bg="#333")
                remove_task_button_yes = Button(
                    remove_task_button_frame, text="Yes", width=10)
                remove_task_button_no = Button(
                    remove_task_button_frame, text="No", width=10)

                remove_task_button_yes.bind('<Button-1>', self.remove_task_yes)
                remove_task_button_no.bind('<Button-1>', self.remove_task_no)

                remove_task_label.grid(
                    row=0, column=0, padx=(10, 10), pady=(10, 10))
                remove_task_button_frame.grid(row=1, column=0, pady=(0, 15))
                remove_task_button_yes.grid(row=0, column=0, padx=(0, 20))
                remove_task_button_no.grid(row=0, column=1)

                self.remove_task_popup.resizable(False, False)
        except:
            pass

    def remove_task_yes(self, event):
        selected_index = self.minute_id
        task_name = self.activity_listbox.get(selected_index)

        self.activity_listbox.config(state=NORMAL)
        self.activity_listbox.delete(selected_index)
        self.activity_listbox.insert(selected_index, '')

        self.task_info.delete(1.0, END)

        self.db.delete('activityList', "hourIndex = %d AND minIndex = %d" % (
            int(self.hour_id), int(selected_index)))
        self.db.delete('activityInfo', "hourIndex = %d AND minIndex = %d" % (
            int(self.hour_id), int(selected_index)))

        self.remove_task_popup.destroy()

        # self.change_task_info()
        self.initialize()

    def remove_task_no(self, event):
        self.remove_task_popup.destroy()
        self.activity_listbox.config(state=NORMAL)

    def clear_task(self, event):
        self.clear_task_popup = Toplevel(self.main_frame)
        self.clear_task_popup.title("Clear All Task")
        self.clear_task_popup.config(bg="#333")

        remove_task_label = Label(self.clear_task_popup, text="Are you sure you would like to clear all activities?",
                                  bg="#333", foreground="#efefef", font=('Arial', 13))

        remove_task_button_frame = Frame(self.clear_task_popup, bg="#333")
        remove_task_button_yes = Button(
            remove_task_button_frame, text="Yes", width=10)
        remove_task_button_no = Button(
            remove_task_button_frame, text="No", width=10)

        remove_task_button_yes.bind('<Button-1>', self.clear_task_yes)
        remove_task_button_no.bind('<Button-1>', self.clear_task_no)

        remove_task_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))
        remove_task_button_frame.grid(row=1, column=0, pady=(0, 15))
        remove_task_button_yes.grid(row=0, column=0, padx=(0, 20))
        remove_task_button_no.grid(row=0, column=1)

        self.clear_task_popup.resizable(False, False)
        self.tool.center(self.clear_task_popup)

    def clear_task_yes(self, event):
        self.activity_listbox.delete(0, END)

        self.db.delete('activityList')
        self.db.delete('activityInfo')

        self.clear_task_popup.destroy()

        self.initialize()

    def clear_task_no(self, event):
        self.clear_task_popup.destroy()


class LearntList:
    def __init__(self):
        root.title("Learnt List")
        root.resizable(False, False)
        self.tool = Tools(root)
        self.db = Database(r"./taskmanager.db")

        main_frame.config(bg="#333")
        main_frame.grid(row=0)

        self.main_frame = Frame(main_frame, bg="#333")
        self.main_frame.grid(row=0, padx=30, pady=15)

        top_frame = Frame(self.main_frame, bg="#333")
        top_frame.grid(row=0)

        grateful_label = Label(top_frame, text="What I Learnt / Achieved For The Day",
                               font=('Helvetica', 17, 'bold'), bg="#333", fg="#efefef")

        self.number_listbox = Listbox(top_frame, width=3, height=20, font=(
            'Arial', 15), justify=CENTER, exportselection=False)

        self.list_listbox = Listbox(top_frame, width=45, height=20, font=(
            'Arial', 15), justify=CENTER, exportselection=False)

        grateful_label.grid(row=0, columnspan=2, pady=(0, 15))
        self.number_listbox.grid(row=1)
        self.list_listbox.grid(row=1, column=1)

        bottom_frame = Frame(self.main_frame, bg="#333")
        bottom_frame.grid(row=1, pady=(20, 0))

        button_width = 14

        add_button = Button(bottom_frame, text="Add",
                            font=('Arial', 14), width=button_width)
        add_button.grid(row=0, padx=(0, 20))

        remove_button = Button(bottom_frame, text="Remove Latest", font=(
            'Arial', 14), width=button_width)
        remove_button.grid(row=0, padx=(0, 20), column=1)

        clear_button = Button(bottom_frame, text="Clear",
                              font=('Arial', 14), width=button_width)
        clear_button.grid(row=0, column=2)

        add_button.bind("<Button-1>", self.add_item)
        remove_button.bind("<Button-1>", self.remove_item)
        clear_button.bind("<Button-1>", self.clear_item)

        root.update_idletasks()
        self.tool.center(root)

        self.initialize()

    def initialize(self):
        self.number_listbox.delete(0, END)
        self.list_listbox.delete(0, END)

        self.db.select("gratList", "*")
        res = self.db.fetchall()

        for num, info in res:
            self.number_listbox.insert(END, '')
            self.list_listbox.insert(END, '')
            self.number_listbox.insert(END, num)
            self.list_listbox.insert(END, self.tool.from_database(info))

    def add_item(self, event=""):
        self.add_item_popup = Toplevel(self.main_frame)
        self.add_item_popup.title("Add")
        self.tool.center(self.add_item_popup)
        self.add_item_popup.config(bg="#333")

        self.center_frame = Frame(self.add_item_popup, bg="#333")
        add_item_label = Label(self.center_frame, text="Add Item", font=(
            "Arial", 14), bg="#333", fg="#efefef")
        self.add_item_entry = Entry(
            self.center_frame, width=50, justify=CENTER)
        add_item_button = Button(self.center_frame, text="Add", width=20)

        self.add_item_entry.bind('<Return>', self.add_item_to_app)
        add_item_button.bind('<Button-1>', self.add_item_to_app)

        self.center_frame.grid(row=0, padx=20, pady=10)
        add_item_label.grid(row=0, pady=(0, 10))
        self.add_item_entry.grid(row=1, pady=(0, 15))
        add_item_button.grid(row=2)

    def add_item_to_app(self, event=""):
        info = self.tool.to_database(self.add_item_entry.get())
        self.db.select("gratList", "MAX(listId)")
        count = self.db.fetchone()[0]
        print(info)
        if count == None:
            self.db.insert("gratList", "listId, gratInfo", "1, \"%s\"" % info)
        else:
            self.db.insert("gratList", "listId, gratInfo",
                           "%d, \"%s\"" % (int(count) + 1, info))

        self.add_item_popup.destroy()
        self.initialize()

    def remove_item(self, event=""):
        self.db.select("gratList", "MAX(listId)")
        lastId = int(self.db.fetchone()[0])
        self.db.delete("gratList", "listId=%d" % lastId)
        self.initialize()

    def clear_item(self, event=""):

        self.db.delete("gratList")
        self.initialize()


class Database:
    def __init__(self, database):
        self.connection = s3.connect(database)
        self.cursor = self.connection.cursor()

        try:
            # To Do List
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS yearList(taskId INT, taskName VARCHAR(40));")
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS dailiesList(taskId INT, taskName VARCHAR(40));")
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS goalsList(taskId INT, taskName VARCHAR(50), deadline VARCHAR(40));")
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS taskInfo(listId INT, taskName VARCHAR(50), taskInfo VARCHAR(200));")

            # Day Planner
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS activityList(hourIndex INT, minIndex INT, taskName VARCHAR(20));")
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS activityInfo(hourIndex INT, minIndex INT, taskInfo VARCHAR(200));")

            # Task Timer
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS taskList(taskId INT PRIMARY KEY, taskName VARCHAR(20));")
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS log(taskId INT, logId INT, time INT, logDate TEXT);")

            # Gratitude List
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS gratList(listId INT, gratInfo VARCHAR(200));")

            self.connection.commit()
            print("Connection Successful")
        except:
            self.connection.rollback()

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def execute(self, query, command):
        try:
            self.cursor.execute(query)
            self.connection.commit()

        except Exception as e:
            if command == "select":
                print("Select Failed:", str(e))
            elif command == "insert":
                print("Insert Failed:", str(e))
            elif command == "update":
                print("Update Failed:", str(e))
            elif command == "delete":
                print("Delete Failed:", str(e))
            else:
                pass
            self.connection.rollback()

    def raw_execute(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print(str(e))

    def select(self, table, columns, conditions=""):
        query = ""
        if conditions != "":
            query = "SELECT %s FROM %s WHERE %s;" % (
                columns, table, conditions)
        else:
            query = "SELECT %s FROM %s;" % (columns, table)
        self.execute(query, "select")

    def insert(self, table, columns, arguments):
        query = "INSERT INTO %s (%s) VALUES (%s);" % (
            table, columns, arguments)
        self.execute(query, "insert")

    def update(self, table, change, conditions=""):
        query = ""
        if conditions != "":
            query = "UPDATE %s SET %s WHERE %s" % (table, change, conditions)
        else:
            query = "UPDATE %s SET %s" % (table, change)
        self.execute(query, "update")

    def delete(self, table, conditions=""):
        query = ""
        if conditions != "":
            query = "DELETE FROM %s WHERE %s" % (table, conditions)
        else:
            query = "DELETE FROM %s" % (table)
        self.execute(query, "delete")

    def __del__(self):
        self.connection.close()


class Tools:
    def __init__(self, master):
        self.master = master

    def set_window_size(self, width, height, window=None):
        if window is not None:
            self.master = window
        w = width
        h = height
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))

    def center(self, window):
        w = window.winfo_reqwidth()
        h = window.winfo_reqheight()
        ws = window.winfo_screenwidth()
        hs = window.winfo_screenheight()
        x = (ws / 2) - w / 2
        y = (hs / 2) - h / 2
        window.geometry("+%d+%d" % (x, y))

    def to_database(self, string):
        string_split = string.split(' ')

        for i in range(len(string_split)):
            string_split[i] = string_split[i].lower()

        new_string = '_'.join(string_split)
        return new_string

    def from_database(self, string):
        string_split = string.split('_')

        for i in range(len(string_split)):
            if len(string_split[i]) > 0:
                string_split[i] = string_split[i][0].upper() + \
                    string_split[i][1:]

        new_string = ' '.join(string_split)
        return new_string

    def to_seconds(self, string):
        time_split = string.split(':')
        seconds = int(time_split[0]) * 3600 + \
            int(time_split[1]) * 60 + int(time_split[2])
        return seconds

    def to_time(self, seconds):
        time = seconds
        day = time // (24 * 3600)
        time = time % (24 * 3600)
        hour = time // 3600
        time %= 3600
        minutes = time // 60
        time %= 60
        seconds = time
        return "%d:%d:%d:%d" % (day, hour, minutes, seconds)


def print_hi():
    print("hi")


def start_screen():
    global main_frame
    main_frame.destroy()
    main_frame = Frame(root, bg="#333")
    main_frame.grid(row=1)
    print("startscreen")
    StartScreen()


def to_do_list():
    global main_frame
    main_frame.destroy()
    main_frame = Frame(root, bg="#333")
    main_frame.grid(row=1)
    print("todolist")
    ToDoList()


def day_planner():
    global main_frame
    main_frame.destroy()
    main_frame = Frame(root, bg="#333")
    main_frame.grid(row=1)
    DayPlanner()


def gratitude_list():
    global main_frame
    main_frame.destroy()
    main_frame = Frame(root, bg="#333")
    main_frame.grid(row=1)
    LearntList()


if __name__ == "__main__":
    root = Tk()
    root.config(bg="#333")
    main_frame = Frame(root, bg="#333")
    main_frame.grid(row=1)
    tool = Tools(root)

    app = start_screen()

    menubar = Menu(root, relief=RAISED, bd=2)
    filemenu = Menu(menubar, tearoff=0)
    menubar.add_command(label="Start Screen",
                        command=start_screen, font=('Arial', 17))
    menubar.add_command(label="To-Do List",
                        command=to_do_list, font=('Arial', 17))
    menubar.add_command(label="Day Planner",
                        command=day_planner, font=('Arial', 17))
    menubar.add_command(label="Learnt List",
                        command=gratitude_list, font=('Arial', 17))
    root.config(menu=menubar)

    tool.center(root)

    root.mainloop()
