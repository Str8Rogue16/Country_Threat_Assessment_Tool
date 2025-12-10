import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# --- DATA MODELS ---

@dataclass
class PoliticalStabilityMetrics:
    government_legitimacy: int
    political_violence: int
    institutional_strength: int
    leadership_stability: int

@dataclass
class SecurityEnvironmentMetrics:
    internal_conflict: int
    regional_security: int
    law_enforcement: int
    military_factors: int

@dataclass
class EconomicStabilityMetrics:
    economic_performance: int
    fiscal_health: int
    trade_dependencies: int
    infrastructure_resilience: int

@dataclass
class SocialIndicatorsMetrics:
    social_cohesion: int
    human_development: int
    demographic_pressures: int
    information_environment: int

@dataclass
class IllicitMarketsMetrics:
    drug_trade: int
    human_trafficking: int
    arms_trafficking: int
    financial_crimes: int
    cybercrime_operations: int
    state_response_capacity: int

@dataclass
class CountryData:
    name: str
    political_stability: PoliticalStabilityMetrics
    security_environment: SecurityEnvironmentMetrics
    economic_stability: EconomicStabilityMetrics
    social_indicators: SocialIndicatorsMetrics
    illicit_markets: IllicitMarketsMetrics
    key_risk_factors: str = ""
    trend_analysis: str = ""
    recommendations: str = ""
    
    WEIGHTS = {
        'political_stability': 0.25,
        'security_environment': 0.20,
        'economic_stability': 0.20,
        'social_indicators': 0.15,
        'illicit_markets': 0.20
    }

    def calculate_category_score(self, category_metrics) -> float:
        if not category_metrics:
            return 0.0
        scores = [getattr(category_metrics, field.name) for field in category_metrics.__dataclass_fields__.values()]
        return sum(scores) / len(scores)

    def calculate_threat_score(self) -> float:
        weighted_scores = []
        pol_stab_score = self.calculate_category_score(self.political_stability)
        weighted_scores.append(pol_stab_score * self.WEIGHTS['political_stability'])
        sec_env_score = self.calculate_category_score(self.security_environment)
        weighted_scores.append(sec_env_score * self.WEIGHTS['security_environment'])
        econ_stab_score = self.calculate_category_score(self.economic_stability)
        weighted_scores.append(econ_stab_score * self.WEIGHTS['economic_stability'])
        social_ind_score = self.calculate_category_score(self.social_indicators)
        weighted_scores.append(social_ind_score * self.WEIGHTS['social_indicators'])
        illicit_mkt_score = self.calculate_category_score(self.illicit_markets)
        weighted_scores.append(illicit_mkt_score * self.WEIGHTS['illicit_markets'])
        return sum(weighted_scores)

    def get_threat_level(self) -> str:
        score = self.calculate_threat_score()
        if 1.0 <= score <= 2.0:
            return "LOW"
        elif 2.1 <= score <= 4.0:
            return "MODERATE"
        elif 4.1 <= score <= 6.0:
            return "ELEVATED"
        elif 6.1 <= score <= 8.0:
            return "HIGH"
        elif 8.1 <= score <= 10.0:
            return "EXTREME"
        else:
            return "UNDEFINED"
    
    def get_threat_description(self) -> str:
        level = self.get_threat_level()
        descriptions = {
            "LOW": "Stable with minimal risks",
            "MODERATE": "Some concerns but manageable",
            "ELEVATED": "Significant risks requiring monitoring",
            "HIGH": "Serious threats with potential for instability",
            "EXTREME": "Critical threats with high probability of crisis",
            "UNDEFINED": "Score out of range."
        }
        return descriptions.get(level, "N/A")

    def get_threat_color(self) -> str:
        level = self.get_threat_level()
        colors_map = {
            "LOW": "#28a745",
            "MODERATE": "#ffc107",
            "ELEVATED": "#17a2b8",
            "HIGH": "#fd7e14",
            "EXTREME": "#dc3545",
            "UNDEFINED": "#6c757d"
        }
        return colors_map.get(level, "#6c757d")

    def get_threat_color_rgb(self) -> tuple:
        """Get RGB tuple for PDF generation"""
        hex_color = self.get_threat_color()
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16)/255.0 for i in (0, 2, 4))

