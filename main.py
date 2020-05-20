import tkinter as tk
from tkinter import ttk
from tkinter import Frame, messagebox as mBox
from sentences import sentence_list
import time
import random

class Main(Frame):
    def __init__(self, window, *args, **kwargs):
        Frame.__init__(self, window, *args, **kwargs)
        # Instanciate window
        self.window = window
        self.window.title("Speed Typing Test")
        self.index = 0
        self.backspace_pressed = False
        self.backspace_count = 0
        self.char_count = 1
        self.start_array = []

        self.create_widgets()
        self.sentence_entry.focus()

    def create_widgets(self):
        # TODO set ScrolledText width to Label wraplength
        # Create index for random sentence to be displayed
        index = random.randrange(0,len(sentence_list))
        self.label_var = tk.StringVar()
        self.label_var.set(sentence_list[index])
        self.entry_var = tk.StringVar()
        self.entry_var.trace_add('write', self.check_chars)
        self.result_var = tk.StringVar()
        self.result_var.set("Result")

        # Widgets
        self.main_frame = tk.Frame(self.window)
        self.main_frame.grid(column=0, row=0, padx=10, pady=10)
        self.sentence_label = ttk.Label(self.main_frame, textvariable=self.label_var)
        self.sentence_label.grid(column=0, row=0, padx=10)
        self.sentence_label.config(font=('Helvetica', 24))
        self.sentence_entry = ttk.Entry(self.main_frame, name='entry1', textvariable=self.entry_var)
        self.sentence_entry.grid(column=0, row=1, sticky='ew')
        self.sentence_entry.config(font=('Helvetica', 24) )
        # self.sentence_entry.bindtags(('.entry1','Entry','self.check_chars','.','all'))
        self.result_label = ttk.Label(self.main_frame, textvariable=self.result_var)
        self.result_label.grid(column=0, row=3, sticky='ew')
        self.result_label.config(font=('Helvetica', 24))

        self.sentence_entry.bind('<Key>', self.check_backspace)

    def check_chars(self, *args):
        """ This function checks every character typed to see if it matches the character from the same index as the one typed from the sentence displayed in the label """
        # TODO fix label index error when entry text longer than label
        if self.entry_var.get() == self.sentence_label['text']:
            end_time = time.time()
            self.total_time = round((end_time - self.start_array[0]), 2)
            self.sentence_entry.configure(state='readonly')
            self.calculate_wpm()
            self.calculate_accuracy()
            # mBox.showinfo("Result", "You finished typing.\nYour result is: %s seconds." % self.total_time)
            mBox.showinfo("Result", "You finished typing.\nYour result is: {} seconds.\nWords per minute (WPM): {}.\nAccuracy: {}%.".format(self.total_time, self.wpm, self.accurracy))
            self.sentence_entry.configure(state='normal')
            self.new_sentence()
        if self.backspace_pressed == True:
            # Reset the index when backspace is pressed (delete character)
            # TODO find different solution how to decrement the index
            self.index -= 2
            if self.index < 0:
                self.index = 0
            self.backspace_pressed = False
            self.char_count += 1
        if self.index < len(self.sentence_label['text']):
            if len(self.entry_var.get()) > 0 and self.backspace_pressed == False:
                start_time = time.time()
                self.start_array.append(start_time)
                # Get typed character to be compared with the character from label at the same index
                ent_char = self.entry_var.get()[self.index]
                lbl_char = self.sentence_label['text'][self.index]
                # Get the typed string so far and compare with the label
                # Get a new index so can get the full sentence as typed
                sentence_index = self.index + 1
                ent_sentence = self.entry_var.get()[:sentence_index]
                lbl_sentence = self.sentence_label['text'][:sentence_index]
                if ent_char == lbl_char and ent_sentence == lbl_sentence:
                    self.sentence_entry.config(foreground='green')
                else:
                    self.sentence_entry.config(foreground='red')
                self.index += 1
                self.char_count += 1
        else:
            self.index += 1
            self.char_count += 1
            self.sentence_entry.config(foreground='red')

    def check_backspace(self, key, *args):
        # This function helps to identify if backspace key is pressed (delete character)
        if key.keysym == 'BackSpace':
            self.backspace_pressed = True
            self.backspace_count += 1

    def show_result(self):
        pass

    def calculate_wpm(self):
        self.wpm = int((self.char_count / 5) / (self.total_time / 60))

    def calculate_accuracy(self):
        self.accurracy = round(((self.char_count - self.backspace_count) / self.char_count) * 100, 2)

    def new_sentence(self):
        self.start_array = []
        self.char_count = 1
        self.backspace_count = 0
        index = random.randrange(0,len(sentence_list))
        self.label_var.set(sentence_list[index])
        self.entry_var.set("")
        self.index = 0
        self.window.focus_set()
        self.sentence_entry.focus()
        # self.result_var.set("Result: %s seconds." % self.total_time)
        self.result_var.set("Result: {} seconds.\nWords per minute (WPM): {}.\nAccuracy: {}%.".format(self.total_time, self.wpm, self.accurracy))



# Start main loop
if __name__ == "__main__":
    root = tk.Tk()
    main = Main(root)
    main.window.mainloop()
