# SureBetting-Bot

## What are sure bets ?

Sure betting is a way of placing bets with a guaranteed profit, **independently from match results**, placing a precise amount of money on two opposite bets, using two (or more) different bookmakers.  

  

## Why do they guarantee a profit ?

This works because any bookmaker has its own odds for the same bets on a match, so you can place bet A on a bookmaker and the opposite bet B on another bookmaker. If odds on the two bookmakers satisfy some criteria, you will be guaranteed a profit. *(Further explanations below)*

You can find more info on different types of bets used in this program [here](https://github.com/andry2327/SureBetting-Bot/blob/master/utility/_utility.md)


## How this program works ? (easy explanation)

First of all, it gets every upcoming match and their quotes on a lot of bookmakers.

***(Up to now, it only works for bookmakers accessible from Europe, and for Under/Over bets, called ‘totals’)*.**

The program updates odds for each match approximately every 5 minutes.

Once it has every odds, it creates every combination for each match from different bookmakers and then it searches for a couple of opposite winning bets to place on different bookmakers *(further explanations of this part below)*.

When it finds them, it sends a message on the [telegram channel](https://t.me/+Dqx_8y7w3rw2YWM0) with infos of the bets to place and their profit.

-> FULL EXPLAINATION [here](https://andry2327.notion.site/SureBetting-Bot-f5c3c41e2bb34219bd9ccf0a302823d6)

---

# Installation and usage

1. Install requirements:
   ```Python
    pip install -r requirements.txt
   ```
2. Run Bot with:
    ```Python
    python3 main.py
   ```