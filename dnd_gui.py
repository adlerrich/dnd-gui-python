###################################################################################
# GUI interface to do some basic D&D 3.5 dice interactions
# Written by Rich Adler - adlerrich - 9/4/23
# MIGHT INCLUDE:
    # Saving throw generator for spells
    # Spell compendium
    # Character Creation
    # D&D Class and Class Feature compendium
    # Modify Attack Window to accept multiple bonuses
    # Graphics, background images, dark mode toggle, and other fluff
###################################################################################

import tkinter as tk
from tkinter import ttk
import random as rn

# Set up parent window to host frames
root = tk.Tk()
main_window = tk.Frame(root)
root.geometry("800x500")
root.config(bg="black")

# Use them to make an attack roll, sorting first by checking to see if it's a critcal roll(note a critcal in D&D is 
#either a naturally generated 20, which means the best possible outcome will occur in a situation, and a naturally
# generated 1, which means the opposite), then checking if the roll + hit bonus is greater than the armor class given
def roll_attacks(segment_type, intvar_list):
    dice_list = [int(item.get()) for item in intvar_list]
    rolls = dice_list[0]
    bonus = dice_list[1]
    ac = dice_list[2]
    damage = dice_list[3]
    crit = int(dice_list[4])
    damage_mod = dice_list[5]

    roll_list = [rn.randint(1,20) for i in range(0, rolls)]
    output = []
    for i in roll_list:
        if i == 1:
            output.append("Critical Fail!  ")
        elif i >= crit:
            output.append("Crit! " + str((rn.randint(1, damage) + damage_mod) * 2) + " damage ")
        elif (i + bonus) > ac:
            temp_damage = rn.randint(1, damage) + damage_mod
            if temp_damage < 10:
                output.append("Hit " + str(temp_damage) + " damage    ")
            elif temp_damage > 9:
                output.append("Hit " + str(temp_damage) + " damage   ")
        else:
            output.append("Miss            ")

    text_area = tk.Text(master=segment_type, width=16, height=len(output), bg="black", fg="white")
    text_area.grid(row=20, column=0)
    for i in range(len(output)):
        index = str(i) + ".0"
        text_area.insert(index, output[i])

# Check for critcal rolls, and add bonus to roll otherwise
def roll_checks(segment_type, intvar_list):
    dice_list = [int(item.get()) for item in intvar_list]

    roll_list = [rn.randint(1,20) for i in range(dice_list[0])]
    output = []
    for roll in roll_list:
        if roll == 1:
            to_append = ("Nat 1 ")
        elif roll == 20:
            to_append = ("Nat 20")
        elif dice_list[1] + roll > 9:
            to_append = (str(roll + dice_list[1]) + "    ")
        else:
            to_append = (str(roll + dice_list[1]) + "     ")
        output.append("You rolled: " + to_append)

    text_area = tk.Text(master=segment_type, width=18, height=len(output), bg="black", fg="white")
    text_area.grid(row=14, column=1)
    for i in range(len(output)):
        index = str(i) + ".0"
        text_area.insert(index, output[i])

# Filter through a giant elif statement to see turnig result. D&D 3.5 turning is... suboptimal
def roll_turn(segment_type, intvar_list):
    dice_list = [int(item.get()) for item in intvar_list]
    levelCleric = dice_list[0]
    cha = dice_list[1]
    output = []

    D20 = rn.randint(1,20) + cha + 2
    D6a = rn.randint(1,6)
    D6b = rn.randint(1,6)
    turn_count = D6a + D6b + cha
    turn_total = None

    if turn_count <= 0 :
        turn_total = levelCleric - 4
    elif 3 >= turn_count > 0 :
        turn_total = levelCleric - 3
    elif 6 >= turn_count > 3 :
        turn_total = levelCleric - 2
    elif 9 >= turn_count > 6 :
        turn_total = levelCleric - 1
    elif 12 >= turn_count > 9 :
        turn_total = levelCleric
    elif 15 >= turn_count > 12 :
        turn_total = levelCleric + 1
    elif 18 >= turn_count > 15 :
        turn_total = levelCleric + 2
    elif 21 >= turn_count > 18 :
        turn_total = levelCleric + 3
    elif turn_count > 21 :
        turn_total = levelCleric + 4

    if turn_total < 10:
        to_append_turn = str(turn_total) + "  "
    elif turn_total > 9:
        to_append_turn = str(turn_total) + " "
  
    output = [" total hit die  ", ("You can turn " + to_append_turn),  "of undead, with ", "a maximum undead", ("hit die of " + str(D20))]

    text_area = tk.Text(master=segment_type, width=16, height=7, bg="black", fg="white")
    text_area.grid(row=7, column=2)
    for i in range(0, len(output)):
        index = str(i) + ".0"
        text_area.insert(index, output[i])
      
