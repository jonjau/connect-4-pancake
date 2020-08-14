"""
Contains animation functions. different file???
"""

def update_coin(coin):
    """Check if coin is still falling and update accordingly."""

    if coin.is_at_the_bottom():
        coin.is_falling = False

    coin.update()
    coin.draw()


def update_coins(coins):
    """Update all coins in the group of sprites `coins`."""
    for coin in coins:
        update_coin(coin)

