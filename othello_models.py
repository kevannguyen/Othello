#  Kevan Hong-Nhan Nguyen 71632979.  ICS 32 Lab sec 9.  Project #5.

import othello
import tkinter


# GUI / tkinter object constants
BACKGROUND_COLOR = '#696969'
GAME_COLOR = '#006000'
FONT = ('Helvetica', 30)
DIALOG_FONT = ('Helvetica', 20)
PLAYERS = {othello.BLACK: 'Black', othello.WHITE: 'White'}
VICTORY_TYPES = {othello.MOST_CELLS: 'Most Cells', othello.LEAST_CELLS: 'Least Cells'}

class GameBoard:
    def __init__(self, game_state: othello.OthelloGame, game_width: float,
                 game_height: float, root_window) -> None:
        # Initialize the game board's settings here
        self._game_state = game_state
        self._rows = self._game_state.get_rows()
        self._cols = self._game_state.get_columns()
        self._board = tkinter.Canvas(master = root_window,
                                     width = game_width,
                                     height = game_height,
                                     background = GAME_COLOR)

    def new_game_settings(self, game_state) -> None:
        ''' The game board's new game settings is now changed accordingly to
            the specified game state '''
        self._game_state = game_state
        self._rows = self._game_state.get_rows()
        self._cols = self._game_state.get_columns()

    def redraw_board(self) -> None:
        ''' Redraws the board '''
        self._board.delete(tkinter.ALL)
        self._redraw_lines()
        self._redraw_cells()

    def _redraw_lines(self) -> None:
        ''' Redraws the board's lines '''
        row_multiplier = float(self._board.winfo_height()) / self._rows
        col_multiplier = float(self._board.winfo_width()) / self._cols
        
        # Draw the horizontal lines first
        for row in range(1, self._rows):
            self._board.create_line(0, row * row_multiplier, self.get_board_width(), row * row_multiplier)

        # Draw the column lines next
        for col in range(1, self._cols):
            self._board.create_line(col * col_multiplier, 0, col * col_multiplier, self.get_board_height())

    def _redraw_cells(self) -> None:
        ''' Redraws all the occupied cells in the board '''
        for row in range(self._rows):
            for col in range(self._cols):
                if self._game_state.get_board()[row][col] != othello.NONE:
                    self._draw_cell(row, col)
                
    def _draw_cell(self, row: int, col: int) -> None:
        ''' Draws the specified cell '''
        self._board.create_oval(col * self.get_cell_width(),
                                row * self.get_cell_height(),
                                (col + 1) * self.get_cell_width(),
                                (row + 1) * self.get_cell_height(),
                                fill = PLAYERS[self._game_state.get_board()[row][col]])                               


    def update_game_state(self, game_state: othello.OthelloGame) -> None:
        ''' Updates our current _game_state to the specified one in the argument '''
        self._game_state = game_state

    def get_cell_width(self) -> float:
        ''' Returns a game cell's width '''
        return self.get_board_width() / self.get_columns()

    def get_cell_height(self) -> float:
        ''' Returns a game cell's height '''
        return self.get_board_height() / self.get_rows()

    def get_board_width(self) -> float:
        ''' Returns the board canvas's width '''
        return float(self._board.winfo_width())

    def get_board_height(self) -> float:
        ''' Returns the board canvas's height '''
        return float(self._board.winfo_height())

    def get_rows(self) -> int:
        ''' Returns the total number of rows in the board '''
        return self._rows

    def get_columns(self) -> int:
        ''' Returns the total number of rows in the board '''
        return self._cols

    def get_board(self) -> tkinter.Canvas:
        ''' Returns the game board '''
        return self._board


class Score:
    def __init__(self, color: str, game_state: othello.OthelloGame, root_window) -> None:
        ''' Initializes the score label '''
        self._player = color
        self._score = game_state.get_total_cells(self._player)
        self._score_label = tkinter.Label(master = root_window,
                                          text = self._score_text(),
                                          background = BACKGROUND_COLOR,
                                          fg = PLAYERS[color],
                                          font = FONT)

    def update_score(self, game_state: othello.OthelloGame) -> None:
        ''' Updates the score with the specified game state '''
        self._score = game_state.get_total_cells(self._player)
        self._change_score_text()

    def get_score_label(self) -> tkinter.Label:
        ''' Returns the score label '''
        return self._score_label

    def get_score(self) -> int:
        ''' Returns the score '''
        return self._score

    def _change_score_text(self) -> None:
        ''' Changes the score label's text '''
        self._score_label['text'] =  self._score_text()

    def _score_text(self) -> str:
        ''' Returns the score in text string format '''
        return PLAYERS[self._player] + ' - ' + str(self._score)



