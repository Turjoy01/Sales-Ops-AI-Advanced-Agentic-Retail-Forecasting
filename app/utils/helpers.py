"""
Utility helper functions
"""
from datetime import datetime, timedelta

def format_date(date_obj: datetime) -> str:
    """Format datetime object to YYYY-MM-DD"""
    return date_obj.strftime('%Y-%m-%d')

def parse_date(date_str: str) -> datetime:
    """Parse YYYY-MM-DD string to datetime object"""
    return datetime.strptime(date_str, '%Y-%m-%d')

def get_date_range(start_date: str, end_date: str):
    """Generate list of dates between start and end"""
    start = parse_date(start_date)
    end = parse_date(end_date)
    
    delta = end - start
    return [format_date(start + timedelta(days=i)) for i in range(delta.days + 1)]
