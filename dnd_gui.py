import tkinter as tk
import random as rn
import sys
import os

window = tk.Tk()

def roll_checks(rolls, bonus):
  roll_list = [rn.randint(1,20) for i in range(0, rolls)]
  return_list = []

  for i in roll_list:
    if i == 1:
      return_list.append('Critical Fail!')
    elif i == 20:
      return_list.append('Critical Succes!')
    else:
      return_list.append(i + bonus)

  textArea = tk.Text(master=window,height=2,width=30)
  textArea.grid(column=1,row=4)
  output = return_list
  textArea.insert(tk.END, output)

def roll_attacks(rolls, bonus, ac, dmg, crit, mod):
    
    rolls_int = int(rolls)
    bonus_int = int(bonus)
    ac_int = int(ac)
    dmg_int = int(dmg)
    crit_int = int(crit)
    mod_int = int(mod)

    roll_list = [rn.randint(1,20) for i in range(0, rolls_int)]

    attack_list = []

    for i in roll_list:
      if i == 1:
        attack_list.append('Critical Fail!')
      elif i >= crit:
        attack_list.append('Critical Success!')
      elif (i + bonus_int) > ac_int:
        attack_list.append('Hit')
      else:
        attack_list.append('Miss')
  
    damage_list = []
  
    for i in attack_list:
      if i == 'Critical Success!':
        damage_list.append(2 * (mod_int + (rn.randint(3, dmg_int))))
      elif i == 'Hit':
        damage_list.append(mod_int + (rn.randint(1, dmg_int)))
      else:
        damage_list.append(0)

      return_list = zip(attack_list, damage_list)
      output = list(return_list)
      print('working maybe')
      textArea = tk.Text(master=window,height=3,width=30)
      textArea.grid(column=1,row=1)
      textArea.insert(tk.END, output)

  
#def get_atk_inputs():
  #ouput = roll_attacks(int(attacks_entry.get()), int(bonus_entry_atk.get()), int(ac_entry.get()), int(dmg_entry.get()), int(crit_entry.get()), int(mod_entry.get()))
  #textArea = tk.Text(master=window,height=3,width=30)
  #textArea.grid(column=1,row=1)
  #textArea.insert(tk.END, output)

def turn_check(levelCleric, cha):
  D20 = rn.randint(1,20) + cha + 2
  D6a = rn.randint(1,6)
  D6b = rn.randint(1,6)
  turnCount = D6a + D6b + cha
  turnTotal = None

  if turnCount <= 0 :
        turnTotal = levelCleric - 4
  elif 3 >= turnCount > 0 :
        turnTotal = levelCleric - 3
  elif 6 >= turnCount > 3 :
        turnTotal = levelCleric - 2
  elif 9 >= turnCount > 6 :
        turnTotal = levelCleric - 1
  elif 12 >= turnCount > 9 :
        turnTotal = levelCleric
  elif 15 >= turnCount > 12 :
        turnTotal = levelCleric + 1
  elif 18 >= turnCount > 15 :
        turnTotal = levelCleric + 2
  elif 21 >= turnCount > 18 :
        turnTotal = levelCleric + 3
  elif turnCount > 21 :
        turnTotal = levelCleric + 4
  
  return '''You can turn {turnTotal} total hit die of undead, with a 
maximum undead hit die of {D20}.
D6 Roll total: {turnCount}
D20 Roll total: {D20}'''

def spell_check():
  pass

def char_create(hitdie):
  def gen_list():
    rand_list = [rn.randint(3,6) for i in range(1, 4)]
    return rand_list

  stat_list = [sum(gen_list()) for i in range(1, 7)]
  hitpoints = rn.randint(3, hitdie)

  return stat_list, hitpoints

class check_window:
  def __init__(self):
    window = tk.Tk()
    window.geometry('600x350')
    window.title(' Skill Check ')
    checks_label = tk.Label(text = 'Number of Checks: ')
    checks_label.grid(column=0, row=0)
    checks_intvar = tk.IntVar()
    checks_entry = tk.Entry(window)
    checks_entry.grid(column=1, row=0)
    bonus_label_chk = tk.Label(text = 'Skill Bonus: ')
    bonus_label_chk.grid(column=0, row=1)

    bonus_entry_chk = tk.Entry(window)
    bonus_entry_chk.grid(column=1, row=1)
    enter_btn_chk = tk.Button(window, text='Roll Checks', command=roll_checks(int(checks_entry.get()), int(bonus_entry_chk.get())))
    enter_btn_chk.grid(column=1, row=2)
    window.mainloop()

def check_launcher():
  window.destroy()
  launcher = check_window()
  return launcher

class attack_window:
  def __init__(self):
    window.geometry('600x350')
    window.title(' Attack Rolls ')
    attacks_label = tk.Label(window, text = 'Number of Attacks: ')
    attacks_label.grid(column=0, row=0)
    attacks_entry = tk.Entry(window)
    attacks_entry.grid(column=0, row=1)
    ac_label = tk.Label(window, text='Enemy AC: ')
    ac_label.grid(column=0, row=2)
    ac_entry = tk.Entry(window)
    ac_entry.grid(column=0, row=3)
    bonus_label_atk = tk.Label(window, text = 'Hit Bonus: ')
    bonus_label_atk.grid(column=0, row=4)
    bonus_entry_atk = tk.Entry(window)
    bonus_entry_atk.grid(column=0, row=5)
    dmg_label = tk.Label(window, text='Damage Die: ')
    dmg_label.grid(column=0, row=6)
    dmg_entry = tk.Entry(window)
    dmg_entry.grid(column=0, row=7)
    crit_label = tk.Label(window, text='Lower Crit Range: ')
    crit_label.grid(column=0, row=8)
    crit_entry = tk.Entry(window)
    crit_entry.grid(column=0, row=9)
    mod_label = tk.Label(window, text='Damage Mod: ')
    mod_label.grid(column=0, row=10)
    mod_entry = tk.Entry(window)
    mod_entry.grid(column=0, row=11)
    enter_btn_atk = tk.Button(window, text='Roll Attacks', command=roll_attacks((attacks_entry.get()), (bonus_entry_atk.get()), (ac_entry.get()), (dmg_entry.get()), (crit_entry.get()), (mod_entry.get())))    
    enter_btn_atk.grid(column=1, row=0)
    window.mainloop()

def attack_launcher():
  window.destroy()
  launcher = attack_window()
  return launcher

class turn_window:
  pass

def turn_launcher():
  window.destroy()
  launcher = turn_window()
  return launcher

class spell_window:
  pass

def spell_launcher():
  window.destroy()
  launcher = spell_window()
  return launcher

class char_create_window:
  pass

def create_launcher():
  window.destroy()
  launcher = char_create_window()
  return launcher

class main_window:
  def __init__(self):
    window.geometry('600x350')
    window.title("Welcome! Push a button below to start pushing buttons!")
    check_btn = tk.Button(window, text='Skill Check', command = check_launcher)
    check_btn.grid(column=0,row=0)
    attack_btn = tk.Button(window, text = "Attack", command = attack_launcher)
    attack_btn.grid(column=1,row=0)
    turn_btn = tk.Button(window, text='Undead Turning', command = turn_launcher)
    turn_btn.grid(column=2, row=0)
    spell_btn = tk.Button(window, text='Spells', command = spell_launcher)
    spell_btn.grid(column=0, row=2)
    char_create_btn = tk.Button(window, text= 'New Character', command = create_launcher)
    char_create_btn.grid(column=1, row=2)
    restart_btn = tk.Button(window, text='Refresh')
    restart_btn.grid(column=2, row=2)
    window.mainloop()

test = attack_window()
test