# TODO do something about this comment
# Defining the main superclass that does most of the heavy lifting, initialize class with a list of the labels to go above the entries, 
# the additional segment(the window wrappers are hard coded in as to keep track of the data and because frames interact with the root window 
# and are responosible for the overlays under the checkboxes, see below for checkbox wrapper set ups, the additional segment (wrapper) will 
# sit on an underlying frame which itself sits on top of the root window), and the value of the column to place the checkbox and drop down menu.  
# Two lists are created based on the length of the label list, one for entries and one for tk.Intvar() objects. The above functions retrieve 
#and work with the intvar lists, the data being obtained from the entry widgets. This superclass also contains the method create_layout(), 
#requiring no arguements, instead setting up the layout based on the init information. Using the grid method, it starts at row 1, as the 
#checkboxes are hosted on row 0, and the column value provided, sets up a label, adds 1 to the current row, then places an entry. 
#It continues this until it runs out of labels, at which point it will attach a button under the final entry widget with an appropriate command. 
#Note that the class launches with the button_command set to None, and it's manually the line after initializing. This is because the command
#uses self data, and cannot initialize with it's own data passed into a function.
class Segment_Layout:
    def __init__(self, label_list, additional_segment, column_val):
        self.label_list = label_list
        self.button_command = None
        self.intvar_list = [tk.IntVar(additional_segment) for i in range(len(label_list))]
        self.entry_list = [0 for i in range(len(label_list))]
        self.column_val = column_val
        self.additional_segment = additional_segment

    def create_layout(self):
        current_row = 1
        num_widgets = len(self.label_list)
        for i in range(num_widgets):
            temp = self.label_list[i]
            self.label_list[i] = tk.Label(self.additional_segment, text=temp, fg="white", bg="black")
            self.label_list[i].grid(row=current_row, column=self.column_val)
            current_row += 1
            self.entry_list[i] = tk.Entry(self.additional_segment, textvariable=self.intvar_list[i], fg="white", bg="slate gray")
            self.entry_list[i].grid(row=current_row, column=self.column_val)
            current_row+=1

        layout_button = tk.Button(self.additional_segment, text="Roll Dice", command=self.button_command, fg="white", bg="dark slate gray")
        layout_button.grid(row=current_row, column=self.column_val)

# Define specific classes that do different math all based on Segment_Layout
class Attack_Layout(Segment_Layout):
    def __init__(Segment_Layout, label_list, additional_segment, column_val):
        super().__init__(label_list, additional_segment, column_val)

class Check_Layout(Segment_Layout):   
    def __init__(Segment_Layout, label_list, additional_segment, column_val):
        super().__init__(label_list, additional_segment, column_val)

class Turn_Layout(Segment_Layout):
    def __init__(Segment_Layout, label_list, additional_segment, column_val):
        super().__init__(label_list, additional_segment, column_val)

# Series of functions to wrap frames over root window when checked 
def on_click_atk():
    if atk_button_var.get() == 1:
        additional_section_atk.grid(row=0, column=0)
        atk_wrapper.config(height = 0)
    elif atk_button_var.get() == 0:
        additional_section_atk.grid_forget()
        atk_wrapper.config(height = 1)

def on_click_check():
    if check_button_var.get() == 1:
        additional_section_check.grid(row=0, column=1)
        check_wrapper.config(height = 0)
    elif check_button_var.get() == 0:
        additional_section_check.grid_forget()
        check_wrapper.config(height = 1)

def on_click_turn():
    if turn_button_var.get() == 1:
        additional_section_turn.grid(row=0, column=2)
        turn_wrapper.config(height = 0)
    elif turn_button_var.get() == 0:
        additional_section_turn.grid_forget()
        turn_wrapper.config(height = 1)

atk_button_var = tk.IntVar()
atk_button= tk.Checkbutton(text="Roll Attacks", variable=atk_button_var, command=on_click_atk, fg="white", bg="black")
atk_button.grid(row=0, column=0)

