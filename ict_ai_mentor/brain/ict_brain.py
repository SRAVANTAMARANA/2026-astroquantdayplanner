class ICTBrain:
    def __init__(self):
        self.score = 0
        self.reasons = []

    def reset(self):
        self.score = 0
        self.reasons = []

    def check_htf_bias(self, bias):
        if bias in ["BEARISH", "BULLISH"]:
            self.score += 1
            self.reasons.append(f"HTF bias confirmed: {bias}")
            return True
        return False

    def check_liquidity(self, liquidity_taken):
        if liquidity_taken:
            self.score += 1
            self.reasons.append("Liquidity sweep confirmed")
            return True
        return False

    def check_fvg(self, fvg):
        if fvg:
            self.score += 1
            self.reasons.append("Fair Value Gap present")
            return True
        return False

    def check_premium_discount(self, zone, direction):
        if direction == "SELL" and zone == "PREMIUM":
            self.score += 1
            self.reasons.append("Sell from premium zone")
            return True
        if direction == "BUY" and zone == "DISCOUNT":
            self.score += 1
            self.reasons.append("Buy from discount zone")
            return True
        return False

    def check_killzone(self, in_killzone):
        if in_killzone:
            self.score += 1
            self.reasons.append("Killzone timing confirmed")
            return True
        return False

    def final_decision(self, min_score=4):
        if self.score >= min_score:
            return True, self.score, self.reasons
        return False, self.score, self.reasons
