#Roman Wambugu & Isaiah Hernandez
#November 29, 2023
#Quoridor Game - FINAL PROJECT
#----------------------------------------------------------------
import tkinter as tk
from PIL import Image, ImageTk
#----------------------------------------------------------------
#This function displays the first screen of the game
def start_screen():
  #Colors & Fonts
  background_color = "#4d2d18" 
  start_button_color = "#a36838"
  start_button_font = ("OpenSans", 35, "bold")

  #Quoridor Window
  global quoridor_win
  quoridor_win = tk.Tk()
  quoridor_win.attributes('-fullscreen', True)
  quoridor_win.config(bg=background_color)

  #Creating frame
  global start_frame
  start_frame = tk.Frame(quoridor_win, bg=background_color)
  start_frame.pack()

  #Creating image
  open_image = Image.open("Instructions.png")
  instruction_image = ImageTk.PhotoImage(open_image)

  #Creates the instruction label (image)
  instruction_label = tk.Label(start_frame, bg=background_color, image=instruction_image)
  instruction_label.grid(row=0, column=0)

  #Creating the start button
  start_button = tk.Button(start_frame, text="Start", width=8, height=2, bg=start_button_color, highlightbackground=background_color, font=start_button_font, command=lambda:main_screen())
  start_button.grid(row=1, column=0, pady=10)

  quoridor_win.mainloop()
#----------------------------------------------------------------
#This function displays the main screen of the game & Runs the entire gaameloop
def main_screen():
  start_frame.destroy()

  #Initial Values
  global last_row, last_col
  global first_click
  global placing_wall
  last_row, last_col = -1, -1
  first_click = True
  placing_wall = False

  #Wall Counts
  global player_wall_count
  global enemy_wall_count
  player_wall_count = 10
  enemy_wall_count = 10

  #Colors
  global background_color
  global board_color
  global highlighted_color
  global wall_color
  global player_color
  global enemy_color

  background_color = "#4d2d18"
  board_color = "#1e130a"
  highlighted_color = "#023701"
  wall_color = "#a36838"
  player_color = "brown"
  enemy_color = "#deaf84"

  #Fonts
  global button_font
  global player_font
  global place_wall_font
  button_font = ("OpenSans", 18, "bold")
  player_font = ("OpenSans", 60, "bold")
  place_wall_font = ("OpenSans", 40, "bold")

  #Player values 
  global player_num
  global enemy_num
  player_num = "1"
  enemy_num = "2"

  #Frames/Grids
  global quoridor_frame
  quoridor_frame = tk.Frame(quoridor_win, bg=background_color)
  quoridor_frame.pack()

  label_frame = tk.Frame(quoridor_frame, bg=background_color)
  label_frame.pack()

  board_frame = tk.Frame(quoridor_frame, bg=background_color)
  board_frame.pack()

  button_frame = tk.Frame(quoridor_frame, bg=background_color)
  button_frame.pack()

  #Creates player turn label
  global player_label
  player_label = tk.Label(label_frame, bg=background_color, text=f"Player {player_num}'s Turn", font=player_font)
  player_label.pack(pady=12)

  #Creates Place Button
  global place_wall_button
  place_wall_button = tk.Button(button_frame, text=f"Place Wall ({player_wall_count})", font=place_wall_font, width=18, height=2, bg=wall_color, highlightbackground=background_color, command=lambda:place_wall_click())
  place_wall_button.grid(row=0, column=0, pady=20)

  #Creates 9x9 Board
  board = create_board(board_frame, 9, 9)
#----------------------------------------------------------------
#This function creates a 2D-list of buttons & assigns Player 1 & 2 locations
def create_board(frame, width, height):
  global board
  board = []
  for row in range(width):
    button_row = []
    for col in range(height):
      button = tk.Button(frame, text="", font=button_font, width=4, height=2, bg=board_color, highlightbackground=background_color)
      button.grid(row=row, column=col)
      button_row.append(button)
    board.append(button_row)
  board[8][4].config(text=player_num, font=button_font, bg=player_color, command=lambda r=8, c=4: move_player(r, c))
  board[0][4].config(text=enemy_num, font=button_font, bg=enemy_color, command=lambda r=0, c=4: move_player(r, c))
