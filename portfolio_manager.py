import requests
from decimal import Decimal, getcontext, ROUND_HALF_UP

# 1. 配置与初始化
getcontext().prec = 20

COINGECKO_CONFIG = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "x-plus": "XPL",
    "onyxcoin": "XCN",
}

# 2. 业务逻辑层 (Pure Logic) - 易于单元测试
def calculate_portfolio_metrics(portfolio: dict, api_prices: dict):
    """
    纯计算逻辑，不含任何 print 或网络请求。
    """
    results = []
    total_cost = Decimal("0")
    total_value = Decimal("0")

    for symbol, data in portfolio.items():
        cg_id = data["cg_id"]
        if cg_id not in api_prices:
            continue
            
        curr_p = Decimal(str(api_prices[cg_id]["usd"]))
        avg_cost = data["cost"]
        amount = data["amount"]
        
        item_cost = avg_cost * amount
        item_value = curr_p * amount
        profit_usd = item_value - item_cost
        profit_pct = (profit_usd / item_cost * 100) if item_cost != 0 else Decimal("0")
        
        total_cost += item_cost
        total_value += item_value
        
        results.append({
            "symbol": symbol,
            "curr_p": curr_p,
            "avg_cost": avg_cost,
            "profit_pct": profit_pct,
            "profit_usd": profit_usd
        })

    total_profit_pct = ((total_value - total_cost) / total_cost * 100) if total_cost != 0 else Decimal("0")
    
    summary = {
        "items": results,
        "total_value": total_value,
        "total_cost": total_cost,
        "total_profit_usd": total_value - total_cost,
        "total_profit_pct": total_profit_pct
    }
    return summary

# 3. 数据采集层 (IO)
def fetch_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    ids = list(COINGECKO_CONFIG.keys())
    try:
        response = requests.get(url, params={"ids": ",".join(ids), "vs_currencies": "usd"}, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching prices: {e}")
        return None

# 4. 呈现层 (UI)
def display_portfolio(summary):
    header = f"{'币种':<6} {'当前价格':<14} {'持仓成本':<14} {'收益率':<10} {'浮盈(USD)':<12}"
    print(header)
    print("-" * len(header))
    
    for item in summary["items"]:
        print(f"{item['symbol']:<6} ${item['curr_p']:<13.6f} ${item['avg_cost']:<13.6f} "
              f"{item['profit_pct']:>8.2f}%  ${item['profit_usd']:>11.2f}")

    print("-" * len(header))
    print(f"总计资产价值: ${summary['total_value']:,.2f}")
    print(f"总体收益率:   {summary['total_profit_pct']:.2f}%")
    print(f"总浮盈/亏:    ${summary['total_profit_usd']:,.2f}")

if __name__ == "__main__":
    # 你的持仓配置
    my_portfolio = {
        "BTC": {"amount": Decimal("0.35644607"), "cost": Decimal("80182.99"), "cg_id": "bitcoin"},
        "ETH": {"amount": Decimal("7.370883"), "cost": Decimal("2718.95"), "cg_id": "ethereum"},
        "XPL": {"amount": Decimal("224821.04"), "cost": Decimal("0.1666"), "cg_id": "x-plus"},
        "XCN": {"amount": Decimal("4533096.00"), "cost": Decimal("0.0110401"), "cg_id": "onyxcoin"}
    }
    
    raw_prices = fetch_prices()
    if raw_prices:
        stats = calculate_portfolio_metrics(my_portfolio, raw_prices)
        display_portfolio(stats)