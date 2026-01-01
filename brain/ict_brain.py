class ICTBrain:
    def __init__(self):
        self.reset()

    def reset(self):
        self.htf_bias = None
        self.liquidity = None
        self.fvg = None
        self.zone = None
        self.direction = None
        self.killzone = False
        self.reasons = []
        self.score = 0

    def check_htf_bias(self, htf_bias):
        self.htf_bias = htf_bias
        if htf_bias == "BULLISH":
            self.score += 1
            self.reasons.append("HTF BULLISH")
        elif htf_bias == "BEARISH":
            self.score += 1
            self.reasons.append("HTF BEARISH")

    def check_liquidity(self, liquidity):
        self.liquidity = liquidity
        if liquidity:
            self.score += 1
            self.reasons.append("Liquidity Sweep")

    def check_fvg(self, fvg):
        self.fvg = fvg
        if fvg:
            self.score += 1
            self.reasons.append("FVG Present")

    def check_premium_discount(self, zone, direction):
        self.zone = zone
        self.direction = direction
        if (zone == "PREMIUM" and direction == "SELL") or (zone == "DISCOUNT" and direction == "BUY"):
            self.score += 1
            self.reasons.append(f"{zone} Zone Confirmed")

    def check_killzone(self, in_killzone):
        self.killzone = in_killzone
        if in_killzone:
            self.score += 1
            self.reasons.append("In Killzone")

    def final_decision(self):
        approved = self.score >= 4
        return approved, self.score, self.reasons
