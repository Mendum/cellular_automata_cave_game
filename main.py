from enum import Flag
from GameLogic.Element.element import IsAir, IsRock
import numpy as np
from time import sleep
from tkinter import E, Canvas, Checkbutton, Entry, IntVar, Label, OptionMenu, StringVar, Tk, Frame, Button, NORMAL, messagebox
from board import generateBoard, readFromFile
from GameLogic.game import Play
from simulation.board import Boards, GenerateFlowDirectionBoard, GenerateTempBoard, saveToFile
import json

from simulation.gameData import Cave, GameData

board_size = 600

class MainWindow(Frame):
    array_entrys = []
    array_chk_btns = []

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title('Simulation')

        self.cave_settings = self.SetCaveData()
        self.game_setting = self.SetGameData()

        top_frame = Frame(self.master, height = 150, width = 700 , bg = '')
        top_frame.grid(row=0, column=0, sticky="nw")

        frame = Frame(self.master, height = 600, width = 700, bg = '#3E4149')
        frame.grid(row=1, column=0, sticky="w")

        right_frame = Frame(self.master, height = 600,width = 280, bg = '#3E4149')
        right_frame.grid(row=1, column=1, sticky="e")

        bottom_frame = Frame(self.master, height = 150, width = 700 , bg = '')
        bottom_frame.grid(row=2, column=0, sticky="s")

        self.cursor_position_label = Label(bottom_frame, text='')
        self.cursor_position_label.grid(row=0, column=0, sticky="")

        self.canvas = Canvas(frame,  height=board_size,  width=board_size)
        self.canvas.bind("<Button-1>", self.callback)
        self.canvas.bind('<Motion>', self.motion)
        self.canvas.grid(row=0, column=0, sticky="")

        window_width = 1050
        window_height = 700
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.master.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.btn_start = Button(
            top_frame,
            text="Play", 
            state = NORMAL, 
            command = self.PlayGame
        )
        self.btn_start.grid(row=0, column=0, sticky="")

        self.options = self.GetElementOptions()
        print(self.options)
        self.drop_menu_selected = StringVar()
        self.drop_menu_selected.set("Elementi")
        self.drop_menu = OptionMenu(top_frame, self.drop_menu_selected, *self.options)
        self.drop_menu.grid(row=0, column=1, sticky="")

        self.btn_add_new_element = Button(
            right_frame,
            text="Add new element", 
            state = NORMAL, 
            command = self.AddNewElement
        )
        self.btn_add_new_element.grid(row=6, column=1, sticky="")

        self.element_atrb = {
            'Value' : 70, 
            'Name' : 'snow', 
            'HexCode' : '#ffffff',  
            'HexOutline' : '#ffffff', 
            'Shape' : 'oval',  
            'Movable' : 'true'
        }
        
        self.var1 = IntVar()
        self.var2 = IntVar()
        self.var3 = IntVar()
        self.var4 = IntVar()
        self.var5 = IntVar()
        self.var6 = IntVar()

        self.element_func = {
            'TryToMoveParticleDown' : self.var1,
            'TryToMoveParticleDiagonal' : self.var2,
            'TryToDisplacesWater' : self.var3,
            'TryToDisplacesWood' : self.var4,
            'TryToSpillWaterIntoAir' : self.var5,
            'TryToSpillWaterIntoWater' : self.var6,
        }

        i = 0
        for key, value in self.element_atrb.items():
            self.lb = Label(right_frame, text = key, bg = '#3E4149', fg = '#000000', font=12)
            self.lb.grid(row=i, column=0, sticky="w")
            
            self.input = Entry(right_frame, width=15)
            self.array_entrys.append(self.input)
            self.input.insert(0, value)
            self.input.grid(row=i, column=1, sticky="w")
            i = i + 1

        ii  = 0
        for key, value in self.element_func.items():
            self.check_btn = Checkbutton(right_frame, text = key, variable = value, onvalue = 1, offvalue = 0)
            self.array_chk_btns.append(self.check_btn)
            self.check_btn.grid(row=ii, column=2, sticky="w")
            ii = ii + 1

        self.btn_generate_cave = Button(
            frame,
            text="Generate new cave", 
            state = NORMAL, 
            command = self.GenerateCave
        )
        #self.btn_generate_cave.pack(side=RIGHT)

        self.draw(self.canvas, self.game_setting.boards, self.game_setting.elements)
        self.cursor_positon = self.canvas.create_rectangle(110, 110, 220, 220, fill='', outline='#ff0000')
        self.update()

    def callback(self, event):
        element_value = self.DrawSelectedElement()
        element_hex_code = self.GetElementHexCode(element_value)
        element_hex_outtline = self.GetElementHexOutline(element_value)
        col_width = self.canvas.winfo_width()
        row_height = self.canvas.winfo_height()
        array_x = int( (event.x % col_width) / 6 )
        array_y = int( (event.y % row_height) / 6 )
        col = int(array_y * 6)
        row = int(array_x * 6)
        t_size = 6.0
        if not IsRock(self.game_setting.boards.old_board[array_y, array_x]):
            self.game_setting.boards.old_board[array_y, array_x] = element_value
            self.canvas.create_rectangle(row, col, row + t_size, col + t_size, fill=element_hex_code, outline=element_hex_outtline)
        else:
            messagebox.showinfo('callback', 'Sorry you cant \n draw over rocks.')

    def motion(self, event):
        col_width = self.canvas.winfo_width()
        row_height = self.canvas.winfo_height()
        array_x = int( (event.x % col_width) / 6 )
        array_y = int( (event.y % row_height) / 6 )
        self.canvas.coords(self.cursor_positon, (array_x * 6), (array_y * 6), (array_x * 6) + 6, (array_y * 6) + 6)
        self.cursor_position_label.config(text=f'Mouse Cursor Position -> x: {array_x}, y: {array_y}')
        
    def PlayGame(self):
        #self.game_board = self.GenerateMap()
        #saveToFile(self.game_board
        #self.AddNewElement(70, "grass", "#00ff00", "rectangle", True, {"TryToMoveParticleDown" : True, "TryToDisplacesWater" : True})

        for i in range(self.game_setting.game_rounds):
            print(f' turn:  {i} ')
            self.game_setting.boards = Play(self.game_setting.boards)
            self.canvas.delete("all")
            self.draw(self.canvas, self.game_setting.boards, self.game_setting.elements)
            self.update()
            sleep(self.game_setting.game_speed)
    
    def SetGameData(self) -> GameData:
        game_rounds = 10
        game_speed = 1
        element_data = self.LoadJsonFile()
        game_board = readFromFile()
        flow_direction_board = GenerateTempBoard()
        boards = Boards(game_board, flow_direction_board)

        return GameData(
            game_rounds,
            game_speed,
            element_data,
            boards
        )

    def SetCaveData(self) -> Cave:
        return Cave(
            birth_rate = 3,
            death_rate = 3,
            change_of_surviving = 0.70
        )

    def GenerateCave(self):
        cave_board = generateBoard(self.cave_settings.change_of_surviving)
        #self.cave_board = self.generateMap(self.game_board)
        for i in range(self.game_setting.game_rounds):
            cave_board = self.NextGeneration(cave_board)
            self.canvas.delete("all")
            self.draw(self.canvas, cave_board)
            self.update()
            sleep(self.game_setting.game_speed)

        return cave_board

    def NextGeneration(self, map):
        temp_map = np.zeros(map.shape)

        for x, y in np.ndindex(temp_map.shape):
            number_of_neighbors = np.sum(map[x-1:x+2, y-1:y+2]) - map[x, y]

            if map[x, y] == 1 and number_of_neighbors > self.cave_settings.death_rate:
                temp_map[x, y] = 0
            if map[x, y] == 0 and number_of_neighbors < self.cave_settings.birth_rate:
                temp_map[x, y] = 1
        
        return temp_map

    def draw(self, canvas, boards: Boards, element_data_json):
        game_board = boards.old_board
        t_size = board_size/len(game_board)
        element_data = element_data_json

        for i in range(len(game_board)):
            for j in range(len(game_board[i])):
                curr_element = game_board[j][i]
                x = i * t_size
                y = j * t_size

                for element in element_data:
                    if curr_element == element['value']:
                        if(element['shape'] == 'rectangle' ):
                            canvas.create_rectangle(x, y, x + t_size, y + t_size, fill=element['hexCode'], outline=element['hexOutline'])
                        elif (element['shape'] == 'oval' ):
                            canvas.create_oval(x, y, x + t_size, y + t_size, fill=element['hexCode'], outline=element['hexOutline'])
    
    def GetElementHexCode(self, element_value):
        json_data = self.LoadJsonFile()

        for data in json_data:
            if data['value'] == element_value:
                return data['hexCode']

    def GetElementHexOutline(self, element_value):
        json_data = self.LoadJsonFile()

        for data in json_data:
            if data['value'] == element_value:
                return data['hexOutline']
    
    def GetElementValue(self, element_name):
        json_data = self.LoadJsonFile()

        for data in json_data:
            if data['name'] == element_name:
                return data['value']

    def DrawSelectedElement(self):
        try:
            element_value = self.GetElementValue(self.drop_menu_selected.get())
            return element_value
        except ValueError:
            messagebox.showinfo('DrawSelectedElement', 'Please select an element \n you would like to draw.')
                
    def LoadJsonFile(self):
        with open('elementsConfig.json') as f:
            data = json.load(f)
            return data

    def GetElementOptions(self):
        data_list = []
        json_data = self.LoadJsonFile()

        for data in json_data:
            data_list.append(data['name'])

        return data_list
    
    def AddNewElement(self):
        
        try:
            value = int(self.array_entrys[0].get())
            name = self.array_entrys[1].get()
            hexCode = self.array_entrys[2].get()
            hexOutline = self.array_entrys[3].get()
            shape = self.array_entrys[4].get()
            # TODO: error, value is always set on True
            movable = bool(self.array_entrys[5].get())

            new_behaviours: dict[str, bool] = {}

            for key, val in self.element_func.items():
                if val.get() == 1:
                    new_behaviours[key] = True
            
            temp_element = { 
                    "value" : value,
                    "name" : name,
                    "hexCode" : hexCode,
                    "hexOutline" : hexOutline,
                    "shape" : shape,
                    "movable" : movable,
                    "behaviours" : new_behaviours
                }

            json_data = list(self.LoadJsonFile())
            elemet_not_exists = True
            for data in json_data:
                if data['name'] == temp_element['name'] or data['value'] == temp_element['value']:
                    elemet_not_exists = False
                    messagebox.showinfo('AddNewElement', 'Element with this \n value or name alredy exsits.')
                else:
                    print('ne obstaja')

            print(elemet_not_exists)
            if elemet_not_exists:
                json_data.append(temp_element)
                with open ('elementsConfig.json', 'w') as f:
                    json.dump(json_data, f, indent=4)

                    messagebox.showinfo('AddNewElement', 'Element ' + temp_element['name'] + ' added')
        
        except ValueError:
            messagebox.showinfo("AddNewElement", "Napaka pri  \n dodajanu elementa")

def main(): 
    root = Tk()
    app = MainWindow(root)
    app.mainloop()

if __name__ == '__main__':
    main()