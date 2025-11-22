import requests
from bs4 import BeautifulSoup

def get_seats(crn: str, term: str) -> int:
    url = f"https://usfonline.admin.usf.edu/pls/prod/bwckschd.p_disp_detail_sched?term_in={term}&crn_in={crn}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    seat_text = soup.find(string="Seats Remaining:")
    if not seat_text:
        return -1  # couldn't find it

    seats_str = seat_text.find_next().text.strip()
    try:
        return int(seats_str)
    except ValueError:
        return -1
