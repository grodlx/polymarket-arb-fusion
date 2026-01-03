def calculate_gas_adjusted_profit(gross_profit_pct, volume_usd, gas_price_gwei=30, matic_price=0.70):
    """Vypočítá, zda zisk pokryje poplatky na Polygonu."""
    # Odhad jednotek plynu pro 2 nákupní transakce
    gas_units = 500000 
    gas_cost_matic = (gas_units * gas_price_gwei) / 10**9
    gas_cost_usd = gas_cost_matic * matic_price
    
    gross_profit_usd = volume_usd * (gross_profit_pct / 100)
    net_profit_usd = gross_profit_usd - gas_cost_usd
    
    return {
        "net_profit": net_profit_usd,
        "gas_cost_usd": gas_cost_usd,
        "is_viable": net_profit_usd > 0
    }
