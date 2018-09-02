clist = [0.95, 0.955, 0.96 ,0.965 ,0.97 ,0.975 ,0,98 ,0.985]
flist = [6, 8 ,10]
bid_control =21
ABlimit = 0.9*bid_control
bid_canditate =[]
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


def average(list):
    total = 0
    for i in list:
        total += i
    average = total/len(list)
    return average