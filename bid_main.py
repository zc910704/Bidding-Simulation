import random
import pandas as pd
import numpy as np
import datetime
import queue

clist = [0.95, 0.955, 0.96, 0.965 ,0.97 ,0.975 ,0.98 ,0.985]
flist = [6, 8 ,10]
BID_CONTROL = 21
ABlimit = 0.9 * BID_CONTROL
queue = queue.Queue(maxsize=3)
Dlist = []

#装饰器定义

def count_time(func):
    def inner_func(*arg, **kwargs):
        start_time = datetime.datetime.now ()
        func(arg[0])
        over_time = datetime.datetime.now()
        total_cost = (over_time-start_time).total_seconds()
        print("程序共计%.2f秒" %total_cost)
    return inner_func    

def eta_time_estimate_every_1000(func):
    def inner_func(*arg, **kwargs):
        inner_i,inner_n = arg[0],arg[1]
        if inner_i%1000 == 0:
            current_time = datetime.datetime.now()
            queue.put(current_time)
            queue.put(current_time)
        func(inner_i, inner_n)
        if inner_i%1000 == 0 and  inner_i != 0 and inner_i != inner_n :
            step_cost = (queue.get()-queue.get()).total_seconds()
            finish_percentage = inner_i*100/inner_n
            eta_time =  step_cost / (1000/inner_n) * (1-inner_i/inner_n)
            print("已完成%d%%,预计剩余%.2f秒" %(finish_percentage, eta_time))
    return inner_func


#函数定义 function definition

@eta_time_estimate_every_1000
def single_bid(i,n):
    C = get_random(clist)
    F = get_random(flist)
    bid_canditate =[]
    bid_canditate = generate_random_biding(bid_canditate)
    bid_canditate_a = []
    bid_canditate_b = []
    for bid in bid_canditate:
        if bid > ABlimit:
            bid_canditate_a.append(bid)
        else:
            bid_canditate_b.append(bid)
        
    if len(bid_canditate_b) > 6 :
        bid_canditate_b.remove(max(bid_canditate_b))
        bid_canditate_b.remove(min(bid_canditate_b))

    bid_canditate_b_mean = average(bid_canditate_b)
    b_max_part, b_medium_part, b_min_part = devide_b_to_part(bid_canditate_b, bid_canditate_b_mean)
    b_max_part_mean = average(b_max_part)
    b_medium_part_mean = average(b_medium_part)
    b_min_part_mean = average(b_min_part)

    b_mean = solve_b_mean(b_max_part_mean, b_medium_part_mean, b_min_part_mean)
    bid_control_85 = 0.85 * BID_CONTROL
    D1 = min(bid_control_85, b_mean)
    E = D1 * C
    D = E * (100-F)/100 +  BID_CONTROL * F / 100
    if not bid_canditate_b:
        D = bid_control_85
    Dlist.append(D)
        
@count_time
def bid_main(n):
    for i in range(n):
        single_bid(i,n)
    save_to_excel(Dlist)

def average(list):
    total = 0
    average = 0
    try:
        for i in list:
            total += i
        average = total/len(list)
    finally:       
        return average

def devide_b_to_part(bid_canditate_b, bid_canditate_b_mean):
    #1.05< part
    #0.95<= part <= 1.05
    #part < 0.95
    b_max_part= []
    b_medium_part= []
    b_min_part= []
    for b in bid_canditate_b:
        if b > 1.05*bid_canditate_b_mean:
            b_max_part.append(b)
        elif b < 0.95*b*bid_canditate_b_mean:
            b_min_part.append(b)
        else:
            b_medium_part.append(b)
            
    return b_max_part, b_medium_part, b_min_part

def solve_b_mean(b_max_part_mean, b_medium_part_mean, b_min_part_mean):
    b_list = []
    if b_max_part_mean:
        b_list.append(b_max_part_mean)
    if b_medium_part_mean:
        b_list.append(b_medium_part_mean)
    if b_min_part_mean:    
        b_list.append(b_min_part_mean)

    if len(b_list)%2 == 0:
        b_mean = average(b_list)
    else:
        index = int(len(b_list)/2)
        b_mean = b_list[index]
    return b_mean

def get_random(list):
    ags = random.choice(list)
    return ags

def generate_random_biding(bid_canditate):
    canditator = random.randint(1,20)
    for company in range(canditator):
        bid_canditate.append(BID_CONTROL*random.uniform(0.7, 1))
    
    return bid_canditate

def get_distribution(Dlist):
    pass

def save_to_excel(list):
    df = pd.DataFrame(list)
    df.to_excel("test.xlsx", sheet_name = "中标价", index = False, header = False)

def main():
    bid_main(10000)
    print(Dlist)

if __name__ == "__main__":
    main()


