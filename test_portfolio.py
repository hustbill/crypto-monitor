import unittest
from decimal import Decimal
from unittest.mock import patch
# 确保文件名与你实际的文件名一致，这里假设是 portfolio_manager.py
from portfolio_manager import calculate_portfolio_metrics, fetch_prices

class TestCryptoPortfolio(unittest.TestCase):

    def setUp(self):
        """初始化测试持仓数据"""
        self.mock_portfolio = {
            "BTC": {"amount": Decimal("1.0"), "cost": Decimal("50000.0"), "cg_id": "bitcoin"},
            "XCN": {"amount": Decimal("1000.0"), "cost": Decimal("0.01"), "cg_id": "onyxcoin"}
        }

    def test_profit_calculation(self):
        """测试收益率和浮盈计算是否精确"""
        mock_api_data = {
            "bitcoin": {"usd": 60000.0},
            "onyxcoin": {"usd": 0.005}
        }
        
        # 调用重构后的函数，它返回一个字典
        summary = calculate_portfolio_metrics(self.mock_portfolio, mock_api_data)
        
        # 验证计算结果
        # BTC profit: (60000-50000)*1 = 10000
        # XCN profit: (0.005-0.01)*1000 = -5
        # Total Profit USD = 9995.0
        self.assertEqual(summary["total_profit_usd"], Decimal("9995.0"))
        self.assertEqual(summary["total_value"], Decimal("60005.0"))

    def test_zero_amount(self):
        """测试边界情况：持仓数量为 0"""
        mock_api_data = {"bitcoin": {"usd": 60000.0}}
        portfolio_with_zero = {
            "BTC": {"amount": Decimal("0"), "cost": Decimal("50000.0"), "cg_id": "bitcoin"}
        }
        summary = calculate_portfolio_metrics(portfolio_with_zero, mock_api_data)
        self.assertEqual(summary["total_value"], Decimal("0"))
        self.assertEqual(summary["total_profit_pct"], Decimal("0"))

    @patch('requests.get')
    def test_api_failure(self, mock_get):
        """测试网络异常处理"""
        # 模拟 requests 抛出异常
        mock_get.side_effect = Exception("Network Down")
        result = fetch_prices()
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()