# --- DATABASE HANDLER ---

class DatabaseHandler:
    def __init__(self, db_path='country_threat_data.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with proper schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS countries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                
                -- Political Stability
                ps_government_legitimacy INTEGER,
                ps_political_violence INTEGER,
                ps_institutional_strength INTEGER,
                ps_leadership_stability INTEGER,
                
                -- Security Environment
                se_internal_conflict INTEGER,
                se_regional_security INTEGER,
                se_law_enforcement INTEGER,
                se_military_factors INTEGER,
                
                -- Economic Stability
                es_economic_performance INTEGER,
                es_fiscal_health INTEGER,
                es_trade_dependencies INTEGER,
                es_infrastructure_resilience INTEGER,
                
                -- Social Indicators
                si_social_cohesion INTEGER,
                si_human_development INTEGER,
                si_demographic_pressures INTEGER,
                si_information_environment INTEGER,
                
                -- Illicit Markets
                im_drug_trade INTEGER,
                im_human_trafficking INTEGER,
                im_arms_trafficking INTEGER,
                im_financial_crimes INTEGER,
                im_cybercrime_operations INTEGER,
                im_state_response_capacity INTEGER,
                
                -- Assessment Notes
                key_risk_factors TEXT,
                trend_analysis TEXT,
                recommendations TEXT,
                
                -- Metadata
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_country(self, country: CountryData):
        """Save or update country data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO countries (
                name,
                ps_government_legitimacy, ps_political_violence, ps_institutional_strength, ps_leadership_stability,
                se_internal_conflict, se_regional_security, se_law_enforcement, se_military_factors,
                es_economic_performance, es_fiscal_health, es_trade_dependencies, es_infrastructure_resilience,
                si_social_cohesion, si_human_development, si_demographic_pressures, si_information_environment,
                im_drug_trade, im_human_trafficking, im_arms_trafficking, im_financial_crimes, 
                im_cybercrime_operations, im_state_response_capacity,
                key_risk_factors, trend_analysis, recommendations,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (
            country.name,
            country.political_stability.government_legitimacy,
            country.political_stability.political_violence,
            country.political_stability.institutional_strength,
            country.political_stability.leadership_stability,
            country.security_environment.internal_conflict,
            country.security_environment.regional_security,
            country.security_environment.law_enforcement,
            country.security_environment.military_factors,
            country.economic_stability.economic_performance,
            country.economic_stability.fiscal_health,
            country.economic_stability.trade_dependencies,
            country.economic_stability.infrastructure_resilience,
            country.social_indicators.social_cohesion,
            country.social_indicators.human_development,
            country.social_indicators.demographic_pressures,
            country.social_indicators.information_environment,
            country.illicit_markets.drug_trade,
            country.illicit_markets.human_trafficking,
            country.illicit_markets.arms_trafficking,
            country.illicit_markets.financial_crimes,
            country.illicit_markets.cybercrime_operations,
            country.illicit_markets.state_response_capacity,
            country.key_risk_factors,
            country.trend_analysis,
            country.recommendations
        ))
        
        conn.commit()
        conn.close()
    
    def load_all_countries(self) -> Dict[str, CountryData]:
        """Load all countries from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM countries')
        rows = cursor.fetchall()
        
        countries = {}
        for row in rows:
            country = CountryData(
                name=row[1],
                political_stability=PoliticalStabilityMetrics(
                    government_legitimacy=row[2],
                    political_violence=row[3],
                    institutional_strength=row[4],
                    leadership_stability=row[5]
                ),
                security_environment=SecurityEnvironmentMetrics(
                    internal_conflict=row[6],
                    regional_security=row[7],
                    law_enforcement=row[8],
                    military_factors=row[9]
                ),
                economic_stability=EconomicStabilityMetrics(
                    economic_performance=row[10],
                    fiscal_health=row[11],
                    trade_dependencies=row[12],
                    infrastructure_resilience=row[13]
                ),
                social_indicators=SocialIndicatorsMetrics(
                    social_cohesion=row[14],
                    human_development=row[15],
                    demographic_pressures=row[16],
                    information_environment=row[17]
                ),
                illicit_markets=IllicitMarketsMetrics(
                    drug_trade=row[18],
                    human_trafficking=row[19],
                    arms_trafficking=row[20],
                    financial_crimes=row[21],
                    cybercrime_operations=row[22],
                    state_response_capacity=row[23]
                ),
                key_risk_factors=row[24] or "",
                trend_analysis=row[25] or "",
                recommendations=row[26] or ""
            )
            countries[row[1]] = country
        
        conn.close()
        return countries
    
    def delete_country(self, country_name: str):
        """Delete a country from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM countries WHERE name = ?', (country_name,))
        conn.commit()
        conn.close()

# --- PDF EXPORT HANDLER ---

class PDFExporter:
    @staticmethod
    def export_country_report(country: CountryData, filename: str):
        """Export comprehensive country report to PDF"""
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title
        story.append(Paragraph("COUNTRY THREAT ASSESSMENT REPORT", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Country header with threat level color
        threat_color = colors.Color(*country.get_threat_color_rgb())
        threat_level = country.get_threat_level()
        
        header_data = [
            ['Country:', country.name],
            ['Assessment Date:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Threat Level:', threat_level],
            ['Threat Score:', f"{country.calculate_threat_score():.2f}/10"],
            ['Description:', country.get_threat_description()]
        ]
        
        header_table = Table(header_data, colWidths=[2*inch, 4*inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8e8e8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 2), (1, 2), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (1, 2), (1, 2), threat_color),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        story.append(header_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Categories breakdown
        categories = [
            ('Political Stability', country.political_stability, [
                ('Government Legitimacy', 'government_legitimacy'),
                ('Political Violence', 'political_violence'),
                ('Institutional Strength', 'institutional_strength'),
                ('Leadership Stability', 'leadership_stability')
            ]),
            ('Security Environment', country.security_environment, [
                ('Internal Conflict', 'internal_conflict'),
                ('Regional Security', 'regional_security'),
                ('Law Enforcement', 'law_enforcement'),
                ('Military Factors', 'military_factors')
            ]),
            ('Economic Stability', country.economic_stability, [
                ('Economic Performance', 'economic_performance'),
                ('Fiscal Health', 'fiscal_health'),
                ('Trade Dependencies', 'trade_dependencies'),
                ('Infrastructure Resilience', 'infrastructure_resilience')
            ]),
            ('Social Indicators', country.social_indicators, [
                ('Social Cohesion', 'social_cohesion'),
                ('Human Development', 'human_development'),
                ('Demographic Pressures', 'demographic_pressures'),
                ('Information Environment', 'information_environment')
            ]),
            ('Illicit Markets & Criminal Activity', country.illicit_markets, [
                ('Drug Trade', 'drug_trade'),
                ('Human Trafficking', 'human_trafficking'),
                ('Arms Trafficking', 'arms_trafficking'),
                ('Financial Crimes', 'financial_crimes'),
                ('Cybercrime Operations', 'cybercrime_operations'),
                ('State Response Capacity', 'state_response_capacity')
            ])
        ]
        
        for cat_name, cat_data, indicators in categories:
            story.append(Paragraph(f"{cat_name}", heading_style))
            
            cat_score = country.calculate_category_score(cat_data)
            weight_key = cat_name.lower().replace(' ', '_').replace('&_', '').replace('__', '_')
            if weight_key == 'illicit_markets_criminal_activity':
                weight_key = 'illicit_markets'
            weight = CountryData.WEIGHTS.get(weight_key, 0)
            
            cat_table_data = [['Indicator', 'Score (1-10)']]
            for ind_name, ind_key in indicators:
                score = getattr(cat_data, ind_key)
                cat_table_data.append([ind_name, str(score)])
            
            cat_table_data.append(['Category Average', f"{cat_score:.1f}"])
            cat_table_data.append(['Weighted Score', f"{cat_score * weight:.2f}"])
            
            cat_table = Table(cat_table_data, colWidths=[4*inch, 1.5*inch])
            cat_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BACKGROUND', (0, -2), (-1, -1), colors.HexColor('#f0f0f0')),
                ('FONTNAME', (0, -2), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            
            story.append(cat_table)
            story.append(Spacer(1, 0.2*inch))
        
        # Assessment Notes
        if country.key_risk_factors or country.trend_analysis or country.recommendations:
            story.append(PageBreak())
            story.append(Paragraph("ASSESSMENT NOTES", heading_style))
            
            if country.key_risk_factors:
                story.append(Paragraph("<b>Key Risk Factors:</b>", styles['Normal']))
                story.append(Paragraph(country.key_risk_factors, styles['Normal']))
                story.append(Spacer(1, 0.15*inch))
            
            if country.trend_analysis:
                story.append(Paragraph("<b>Trend Analysis:</b>", styles['Normal']))
                story.append(Paragraph(country.trend_analysis, styles['Normal']))
                story.append(Spacer(1, 0.15*inch))
            
            if country.recommendations:
                story.append(Paragraph("<b>Recommendations:</b>", styles['Normal']))
                story.append(Paragraph(country.recommendations, styles['Normal']))
        
        doc.build(story)

# --- TKINTER APPLICATION ---

class CountryRiskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Country Threat Assessment Tool - Enhanced")
        self.root.geometry("1100x900")
        self.root.configure(bg='#f8f9fa')
        
        self.db = DatabaseHandler()
        self.countries: Dict[str, CountryData] = {}
        self.metric_value_labels = {}  # Store label references
        
        self.load_data()
        self.setup_ui()
        self.update_country_list()
        self.update_status()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status frame
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        title_label = ttk.Label(status_frame, text="🌍 Country Threat Assessment", 
                                font=('Arial', 20, 'bold'))
        title_label.pack()
        
        self.status_label = ttk.Label(status_frame, text="Loading...", 
                                     font=('Arial', 10), foreground='blue')
        self.status_label.pack(pady=(5, 0))
        
        # Input Section
        input_canvas = tk.Canvas(main_frame, bg='#f8f9fa', highlightthickness=0, height=400)
        input_canvas.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        input_frame_inner = ttk.Frame(input_canvas, padding="15")
        input_canvas.create_window((0, 0), window=input_frame_inner, anchor="nw")
        
        input_frame_inner.bind("<Configure>", lambda e: input_canvas.configure(
            scrollregion=input_canvas.bbox("all")
        ))
        
        v_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=input_canvas.yview)
        v_scrollbar.grid(row=1, column=3, sticky=(tk.N, tk.S))
        input_canvas.configure(yscrollcommand=v_scrollbar.set)
        
        # Country name
        ttk.Label(input_frame_inner, text="Country Name:", font=('Arial', 11, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.country_name = ttk.Entry(input_frame_inner, width=40, font=('Arial', 11))
        self.country_name.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0,10))
        
        self.metric_vars = {}
        
        categories_and_indicators = {
            "Political Stability": {
                "government_legitimacy": "Government Legitimacy (1=Low, 10=High)",
                "political_violence": "Political Violence (1=Low, 10=High)",
                "institutional_strength": "Institutional Strength (1=Weak, 10=Strong)",
                "leadership_stability": "Leadership Stability (1=Unstable, 10=Stable)"
            },
            "Security Environment": {
                "internal_conflict": "Internal Conflict (1=Low, 10=High)",
                "regional_security": "Regional Security (1=Stable, 10=Unstable)",
                "law_enforcement": "Law Enforcement (1=Weak, 10=Strong)",
                "military_factors": "Military Factors (1=Loyal, 10=Unstable)"
            },
            "Economic Stability": {
                "economic_performance": "Economic Performance (1=Poor, 10=Strong)",
                "fiscal_health": "Fiscal Health (1=Poor, 10=Strong)",
                "trade_dependencies": "Trade Dependencies (1=Low Risk, 10=High Risk)",
                "infrastructure_resilience": "Infrastructure Resilience (1=Resilient, 10=Vulnerable)"
            },
            "Social Indicators": {
                "social_cohesion": "Social Cohesion (1=Low, 10=High)",
                "human_development": "Human Development (1=Low, 10=High)",
                "demographic_pressures": "Demographic Pressures (1=Low, 10=High)",
                "information_environment": "Information Environment (1=Free, 10=Controlled)"
            },
            "Illicit Markets & Criminal Activity": {
                "drug_trade": "Drug Trade (1=Low, 10=High)",
                "human_trafficking": "Human Trafficking (1=Low, 10=High)",
                "arms_trafficking": "Arms Trafficking (1=Low, 10=High)",
                "financial_crimes": "Financial Crimes (1=Low, 10=High)",
                "cybercrime_operations": "Cybercrime Operations (1=Low, 10=High)",
                "state_response_capacity": "State Response Capacity (1=Strong, 10=Weak)"
            }
        }
        
        current_row = 1
        
        for category_name, indicators in categories_and_indicators.items():
            category_frame = ttk.LabelFrame(input_frame_inner, text=f"📊 {category_name} (1-10)", 
                                           padding="10")
            category_frame.grid(row=current_row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
            current_row += 1
            
            category_frame.columnconfigure(1, weight=1)
            
            cat_key = category_name.lower().replace(' ', '_').replace('&_', '').replace('__', '_')
            self.metric_vars[cat_key] = {}
            
            for i, (indicator_key, indicator_label) in enumerate(indicators.items()):
                ttk.Label(category_frame, text=f"{indicator_label}:").grid(
                    row=i, column=0, sticky=tk.W, pady=2)
                
                var = tk.IntVar(value=5)
                self.metric_vars[cat_key][indicator_key] = var
                
                scale = ttk.Scale(category_frame, from_=1, to=10, variable=var, orient=tk.HORIZONTAL)
                scale.grid(row=i, column=1, sticky=(tk.W, tk.E), padx=(10, 10), pady=2)
                
                value_label = ttk.Label(category_frame, text="5", font=('Arial', 10, 'bold'))
                value_label.grid(row=i, column=2, pady=2, padx=(5, 0))
                
                # Store label reference with unique key - FIXED APPROACH
                label_key = f"{cat_key}_{indicator_key}"
                self.metric_value_labels[label_key] = value_label
                
                # Update function with closure
                def make_update_func(lbl, v):
                    def update(val):
                        lbl.config(text=str(int(float(val))))
                    return update
                
                scale.config(command=make_update_func(value_label, var))
        
        # Assessment Notes
        notes_frame = ttk.LabelFrame(input_frame_inner, text="📝 Assessment Notes", padding="10")
        notes_frame.grid(row=current_row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        notes_frame.columnconfigure(0, weight=1)
        
        ttk.Label(notes_frame, text="Key Risk Factors:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.key_risk_factors_text = tk.Text(notes_frame, height=3, width=80, wrap=tk.WORD, 
                                            font=('Arial', 9))
        self.key_risk_factors_text.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0,5))
        
        ttk.Label(notes_frame, text="Trend Analysis:").grid(row=2, column=0, sticky=tk.W, pady=(10,2))
        self.trend_analysis_text = tk.Text(notes_frame, height=3, width=80, wrap=tk.WORD, 
                                          font=('Arial', 9))
        self.trend_analysis_text.grid(row=3, column=0, sticky=(tk.W, tk.E), padx=(0,5))
        
        ttk.Label(notes_frame, text="Recommendations:").grid(row=4, column=0, sticky=tk.W, pady=(10,2))
        self.recommendations_text = tk.Text(notes_frame, height=3, width=80, wrap=tk.WORD, 
                                           font=('Arial', 9))
        self.recommendations_text.grid(row=5, column=0, sticky=(tk.W, tk.E), padx=(0,5))
        
        # Action Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="✅ Add/Update Country", 
                   command=self.add_country).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Clear Form", 
                   command=self.clear_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📄 Export to PDF", 
                   command=self.export_current_to_pdf).pack(side=tk.LEFT, padx=5)
        
        # Results Section with colored threat levels
        results_frame = ttk.LabelFrame(main_frame, text="📊 Threat Assessment Results", padding="15")
        results_frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.results_text = tk.Text(results_frame, height=12, width=90, wrap=tk.WORD, 
                                   font=('Courier New', 10))
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        # Configure color tags for threat levels
        self.results_text.tag_config("low", foreground="#28a745", font=('Courier New', 12, 'bold'))
        self.results_text.tag_config("moderate", foreground="#ffc107", font=('Courier New', 12, 'bold'))
        self.results_text.tag_config("elevated", foreground="#17a2b8", font=('Courier New', 12, 'bold'))
        self.results_text.tag_config("high", foreground="#fd7e14", font=('Courier New', 12, 'bold'))
        self.results_text.tag_config("extreme", foreground="#dc3545", font=('Courier New', 12, 'bold'))
        
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Country List Management
        list_frame = ttk.LabelFrame(main_frame, text="🗂️ Saved Countries", padding="15")
        list_frame.grid(row=4, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        dropdown_frame = ttk.Frame(list_frame)
        dropdown_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(dropdown_frame, text="Select Country:", font=('Arial', 10, 'bold')).pack(
            side=tk.LEFT, padx=(0, 5))
        
        self.country_dropdown = ttk.Combobox(dropdown_frame, state="readonly", width=30)
        self.country_dropdown.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(dropdown_frame, text="📋 Load", 
                   command=self.load_country_from_dropdown).pack(side=tk.LEFT, padx=5)
        ttk.Button(dropdown_frame, text="📊 Show Report", 
                   command=self.show_country_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(dropdown_frame, text="📄 Export PDF", 
                   command=self.export_selected_to_pdf).pack(side=tk.LEFT, padx=5)
        ttk.Button(dropdown_frame, text="🗑️ Delete", 
                   command=self.delete_country).pack(side=tk.LEFT, padx=5)
        
        # Listbox
        self.country_listbox = tk.Listbox(list_frame, height=6, selectmode=tk.SINGLE, 
                                         font=('Arial', 11), bg='#ffffff')
        list_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, 
                                      command=self.country_listbox.yview)
        self.country_listbox.configure(yscrollcommand=list_scrollbar.set)
        
        self.country_listbox.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S), pady=(0, 10))
        
        self.country_listbox.bind('<Double-1>', lambda e: self.load_country_from_listbox())
        
        self.country_count_label = ttk.Label(list_frame, text="", font=('Arial', 10, 'bold'))
        self.country_count_label.grid(row=2, column=0, sticky=tk.W)
        
        # Grid configuration
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        main_frame.rowconfigure(4, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=1)
    
    def add_country(self):
        name = self.country_name.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a country name")
            return
        
        if not name.replace(' ', '').replace('-', '').isalnum():
            messagebox.showerror("Error", "Country name contains invalid characters")
            return
        
        try:
            political_stability = PoliticalStabilityMetrics(
                government_legitimacy=self.metric_vars['political_stability']['government_legitimacy'].get(),
                political_violence=self.metric_vars['political_stability']['political_violence'].get(),
                institutional_strength=self.metric_vars['political_stability']['institutional_strength'].get(),
                leadership_stability=self.metric_vars['political_stability']['leadership_stability'].get()
            )
            
            security_environment = SecurityEnvironmentMetrics(
                internal_conflict=self.metric_vars['security_environment']['internal_conflict'].get(),
                regional_security=self.metric_vars['security_environment']['regional_security'].get(),
                law_enforcement=self.metric_vars['security_environment']['law_enforcement'].get(),
                military_factors=self.metric_vars['security_environment']['military_factors'].get()
            )
            
            economic_stability = EconomicStabilityMetrics(
                economic_performance=self.metric_vars['economic_stability']['economic_performance'].get(),
                fiscal_health=self.metric_vars['economic_stability']['fiscal_health'].get(),
                trade_dependencies=self.metric_vars['economic_stability']['trade_dependencies'].get(),
                infrastructure_resilience=self.metric_vars['economic_stability']['infrastructure_resilience'].get()
            )
            
            social_indicators = SocialIndicatorsMetrics(
                social_cohesion=self.metric_vars['social_indicators']['social_cohesion'].get(),
                human_development=self.metric_vars['social_indicators']['human_development'].get(),
                demographic_pressures=self.metric_vars['social_indicators']['demographic_pressures'].get(),
                information_environment=self.metric_vars['social_indicators']['information_environment'].get()
            )
            
            illicit_markets = IllicitMarketsMetrics(
                drug_trade=self.metric_vars['illicit_markets_criminal_activity']['drug_trade'].get(),
                human_trafficking=self.metric_vars['illicit_markets_criminal_activity']['human_trafficking'].get(),
                arms_trafficking=self.metric_vars['illicit_markets_criminal_activity']['arms_trafficking'].get(),
                financial_crimes=self.metric_vars['illicit_markets_criminal_activity']['financial_crimes'].get(),
                cybercrime_operations=self.metric_vars['illicit_markets_criminal_activity']['cybercrime_operations'].get(),
                state_response_capacity=self.metric_vars['illicit_markets_criminal_activity']['state_response_capacity'].get()
            )
            
            country_data = CountryData(
                name=name,
                political_stability=political_stability,
                security_environment=security_environment,
                economic_stability=economic_stability,
                social_indicators=social_indicators,
                illicit_markets=illicit_markets,
                key_risk_factors=self.key_risk_factors_text.get(1.0, tk.END).strip(),
                trend_analysis=self.trend_analysis_text.get(1.0, tk.END).strip(),
                recommendations=self.recommendations_text.get(1.0, tk.END).strip()
            )
            
            self.countries[name] = country_data
            self.db.save_country(country_data)
            self.display_risk_assessment(country_data)
            self.update_country_list()
            self.update_status()
            
            messagebox.showinfo("Success", f"Country '{name}' saved to database!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error adding country: {str(e)}")
    
    def display_risk_assessment(self, country: CountryData):
        self.results_text.delete(1.0, tk.END)
        
        pol_stab_score = country.calculate_category_score(country.political_stability)
        sec_env_score = country.calculate_category_score(country.security_environment)
        econ_stab_score = country.calculate_category_score(country.economic_stability)
        social_ind_score = country.calculate_category_score(country.social_indicators)
        illicit_mkt_score = country.calculate_category_score(country.illicit_markets)
        
        total_threat_score = country.calculate_threat_score()
        threat_level = country.get_threat_level()
        
        report = f"""
COUNTRY THREAT ASSESSMENT
{'='*60}

Country: {country.name}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        self.results_text.insert(tk.END, report)
        
        # Insert threat level with color
        self.results_text.insert(tk.END, f"Threat Level: ")
        self.results_text.insert(tk.END, f"{threat_level}\n", threat_level.lower())
        self.results_text.insert(tk.END, f"Score: {total_threat_score:.2f}/10\n")
        self.results_text.insert(tk.END, f"Description: {country.get_threat_description()}\n\n")
        
        report2 = f"""CATEGORY SCORES:
{'='*60}
Political Stability:        {pol_stab_score:.1f}/10  (Weight: 25%)
Security Environment:       {sec_env_score:.1f}/10  (Weight: 20%)
Economic Stability:         {econ_stab_score:.1f}/10  (Weight: 20%)
Social Indicators:          {social_ind_score:.1f}/10  (Weight: 15%)
Illicit Markets:            {illicit_mkt_score:.1f}/10  (Weight: 20%)

"""
        self.results_text.insert(tk.END, report2)
        
        if country.key_risk_factors:
            self.results_text.insert(tk.END, f"\nKEY RISK FACTORS:\n{country.key_risk_factors}\n")
        if country.trend_analysis:
            self.results_text.insert(tk.END, f"\nTREND ANALYSIS:\n{country.trend_analysis}\n")
        if country.recommendations:
            self.results_text.insert(tk.END, f"\nRECOMMENDATIONS:\n{country.recommendations}\n")
    
    def populate_form(self, country: CountryData):
        self.country_name.delete(0, tk.END)
        self.country_name.insert(0, country.name)
        
        category_map = {
            'political_stability': country.political_stability,
            'security_environment': country.security_environment,
            'economic_stability': country.economic_stability,
            'social_indicators': country.social_indicators,
            'illicit_markets_criminal_activity': country.illicit_markets
        }
        
        for cat_key, cat_data in category_map.items():
            if cat_key in self.metric_vars:
                for ind_key, var in self.metric_vars[cat_key].items():
                    value = getattr(cat_data, ind_key, 5)
                    var.set(value)
                    
                    # Update label using stored reference
                    label_key = f"{cat_key}_{ind_key}"
                    if label_key in self.metric_value_labels:
                        self.metric_value_labels[label_key].config(text=str(value))
        
        self.key_risk_factors_text.delete(1.0, tk.END)
        self.key_risk_factors_text.insert(tk.END, country.key_risk_factors)
        self.trend_analysis_text.delete(1.0, tk.END)
        self.trend_analysis_text.insert(tk.END, country.trend_analysis)
        self.recommendations_text.delete(1.0, tk.END)
        self.recommendations_text.insert(tk.END, country.recommendations)
    
    def clear_form(self):
        self.country_name.delete(0, tk.END)
        for cat_key, indicators in self.metric_vars.items():
            for ind_key, var in indicators.items():
                var.set(5)
                label_key = f"{cat_key}_{ind_key}"
                if label_key in self.metric_value_labels:
                    self.metric_value_labels[label_key].config(text="5")
        
        self.key_risk_factors_text.delete(1.0, tk.END)
        self.trend_analysis_text.delete(1.0, tk.END)
        self.recommendations_text.delete(1.0, tk.END)
        self.results_text.delete(1.0, tk.END)
    
    def export_current_to_pdf(self):
        name = self.country_name.get().strip()
        if not name or name not in self.countries:
            messagebox.showwarning("Warning", "Please load or create a country first")
            return
        
        self.export_to_pdf(self.countries[name])
    
    def export_selected_to_pdf(self):
        selected = self.country_dropdown.get()
        if not selected:
            messagebox.showwarning("Warning", "Please select a country")
            return
        
        self.export_to_pdf(self.countries[selected])
    
    def export_to_pdf(self, country: CountryData):
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                initialfile=f"{country.name}_threat_assessment_{datetime.now().strftime('%Y%m%d')}.pdf"
            )
            
            if filename:
                PDFExporter.export_country_report(country, filename)
                messagebox.showinfo("Success", f"Report exported to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export PDF: {str(e)}")
    
    def load_country_from_dropdown(self):
        selected = self.country_dropdown.get()
        if selected and selected in self.countries:
            self.populate_form(self.countries[selected])
            self.display_risk_assessment(self.countries[selected])
    
    def load_country_from_listbox(self):
        selection = self.country_listbox.curselection()
        if selection:
            display_text = self.country_listbox.get(selection[0])
            country_name = display_text.split(" - ")[0]
            if country_name in self.countries:
                self.populate_form(self.countries[country_name])
                self.display_risk_assessment(self.countries[country_name])
    
    def show_country_report(self):
        selected = self.country_dropdown.get()
        if selected and selected in self.countries:
            self.display_risk_assessment(self.countries[selected])
    
    def delete_country(self):
        selected = self.country_dropdown.get()
        if not selected:
            messagebox.showwarning("Warning", "Please select a country")
            return
        
        if messagebox.askyesno("Confirm", f"Delete '{selected}' from database?"):
            self.db.delete_country(selected)
            del self.countries[selected]
            self.update_country_list()
            self.update_status()
            messagebox.showinfo("Success", f"'{selected}' deleted")
    
    def update_country_list(self):
        self.country_listbox.delete(0, tk.END)
        
        country_names = sorted(self.countries.keys())
        self.country_dropdown['values'] = country_names
        if country_names:
            self.country_dropdown.set(country_names[0])
        
        self.country_count_label.config(
            text=f"Total countries: {len(self.countries)}",
            foreground='green' if self.countries else 'red'
        )
        
        if not self.countries:
            self.country_listbox.insert(tk.END, "(No countries saved)")
        else:
            for name in country_names:
                country = self.countries[name]
                threat_level = country.get_threat_level()
                score = country.calculate_threat_score()
                display = f"{name} - {threat_level} ({score:.1f})"
                self.country_listbox.insert(tk.END, display)
    
    def update_status(self):
        if not self.countries:
            self.status_label.config(text="No countries loaded", foreground='orange')
        else:
            self.status_label.config(
                text=f"✅ {len(self.countries)} countries in database",
                foreground='green'
            )
    
    def load_data(self):
        try:
            self.countries = self.db.load_all_countries()
            print(f"Loaded {len(self.countries)} countries from database")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {str(e)}")
            self.countries = {}

def main():
    root = tk.Tk()
    app = CountryRiskApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
