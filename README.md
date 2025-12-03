# TradeForge 📈

A powerful Technical Analysis Platform and API built with FastAPI that provides real-time stock data, technical indicators, and interactive charting for informed trading decisions.

🌐 Live Demo: https://tradeforgeweb-production.up.railway.app/

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Redis](https://img.shields.io/badge/Redis-Caching-red.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- 🔴 **Real-time Stock Data** - Live prices and updates from yfinance
- 📊 **Technical Indicators** - SMA (5, 10, 20, 50, 100, 200 days)
- 📉 **Interactive Charts** - Chart.js visualizations with multiple indicators
- ⚡ **Redis Caching** - Fast data retrieval with 60-second cache
- 📄 **Pagination Support** - Efficient handling of large datasets
- 🌍 **Multi-Market Support** - Indian stocks (BSE) and international markets

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Redis server
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/RajNair06/tradeforge_web.git
cd tradeforge_web

# Navigate to the backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Start Redis server (if not already running)
redis-server

# Run the application
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## 📚 API Endpoints

### 1. Latest Technical Features
Get the latest technical indicators and price data for a specific stock.

```http
GET /latest-features/{symbol}
```

**Example:**
```bash
curl http://localhost:8000/latest-features/TCS.BO
```

**Response:**
```json
{
  "symbol": "TCS.BO",
  "latest_features": {
    "basic_info": {
      "price": 3105.70,
      "timestamp": "2025-11-13 12:49:46"
    },
    "technical_indicators": {
      "sma_20": 3033.66,
      "sma_50": 3031.65,
      "sma_200": 3326.27
    }
  }
}
```

### 2. Historical Data
Retrieve historical stock data with pagination and caching.

```http
GET /historical-data/{symbol}?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&offset=0&limit=50
```

**Parameters:**
- `symbol` - Stock symbol (e.g., TCS.BO, AAPL)
- `start_date` - Start date (YYYY-MM-DD)
- `end_date` - End date (YYYY-MM-DD)
- `offset` - Pagination offset (default: 0)
- `limit` - Results per page (default: 50)

**Example:**
```bash
curl "http://localhost:8000/historical-data/TCS.BO?start_date=2025-01-01&end_date=2025-11-13&limit=100"
```

**Features:**
- ✅ Redis caching (60 seconds)
- ✅ Automatic data freshness
- ✅ Efficient pagination

### 3. Interactive Chart
Interactive Chart.js visualization with technical indicators.

```http
GET /plotting/{symbol}/live?start_date=YYYY-MM-DD&use_cache=true
```

**Parameters:**
- `symbol` - Stock symbol
- `start_date` - Start date (YYYY-MM-DD)
- `use_cache` - Use cached data (default: true)

**Example:**
```bash
curl "http://localhost:8000/plotting/TCS.BO/live?start_date=2025-10-01"
```

**Features:**
- ✅ Multiple SMA overlays (20, 50, 100, 200)
- ✅ Price lag indicators (1, 2, 3 days)
- ✅ Current values display
- ✅ Responsive and interactive

## 📊 Supported Symbols

### Indian Stocks (BSE)
- `TCS.BO` - Tata Consultancy Services
- `RELIANCE.BO` - Reliance Industries
- `HDFCBANK.BO` - HDFC Bank
- `INFY.BO` - Infosys

### International Stocks
- `AAPL` - Apple Inc.
- `TSLA` - Tesla Inc.
- `MSFT` - Microsoft
- `GOOGL` - Alphabet (Google)

## 🛠️ Technical Stack

- **Backend:** FastAPI
- **Database/Cache:** Redis
- **Data Source:** yfinance
- **Visualization:** Chart.js
- **Frontend:** Bootstrap 5, Font Awesome

## 📈 Technical Indicators

The platform calculates and provides:

- **Simple Moving Averages (SMA):** 5, 10, 20, 50, 100, 200 days
- **Price Lags:** 1, 2, 3 day historical prices
- **Real-time Updates:** Live price data from market sources

## 🔧 Configuration

Configure Redis connection and other settings in your environment:

```python
# Example configuration
REDIS_HOST = "localhost"
REDIS_PORT = 6379
CACHE_EXPIRY = 60  # seconds
```

## 📝 Usage Examples

### Python
```python
import requests

# Get latest features
response = requests.get("http://localhost:8000/latest-features/TCS.BO")
data = response.json()
print(f"Current price: {data['latest_features']['basic_info']['price']}")

# Get historical data
response = requests.get(
    "http://localhost:8000/historical-data/AAPL",
    params={
        "start_date": "2025-01-01",
        "end_date": "2025-11-13",
        "limit": 100
    }
)
historical_data = response.json()
```

### JavaScript
```javascript
// Fetch latest features
fetch('http://localhost:8000/latest-features/TCS.BO')
  .then(response => response.json())
  .then(data => console.log(data));

// Fetch historical data
fetch('http://localhost:8000/historical-data/AAPL?start_date=2025-01-01&end_date=2025-11-13')
  .then(response => response.json())
  .then(data => console.log(data));
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.




## 👨‍💻 Author

**Raj Nair**

- GitHub: [@RajNair06](https://github.com/RajNair06)
- Project Link: [TradeForge](https://github.com/RajNair06/tradeforge_web)



⭐ If you find this project useful, please consider giving it a star on GitHub!