import tkinter as tk
from tkinter import ttk
import random
import math

# ─── GAME LOGIC ────────────────────────────────────────────

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.player_pos = None
        self.target_pos = None          # Portal
        self.enemy_positions = []
        self.wall_positions = []
        self.gem_positions = []         # 3 gems
        self.collected_gems = 0
        self.lives = 3
        self.game_over = False
        self.won = False

        # Piece symbols & colors
        self.symbols = {
            'wall': ('█', '#3a4a5a', '#2a3a4a'),
            'me': ('☺', '#00ddff', '#004466'),
            'portal': ('🚪', '#ff8800', '#553300'),
            'enemy': ('K', '#ff4444', '#660000'),
            'gem': ('💎', '#44ddff', '#004466'),
            'ground': (' ', '#1e2f3f', '#1a2a3a')
        }
        self.setup()

    def setup(self):
        # Reset state
        self.collected_gems = 0
        self.lives = 3
        self.game_over = False
        self.won = False
        self.wall_positions = []
        self.enemy_positions = []
        self.gem_positions = []

        # Walls: top row (except last), bottom row (except last), plus pillars
        for c in range(self.cols - 1):
            self.wall_positions.append((0, c))
        for r in range(2, self.rows, 3):
            for c in range(2, self.cols - 1, 4):
                self.wall_positions.append((r, c))
        for r in range(1, self.rows - 1, 4):
            self.wall_positions.append((r, self.cols - 2))

        # Player (bottom-left area)
        self.player_pos = (self.rows - 2, 1)

        # Enemies (3 of them, scattered, not on walls or player)
        possible = [(r, c) for r in range(1, self.rows-1) for c in range(1, self.cols-1)
                    if (r, c) not in self.wall_positions and (r, c) != self.player_pos]
        random.shuffle(possible)
        self.enemy_positions = possible[:3]

        # Gems (3 of them, not on walls, player, or enemies)
        possible = [(r, c) for r in range(1, self.rows-1) for c in range(1, self.cols-1)
                    if (r, c) not in self.wall_positions and (r, c) != self.player_pos
                    and (r, c) not in self.enemy_positions]
        random.shuffle(possible)
        self.gem_positions = possible[:3]

        # Portal starts hidden (None)
        self.target_pos = None

    def get_cell_info(self, r, c):
        """Return (symbol, bg_color, fg_color) for a given cell."""
        if (r, c) == self.player_pos:
            return self.symbols['me']
        if (r, c) == self.target_pos:
            return self.symbols['portal']
        if (r, c) in self.enemy_positions:
            return self.symbols['enemy']
        if (r, c) in self.gem_positions:
            return self.symbols['gem']
        if (r, c) in self.wall_positions:
            return self.symbols['wall']
        return self.symbols['ground']

    def is_walkable(self, r, c, ignore_enemies=False):
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return False
        if (r, c) in self.wall_positions:
            return False
        if not ignore_enemies and (r, c) in self.enemy_positions:
            return False
        return True

    def move_player(self, dr, dc):
        if self.game_over or self.won:
            return False

        r, c = self.player_pos
        nr, nc = r + dr, c + dc
        if not self.is_walkable(nr, nc):
            return False

        # Move player
        self.player_pos = (nr, nc)

        # Check gem collection
        if (nr, nc) in self.gem_positions:
            self.gem_positions.remove((nr, nc))
            self.collected_gems += 1
            # If all gems collected, spawn portal
            if self.collected_gems >= 3 and self.target_pos is None:
                # Find empty spot for portal (not on player, enemies, walls)
                possible = [(r, c) for r in range(1, self.rows-1) for c in range(1, self.cols-1)
                            if (r, c) not in self.wall_positions and (r, c) != self.player_pos
                            and (r, c) not in self.enemy_positions and (r, c) not in self.gem_positions]
                if possible:
                    self.target_pos = random.choice(possible)

        # Check win condition (portal reached)
        if self.target_pos and (nr, nc) == self.target_pos:
            self.won = True
            return True

        # Now move enemies (hunting AI)
        self.move_enemies()

        # Check if enemy caught player
        if self.player_pos in self.enemy_positions:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                # Reset player to start, enemies scatter
                self.player_pos = (self.rows - 2, 1)
                # Move enemies away from player
                new_enemies = []
                for (er, ec) in self.enemy_positions:
                    # Try to move enemy away from player
                    best = None
                    best_dist = -1
                    for dr2, dc2 in [(-1,0),(1,0),(0,-1),(0,1)]:
                        nr2, nc2 = er + dr2, ec + dc2
                        if self.is_walkable(nr2, nc2, ignore_enemies=True) and (nr2, nc2) != self.player_pos:
                            dist = abs(nr2 - self.player_pos[0]) + abs(nc2 - self.player_pos[1])
                            if dist > best_dist:
                                best_dist = dist
                                best = (nr2, nc2)
                    if best:
                        new_enemies.append(best)
                    else:
                        new_enemies.append((er, ec))
                self.enemy_positions = new_enemies
        return True

    def move_enemies(self):
        """Hunting AI: if within 3 steps, chase; else random."""
        new_enemies = []
        pr, pc = self.player_pos
        for (er, ec) in self.enemy_positions:
            dist = abs(er - pr) + abs(ec - pc)
            moved = False

            if dist <= 3:
                # Chase: move towards player
                moves = []
                for dr2, dc2 in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nr2, nc2 = er + dr2, ec + dc2
                    if self.is_walkable(nr2, nc2, ignore_enemies=True) and (nr2, nc2) != self.player_pos:
                        new_dist = abs(nr2 - pr) + abs(nc2 - pc)
                        moves.append((new_dist, nr2, nc2))
                if moves:
                    moves.sort(key=lambda x: x[0])
                    nr2, nc2 = moves[0][1], moves[0][2]
                    new_enemies.append((nr2, nc2))
                    moved = True
            else:
                # Random wander
                dirs = [(-1,0),(1,0),(0,-1),(0,1)]
                random.shuffle(dirs)
                for dr2, dc2 in dirs:
                    nr2, nc2 = er + dr2, ec + dc2
                    if (self.is_walkable(nr2, nc2, ignore_enemies=True) and
                        (nr2, nc2) != self.player_pos and
                        (nr2, nc2) not in new_enemies):
                        new_enemies.append((nr2, nc2))
                        moved = True
                        break
            if not moved:
                new_enemies.append((er, ec))
        self.enemy_positions = new_enemies


