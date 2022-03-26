from xml.dom.minidom import Element
import numpy as np
from time import sleep
from tkinter import Canvas, Tk, Frame, Button, LEFT, BOTTOM, NORMAL
#from GameLogic.Board.board import generateBoard, readFromFile
from board import generateBoard, readFromFile
from GameLogic.game import Play
from simulation.board import saveToFile
import json

board_size = 600

#[game_settings]
birth_rate = 3
death_rate = 3
game_rounds = 50
change_of_surviving = 0.70
game_speed = 0.75

class MainWindow(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title('Simulation')

        frame = Frame(self.master)
        frame.pack()

        self.canvas = Canvas(frame,  height=board_size,  width=board_size)
        self.canvas.pack(side=BOTTOM)

        window_width = 700
        window_height = 700
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.master.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.btn_start = Button(
            frame,
            text="Igraj", 
            state = NORMAL, 
            command = self.generateMap
        )
        self.btn_start.pack(side=LEFT)

        self.play_game()

        
    def play_game(self):
        #self.game_board = self.generateMap()
        #saveToFile(self.game_board
        #self.AddNewElement(self, 70, "grass", "#007700", "rectangle", True, {"TryToMoveParticleDown" : True})
        element_data = self.LoadJsonFile()
        game_board = readFromFile()

        for i in range(game_rounds):
            print(i)
            self.canvas.delete("all")
            self.draw(self.canvas, game_board, element_data)
            game_board = Play(game_board)
            self.update()
            sleep(game_speed)

    def generateMap(self):
        cave_board = generateBoard(change_of_surviving)
        #self.cave_board = self.generateMap(self.game_board)
        for i in range(game_rounds):
            cave_board = self.nextGeneration(cave_board)

            self.canvas.delete("all")
            self.draw(self.canvas, cave_board)
            self.update()
            sleep(game_speed)

        return cave_board

    def nextGeneration(self, map):
        temp_map = np.zeros(map.shape)

        for x, y in np.ndindex(temp_map.shape):
            number_of_neighbors = np.sum(map[x-1:x+2, y-1:y+2]) - map[x, y]

            if map[x, y] == 1 and number_of_neighbors > death_rate:
                temp_map[x, y] = 0
            if map[x, y] == 0 and number_of_neighbors < birth_rate:
                temp_map[x, y] = 1
        
        return temp_map

    def draw(self, canvas, board, element_data_json):
        game_board = board
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
                            canvas.create_rectangle(x, y, x + t_size, y + t_size, fill=element['hexCode'], outline=element['hexCode'])
                        elif (element['shape'] == 'oval' ):
                            canvas.create_oval(x, y, x + t_size, y + t_size, fill=element['hexCode'], outline=element['hexCode'])
                
    def LoadJsonFile(self):
        with open('elementsConfig.json') as f:
            data = json.load(f)
            return data
    
    def AddNewElement(self, value, name, hexCode, shape, movable, selected_behaviours : list[str, bool]):
                
        behaviours = {}
        for behaviour in selected_behaviours:
            behaviours.append(behaviour)
        
        temp_element = { 
                "value" : value,
                "name" : name,
                "hexCode" : hexCode,
                "shape" : shape,
                "movable" : movable,
                "behaviour" : behaviours
            }

        json_data = list(self.LoadJsonFile())
        json_data.append(temp_element)
        json.dump(json_data, "elementsConfig.json")
        

def main(): 
    root = Tk()
    app = MainWindow(root)
    app.mainloop()

if __name__ == '__main__':
    main()