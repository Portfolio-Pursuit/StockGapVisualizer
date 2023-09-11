from datetime import datetime, timedelta
from papertrades.interactive.models.leaderboard_interactive import WeeklyLeaderboard
from papertrades.interactive.models.papertrade_interactive import PaperTradeInteractive
from common.application.application import db

def calculate_weekly_profits():
    # Get the current date
    current_date = datetime.now().date()

    # Calculate the start of the current week
    start_of_week = current_date - timedelta(days=current_date.weekday())

    # Calculate the end of the current week
    end_of_week = start_of_week + timedelta(days=6)

    # Query paper trades within the current week
    paper_trades = PaperTradeInteractive.query.filter(
        PaperTradeInteractive.timestamp >= start_of_week,
        PaperTradeInteractive.timestamp <= end_of_week
    ).all()

    # Calculate weekly profits for each user
    user_profits = {}  # Dictionary to store user_id -> weekly_profit

    for trade in paper_trades:
        if trade.user_id not in user_profits:
            user_profits[trade.user_id] = 0.0

        is_buy = trade.direction == "buy"
        profit = (1 if is_buy else -1) * (trade.current_price - trade.entry_price) * trade.quantity
        user_profits[trade.user_id] += profit

    # Update the WeeklyLeaderboard table with the calculated weekly profits
    for user_id, weekly_profit in user_profits.items():
        leaderboard_entry = WeeklyLeaderboard(
            user_id=user_id,
            week_start_date=start_of_week,
            weekly_profit=weekly_profit
        )
        db.session.add(leaderboard_entry)

    db.session.commit()
