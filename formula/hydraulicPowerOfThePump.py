#P = Q*H*p*g
#[Вт] = [м*м*м/с]*[м]*[кг/м*м*м]*[м/с*с]
def hydraulicPowerOfThePump(Q,H):
    return Q*H*800*9.81