check_button_var = tk.IntVar()
check_button = tk.Checkbutton(text="Roll Checks", variable=check_button_var, command=on_click_check, fg="white", bg="black")
check_button.grid(row=0, column=1)

turn_button_var = tk.IntVar()
turn_button= tk.Checkbutton(text="Turn Undead", variable=turn_button_var, command=on_click_turn, fg="white", bg="black")
turn_button.grid(row=0, column=2)

# Set up each frame, and frame wrapper, attach it to the appropriate class, define it's button commands, and create a layout based on init data
atk_wrapper = tk.Frame(root)
atk_wrapper.grid(row=1, column=0)
additional_section_atk = tk.Frame(atk_wrapper, bg="black")
attack_segment = Attack_Layout(["Number of Attacks", "Hit Bonus", "Enemy AC", "Damage Die", "Lower Crit Range", "Damage Bonus"], additional_section_atk, 0)
attack_segment.button_command = lambda: roll_attacks(additional_section_atk, attack_segment.intvar_list)
attack_segment.create_layout()

check_wrapper = tk.Frame(root)
check_wrapper.grid(row=1, column=1)
additional_section_check = tk.Frame(check_wrapper, bg="black")
check_segment = Check_Layout(["Number of Checks", "Skill Bonus"], additional_section_check, 1)
check_segment.button_command = lambda: roll_checks(additional_section_check, check_segment.intvar_list)
check_segment.create_layout()

turn_wrapper = tk.Frame(root)
turn_wrapper.grid(row=1, column=2)
additional_section_turn = tk.Frame(turn_wrapper, bg="black")
turn_segment = Turn_Layout(["Cleric Level", "Charisma Modifier"], additional_section_turn, 2)
turn_segment.button_command = lambda: roll_turn(additional_section_turn, turn_segment.intvar_list)
turn_segment.create_layout()

def hide_segments():
    additional_section_atk.grid_forget()
    atk_wrapper.config(height = 1)
    atk_button_var.set(0)
    additional_section_check.grid_forget()
    check_wrapper.config(height = 1)
    check_button_var.set(0)
    additional_section_turn.grid_forget()
    turn_wrapper.config(height = 1)
    turn_button_var.set(0)

def exit_program():
    root.destory()
    atk_wrapper.destroy()
    check_wrapper.destroy()
    turn_wrapper.destory()

def reset_windows(intvar_list_1, intvar_list_2, intvar_list_3):
    for value in intvar_list_1:        
        value.set(0)

    for value in intvar_list_2:
        value.set(0)

    for value in intvar_list_3:
        value.set(0)

    #additional_segment_atk.grid_forget(row=20, column=0)
    #additional_segment_check.grid_forget(row=14, column=1)
    #additional_segment_turn.grid_forget(row=7, column=2)

menubar = tk.Menu(root)

filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Hide Menus", command=hide_segments)
filemenu.add_command(label="Refresh Menus", command=reset_windows)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=exit_program)
menubar.add_cascade(label="File", menu=filemenu)

# Launch window with a little info about the program and I
def about():
    about_window = tk.Tk()
    about_window.geometry("425x350")
    about_window.config(bg="black")
    about_text = '''I created this window because the D&D 3.5 system  to rebuke undead is very tiresome, and preferred  to do it automatically instead. While I was at it,I decided to go ahead and add some extra          fuctionality to it, cause I got tired of rolling 9swim checks across 2 characters and pets. I wantedto learn more about python, and I wanted to make  something a little more user friendly outside the terminal, instead using tkinter to build a gui.   Hopefully I'll add more to it over time, as it's  been a fun hobby project. For now, it includes    attacks, although there's no way to set different attack bonuses, checks, and of course, it rebukes undead about 5 minutes faster than I can roll the dice and do the math.'''
    window_text = tk.Text(master=about_window, height = 16, width=50, bg="black", fg="white")
    window_text.grid(row=0, column=0)
    window_text.insert(tk.END, about_text)
    destroy_button = tk.Button(about_window, text="Close", command=about_window.destroy, bg="dark slate gray", fg="white")
    destroy_button.grid(row=1, column=0)
    about_window.mainloop()

# TDOO WRITE Launch window with information about how to operate the program

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=None)
helpmenu.add_command(label="About...", command=about)
menubar.add_cascade(label="Help", menu=helpmenu)
root.config(menu=menubar)
root.mainloop()