class Turn:
    def __init__(self, game_state: othello.OthelloGame, root_window) -> None:
        ''' Initializes the player's turn Label '''
        self._player = game_state.get_turn()
        self._turn_label = tkinter.Label(master = root_window,
                                          text = self._turn_text(),
                                          background = BACKGROUND_COLOR,
                                          fg = PLAYERS[self._player],
                                          font = FONT)

    def display_winner(self, winner: str) -> None:
        ''' Only called when the game is over. Displays the game winner '''
        if winner == None:
            victory_text = 'Tie game. Nobody wins!'
            text_color = 'BLACK'
        else:
            victory_text = PLAYERS[winner] + ' player wins!'
            text_color = PLAYERS[winner]
        self._turn_label['text'] = victory_text
        self._turn_label['fg'] = text_color

    def switch_turn(self, game_state: othello.OthelloGame) -> None:
        ''' Switch's the turn between the players '''
        self._player = game_state.get_turn()
        self.change_turn_text()

    def change_turn_text(self) -> None:
        ''' Changes the turn label's text '''
        self._turn_label['text'] = self._turn_text()
        self._turn_label['fg'] = PLAYERS[self._player]

    def get_turn_label(self) -> None:
        ''' Returns the tkinter turn label '''
        return self._turn_label

    def update_turn(self, turn: str) -> None:
        ''' Updates the turn to whatever the current game state's turn is '''
        self._player = turn
        self.change_turn_text()

    def _turn_text(self) -> None:
        ''' Returns the turn in text/string form '''
        return PLAYERS[self._player] + " player's turn"

    def _opposite_turn(self) -> None:
        ''' Returns the opposite turn of current turn '''
        return {othello.BLACK: othello.WHITE, othello.WHITE: othello.BLACK}[self._player]


