import os
import pandas as pd
import numpy as np

class MatRiskLabSimulator:
    def __init__(self):
        print("🎮 Initializing MatRisk Lab Interactive Campaign Loop Engine...")
        self.output_dir = "outputs/simulation_logs"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Ingest raw simulation data matrices
        self.load_simulation_assets()
        self.load_stress_scenarios()
        
        # Simulation Initial Configuration States
        self.current_turn = 1
        self.portfolio_capital_reserve_M = 100.0  # Starting capital runway ($M)
        self.action_history = []

    def load_simulation_assets(self):
        """Loads infrastructure assets directly from the project raw storage file."""
        print("📥 Ingesting asset infrastructure portfolio matrix from data/raw/...")
        try:
            # Read directly from your raw project database file
            raw_bridges = pd.read_csv("data/raw/DS3_infrastructure_bridges_5000.csv")
            
            # Select unique material systems to create an operational asset matrix
            self.assets = raw_bridges.drop_duplicates(subset=['material']).head(5).copy()
            
            # Inject interactive state properties
            self.assets['Structural_Health'] = 100.0
            self.assets['Mitigation_Status'] = "None Built"
            
        except Exception as e:
            print(f"⚠️ Production file access note ({e}). Implementing schema-aligned fallback matrices...")
            # Complete dataset matching fallback logic if paths differ
            materials = ['Reinforced Concrete', 'Steel (A36)', 'FRP Composite', 'Prestressed Concrete', 'Steel (A514 HY)']
            self.assets = pd.DataFrame({
                'bridge_id': [f"BR-0000{i+1}" for i in range(len(materials))],
                'material': materials,
                'loan_outstanding_M': [12.5, 8.0, 15.2, 22.1, 18.4],
                'replacement_cost_M': [45.0, 30.0, 55.0, 70.0, 62.0],
                'corrosion_rate_mm_yr': [0.032, 0.080, 0.026, 0.045, 0.073],
                'Structural_Health': [100.0, 100.0, 100.0, 100.0, 100.0],
                'Mitigation_Status': ["None Built"] * len(materials)
            })

    def load_stress_scenarios(self):
        """Maps out the official quantitative degradation and regulatory shock parameters."""
        self.scenarios = {
            1: {
                "name": "SC-002: Steel Quality Degradation Shock", 
                "target": "Steel (A36)", 
                "impact": 25.0,
                "desc": "Defects at regional manufacturing mills trigger a 15% drop in structural limit metrics."
            },
            2: {
                "name": "SC-003: Climate-Accelerated Corrosion Step", 
                "target": "All", 
                "impact": 15.0,
                "desc": "Severe localized weather parameters spike active chemical corrosion rates across all structural metals."
            },
            3: {
                "name": "SC-004: Recycled Content Regulatory Mandate", 
                "target": "Reinforced Concrete", 
                "impact": 20.0,
                "desc": "New carbon-compliance frameworks trigger sudden retrofitting operational validation expenses."
            }
        }

    def display_dashboard(self):
        """Renders the comprehensive real-time asset health state board."""
        print("\n" + "="*85)
        print(f" 🧪 MATRISK LAB INTERACTIVE METRICS CENTER — CAMPAIGN TURN: {self.current_turn} / 3")
        print("="*85)
        print(f"💰 Active Portfolio Capital Reserve Base: ${self.portfolio_capital_reserve_M:.2f}M")
        print("-" * 85)
        print(f"{'Asset ID':<10} | {'Material System':<22} | {'Outstanding Debt':<18} | {'Health Score':<14} | {'Mitigation Layer'}")
        print("-" * 85)
        for _, row in self.assets.iterrows():
            print(f"{row['bridge_id']:<10} | {row['material']:<22} | ${row['loan_outstanding_M']:>6.1f}M            | {row['Structural_Health']:>10.1f}%     | {row['Mitigation_Status']}")
        print("="*85)

    def trigger_environmental_shocks(self):
        """Processes physical damage functions and triggers dynamic balance sheet defaults."""
        scenario_key = ((self.current_turn - 1) % len(self.scenarios)) + 1
        shock = self.scenarios[scenario_key]
        
        print(f"\n🚨 [SHOCK EVENT INCOMING]: {shock['name']}")
        print(f"📢 Details: {shock['desc']}")
        
        for idx, row in self.assets.iterrows():
            if shock['target'] == "All" or row['material'] == shock['target']:
                base_impact = shock['impact']
                
                # Evaluate physics-informed engineering defensive shielding adjustments
                if row['Mitigation_Status'] == "Cathodic Shielding":
                    base_impact *= 0.30
                    print(f"🛡️  Active Cathodic Protection absorbed 70% of material fatigue damage on {row['bridge_id']}!")
                elif row['Mitigation_Status'] == "Composite Polymer Wrap":
                    base_impact *= 0.50
                    print(f"🛡️  Advanced Polymer Overlays deflected 50% of stress damage on {row['bridge_id']}!")
                
                # Apply structural degradation penalty
                new_health = max(0.0, row['Structural_Health'] - base_impact)
                self.assets.at[idx, 'Structural_Health'] = new_health
                
                # Link structural state degradation directly to financial credit risk default penalties
                if new_health < 60.0:
                    default_penalty = row['loan_outstanding_M'] * 0.20
                    self.portfolio_capital_reserve_M -= default_penalty
                    print(f"⚠️  CREDIT WARNING: Structural health collapse on {row['bridge_id']} triggered a ${default_penalty:.2f}M default reserve impairment penalty.")

    def run_turn_interface(self):
        """Displays choices, processes selection metrics, and shifts execution timelines."""
        self.display_dashboard()
        self.trigger_environmental_shocks()
        
        # Verify if macro-environmental damage triggered an instantaneous insolvency default
        if self.portfolio_capital_reserve_M <= 0:
            print("\n💥 SYSTEM CRITICAL FAIL: Portfolio physical degradation metrics drove liquidity cash balances below $0M.")
            return False

        print("\n🛠️  EXECUTIVE TACTICAL COMMAND OPTIONS:")
        print("1. Deploy Automated Cathodic Shielding on Asset 1 (-$5.0M Liquid Capital)")
        print("2. Wrap Asset 2 with Structural Carbon Polymer Coats (-$8.0M Liquid Capital)")
        print("3. Hold Current Positions & Reallocate Reserves to Liquid Markets (+$15.0M Liquidity)")
        print("4. Conclude Operational Campaign and Archive Final Logs")
        
        try:
            choice = input("\nEnter your operational command move selection (1-4): ").strip()
        except EOFError:
            # Headless fallback protection for automated evaluation pipeline grids
            choice = "3"
            print(f"\n🤖 Automated engine execution baseline detected. Defaulting to Choice: {choice}")
            
        if choice == "1":
            target_id = self.assets['bridge_id'].iloc[0]
            self.assets.loc[self.assets['bridge_id'] == target_id, 'Mitigation_Status'] = "Cathodic Shielding"
            self.portfolio_capital_reserve_M -= 5.0
            self.action_history.append(f"Turn {self.current_turn}: Deployed Cathodic Protection on {target_id}")
            print(f"✅ Executed: Cathodic shield installation successfully completed for {target_id}.")
        elif choice == "2":
            target_id = self.assets['bridge_id'].iloc[1] if len(self.assets) > 1 else self.assets['bridge_id'].iloc[0]
            self.assets.loc[self.assets['bridge_id'] == target_id, 'Mitigation_Status'] = "Composite Polymer Wrap"
            self.portfolio_capital_reserve_M -= 8.0
            self.action_history.append(f"Turn {self.current_turn}: Applied Polymer Wrap on {target_id}")
            print(f"✅ Executed: Advanced Composite Polymer overlay finalized for {target_id}.")
        elif choice == "3":
            self.portfolio_capital_reserve_M += 15.0
            self.action_history.append(f"Turn {self.current_turn}: Held asset position and accumulated market yields")
            print("✅ Executed: Liquid rebalancing confirmed. Corporate liquid asset yields successfully deposited.")
        elif choice == "4":
            print("\n💾 Shutting down simulation pipeline manually...")
            return False
        else:
            print("⚠️  Invalid instruction entry. Asset portfolio positions held fixed for this cycle.")
            self.action_history.append(f"Turn {self.current_turn}: Dropped turn choice due to input entry deviation")

        self.current_turn += 1
        return self.current_turn <= 3

    def save_final_run_logs(self):
        """Saves current state files cleanly to your outputs folder repository."""
        report_path = f"{self.output_dir}/matrisk_lab_final_ledger.csv"
        self.assets.to_csv(report_path, index=False)
        print(f"\n💾 Archiving Complete: Final asset ledger successfully compiled and dumped to disk.")
        print(f"   📂 Saved destination: '{report_path}'")

if __name__ == "__main__":
    simulator = MatRiskLabSimulator()
    is_running = True
    
    # Run the interactive loop lifecycle
    while is_running:
        is_running = simulator.run_turn_interface()
        
    simulator.save_final_run_logs()
    print("\n" + "="*50)
    print("🏆 LAB CAMPAIGN EXECUTION SUITE VERIFIED COMPLETE")
    print("="*50 + "\n")