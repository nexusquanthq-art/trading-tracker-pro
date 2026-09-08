```markdown
# Trading Win Rate Calculator

GUI-based trading tracker that calculates win rate, tracks capital growth, and manages trade history with automatic saving.

## What It Does

- Tracks wins and losses
- Calculates win rate percentage
- Tracks capital growth over time
- Calculates profit/loss with percentage
- Uses Risk/Reward ratio for realistic P&L
- Auto-saves all data to JSON
- Undo last trade functionality
- Reset statistics option
- Clean dark theme GUI

## How It Works

1. Set your initial capital (e.g., $1000)
2. Set your risk percentage per trade (e.g., 2%)
3. Set your reward:risk ratio (e.g., 2:1)
4. Click WIN or LOSS for each trade
5. The calculator automatically:
   - Updates your capital
   - Calculates win rate
   - Tracks profit/loss
   - Saves to JSON file

## Example

- Initial capital: $1000
- Risk per trade: 2% ($20)
- Reward:Risk ratio: 2:1 ($40 reward)

After 10 trades (6 wins, 4 losses):
- Wins: 6 × $40 = $240 profit
- Losses: 4 × $20 = $80 loss
- Net profit: $160
- Win rate: 60%

## Features

- Auto-save to JSON on every trade
- Settings saved separately
- Undo last trade
- Reset all statistics
- Trade history tracking
- Dark themed GUI
- Real-time capital updates
- Profit/Loss coloring (green/red)

## Installation

No external libraries needed. Uses only Python standard library (tkinter, json, os).

## How To Run

```bash
python win_rate_calculator.py
```

## Data Files

- `trading_tracker_data.json` - Trade history and current state
- `trading_tracker_settings.json` - User settings

Both files are auto-generated.

## Configuration

All settings are changed through the GUI:

- Initial capital
- Risk percentage per trade
- Reward:Risk ratio

## License

All Rights Reserved - See LICENSE file

## Author

Nexus
- Telegram: @Nexushqh
```