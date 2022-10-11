from random import shuffle


class Grid:
    def __init__(self, canvas, width, height, square_colors=('grey', 'light grey'), 
                 window_size=(1000, 1000), display_type='text', 
                 pieces=('', 'x', 'o'), text_color='black'):
        self.passive, self.active = square_colors
        self.blank, self.pieces = pieces[0], pieces[1:]
        self.text_color = text_color
        self.array = [[Square(self.blank) for col in range(width)] for row in range(height)]
        self.size = width, height
        self.display = self.display_text if display_type == 'text' else self.display_image
        
        self.scaleX, self.scaleY = window_size[0] / width, window_size[1] / width
        self.canvas = canvas
        
    def display_text(self):
        self.canvas.delete('all')
        for i, row in enumerate(self.array):
            for j, square in enumerate(row):
                x, y = j * self.scaleY, i * self.scaleX
                x1, y1 = x + self.scaleX, y + self.scaleY                
                self.canvas.create_rectangle(x, y, x1, y1, fill=self.passive,
                                             activefill=self.active)
                self.canvas.create_text(x + self.scaleX / 2, y + self.scaleY / 2,
                                        text=square.value, fill=self.text_color, font=('Niagara Bold', 20))
    
    def display_image(self):
        self.canvas.delete('all')
        for i, row in enumerate(self.array):
            for j, square in enumerate(row):
                x, y = j * self.scaleY, i * self.scaleX
                x1, y1 = x + self.scaleX, y + self.scaleY
                self.canvas.create_rectangle(x, y, x1, y1, fill=self.passive, 
                                             activefill=self.active)
                self.canvas.create_image(x + self.scaleX / 2, y + self.scaleY / 2,
                                         image=square.value)
    
    def move(self, origin, destination):
        destination.value = origin.value
        origin.value = self.blank
    
    @staticmethod
    def swap(origin, destination):
        temp = destination.value
        destination.value = origin.value
        origin.value = temp

    def random_board(self):
        for row in self.array:
            shuffle(row)

    def assign(self, row, col, piece):
        self.array[row][col].value = piece
        

class Square:
    def __init__(self, value):
        self.value = value