# ─── GUI ──────────────────────────────────────────────────

class DungeonDash:
    def __init__(self, master):
        self.master = master
        master.title("⚔️ Dungeon Dash – Gems & Glory")
        master.geometry("1000x750")
        master.minsize(600, 500)
        master.configure(bg='#0a121f')

        self.rows, self.cols = 14, 16
        self.board = Board(self.rows, self.cols)

        # ── Layout ──
        main_frame = ttk.Frame(master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left: Canvas
        self.canvas = tk.Canvas(main_frame, bg='#0f1a2b', highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.bind('<Configure>', self.on_resize)
        self.canvas.bind('<Button-1>', self.on_click)

        # Right: Info Panel
        info_frame = ttk.Frame(main_frame, width=240)
        info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(15, 0))
        info_frame.pack_propagate(False)

        # Title
        ttk.Label(info_frame, text="⚔️ DUNGEON DASH",
                  font=('Arial', 18, 'bold'), foreground='#ffaa44').pack(pady=(0, 10))

        # Status box
        status_box = tk.Frame(info_frame, bg='#0a121f', relief='sunken', bd=2)
        status_box.pack(fill='x', pady=(0, 12))
        self.status_var = tk.StringVar()
        self.status_var.set("💎 Collect 3 gems!\n🚪 Portal appears!\n🧟 Avoid enemies!")
        status_lbl = tk.Label(status_box, textvariable=self.status_var,
                              justify=tk.LEFT, font=('Segoe UI', 10, 'bold'),
                              bg='#0a121f', fg='#c0d8e8', padx=8, pady=8)
        status_lbl.pack()

        # Lives
        self.lives_var = tk.StringVar()
        lives_lbl = tk.Label(info_frame, textvariable=self.lives_var,
                             font=('Segoe UI', 14, 'bold'), bg='#0a121f', fg='#ff4466')
        lives_lbl.pack(pady=(0, 5))
        self.update_lives()

        # Gems
        self.gems_var = tk.StringVar()
        gems_lbl = tk.Label(info_frame, textvariable=self.gems_var,
                            font=('Segoe UI', 14, 'bold'), bg='#0a121f', fg='#44ddff')
        gems_lbl.pack(pady=(0, 15))
        self.update_gems()

        # Legend
        legend = tk.Frame(info_frame, bg='#0a121f')
        legend.pack(anchor='w', pady=(0, 15))
        legend_items = [
            ('☺', '#00ddff', 'You'),
            ('💎', '#44ddff', 'Gem'),
            ('🚪', '#ff8800', 'Portal'),
            ('K', '#ff4444', 'Enemy'),
            ('█', '#3a4a5a', 'Wall')
        ]
        for sym, col, txt in legend_items:
            tk.Label(legend, text=f"{sym}  {txt}", bg='#0a121f',
                     fg=col, font=('Segoe UI', 10)).pack(anchor='w')

        # Buttons
        btn_frame = ttk.Frame(info_frame)
        btn_frame.pack(fill='x', pady=(0, 10))
        ttk.Button(btn_frame, text="🔄 Restart", command=self.restart).pack(fill='x')
        ttk.Button(info_frame, text="❓ How to Play", command=self.show_help).pack(fill='x', pady=(5, 0))

        # Key binds
        master.bind_all('<Up>', lambda e: self.move(-1, 0))
        master.bind_all('<Down>', lambda e: self.move(1, 0))
        master.bind_all('<Left>', lambda e: self.move(0, -1))
        master.bind_all('<Right>', lambda e: self.move(0, 1))
        master.bind_all('<w>', lambda e: self.move(-1, 0))
        master.bind_all('<s>', lambda e: self.move(1, 0))
        master.bind_all('<a>', lambda e: self.move(0, -1))
        master.bind_all('<d>', lambda e: self.move(0, 1))

        # Store cell IDs for fast updates
        self.cell_ids = {}  # (r,c) -> (rect_id, text_id)
        self.cell_size = 0
        self.offset_x = 0
        self.offset_y = 0
        self.draw_board()

    # ─── Fast Drawing ─────────────────────────────────────

    def on_resize(self, e):
        self.draw_board()

    def draw_board(self):
        """Draw or redraw the entire board (only on resize/restart)."""
        self.canvas.delete('all')
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10 or h < 10:
            return

        self.cell_w = w / self.cols
        self.cell_h = h / self.rows
        self.cell_size = min(self.cell_w, self.cell_h)
        self.offset_x = (w - self.cell_size * self.cols) / 2
        self.offset_y = (h - self.cell_size * self.rows) / 2

        self.cell_ids = {}
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = self.offset_x + c * self.cell_size
                y1 = self.offset_y + r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                sym, bg, fg = self.board.get_cell_info(r, c)

                rect = self.canvas.create_rectangle(x1, y1, x2, y2,
                                                    fill=bg, outline='#2a4a5a', width=1)
                fs = int(self.cell_size * 0.5)
                txt = self.canvas.create_text((x1+x2)//2, (y1+y2)//2,
                                              text=sym, font=('Segoe UI', fs, 'bold'),
                                              fill=fg)
                self.cell_ids[(r, c)] = (rect, txt)

    def update_cell(self, r, c):
        """Fast update: only change the cell that changed."""
        if (r, c) not in self.cell_ids:
            return
        rect_id, text_id = self.cell_ids[(r, c)]
        sym, bg, fg = self.board.get_cell_info(r, c)
        self.canvas.itemconfig(rect_id, fill=bg)
        self.canvas.itemconfig(text_id, text=sym, fill=fg)

    def update_all(self):
        """Refresh all cells (used after a big reset)."""
        for r in range(self.rows):
            for c in range(self.cols):
                self.update_cell(r, c)

    def update_lives(self):
        self.lives_var.set("❤️ " * self.board.lives if self.board.lives > 0 else "💀 DEAD")

    def update_gems(self):
        self.gems_var.set(f"💎 {self.board.collected_gems} / 3")

    # ─── Game Actions ─────────────────────────────────────

    def move(self, dr, dc):
        if self.board.game_over or self.board.won:
            return
        old_pos = self.board.player_pos
        old_enemies = self.board.enemy_positions.copy()
        old_gems = self.board.gem_positions.copy()
        old_portal = self.board.target_pos

        success = self.board.move_player(dr, dc)

        if success:
            # Update changed cells
            new_pos = self.board.player_pos
            new_enemies = self.board.enemy_positions
            new_gems = self.board.gem_positions
            new_portal = self.board.target_pos

            # Update player (old and new)
            if old_pos != new_pos:
                self.update_cell(old_pos[0], old_pos[1])
                self.update_cell(new_pos[0], new_pos[1])

            # Update enemies (check all enemy positions)
            all_old = set(old_enemies)
            all_new = set(new_enemies)
            for (r, c) in all_old.union(all_new):
                self.update_cell(r, c)

            # Update gems
            all_gems = set(old_gems).union(set(new_gems))
            for (r, c) in all_gems:
                self.update_cell(r, c)

            # Update portal
            if old_portal != new_portal:
                if old_portal:
                    self.update_cell(old_portal[0], old_portal[1])
                if new_portal:
                    self.update_cell(new_portal[0], new_portal[1])

            # Update HUD
            self.update_lives()
            self.update_gems()

            # Status messages & win/lose
            if self.board.won:
                self.status_var.set("🏆 YOU WIN! Portal reached! Press Restart.")
            elif self.board.game_over:
                self.status_var.set("💀 GAME OVER – out of lives! Press Restart.")
            elif self.board.lives < 3 and not self.board.game_over:
                self.status_var.set(f"💥 Ouch! {self.board.lives} lives left. Keep going!")
            else:
                self.status_var.set(f"💎 {self.board.collected_gems}/3 gems. Find the portal!")

    def on_click(self, e):
        if self.board.game_over or self.board.won:
            return
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10 or h < 10:
            return
        col = int((e.x - self.offset_x) // self.cell_size)
        row = int((e.y - self.offset_y) // self.cell_size)
        if 0 <= row < self.rows and 0 <= col < self.cols:
            pr, pc = self.board.player_pos
            dr, dc = row - pr, col - pc
            if abs(dr) + abs(dc) == 1:
                self.move(dr, dc)

    def restart(self):
        self.board.setup()
        self.draw_board()
        self.status_var.set("🔄 Restarted! Collect 3 gems to open the portal!")
        self.update_lives()
        self.update_gems()
        
    def show_help(self):
        win = tk.Toplevel(self.master)
        win.title("📖 How to Play")
        win.geometry("480x500")
        win.configure(bg='#0a121f')
        win.resizable(False, False)

        text = """
⚔️ DUNGEON DASH – RULES

🎯 GOAL:
Collect 3 💎 GEMS to make the 🚪 PORTAL appear.
Reach the portal to win!

🕹️ CONTROLS:
• Arrow Keys or WASD to move.
• Click an adjacent cell to move.

🧟 ENEMIES:
• Enemies wander randomly, but if you're
  within 3 steps, they CHASE you!
• Touching an enemy costs 1 ❤️ life.

❤️ LIVES:
• Start with 3 lives.
• Lose all = GAME OVER.
• After losing a life, you teleport back
  to the start and enemies scatter.

💡 TIPS:
• Plan your route to grab gems quickly.
• Use walls to block chasing enemies.
• Don't get cornered!

Good luck, adventurer! 🏰
        """
        lbl = tk.Label(win, text=text, justify=tk.LEFT, bg='#0a121f',
                       fg='#c0d8e8', font=('Segoe UI', 11), padx=20, pady=20)
        lbl.pack(fill=tk.BOTH, expand=True)
        ttk.Button(win, text="Close", command=win.destroy).pack(pady=(0, 15))

if __name__ == "__main__":
    root = tk.Tk()
    app = DungeonDash(root)
    root.mainloop()