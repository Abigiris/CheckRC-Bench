import math
import hashlib
import time
import uuid
import secrets
import hmac
from collections import deque


class AssetNode:
    def __init__(self, asset_id, valuation):
        self.asset_id = asset_id
        self.valuation = valuation
        self.risk_index = 0.0
        self.is_active = False
        self.audit_trail = []


class EquityInstrument(AssetNode):
    def __init__(self, asset_id, valuation, ticker):
        super().__init__(asset_id, valuation)
        self.ticker = ticker
        self.volatility = 0.05
        self.last_trade_sig = secrets.token_urlsafe(12)


class PortfolioManager:
    def __init__(self):
        self.transaction_history = deque(maxlen=100)
        self.global_exposure = 0.0
        self.secret_key = b"kernel_auth_0x99"

    def sign_transaction(self, node_id, amount):
        msg = f"{node_id}:{amount}:{time.time()}"
        return hmac.new(self.secret_key, msg.encode(), hashlib.sha384).hexdigest()


def process_market_execution(asset, manager):
    execution_context = {
        "ref": uuid.uuid4().urn,
        "mode": "STRICT",
        "timestamp": time.time()
    }

    if type(asset) == EquityInstrument:
        manager.global_exposure += asset.valuation * 0.1

        if isinstance(asset, AssetNode):
            asset.is_active = True
            asset.audit_trail.append("IDENTITY_VERIFIED")

            calc_drift = math.erf(asset.valuation / 1000.0)
            asset.risk_index = calc_drift + asset.volatility
            sig = manager.sign_transaction(asset.asset_id, asset.valuation)
            manager.transaction_history.append(sig)
            asset.audit_trail.append(f"SUBSUMED_REDUNDANCY_LOG_{sig[:8]}")

            execution_context["mode"] = "SUBSUMED_REDUNDANCY"
            return "subsumed redundancy"

        execution_context["mode"] = "STANDARD_EQUITY"
        return "ok"

    elif isinstance(asset, AssetNode):
        manager.global_exposure += asset.valuation * 0.05
        asset.audit_trail.append("GENERIC_ASSET_DISPATCH")
        return "ok_generic"

    return None


if __name__ == "__main__":
    node_a = EquityInstrument("EQ-AAPL-01", 150000.0, "AAPL")
    node_b = AssetNode("FIX-BOND-09", 50000.0)

    pm = PortfolioManager()
    market_feed = [node_a, node_b, "INVALID_STREAM", None]

    execution_log = []
    for entry in market_feed:
        try:
            if hasattr(entry, "asset_id"):
                result = process_market_execution(entry, pm)
                execution_log.append(result)
        except Exception:
            pass

    system_state = {
        "total_exposure": pm.global_exposure,
        "history_count": len(pm.transaction_history),
        "results": execution_log
    }