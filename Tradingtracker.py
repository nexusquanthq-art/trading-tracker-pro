import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class TradingTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Trading Win Rate Calculator")
        self.root.geometry("400x650")
        self.root.resizable(False, False)
        
        # Variables
        self.total_trades = 0
        self.wins = 0
        self.losses = 0
        self.initial_capital = 0.0
        self.current_capital = 0.0
        self.risk_percent = 0.0
        self.reward_risk_ratio = 0.0
        self.trade_history = []  # Store trade history for proper undo
        
        # File paths
        self.data_file = "trading_tracker_data.json"
        self.settings_file = "trading_tracker_settings.json"
        
        # Style
        self.root.configure(bg='#2C3E50')
        style = ttk.Style()
        style.theme_use('clam')
        
        # Title
        title_label = tk.Label(root, text="📊 TRADING TRACKER", 
                               font=('Arial', 16, 'bold'), 
                               bg='#2C3E50', fg='#ECF0F1')
        title_label.pack(pady=10)
        
        # Settings Frame
        settings_frame = tk.Frame(root, bg='#34495E', bd=2, relief='groove')
        settings_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(settings_frame, text="⚙️ ACCOUNT SETTINGS", 
                font=('Arial', 12, 'bold'), 
                bg='#34495E', fg='#ECF0F1').pack(pady=5)
        
        # Initial Capital
        capital_frame = tk.Frame(settings_frame, bg='#34495E')
        capital_frame.pack(pady=5, padx=10, fill='x')
        tk.Label(capital_frame, text="Initial Capital ($):", 
                bg='#34495E', fg='#ECF0F1', width=20, anchor='w').pack(side='left')
        self.capital_entry = tk.Entry(capital_frame, font=('Arial', 11), 
                                      justify='center', width=15)
        self.capital_entry.insert(0, "1000")
        self.capital_entry.pack(side='right')
        
        # Risk Percentage
        risk_frame = tk.Frame(settings_frame, bg='#34495E')
        risk_frame.pack(pady=5, padx=10, fill='x')
        tk.Label(risk_frame, text="Risk per Trade (%):", 
                bg='#34495E', fg='#ECF0F1', width=20, anchor='w').pack(side='left')
        self.risk_entry = tk.Entry(risk_frame, font=('Arial', 11), 
                                   justify='center', width=15)
        self.risk_entry.insert(0, "2")
        self.risk_entry.pack(side='right')
        
        # Reward:Risk Ratio
        reward_frame = tk.Frame(settings_frame, bg='#34495E')
        reward_frame.pack(pady=5, padx=10, fill='x')
        tk.Label(reward_frame, text="Reward:Risk Ratio:", 
                bg='#34495E', fg='#ECF0F1', width=20, anchor='w').pack(side='left')
        self.reward_entry = tk.Entry(reward_frame, font=('Arial', 11), 
                                     justify='center', width=15)
        self.reward_entry.insert(0, "2")
        self.reward_entry.pack(side='right')
        
        # Calculation Info
        info_frame = tk.Frame(settings_frame, bg='#34495E')
        info_frame.pack(pady=10, padx=10, fill='x')
        
        self.risk_amount_label = tk.Label(info_frame, 
                                          text="Risk: $20.00 | Reward: $40.00", 
                                          font=('Arial', 9), 
                                          bg='#34495E', fg='#95A5A6')
        self.risk_amount_label.pack()
        
        # Apply Settings Button
        self.apply_button = tk.Button(settings_frame, text="APPLY SETTINGS", 
                                      font=('Arial', 10, 'bold'),
                                      bg='#3498DB', fg='white',
                                      command=self.apply_settings)
        self.apply_button.pack(pady=8)
        
        # Trade Buttons Frame
        buttons_frame = tk.Frame(root, bg='#2C3E50')
        buttons_frame.pack(pady=20)
        
        # Win Button
        self.win_button = tk.Button(buttons_frame, text="✅ WIN", 
                                    font=('Arial', 14, 'bold'),
                                    bg='#27AE60', fg='white',
                                    width=10, height=2,
                                    command=self.add_win,
                                    state='disabled')
        self.win_button.pack(side='left', padx=10)
        
        # Loss Button
        self.loss_button = tk.Button(buttons_frame, text="❌ LOSS", 
                                     font=('Arial', 14, 'bold'),
                                     bg='#E74C3C', fg='white',
                                     width=10, height=2,
                                     command=self.add_loss,
                                     state='disabled')
        self.loss_button.pack(side='left', padx=10)
        
        # Statistics Frame
        stats_frame = tk.Frame(root, bg='#34495E', bd=2, relief='groove')
        stats_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(stats_frame, text="📈 TRADE STATISTICS", 
                font=('Arial', 12, 'bold'), 
                bg='#34495E', fg='#ECF0F1').pack(pady=5)
        
        # Stats labels
        self.total_label = tk.Label(stats_frame, text="Total Trades: 0", 
                                    font=('Arial', 11), 
                                    bg='#34495E', fg='#ECF0F1')
        self.total_label.pack()
        
        self.wins_label = tk.Label(stats_frame, text="Wins: 0", 
                                   font=('Arial', 11), 
                                   bg='#34495E', fg='#2ECC71')
        self.wins_label.pack()
        
        self.losses_label = tk.Label(stats_frame, text="Losses: 0", 
                                     font=('Arial', 11), 
                                     bg='#34495E', fg='#E74C3C')
        self.losses_label.pack()
        
        self.winrate_label = tk.Label(stats_frame, text="Win Rate: 0.0%", 
                                      font=('Arial', 12, 'bold'), 
                                      bg='#34495E', fg='#F39C12')
        self.winrate_label.pack(pady=5)
        
        # Capital Result Frame
        capital_result_frame = tk.Frame(root, bg='#34495E', bd=2, relief='groove')
        capital_result_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(capital_result_frame, text="💰 CAPITAL RESULT", 
                font=('Arial', 12, 'bold'), 
                bg='#34495E', fg='#ECF0F1').pack(pady=5)
        
        self.final_capital_label = tk.Label(capital_result_frame, 
                                            text="Final Capital: $1,000.00", 
                                            font=('Arial', 12, 'bold'), 
                                            bg='#34495E', fg='#3498DB')
        self.final_capital_label.pack()
        
        self.profit_loss_label = tk.Label(capital_result_frame, 
                                         text="Profit/Loss: $0.00 (0.00%)", 
                                         font=('Arial', 10), 
                                         bg='#34495E', fg='#95A5A6')
        self.profit_loss_label.pack(pady=5)
        
        # Control Buttons
        control_frame = tk.Frame(root, bg='#2C3E50')
        control_frame.pack(pady=15)
        
        self.reset_button = tk.Button(control_frame, text="🔄 RESET", 
                                      font=('Arial', 11, 'bold'),
                                      bg='#E74C3C', fg='white',
                                      width=12,
                                      command=self.reset_stats)
        self.reset_button.pack(side='left', padx=5)
        
        self.undo_button = tk.Button(control_frame, text="↩️ UNDO", 
                                     font=('Arial', 11, 'bold'),
                                     bg='#F39C12', fg='white',
                                     width=12,
                                     command=self.undo_last_trade)
        self.undo_button.pack(side='left', padx=5)
        
        # Load saved data on startup
        self.load_data()
    
    def save_data(self):
        """Save current state to JSON file"""
        data = {
            'total_trades': self.total_trades,
            'wins': self.wins,
            'losses': self.losses,
            'initial_capital': self.initial_capital,
            'current_capital': self.current_capital,
            'risk_percent': self.risk_percent,
            'reward_risk_ratio': self.reward_risk_ratio,
            'trade_history': self.trade_history
        }
        
        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def save_settings(self):
        """Save settings to separate JSON file"""
        settings = {
            'initial_capital': self.capital_entry.get(),
            'risk_percent': self.risk_entry.get(),
            'reward_risk_ratio': self.reward_entry.get()
        }
        
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def load_data(self):
        """Load saved data from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                
                self.total_trades = data.get('total_trades', 0)
                self.wins = data.get('wins', 0)
                self.losses = data.get('losses', 0)
                self.initial_capital = data.get('initial_capital', 0.0)
                self.current_capital = data.get('current_capital', 0.0)
                self.risk_percent = data.get('risk_percent', 0.0)
                self.reward_risk_ratio = data.get('reward_risk_ratio', 0.0)
                self.trade_history = data.get('trade_history', [])
                
                # Update entry fields with saved values
                if self.initial_capital > 0:
                    self.capital_entry.delete(0, tk.END)
                    self.capital_entry.insert(0, str(self.initial_capital))
                
                if self.risk_percent > 0:
                    self.risk_entry.delete(0, tk.END)
                    self.risk_entry.insert(0, str(self.risk_percent))
                
                if self.reward_risk_ratio > 0:
                    self.reward_entry.delete(0, tk.END)
                    self.reward_entry.insert(0, str(self.reward_risk_ratio))
                
                # Update stats display
                self.update_stats()
                
                # Enable trade buttons if we have valid data
                if self.initial_capital > 0 and self.risk_percent > 0 and self.reward_risk_ratio > 0:
                    self.win_button.config(state='normal')
                    self.loss_button.config(state='normal')
                    
                    # Update risk amount display
                    risk_amount = self.calculate_risk_amount()
                    reward_amount = risk_amount * self.reward_risk_ratio
                    self.risk_amount_label.config(
                        text=f"Risk: ${risk_amount:.2f} | Reward: ${reward_amount:.2f}"
                    )
        
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def apply_settings(self):
        """Apply settings and enable trade buttons"""
        try:
            self.initial_capital = float(self.capital_entry.get())
            self.risk_percent = float(self.risk_entry.get())
            self.reward_risk_ratio = float(self.reward_entry.get())
            
            if self.initial_capital <= 0:
                messagebox.showerror("Error", "Initial capital must be greater than 0!")
                return
            
            if self.risk_percent <= 0 or self.risk_percent > 100:
                messagebox.showerror("Error", "Risk percentage must be between 0 and 100!")
                return
            
            if self.reward_risk_ratio <= 0:
                messagebox.showerror("Error", "Reward:Risk ratio must be greater than 0!")
                return
            
            self.current_capital = self.initial_capital
            
            # Calculate amounts
            risk_amount = self.calculate_risk_amount()
            reward_amount = risk_amount * self.reward_risk_ratio
            
            self.risk_amount_label.config(
                text=f"Risk: ${risk_amount:.2f} | Reward: ${reward_amount:.2f}"
            )
            
            # Enable trade buttons
            self.win_button.config(state='normal')
            self.loss_button.config(state='normal')
            
            # Reset stats if needed
            self.total_trades = 0
            self.wins = 0
            self.losses = 0
            self.trade_history = []
            
            # Save settings
            self.save_settings()
            self.save_data()
            
            self.update_stats()
            
            messagebox.showinfo("Success", "Settings applied successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
    
    def calculate_risk_amount(self):
        """Calculate risk amount based on current capital"""
        return self.current_capital * (self.risk_percent / 100)
    
    def add_win(self):
        """Add a win trade"""
        self.total_trades += 1
        self.wins += 1
        
        # Add profit to capital
        risk_amount = self.calculate_risk_amount()
        profit = risk_amount * self.reward_risk_ratio
        self.current_capital += profit
        
        # Add to trade history
        self.trade_history.append({
            'type': 'win',
            'risk_amount': risk_amount,
            'profit': profit,
            'capital_before': self.current_capital - profit,
            'capital_after': self.current_capital
        })
        
        self.update_stats()
        self.save_data()
    
    def add_loss(self):
        """Add a loss trade"""
        self.total_trades += 1
        self.losses += 1
        
        # Subtract risk from capital
        risk_amount = self.calculate_risk_amount()
        self.current_capital -= risk_amount
        
        if self.current_capital < 0:
            self.current_capital = 0
        
        # Add to trade history
        self.trade_history.append({
            'type': 'loss',
            'risk_amount': risk_amount,
            'loss': risk_amount,
            'capital_before': self.current_capital + risk_amount,
            'capital_after': self.current_capital
        })
        
        self.update_stats()
        self.save_data()
    
    def undo_last_trade(self):
        """Undo the last trade"""
        if self.total_trades == 0 or len(self.trade_history) == 0:
            messagebox.showwarning("Warning", "No trades to undo!")
            return
        
        # Ask for confirmation
        result = messagebox.askyesno("Confirm Undo", "Undo the last trade?")
        if not result:
            return
        
        # Get last trade from history
        last_trade = self.trade_history.pop()
        
        # Revert the trade
        self.total_trades -= 1
        
        if last_trade['type'] == 'win':
            self.wins -= 1
            self.current_capital = last_trade['capital_before']
        else:  # loss
            self.losses -= 1
            self.current_capital = last_trade['capital_before']
        
        self.update_stats()
        self.save_data()
    
    def calculate_final_stats(self):
        """Calculate final statistics"""
        profit_loss = self.current_capital - self.initial_capital
        profit_loss_percent = (profit_loss / self.initial_capital) * 100 if self.initial_capital > 0 else 0
        
        return profit_loss, profit_loss_percent
    
    def update_stats(self):
        """Update all statistics labels"""
        self.total_label.config(text=f"Total Trades: {self.total_trades}")
        self.wins_label.config(text=f"Wins: {self.wins}")
        self.losses_label.config(text=f"Losses: {self.losses}")
        
        # Calculate win rate
        if self.total_trades > 0:
            win_rate = (self.wins / self.total_trades) * 100
            self.winrate_label.config(text=f"Win Rate: {win_rate:.1f}%")
        else:
            self.winrate_label.config(text="Win Rate: 0.0%")
        
        # Update capital display
        profit_loss, profit_loss_percent = self.calculate_final_stats()
        
        if profit_loss >= 0:
            color = '#2ECC71'  # Green for profit
            sign = '+'
        else:
            color = '#E74C3C'  # Red for loss
            sign = ''
        
        self.final_capital_label.config(
            text=f"Final Capital: ${self.current_capital:,.2f}",
            fg=color
        )
        
        self.profit_loss_label.config(
            text=f"Profit/Loss: {sign}${profit_loss:,.2f} ({sign}{profit_loss_percent:.2f}%)",
            fg=color
        )
        
        # Update risk amount display
        if self.risk_percent > 0 and self.current_capital > 0:
            risk_amount = self.calculate_risk_amount()
            reward_amount = risk_amount * self.reward_risk_ratio
            self.risk_amount_label.config(
                text=f"Risk: ${risk_amount:.2f} | Reward: ${reward_amount:.2f}"
            )
    
    def reset_stats(self):
        """Reset all statistics"""
        result = messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all statistics?")
        if not result:
            return
        
        self.total_trades = 0
        self.wins = 0
        self.losses = 0
        self.current_capital = self.initial_capital
        self.trade_history = []
        
        self.update_stats()
        self.save_data()
        
        # Clear data file
        try:
            if os.path.exists(self.data_file):
                os.remove(self.data_file)
            if os.path.exists(self.settings_file):
                os.remove(self.settings_file)
        except Exception as e:
            print(f"Error removing files: {e}")
        
        messagebox.showinfo("Reset", "All statistics have been reset!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingTracker(root)
    root.mainloop()