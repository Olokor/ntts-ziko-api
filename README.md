# NTTS Digital Receipt Core Engine
**Ziko Eats Order API** | Back End Web Dev Track - Week 1

A RESTful API that powers the checkout flow for Ziko Eats — accepting orders, calculating totals, and returning structured digital receipts.

---

## Stack
- **Python 3.12** + **Flask**
- Deployed on **Render** (free tier)
- Containerised with **Docker**

---

## Local Setup

### 1. fork the repo
```bash
https://github.com/Olokor/ntts-ziko-api
cd ntts-ziko-api
```

### 2. Create virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables
```bash
cp .env.example .env
```

### 4. Run the server
```bash
python app.py
```

Server starts at `http://localhost:5000`

---

## Run with Docker

```bash
docker build -t ntts-ziko-api .
docker run -p 5000:5000 --env-file .env ntts-ziko-api
```

---

## API Endpoints

### GET /api/health
Returns server health status.

**curl:**
```bash
curl https://ntts-ziko-api.render.com/api/health
```

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2026-06-07T12:00:00Z",
  "service": "ntts-order-api"
}
```

---

### POST /api/orders
Accepts an order and returns a digital receipt.

**curl:**
```bash
curl -X POST https://ntts-ziko-api.render.com/api/orders \
  -H "Content-Type: application/json" \
  -d '{"product_name": "Spicy Chicken Pizza", "quantity": 2, "unit_price": 4500.00}'
```

**Request Body:**
```json
{
  "product_name": "Spicy Chicken Pizza",
  "quantity": 2,
  "unit_price": 4500.00
}
```

**Response:**
```json
{
  "status": "success",
  "receipt": {
    "order_id": "550e8400-e29b-41d4-a716-446655440000",
    "product_name": "Spicy Chicken Pizza",
    "quantity": 2,
    "unit_price": 4500.00,
    "total": 9000.00,
    "currency": "NGN"
  }
}
```

---

### GET /docs  or  GET /api-docs
Returns full API documentation in JSON format, including curl examples for your live base URL.

---

## Deploying to Render

1. Push this repo to GitHub (public)
2. Go to [render.com](https://render.com) and create a new **Web Service**
3. Connect your GitHub repo
4. Set the following:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT app:app`
   - **Environment Variables:** add `SERVICE_NAME=ntts-order-api`
5. Deploy and copy your live URL

---

## Team Vibes
Built for **NTTS Back End Web Dev Track - Week 1**

#NTTSBackEndDevTrack #TechTalentSpotlight #MTA