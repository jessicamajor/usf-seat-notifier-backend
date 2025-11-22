import requests
from bs4 import BeautifulSoup

def get_seats(crn: str, term: str) -> int | None:
    """
    Returns the number of remaining seats, or None if scraping fails.
    """
    url = (
        "https://usfonline.admin.usf.edu/pls/prod/"
        f"bwckschd.p_disp_detail_sched?term_in={term}&crn_in={crn}"
    )

    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
    except Exception as e:
        print("Error fetching CRN", crn, ":", e)
        return None

    soup = BeautifulSoup(r.text, "html.parser")

    seat_text = soup.find(string="Seats Remaining:")
    if not seat_text:
        print("Could not locate seat field for CRN", crn)
        return None

    try:
        seats_str = seat_text.find_next().text.strip()
        return int(seats_str)
    except Exception:
        print("Seat number parsing failed for CRN", crn)
        return None
