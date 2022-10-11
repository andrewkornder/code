import tkinter
from os import system
from webbrowser import register, get, BackgroundBrowser

#TODO: file system, binds, display


class Button:
	def __init__(self, window, index, item, color, image):
		self.x, self.y, self.x1, self.y1 = self.from_index(window, index)
		(self.text, self.item), self.image = item, image
	
		self.button_ui = window.canvas.create_rectangle(*self.coords, fill=color)
		text_x = self.x1 + window.border + len(self.text) * window.font_size // 2
		self.text_ui = window.canvas.create_text(text_x, (self.y + self.y1) / 2, text=self.text, font=(window.font, window.font_size))
		
		# self.image_ui = window.canvas.create_image()

	@property
	def coords(self): return self.x, self.y, self.x1, self.y1
	
	@staticmethod
	def from_index(window, index):
		x = window.edge_dist + window.border
		y = (window.border + window.button_height) * index + window.border + window.edge_dist

		x1, y1 = x + window.button_width, y + window.button_height
		return x, y, x1, y1
	
	def check_clicked(self, x, y): return (self.x <= x <= self.x1) and (self.y <= y <= self.y1)


class Mouse:
	def __init__(self, window):
		self.window = window
		self.holding = None
		
		self.window.root.bind('<Button-1>', self.click)
		self.window.root.bind('<Motion>', self.drag)
	
	def click(self, event):
		self.holding = self.get_item(event.x, event.y)
		if self.holding is None:
			return

		if self.window.in_edit_mode:
			pass  # TODO: drag n drop needs set up
			return
		self.window.open(self.holding.item)
		self.holding = None
	
	def drag(self, event):
		pass

	def get_item(self, x, y):
		for button in self.window.buttons: 
			if button.check_clicked(x, y): return button


class Home:
	binds = [
		
	]
	
	settings = ['width', 'height', 'border', 'max_button_w', 'max_button_h', 'font', 'font_size', 'browser']

	def __init__(self):
		self.items, settings = self.read('./settings.txt')
		self.__dict__.update({k: int(v) if k not in ('font', 'browser') else v for k, v in settings.items()})
		self.edge_dist = 50  # how far the buttons are from the edge, not including border around buttons

		# setting up browser for opening links using library 'webbrowser'
		register(self.browser, None, BackgroundBrowser(self.browser))
		self.browser = get(self.browser)

		self.root, self.canvas = self.get_window(self.width, self.height, self.binds)
		self.buttons = []
		self.button_width, self.button_height = self.get_button_dim()
		for item in self.items.items(): self.create_button(item)		

		self.mouse = Mouse(self)
		self.in_edit_mode = False  # TODO: set up menu at top or bottom for edit mode (drag and drop buttons), color change, etc.

	def read(self, file):
		items_file, settings = open(file).read().split('\n')[:2]
		settings = dict(zip(self.settings, settings.split(',')))	

		links = dict(a.split(' => ') for a in open(items_file).read().split('\n'))
		
		return links, settings

	@staticmethod
	def get_window(w, h, binds):
		root = tkinter.Tk()
		root.geometry(f'{w}x{h + 80}')  # adding 80 to height to add a menu at the top or bottom, (probably bottom since then calculating the loc of a button is easier

		canvas = tkinter.Canvas(root, width=w, height=h + 80, bg='black')
		canvas.pack()

		for item, seq, func in binds: (root if item == 'root' else canvas).bind(f'<{seq}>', func)
	
		return root, canvas

	def get_button_dim(self):
		items = len(self.items)

		w = self.width - self.border
		h = self.height - self.border

		w, h =  w / items - self.border, h / items - self.border
		return min(w, self.max_button_w), min(h, self.max_button_h) 

	# TODO: get images, save in folder, add way to add/change them		
	def create_button(self, item, image=None, color='red'):  self.buttons.append(Button(self, len(self.buttons), item, color, image))

	def open(self, item): system(f'"{item}"') if item[:8] != 'https://' else self.browser.open_new(item)

	def run(self): self.root.mainloop()

if __name__ == '__main__':
	Home().run()



