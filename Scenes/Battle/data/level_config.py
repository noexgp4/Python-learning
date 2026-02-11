import math

def get_required_exp(level):
    if level >= 100: 
        return 999999999  # 满级封顶
    
    # 基础值 100，指数 2.3
    # 1级升2级：100 * (1^2.3) = 100
    # 10级升11级：100 * (10^2.3) ≈ 19,952
    # 99级升100级：100 * (99^2.3) ≈ 3,980,000
    base_exp = 100
    multiplier = 2.3
    
    return int(base_exp * math.pow(level, multiplier))