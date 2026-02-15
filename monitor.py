import ccxt
import time
import requests

# --- 配置区域 ---
# 在 Telegram 搜索 @BotFather 获取 TOKEN，搜索 @getidsbot 获取 CHAT_ID
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

# 你的调仓/止损逻辑配置
WATCH_LIST = {
    'BTC/USDT': {'target': 72000, 'stop': 64500},
    'ETH/USDT': {'target': 2150,  'stop': 1950},
    'XPL/USDT': {'target': 0.11,   'stop': 0.085}, # 2.25解锁前调仓点
    'XCN/USDT': {'target': 0.0065, 'stop': 0.0048}
}

def send_tg_msg(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"发送失败: {e}")

def monitor_prices():
    # 使用公开 API，无需 Key (若请求频繁可加 API Key)
    exchange = ccxt.binance({'enableRateLimit': True})
    print(f"[{time.strftime('%H:%M:%S')}] 监控启动，专心刷题吧！")
    
    while True:
        try:
            for symbol, levels in WATCH_LIST.items():
                ticker = exchange.fetch_ticker(symbol)
                current_price = ticker['last']
                
                # 触发止盈/调仓点
                if current_price >= levels['target']:
                    msg = f"🚀 *{symbol} 达到目标价!* \n当前: {current_price}\n建议：考虑执行减仓/调仓计划。"
                    send_tg_msg(msg)
                    # 触发后移除，防止刷屏（或修改 levels）
                    levels['target'] = float('inf') 
                
                # 触发止损点
                elif current_price <= levels['stop']:
                    msg = f"⚠️ *{symbol} 触发止损警报!* \n当前: {current_price}\n建议：检查基本面，执行止损。"
                    send_tg_msg(msg)
                    levels['stop'] = float('-inf')

            time.sleep(60) # 每分钟检查一次，不占用 CPU
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    monitor_prices()