import requests

def test_range(start, end):
    print(f"Testing range: {start} to {end}")
    url = f"http://localhost:8000/api/v1/risk/analysis?start_date={start}&end_date={end}"
    try:
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Count: {len(data)}")
        if len(data) > 0:
            print(f"Dates returned: {data[0]['date']} to {data[-1]['date']}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 20)

# Test future range
test_range("2026-06-01", "2026-06-05")

# Test historical range
test_range("2017-01-01", "2017-01-05")
