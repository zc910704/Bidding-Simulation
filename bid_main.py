import random
import pandas as pd
import numpy as np
import datetime

clist = [0.95, 0.955, 0.96, 0.965 ,0.97 ,0.975 ,0.98 ,0.985]
flist = [6, 8 ,10]
BID_CONTROL = 21
ABlimit = 0.9 * BID_CONTROL
Dlist = []

#装饰器
def count_time(func):
    def inner_func(*arg, **kwargs):
        start_time = datetime.datetime.now ()
        func(arg[0])
        over_time = datetime.datetime.now()
        total_cost = (over_time-start_time).total_seconds()
        print("程序共计%s秒" %total_cost)
    return inner_func    

#函数定义 function definition
@count_time
def bid_main(n):
    for i in range(n):
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

def save_to_excel(list):
    df = pd.DataFrame(list)
    df.to_excel("test.xlsx", sheet_name = "中标价", index = False, header = False)

def main():
    bid_main(10)
    print(Dlist)

if __name__ == "__main__":
    main()


