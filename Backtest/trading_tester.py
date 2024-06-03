import os
from strategy import Trader
import time
from prices import ticker_list
           
timer = time.time()



os.system('color a')

begin_exit_win = 1.001
end_exit_win = 1.1

begin_exit_loss = 0.85
end_exit_loss = 1.0


###Simulation Generator###
# for x in range(0,6):
#     incr = x * 0.01
#     perc = begin_exit_win + incr
#     perc = round(perc, 4)
#     for y in range(0,4):
#         incry = y * 0.05
#         percy = begin_exit_loss + incry
#         percy = round(percy, 4)
#         for z in range(0, 13):
#             percz = z * 5
#             trader = Trader(cash=10000, stocks=ticker_list, strategy_name='Shooting Star. Golden Cross', exit_win=perc, exit_max_loss=percy, exit_max_time=percz)
#             trader.run(trader)
    
trader = Trader(cash=10000, stocks=ticker_list, strategy_name='Shooting Star. Golden Cross', exit_win=1.011, exit_max_loss=1, exit_max_time=35)
trader.run(trader)



###
# trader = Trader(cash=10000, stocks=ticker_list, strategy_name='Shooting Star. Golden Cross', exit_win=1.001, exit_max_loss=1, exit_max_time=30)
# trader.run(trader)
###

# print(f'Initial account value: ${trader.cash:,.2f}')
# print(f'Initial account value: ${trader2.cash:,.2f}')



# print('\n----------------------------------\n')
# trader.history()


# print('\n----------------------------------\n')
# trader2.history()

print("\n\n--- %s seconds ---" % (time.time() - timer))