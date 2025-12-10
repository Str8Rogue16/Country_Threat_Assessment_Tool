# 🌍 Country Threat Assessment Tool

A comprehensive desktop application for analyzing and assessing country-level threats across multiple risk categories. Built with Python and Tkinter, featuring professional PDF report generation and SQLite database storage.

![Version](https://img.shields.io/badge/version-2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

---

## 📋 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Database Structure](#-database-structure)
- [Assessment Methodology](#-assessment-methodology)
- [PDF Export](#-pdf-export)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### Core Functionality
- ✅ **24 Threat Indicators** across 5 major categories
- ✅ **Weighted Scoring Algorithm** with customizable weights
- ✅ **5-Tier Threat Levels** (LOW → MODERATE → ELEVATED → HIGH → EXTREME)
- ✅ **SQLite Database** for reliable data persistence
- ✅ **Professional PDF Reports** with color-coded threat levels
- ✅ **Real-time Visual Feedback** with color-coded displays
- ✅ **Assessment Notes** for detailed risk analysis
- ✅ **Data Validation** to ensure accuracy

### User Interface
- 🎨 **Intuitive Slider Controls** (1-10 scale) with live value display
- 🎨 **Color-Coded Threat Levels** (Green → Red)
- 🎨 **Dual Selection Methods** (dropdown + listbox)
- 🎨 **Scrollable Input Form** for easy navigation
- 🎨 **Professional Styling** with emoji icons

### Data Management
- 💾 **Auto-save** on every update
- 💾 **Load/Edit/Delete** countries easily
- 💾 **View All Countries** with threat level summary
- 💾 **Export Individual Reports** to PDF
- 💾 **Database Located** in organized `data/` folder

---

## 🖼️ Screenshots

### Main Interface
```
┌─────────────────────────────────────────────────────┐
│  🌍 Country Threat Assessment Tool                  │
│  ✅ 15 countries in database                        │
├─────────────────────────────────────────────────────┤
│  Country Name: [Venezuela________________]          │
│                                                      │
│  📊 Political Stability (1-10)                      │
│    Government Legitimacy:     [====|====] 7         │
│    Political Violence:        [====|====] 8         │
│    ...                                               │
│                                                      │
│  📝 Assessment Notes                                │
│    Key Risk Factors: [text area]                    │
│                                                      │
│  [✅ Add/Update] [🔄 Clear] [📄 Export PDF]         │
├─────────────────────────────────────────────────────┤
│  📊 Threat Assessment Results                       │
│  ┌───────────────────────────────────────────────┐ │
│  │ Country: Venezuela                            │ │
│  │ Threat Level: HIGH (7.2/10)                  │ │
│  │ ...                                           │ │
│  └───────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────┤
│  🗂️ Saved Countries                                │
│  Select: [Venezuela ▼] [📋Load] [📊Report] [🗑️Del] │
│  ┌───────────────────────────────────────────────┐ │
│  │ Venezuela - HIGH (7.2)                        │ │
│  │ Colombia - ELEVATED (5.8)                     │ │
│  │ ...                                           │ │
│  └───────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone or Download
```bash
# Clone the repository
git clone https://github.com/yourusername/country-threat-assessment.git
cd country-threat-assessment

# Or download and extract the ZIP file
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**requirements.txt:**
```txt
reportlab>=4.0.0
```

### Step 3: Run the Application
```bash
python main.py
```

The application will automatically:
- Create a `data/` folder
- Initialize the SQLite database
- Display the main interface

---

## 🎯 Quick Start

### Adding Your First Country Assessment

1. **Enter Country Name**
   - Type the country name in the text field at the top

2. **Adjust Threat Indicators**
   - Use the sliders (1-10 scale) across 5 categories:
     - 📊 Political Stability (4 indicators)
     - 🛡️ Security Environment (4 indicators)
     - 💰 Economic Stability (4 indicators)
     - 👥 Social Indicators (4 indicators)
     - ⚠️ Illicit Markets & Criminal Activity (6 indicators)

3. **Add Assessment Notes** (Optional)
   - Key Risk Factors
   - Trend Analysis
   - Recommendations

4. **Save the Assessment**
   - Click **"✅ Add/Update Country"**
   - Data is automatically saved to the database

5. **Export to PDF**
   - Click **"📄 Export to PDF"**
   - Choose save location
   - Professional report generated instantly

---

## 📖 Usage Guide

### Loading Existing Countries

**Method 1: Dropdown Selection**
1. Select country from dropdown menu
2. Click **"📋 Load"** to populate the form
3. Click **"📊 Show Report"** to view assessment

**Method 2: Listbox**
1. Double-click any country in the list
2. Form automatically populates
3. Assessment displays in results panel

### Editing a Country
1. Load the country using either method above
2. Adjust any sliders or text fields
3. Click **"✅ Add/Update Country"**
4. Changes are saved immediately

### Deleting a Country
1. Select country from dropdown
2. Click **"🗑️ Delete"**
3. Confirm deletion
4. Country removed from database

### Exporting Reports

**Individual Country:**
- Load country → Click **"📄 Export to PDF"**
- Or select from dropdown → Click **"📄 Export PDF"**

**Bulk Export:** (Feature for future enhancement)
- Select multiple countries
- Export comparison report

### Clearing the Form
- Click **"🔄 Clear Form"** to reset all fields
- Useful when starting a new assessment

---

## 🗄️ Database Structure

### Location
```
your_project/
├── main.py
├── data/
│   └── country_threat_data.db  ← Your database is here
```

The database path is printed to console on startup:
```
📁 Database location: /full/path/to/data/country_threat_data.db
```

### Schema

**Table: `countries`**

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key (auto-increment) |
| `name` | TEXT | Country name (unique) |
| `ps_government_legitimacy` | INTEGER | Political stability indicator (1-10) |
| `ps_political_violence` | INTEGER | Political stability indicator (1-10) |
| `ps_institutional_strength` | INTEGER | Political stability indicator (1-10) |
| `ps_leadership_stability` | INTEGER | Political stability indicator (1-10) |
| `se_internal_conflict` | INTEGER | Security environment indicator (1-10) |
| `se_regional_security` | INTEGER | Security environment indicator (1-10) |
| `se_law_enforcement` | INTEGER | Security environment indicator (1-10) |
| `se_military_factors` | INTEGER | Security environment indicator (1-10) |
| `es_economic_performance` | INTEGER | Economic stability indicator (1-10) |
| `es_fiscal_health` | INTEGER | Economic stability indicator (1-10) |
| `es_trade_dependencies` | INTEGER | Economic stability indicator (1-10) |
| `es_infrastructure_resilience` | INTEGER | Economic stability indicator (1-10) |
| `si_social_cohesion` | INTEGER | Social indicators (1-10) |
| `si_human_development` | INTEGER | Social indicators (1-10) |
| `si_demographic_pressures` | INTEGER | Social indicators (1-10) |
| `si_information_environment` | INTEGER | Social indicators (1-10) |
| `im_drug_trade` | INTEGER | Illicit markets indicator (1-10) |
| `im_human_trafficking` | INTEGER | Illicit markets indicator (1-10) |
| `im_arms_trafficking` | INTEGER | Illicit markets indicator (1-10) |
| `im_financial_crimes` | INTEGER | Illicit markets indicator (1-10) |
| `im_cybercrime_operations` | INTEGER | Illicit markets indicator (1-10) |
| `im_state_response_capacity` | INTEGER | Illicit markets indicator (1-10) |
| `key_risk_factors` | TEXT | Assessment notes |
| `trend_analysis` | TEXT | Assessment notes |
| `recommendations` | TEXT | Assessment notes |
| `created_at` | TIMESTAMP | Record creation time |
| `updated_at` | TIMESTAMP | Last update time |

### Viewing Database Contents

**Using DB Browser for SQLite (Recommended):**
1. Download from https://sqlitebrowser.org/
2. Open → Browse to `data/country_threat_data.db`
3. View and edit data with GUI

**Using Command Line:**
```bash
cd data
sqlite3 country_threat_data.db
.tables
SELECT name, updated_at FROM countries;
.quit
```

**Using Python:**
```python
import sqlite3

conn = sqlite3.connect('data/country_threat_data.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM countries")
print([row[0] for row in cursor.fetchall()])
conn.close()
```

---

## 📊 Assessment Methodology

### Threat Categories & Weights

| Category | Weight | Indicators | Description |
|----------|--------|------------|-------------|
| **Political Stability** | 25% | 4 | Government legitimacy, violence, institutions, leadership |
| **Security Environment** | 20% | 4 | Internal conflict, regional security, law enforcement, military |
| **Economic Stability** | 20% | 4 | Economic performance, fiscal health, trade, infrastructure |
| **Illicit Markets** | 20% | 6 | Drug trade, trafficking, arms, financial crimes, cybercrime |
| **Social Indicators** | 15% | 4 | Social cohesion, human development, demographics, information |

### Scoring Formula

```
Category Score = (Sum of Indicators) / Number of Indicators

Weighted Category Score = Category Score × Category Weight

Total Threat Score = Sum of All Weighted Category Scores
```

**Example:**
```
Political Stability Indicators: [7, 8, 6, 7]
Category Score = (7+8+6+7)/4 = 7.0
Weighted Score = 7.0 × 0.25 = 1.75

[Repeat for all categories]

Total Threat Score = 1.75 + 1.4 + 1.2 + 1.3 + 0.9 = 6.55
```

### Threat Level Classification

| Score Range | Level | Color | Description |
|-------------|-------|-------|-------------|
| 1.0 - 2.0 | **LOW** | 🟢 Green | Stable with minimal risks |
| 2.1 - 4.0 | **MODERATE** | 🟡 Yellow | Some concerns but manageable |
| 4.1 - 6.0 | **ELEVATED** | 🔵 Blue | Significant risks requiring monitoring |
| 6.1 - 8.0 | **HIGH** | 🟠 Orange | Serious threats with potential instability |
| 8.1 - 10.0 | **EXTREME** | 🔴 Red | Critical threats, high crisis probability |

### Indicator Scales (1-10)

Most indicators use this interpretation:
- **1-3**: Low risk/threat
- **4-6**: Moderate risk/threat
- **7-8**: High risk/threat
- **9-10**: Extreme risk/threat

*Note: Some indicators like "Government Legitimacy" are inverted where 1=Low and 10=High.*

---

## 📄 PDF Export

### Features

✅ **Professional Formatting**
- Header with country name and date
- Color-coded threat level display
- Comprehensive category breakdowns
- Individual indicator scores
- Category averages and weighted scores

✅ **Assessment Notes Section**
- Key risk factors
- Trend analysis
- Recommendations

✅ **High-Quality Output**
- Uses ReportLab library
- Letter size (8.5" × 11")
- Print-ready format
- Branded styling

### Export Options

**Option 1: Export Current Form**
- Fill out the form
- Click **"📄 Export to PDF"** (top button)

**Option 2: Export Saved Country**
- Select country from dropdown
- Click **"📄 Export PDF"** (bottom button)

### File Naming Convention
```
CountryName_threat_assessment_YYYYMMDD.pdf

Example: Venezuela_threat_assessment_20241209.pdf
```

---

## ⚙️ Configuration

### Customizing Category Weights

Edit the `WEIGHTS` dictionary in the `CountryData` class:

```python
WEIGHTS = {
    'political_stability': 0.25,    # 25%
    'security_environment': 0.20,   # 20%
    'economic_stability': 0.20,     # 20%
    'social_indicators': 0.15,      # 15%
    'illicit_markets': 0.20         # 20%
}
# Total must equal 1.0 (100%)
```

### Adjusting Threat Level Ranges

Modify the `get_threat_level()` method:

```python
def get_threat_level(self) -> str:
    score = self.calculate_threat_score()
    if 1.0 <= score <= 2.5:  # Changed from 2.0
        return "LOW"
    elif 2.6 <= score <= 4.5:  # Changed from 2.1-4.0
        return "MODERATE"
    # ... etc
```

### Changing Colors

Edit the `get_threat_color()` method:

```python
colors_map = {
    "LOW": "#28a745",       # Green
    "MODERATE": "#ffc107",  # Yellow
    "ELEVATED": "#17a2b8",  # Cyan/Blue
    "HIGH": "#fd7e14",      # Orange
    "EXTREME": "#dc3545"    # Red
}
```

### Database Location

To change where the database is stored:

```python
# In DatabaseHandler.__init__()
data_dir = os.path.join(script_dir, 'my_custom_folder')
```

Or specify at initialization:
```python
db = DatabaseHandler(db_path='/path/to/my_database.db')
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "No module named 'reportlab'"
**Solution:**
```bash
pip install reportlab
```

#### 2. Database file not found
**Check:**
- Look in the `data/` folder in the same directory as `main.py`
- Console will print the exact path on startup
- Ensure you have write permissions

#### 3. PDF Export fails
**Possible causes:**
- No write permission in selected folder
- ReportLab not installed correctly
- Country not loaded into form

**Solution:**
```bash
pip install --upgrade reportlab
```

#### 4. Sliders not updating values
**This has been fixed in v2.0!**
- Labels now update via stored references
- If still having issues, ensure you're using the latest version

#### 5. Application won't start
**Check Python version:**
```bash
python --version  # Should be 3.7+
```

**Check dependencies:**
```bash
pip list | grep reportlab
```

#### 6. Data not saving
**Verify:**
- Check console for error messages
- Ensure `data/` folder exists
- Check file permissions
- Look for database lock files (`.db-journal`)

### Getting Help

1. Check the console output for error messages
2. Verify all dependencies are installed
3. Ensure you're running Python 3.7+
4. Check the database path in console output

---

## 💾 Backup & Migration

### Backing Up Your Data

**Quick Backup:**
```bash
cp -r data/ backups/backup_$(date +%Y%m%d)/
```

**Windows:**
```cmd
xcopy data backups\backup_%date:~-4,4%%date:~-10,2%%date:~-7,2% /E /I
```

**Automated Backup Script:**
```python
import shutil
from datetime import datetime

source = 'data/country_threat_data.db'
backup = f'backups/country_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
shutil.copy2(source, backup)
print(f"Backup created: {backup}")
```

### Migrating from Old JSON Version

If you have data in `country_threat_data.json`:

```python
import json
from main import DatabaseHandler, CountryData, PoliticalStabilityMetrics
# ... (import other metric classes)

# Load old JSON data
with open('country_threat_data.json', 'r') as f:
    old_data = json.load(f)

# Initialize new database
db = DatabaseHandler()

# Convert each country
for name, country_dict in old_data.items():
    country = CountryData(
        name=name,
        political_stability=PoliticalStabilityMetrics(**country_dict['political_stability']),
        # ... (reconstruct other categories)
    )
    db.save_country(country)
    print(f"Migrated: {name}")

print("Migration complete!")
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Bugs
1. Check existing issues first
2. Provide detailed description
3. Include error messages and screenshots
4. Specify Python version and OS

### Suggesting Features
- Open an issue with the "enhancement" label
- Describe the feature and use case
- Explain how it would benefit users

### Code Contributions
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Add docstrings to functions
- Comment complex logic
- Test thoroughly before submitting

---

## 📜 License

This project is licensed under the MIT License - see below for details.

```
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- **ReportLab** - PDF generation library
- **SQLite** - Embedded database engine
- **Tkinter** - Python GUI framework
- **Python Community** - For excellent documentation and support

---

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/country-threat-assessment/issues)
- **Email**: oaks.dustin@gmail.com
- **Documentation**: This README and inline code comments

---

## 🗺️ Roadmap

### Version 2.1 (Planned)
- [ ] Country comparison feature
- [ ] Historical tracking with charts
- [ ] Bulk PDF export
- [ ] Search and filter functionality

### Version 2.2 (Future)
- [ ] Data visualization dashboard
- [ ] Export to Excel format
- [ ] Import from CSV
- [ ] Multi-user support with authentication

### Version 3.0 (Long-term)
- [ ] Web-based version
- [ ] API integration for real-time data
- [ ] Machine learning threat predictions
- [ ] Mobile app companion

---

## ⭐ Star This Project

If you find this tool useful for your client work or threat assessments, please give it a star on GitHub!

---

**Last Updated**: December 9, 2025  
**Version**: 2.0 Enhanced  
**Status**: Production Ready ✅

---

## 📅 Version History

### v2.0 Enhanced (December 2025)
- Fixed scale label update mechanism
- Added professional PDF export functionality
- Implemented SQLite database backend
- Enhanced visual design with color-coded threat levels
- Improved data validation and error handling

### v1.0 Initial (2025)
- Basic threat assessment functionality
- JSON data storage
- Text-based reporting