# Dialog for when the user wants to change the game's settings
class OptionDialog:
    def __init__(self, current_rows, current_columns, current_first_player,
                 current_top_left_player, current_victory_type):
        self._dialog_window = tkinter.Toplevel()

        self._row_column_option_list = (4, 6, 8, 10 ,12, 14, 16)
        self._player_option_list = ('Black', 'White')
        self._victory_option_list = ('Most Cells', 'Least Cells')

        # Initialize given game attributes
        self._rows = current_rows
        self._columns = current_columns
        self._first_player = current_first_player
        self._top_left_player = current_top_left_player
        self._victory_type = current_victory_type


        # Row drop-down menu
        self._row_frame = tkinter.Frame(master = self._dialog_window)
        self._row_label = tkinter.Label(master = self._row_frame,
                                        text = 'Rows:',
                                        font = DIALOG_FONT)
        self._row_label.grid(row = 0, column = 0, sticky = tkinter.E,
                             padx = 10, pady = 10)
        self._rows = tkinter.IntVar()
        self._rows.set(current_rows)
        self._row_option_menu = tkinter.OptionMenu(self._row_frame,
                                                   self._rows,
                                                   *self._row_column_option_list)
        self._row_option_menu.grid(row = 0, column = 1, sticky = tkinter.W,
                                   padx = 10, pady = 10)
        self._row_frame.grid(row = 0, column = 0, sticky = tkinter.W,
                             padx = 10, pady = 10)
        
        # Column drop-down menu
        self._column_frame = tkinter.Frame(master = self._dialog_window)
        self._column_label = tkinter.Label(master = self._column_frame,
                                           text = 'Columns:',
                                           font = DIALOG_FONT)
        self._column_label.grid(row = 0, column = 0, sticky = tkinter.E,
                                padx = 10, pady = 10)
        self._columns = tkinter.IntVar()
        self._columns.set(current_columns)
        self._column_option_menu = tkinter.OptionMenu(self._column_frame,
                                                      self._columns,
                                                      *self._row_column_option_list)
        self._column_option_menu.grid(row = 0, column = 1, sticky = tkinter.W,
                                      padx = 10, pady = 10)
        self._column_frame.grid(row = 0, column = 1, sticky = tkinter.W,
                                padx = 10, pady = 10)


        # First player drop-down menu
        self._first_player_frame = tkinter.Frame(master = self._dialog_window)
        self._first_player_label = tkinter.Label(master = self._first_player_frame,
                                                 text = 'First player:',
                                                 font = DIALOG_FONT)
        self._first_player_label.grid(row = 0, column = 0, sticky = tkinter.E,
                                      padx = 10, pady = 10)
        self._first_players = tkinter.StringVar()
        self._first_players.set(PLAYERS[current_first_player])
        self._first_player_option_menu = tkinter.OptionMenu(self._first_player_frame,
                                                            self._first_players,
                                                            *self._player_option_list)
        self._first_player_option_menu.grid(row = 0, column = 1, sticky = tkinter.W,
                                            padx = 10, pady = 10)
        self._first_player_frame.grid(row = 1, column = 0, sticky = tkinter.W,
                                      padx = 10, pady = 10)
        

        # Victory type
        self._victory_type_frame = tkinter.Frame(master = self._dialog_window)
        self._victory_type_label = tkinter.Label(master = self._victory_type_frame,
                                                        text = 'Victory type:',
                                                        font = DIALOG_FONT)
        self._victory_type_label.grid(row = 0, column = 0, sticky = tkinter.E,
                                             padx = 10, pady = 10)
        self._victory_types = tkinter.StringVar()
        self._victory_types.set(VICTORY_TYPES[current_victory_type])
        self._victory_type_option_menu = tkinter.OptionMenu(self._victory_type_frame,
                                                            self._victory_types,
                                                            *self._victory_option_list)
        self._victory_type_option_menu.grid(row = 0, column = 1, sticky = tkinter.W,
                                            padx = 10, pady = 10)
        self._victory_type_frame.grid(row = 1, column = 1, sticky = tkinter.W,
                                      padx = 10, pady = 10)

        
        # Top-left player drop-down menu
        self._top_left_player_frame = tkinter.Frame(master = self._dialog_window)
        self._top_left_player_label = tkinter.Label(master = self._top_left_player_frame,
                                                    text = 'Top-left center position:',
                                                    font = DIALOG_FONT)
        self._top_left_player_label.grid(row = 0, column = 0, sticky = tkinter.E,
                                         padx = 10, pady = 10)
        self._top_left_players = tkinter.StringVar()
        self._top_left_players.set(PLAYERS[current_top_left_player])
        self._top_left_player_option_menu = tkinter.OptionMenu(self._top_left_player_frame,
                                                               self._top_left_players,
                                                               *self._player_option_list)
        self._top_left_player_option_menu.grid(row = 0, column = 1, sticky = tkinter.W,
                                               padx = 10, pady = 10)
        self._top_left_player_frame.grid(row = 2, column = 0, columnspan = 2,
                                               sticky = tkinter.W, padx = 10, pady = 10)


        # OK and Cancel Buttons
        self._button_frame = tkinter.Frame(master = self._dialog_window)
        self._button_frame.grid(row = 3, column = 1, sticky = tkinter.E,
                                padx = 10, pady = 10)
        
        self._ok_button = tkinter.Button(master = self._button_frame,
                                         text = 'OK',
                                         font = DIALOG_FONT,
                                         command = self._on_ok_button)
        self._ok_button.grid(row = 0, column = 0, padx = 10, pady = 10)

        self._cancel_button = tkinter.Button(master = self._button_frame,
                                             text = 'Cancel',
                                             font = DIALOG_FONT,
                                             command = self._on_cancel_button)
        self._cancel_button.grid(row = 0, column = 1, padx = 10, pady = 10)


        # Configure the dialog window's row/column weight (from the grid layout)
        self._dialog_window.rowconfigure(0, weight = 1)
        self._dialog_window.rowconfigure(1, weight = 1)
        self._dialog_window.rowconfigure(2, weight = 1)
        self._dialog_window.rowconfigure(3, weight = 1)
        self._dialog_window.columnconfigure(0, weight = 1)
        self._dialog_window.columnconfigure(1, weight = 1)


        # Variable to determine what to do when the 'OK' button is clicked
        self._ok_clicked = False


    def show(self) -> None:
        self._dialog_window.grab_set()
        self._dialog_window.wait_window()

    def was_ok_clicked(self) -> bool:
        return self._ok_clicked

    def get_rows(self) -> int:
        return self._rows

    def get_columns(self) -> int:
        return self._columns

    def get_first_player(self) -> str:
        return self._first_player[0]

    def get_top_left_player(self) -> str:
        return self._top_left_player[0]

    def get_victory_type(self) -> str:
        return self._victory_type[0]


    # Functions assigned to button commands
    def _on_ok_button(self):
        self._ok_clicked = True
        self._rows = self._rows.get()
        self._columns = self._columns.get()
        self._first_player = self._first_players.get()
        self._top_left_player = self._top_left_players.get()
        self._victory_type = self._victory_types.get()
        self._dialog_window.destroy()

    def _on_cancel_button(self):
        self._dialog_window.destroy()