#----------------------------------------------------------------
#this function unbinds the entire board or only the non-highlighted buttons
def unbind(modification):
  for row in board:
    for button in row:
      #Unbinds the entire board
      if modification == "board":
        button.unbind("<Button-1>")

      #Unbinds every non-highlighted button
      if modification == "non_highlighted" and button.cget("bg") != highlighted_color:
        button.unbind("<Button-1>")
#----------------------------------------------------------------
#This function either changes button functions or button colors
def modify_board(modification):
  for row_idx, row in enumerate(board):
    for col_idx, button in enumerate(row):

      #Changes the function for every blank space
      if button.cget("text") == "":
        if modification == "move_player_function":
          button.bind("<Button-1>", lambda event, r=row_idx, c=col_idx: move_player(r, c))
        elif modification == "place_wall_function":
          button.bind("<Button-1>", lambda event, r=row_idx, c=col_idx: place_wall(r, c))

      #Changes the color of the highlighted (green) space  
      if modification == "remove_highlight":
        button.config(highlightbackground=background_color)
        if button.cget("bg") == highlighted_color:
          button.config(bg=board_color)

      #Changes the wall color from a dark shade to a lighter shade
      if modification == "change_wall_color" and button.cget("text") == "━" and button.cget("bg") == "#85552d":
          button.config(bg=wall_color)
#----------------------------------------------------------------
#This function is the movement function that is binded to the current player and every empty space & allows text and color swaps
def move_player(row, col):
  global last_row, last_col
  global first_click
  global placing_wall

  #This if statement runs after the player has clicked their own button.
  if board[row][col].cget("text") == player_num and first_click and not placing_wall:
    if player_wall_count <= 0:
      place_wall_button.config(text="Wall (0)", bg=wall_color)
    else:
      place_wall_button.config(text=f"Place Wall ({player_wall_count})", bg=wall_color)

    last_row, last_col = row, col
    highlight_adjacent_buttons(last_row, last_col)
    player_label.config(text="Moving...")
    first_click = False
    unbind("board")
    modify_board("move_player_function") 

  #This else statments runs after the player has clicked a green adjacent location.
  else:
    if board[row][col].cget("bg") == highlighted_color and board[row][col].cget("text") == "":

      #Swap the texts of the two buttons
      text_first = board[last_row][last_col].cget("text")
      text_second = board[row][col].cget("text")

      #Swap the colors of the two buttons
      first_color = board[last_row][last_col].cget("bg")
      second_color = board[row][col].cget("bg")

      #Configures buttons with swapped values
      board[last_row][last_col].config(text=text_second, bg=second_color)
      board[row][col].config(text=text_first, bg=first_color)
      modify_board("remove_highlight")

      #Checks if the movement resulted in a win, otherwise switch players
      if check_win(col):
        pass
      else:
        next_player()
    first_click = True
#----------------------------------------------------------------
#This function highlights adjacent location that the player can move to, or place a wall. The function also includes a jummp player ferature.
def highlight_adjacent_buttons(row, col):
  adjacent_positions = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
  for r, c in adjacent_positions:
    #checks if adjacent buttons are on the board
    if  0 <= r < 9 and 0 <= c < 9:
      #if the adjacent button is blank, it becomes highlighted and clickable
      if board[r][c].cget("text") == "":
        board[r][c].config(bg=highlighted_color, highlightbackground=highlighted_color, command=lambda r=r, c=c: move_player(r, c))
      #if the adjacent button is the enemy player, the next row or column over becomes highlighted and clickable
      elif board[r][c].cget("text") == enemy_num: 
        #Doubling the adjacent row/col and then subtracting the player row/cols returns a difference of 2 in location, instead of 1
        next_r = 2 * r - row
        next_c = 2 * c - col
        #checks if the next row or column over is on the board & if the button is blank
        if 0 <= next_r < 9 and 0 <= next_c < 9 and board[next_r][next_c].cget("text") == "":
          board[next_r][next_c].config(bg=highlighted_color, highlightbackground=highlighted_color, command=lambda r=next_r, c=next_c: move_player(r, c))
