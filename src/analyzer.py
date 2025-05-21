from src.database import Database

class Analyzer:
    def __init__(self, data_path):
        self.db = Database(data_path)
    
    def analyze_crypto_earnings(self):
        crypto_earnings = self.db.filter_by_payment_method('Crypto')['Earnings_USD'].mean()
        other_earnings = self.db.get_data()[self.db.get_data()['Payment_Method'] != 'Crypto']['Earnings_USD'].mean()
        diff = crypto_earnings - other_earnings
        return f"Доход фрилансеров с криптовалютой на {diff:.2f} USD выше, чем с другими методами."
    
    def analyze_region_distribution(self):
        regions = self.db.group_by_region()
        result = "Распределение доходов по регионам:\n"
        for _, row in regions.iterrows():
            result += f"- {row['Client_Region']}: {row['mean']:.2f} USD (фрилансеров: {row['count']})\n"
        return result.strip()
    
    def analyze_expert_projects(self):
        percentage = self.db.expert_project_stats()
        return f"{percentage:.2f}% экспертов выполнили менее 100 проектов."
    
    def analyze_highest_region_earnings(self):
        regions = self.db.group_by_region()
        max_region = regions.loc[regions['mean'].idxmax()]
        return f"Регион с наибольшим средним доходом: {max_region['Client_Region']} ({max_region['mean']:.2f} USD)"
    
    def analyze_crypto_usage(self):
        crypto_users = self.db.filter_by_payment_method('Crypto')
        percentage = len(crypto_users) / len(self.db.get_data()) * 100
        return f"{percentage:.2f}% фрилансеров используют криптовалюту."
    
    def get_region_earnings_chart(self):
        regions = self.db.group_by_region()
        return {
            "type": "bar",
            "data": {
                "labels": regions['Client_Region'].tolist(),
                "datasets": [{
                    "label": "Средний доход (USD)",
                    "data": regions['mean'].tolist(),
                    "backgroundColor": ["#36A2EB", "#FF6384", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40", "#4CAF50"],
                    "borderColor": ["#2A8CC2", "#D44F6E", "#D4A83E", "#3A9C9C", "#7A4FD1", "#D47F30", "#3D8F40"],
                    "borderWidth": 1
                }]
            },
            "options": {
                "scales": {
                    "y": {
                        "beginAtZero": True,
                        "title": {"display": True, "text": "Доход (USD)"}
                    },
                    "x": {
                        "title": {"display": True, "text": "Регион"}
                    }
                },
                "plugins": {
                    "legend": {"display": True},
                    "title": {"display": True, "text": "Средний доход фрилансеров по регионам"}
                }
            }
        }
    
    def get_crypto_usage_chart(self):
        crypto_count = len(self.db.filter_by_payment_method('Crypto'))
        total = len(self.db.get_data())
        other_count = total - crypto_count
        return {
            "type": "pie",
            "data": {
                "labels": ["Crypto", "Other"],
                "datasets": [{
                    "label": "Методы оплаты",
                    "data": [crypto_count / total * 100, other_count / total * 100],
                    "backgroundColor": ["#36A2EB", "#FF6384"],
                    "borderColor": ["#2A8CC2", "#D44F6E"],
                    "borderWidth": 1
                }]
            },
            "options": {
                "plugins": {
                    "legend": {"display": True},
                    "title": {"display": True, "text": "Процент использования криптовалюты"}
                }
            }
        }
    
    def custom_query(self, query_type):
        if query_type == "compare cryptocurrency payment earnings":
            return self.analyze_crypto_earnings()
        elif query_type == "distribution of earnings by client region":
            return self.analyze_region_distribution()
        elif query_type == "expert freelancers project statistics":
            return self.analyze_expert_projects()
        elif query_type == "region with highest average earnings":
            return self.analyze_highest_region_earnings()
        elif query_type == "percentage of cryptocurrency payment usage":
            return self.analyze_crypto_usage()
        else:
            return "Запрос не распознан."