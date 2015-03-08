import re
from datetime import datetime

def parse_court_names(soup):
    # Load list of courts and fips codes
    fips = [tag['value'] for tag in soup.find_all('input', 
        {'name':'courtFips'})]
    names = [tag['value'] for tag in soup.find_all('input', 
        {'name':'courtName'})]
    court_names = {}
    for f, c in zip(fips, names):
        court_names[f] = c
    return court_names

def parse_hearing_date_search(soup):
    cases = []
    rows = soup.find('table', {'class':'tableborder'}).find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if cells[0]['class'][0] == 'gridheader':
            continue
        cases.append({
            'details_url': cells[1].a['href'],
            'status': list(cells[6].stripped_strings)[0]
        })
    return cases

def next_button_found(soup):
    return soup.find('input', {'name': 'caseInfoScrollForward'}) is not None

def parse_case_details(soup):
    cells = list(soup.find('td', text=re.compile('Case Number')) \
                     .parent.find_all('td'))
    case_number = cells[1].text.strip()
    filed_date = datetime.strptime(cells[3].text.strip(), "%m/%d/%Y")
    
    cells = list(soup.find('td', text=re.compile('Name')) \
                     .parent.find_all('td'))
    name = cells[1].text.strip()
    
    cells = list(soup.find('td', text=re.compile('Case Type')) \
                     .parent.find_all('td'))
    case_type = cells[3].text.strip()
    offense_class = cells[5].text.strip()
    return {
        'case_number': case_number,
        'name': name,
        'filed_date': filed_date,
        'case_type': case_type,
        'offense_class': offense_class
    }
