import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        height, width = screen.getmaxyx()
        if height < 3 or width < 3:
            return
        if width > 2:
            try:
                screen.addstr(0, 0, "+" + "-" * (width - 2) + "+")
            except:
                pass
        if width > 2 and height > 1:
            try:
                screen.addstr(height - 1, 0, "+" + "-" * (width - 2) + "+")
            except:
                pass
        for y in range(1, height - 1):
            if y < height:
                try:
                    screen.addstr(y, 0, "|")
                except:
                    pass
            if y < height and width > 1:
                try:
                    screen.addstr(y, width - 1, "|")
                except:
                    pass

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        height, width = screen.getmaxyx()
        grid_height = min(self.life.rows, height - 4)
        grid_width = min(self.life.cols * 2, width - 4)
        start_y = (height - grid_height) // 2
        start_x = (width - grid_width) // 2
        for y in range(grid_height):
            if y >= self.life.rows:
                break
            for x in range(grid_width // 2):
                if x >= self.life.cols:
                    break
                if self.life.curr_generation[y][x] == 1:
                    screen.addstr(start_y + y, start_x + x * 2, "██")
                else:
                    screen.addstr(start_y + y, start_x + x * 2, "  ")

    def run(self) -> None:
        try:
            screen = curses.initscr()
            screen.nodelay(True)
            curses.noecho()
            curses.cbreak()
            running = True
            while running:
                screen.clear()
                self.draw_borders(screen)
                self.draw_grid(screen)
                try:
                    height, width = screen.getmaxyx()
                    if height > 1 and width > 20:
                        info = f"Gen: {self.life.generations} | Press ESC to exit"
                        if len(info) < width:
                            screen.addstr(1, 2, info)
                except:
                    pass
                screen.refresh()
                self.life.step()
                try:
                    key = screen.getch()
                    if key == 27:
                        running = False
                        break
                except:
                    pass
        finally:
            try:
                curses.nocbreak()
                screen.nodelay(False)
                curses.echo()
                curses.endwin()
                curses.endwin()
            except:
                pass
