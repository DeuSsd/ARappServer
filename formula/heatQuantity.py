def heatQuantity(TempBefore,TempAfter,massOfLiquid):
    heatQuantity = massOfLiquid*4200*(TempAfter-TempBefore)
    return heatQuantity