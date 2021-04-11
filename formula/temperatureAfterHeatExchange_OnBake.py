#t_after = (w/C*Q)+t_before
#[оС] = [ВТ]/([ВТ/м*м*м*оС]*[м*м*м/час])+[оС]
def temperatureAfterHeatExchange_OnBake(Q,t_before):
    w = 20000000
    C = 1163
    return (w/C*Q)+t_before

