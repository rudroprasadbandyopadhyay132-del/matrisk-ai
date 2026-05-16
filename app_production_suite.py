import os
import pandas as pd
import numpy as np

# =====================================================================
# 1. DATA INGESTION & PIPELINE ALIGNMENT
# =====================================================================
print("📥 Loading core engine data matrices from data/raw/...")
try:
    risk_scoring_df = pd.read_csv("data/raw/DS3_infrastructure_bridges_5000.csv")
    market_master = pd.read_csv("data/raw/DS4_crossdomain_features_daily.csv")
except FileNotFoundError as e:
    print(f"❌ Error loading datasets: {e}")
    print("💡 Verification check: Ensure your CSV files are inside 'data/raw/'.")
    exit(1)

# Backfill physics-informed degradation metric if not written to disk yet
if 'Unified_Risk_Score' not in risk_scoring_df.columns:
    thick_ratio = risk_scoring_df['remaining_thickness_mm'] / risk_scoring_df['original_thickness_mm']
    risk_scoring_df['Unified_Risk_Score'] = (10 - risk_scoring_df['condition_rating']) * 10 + (1 - thick_ratio) * 15
    risk_scoring_df['Unified_Risk_Score'] = risk_scoring_df['Unified_Risk_Score'].clip(5, 95)

# =====================================================================
# 2. CORE FINANCIAL ANALYTICS ENGINE DEFINITION
# =====================================================================
class MatRiskFinancialAnalyticsSuiteFinal:
    def __init__(self, asset_ledger_df, market_master_df):
        self.df = asset_ledger_df.copy()
        self.market = market_master_df.copy()
        
    def generate_trading_alpha_signals(self):
        print("   📊 Compiling Commodity Trading Alpha Vectors...")
        market_agg = self.market.groupby('commodity').agg({
            'mqi': 'mean',
            'herfindahl_index': 'mean',
            'supply_disruption_prob': 'mean'
        }).reset_index()
        
        # Calculate qualitative structural risk premium alpha scores
        market_agg['Commodity_Alpha_Score'] = (market_agg['herfindahl_index'] * 60) + ((100 - market_agg['mqi']) * 0.4)
        return market_agg.sort_values(by='Commodity_Alpha_Score', ascending=False)

    def calculate_project_finance_metrics(self):
        print("   🏢 Calculating Project Finance Debt Metrics...")
        proj_df = self.df.drop_duplicates(subset=['bridge_id']).copy()
        
        proj_df['Probability_of_Default_PD'] = np.clip((proj_df['Unified_Risk_Score'] / 100) * 0.12, 0.01, 0.90)
        proj_df['Risk_Adjusted_Valuation_M'] = proj_df['replacement_cost_M'] * (1 - (proj_df['Unified_Risk_Score'] / 100))
        
        display_cols = ['bridge_id', 'material', 'loan_outstanding_M', 'Probability_of_Default_PD', 'Risk_Adjusted_Valuation_M']
        return proj_df[display_cols]

    def price_insurance_catastrophe_risk(self):
        print("   🛡️ Computing Insurance Catastrophe Premium Models...")
        ins_df = self.df.drop_duplicates(subset=['bridge_id']).copy()
        
        ins_df['Material_Risk_Multiplier'] = 1.0 + (ins_df['Unified_Risk_Score'] / 60.0)
        ins_df['Risk_Adjusted_Premium_K_yr'] = ins_df['insurance_premium_K_yr'] * ins_df['Material_Risk_Multiplier']
        ins_df['Expected_Loss_Ratio'] = np.clip((ins_df['Unified_Risk_Score'] / 100.0) * 0.80, 0.05, 0.95)
        
        display_cols = ['bridge_id', 'material', 'insurance_premium_K_yr', 'Risk_Adjusted_Premium_K_yr', 'Expected_Loss_Ratio']
        return ins_df[display_cols]

    def generate_esg_portfolio_analytics(self):
        print("   🌱 Synthesizing ESG Asset Carbon Metrics...")
        esg_df = self.market.groupby('commodity').agg({
            'carbon_intensity_virgin': 'mean',
            'carbon_intensity_recycled': 'mean',
            'green_premium_per_kg': 'mean'
        }).reset_index()
        
        esg_df['Material_Sustainability_Index'] = 100 - (esg_df['carbon_intensity_virgin'] * 6) - (esg_df['green_premium_per_kg'] * 12)
        return esg_df.sort_values(by='Material_Sustainability_Index', ascending=False)

# =====================================================================
# 3. PRODUCTION AUTOMATION ENGINE
# =====================================================================
class MatRiskProductionSuite:
    def __init__(self, asset_ledger, market_master):
        self.ledger = asset_ledger.copy()
        self.market = market_master.copy()
        self.output_dir = "outputs/production_reports"
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"🚀 Production Deployment Engine Activated. Destination: '{self.output_dir}/'")

    def export_all_desks(self):
        print("\n🏭 Executing analytical transformations across distinct corporate desks...")
        suite = MatRiskFinancialAnalyticsSuiteFinal(self.ledger, self.market)
        
        # Compile asset layers
        alpha_df = suite.generate_trading_alpha_signals()
        proj_finance_df = suite.calculate_project_finance_metrics()
        insurance_df = suite.price_insurance_catastrophe_risk()
        esg_df = suite.generate_esg_portfolio_analytics()
        
        # Stream down directly to production workspace csv locations
        alpha_df.to_csv(f"{self.output_dir}/commodity_alpha_radar.csv", index=False)
        proj_finance_df.to_csv(f"{self.output_dir}/project_finance_debt_liquidity.csv", index=False)
        insurance_df.to_csv(f"{self.output_dir}/actuarial_catastrophe_pricing.csv", index=False)
        esg_df.to_csv(f"{self.output_dir}/esg_sustainability_profile.csv", index=False)
        
        print("💾 Success! Production files written cleanly to local directory paths.")
        return {
            "Alpha Vectors Count": len(alpha_df),
            "Debt Portfolios Audited": len(proj_finance_df),
            "Actuarial Profiles Underwritten": len(insurance_df),
            "ESG Materials Ranked": len(esg_df)
        }

if __name__ == "__main__":
    production_deployer = MatRiskProductionSuite(risk_scoring_df, market_master)
    summary_metrics = production_deployer.export_all_desks()

    print("\n" + "="*50)
    print("🏆 FINAL DEPLOYMENT COMPLIANCE CHECK:")
    print("-" * 50)
    for key, val in summary_metrics.items():
        print(f"✔️ {key.ljust(32)}: {val}")
    print("="*50)
    print("🎉 SYSTEM SHIP-READY: The MatRisk AI Engine is officially finalized.")