#----------------------------------------------------------------
#This function runs only when the place_wall_button is clicked. It binds the entire board's empty space with the place_wall function down below.
def place_wall_click():
  global first_click

  #Button does nothing if the player has no walls left
  if player_wall_count <= 0:
    pass
  else:
    if not placing_wall:
      #Allows for the player to switch from moving to placing a wall
      modify_board("remove_highlight")
      first_click = True
      player_label.config(text=f"Player {player_num}'s Turn")
      place_wall_button.config(text="Placing...", bg="#85552d")

      #Switches every empty space to the place_wall function
      unbind("board")
      modify_board("place_wall_function")
#----------------------------------------------------------------
#This function runs when an empty space is clicked after the place_wall button has been clicked. It changes the text and color of two buttons to indicate wall placement.
def place_wall(row, col):
  global player_wall_count
  global placing_wall

  #Runs the player's second half of the wall
  if board[row][col].cget("bg") == highlighted_color and board[row][col].cget("text") == "":
    board[row][col].config(text="━", bg="#85552d")
    player_wall_count -= 1
    placing_wall = False
    modify_board("remove_highlight")
    unbind("board")
    modify_board("change_wall_color")
    next_player()

  #Runs the player's first half of the wall
  elif board[row][col].cget("text") == "" and first_click:
    board[row][col].config(text="━", bg="#85552d") 
    placing_wall = True
    highlight_adjacent_buttons(row, col)
    unbind("non_highlighted")
#----------------------------------------------------------------
#This swaps the global values and texts on the window to simulate a player turn.
def next_player():
  global player_num, enemy_num
  global player_color, enemy_color
  global player_wall_count, enemy_wall_count
  global first_click

  #Switches the enmeny and player wall counts
  temp = player_wall_count
  player_wall_count = enemy_wall_count
  enemy_wall_count = temp

  #Switches the enmeny and player number (1 & 2)
  temp = player_num
  player_num = enemy_num
  enemy_num =  temp

  #Switches the enmeny and player color
  temp = player_color
  player_color = enemy_color
  enemy_color = temp

  #Resets any changes made from the previous turn
  first_click = True
  modify_board("remove_highlight")
  player_label.config(text=f"Player {player_num}'s Turn")
  if player_wall_count <= 0:
    place_wall_button.config(text="Wall (0)", bg=wall_color)
  else:
    place_wall_button.config(text=f"Place Wall ({player_wall_count})", bg=wall_color)

  #Binds every blank space back to the move_player function
  unbind("board")
  modify_board("move_player_function")
#----------------------------------------------------------------
#This function checks wether either player has reached the other end of the baord.
def check_win(col):
  for col in range(len(board[0])):
    #Changes the screen if player 1 reaches row 0
    if board[0][col].cget("text") == "1":
      winner = "Player 1 wins!"
      win_screen(winner)
      return True
    #Changes the screen if player 2 reaches row 8
    elif board[8][col].cget("text") == "2":
      winner = "Player 2 wins!"
      win_screen(winner)
      return True
  return False
#----------------------------------------------------------------
#This function changes the screen for when a player has won.
def win_screen(winner):
  quoridor_frame.destroy()

  #Colors & Fonts
  background_color = "#4d2d18"
  text_color = "black"
  win_font = ("OpenSans", 75, "bold")

  #Creating Image
  global winner_gif_image
  open_image = Image.open("Winner.png")
  winner_gif_image = ImageTk.PhotoImage(open_image)

  #Creating Frame for Image
  global winner_frame
  winner_frame = tk.Frame(quoridor_win)
  winner_frame.config(bg=background_color)
  winner_frame.pack()

  #Label for the Winner
  winner_label = tk.Label(winner_frame, bg=background_color, fg=text_color, text=winner, font=win_font)
  winner_label.grid(row=0, column=0)

  #Label for the Image
  winner_gif = tk.Label(winner_frame, bg=background_color, image=winner_gif_image)
  winner_gif.grid(row=1, column=0, pady=30)
#----------------------------------------------------------------
#Starts the game off
start_screen()