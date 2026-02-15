import requests

# CoinGecko 币种 id 与 代码的对应（用于统一返回 BTCUSDT/ETHUSDT 格式）
COINGECKO_IDS = {
    "bitcoin": "BTCUSDT",
    "ethereum": "ETHUSDT",
}

def get_crypto_prices():
    # 使用 CoinGecko API 获取实时价格 (无需 API Key，无地区限制)
    url = "https://api.coingecko.com/api/v3/simple/price"
    ids = list(COINGECKO_IDS.keys())
    prices = {}

    try:
        response = requests.get(
            url,
            params={"ids": ",".join(ids), "vs_currencies": "usd"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, dict):
            print("获取价格失败: 无法解析响应")
            return None

        for cg_id, usdt_key in COINGECKO_IDS.items():
            if cg_id in data and isinstance(data[cg_id], dict) and "usd" in data[cg_id]:
                prices[usdt_key] = float(data[cg_id]["usd"])
        return prices if len(prices) == len(COINGECKO_IDS) else None
    except requests.RequestException as e:
        print(f"获取价格失败: {e}")
        return None
    except Exception as e:
        print(f"获取价格失败: {e}")
        return None

def calculate_portfolio(current_prices):
    # 你的持仓数据 (基于你提供的信息)
    portfolio = {
        "BTC": {"amount": 0.35644607, "cost": 80182.99},
        "ETH": {"amount": 7.370883, "cost": 2718.95}
    }
    
    print(f"{'币种':<6} {'当前价格':<12} {'持仓成本':<12} {'收益率':<10} {'浮盈(USD)':<10}")
    print("-" * 55)
    
    total_cost = 0
    total_value = 0
    
    for symbol, data in portfolio.items():
        curr_p = current_prices[f"{symbol}USDT"]
        avg_cost = data["cost"]
        amount = data["amount"]
        
        # 计算单项收益
        profit_pct = (curr_p - avg_cost) / avg_cost * 100
        profit_usd = (curr_p - avg_cost) * amount
        
        total_cost += avg_cost * amount
        total_value += curr_p * amount
        
        print(f"{symbol:<6} ${curr_p:<11.2f} ${avg_cost:<11.2f} {profit_pct:>8.2f}%  ${profit_usd:>9.2f}")

    total_profit_pct = (total_value - total_cost) / total_cost * 100
    print("-" * 55)
    print(f"总计资产价值: ${total_value:.2f}")
    print(f"总体收益率: {total_profit_pct:.2f}%")

if __name__ == "__main__":
    prices = get_crypto_prices()
    if prices:
        calculate_portfolio(prices)