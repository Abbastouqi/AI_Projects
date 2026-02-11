import requests
from bs4 import BeautifulSoup

POLICIES_URL = 'https://riphahsahiwal.edu.pk/rules-and-policies/'

def fetch_policies():
    try:
        response = requests.get(POLICIES_URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        policies = {
            'url': POLICIES_URL,
            'title': 'Rules and Policies',
            'categories': [],
            'details': []
        }
        
        policy_cards = soup.find_all('div', class_='gdlr-core-pbf-column')
        for card in policy_cards:
            link = card.find('a')
            title_elem = card.find('h3', class_='gdlr-core-title-item-title')
            if link and title_elem:
                policy_name = title_elem.get_text(strip=True)
                policy_url = link.get('href', '')
                if policy_name and policy_url:
                    policies['categories'].append({'name': policy_name, 'url': policy_url})
        
        toggle_boxes = soup.find_all('div', class_='gdlr-core-toggle-box-item-tab')
        for box in toggle_boxes:
            title_elem = box.find('h4', class_='gdlr-core-toggle-box-item-title')
            content_elem = box.find('div', class_='gdlr-core-toggle-box-item-content')
            if title_elem:
                policy_title = title_elem.get_text(strip=True)
                policy_content = content_elem.get_text(strip=True) if content_elem else ''
                policies['details'].append({
                    'title': policy_title,
                    'content': policy_content[:500] + '...' if len(policy_content) > 500 else policy_content
                })
        
        return policies
    except Exception as e:
        return {'error': str(e), 'url': POLICIES_URL, 'message': 'Failed to fetch policies'}

def get_policy_summary():
    policies = fetch_policies()
    if 'error' in policies:
        return f"Error: {policies['message']}"
    summary = f"University Policies\nSource: {policies['url']}\n\n"
    if policies['categories']:
        summary += 'Policy Categories:\n'
        for i, cat in enumerate(policies['categories'], 1):
            summary += f"{i}. {cat['name']}\n"
    return summary

def search_policy(keyword):
    policies = fetch_policies()
    if 'error' in policies:
        return []
    results = []
    keyword_lower = keyword.lower()
    for cat in policies.get('categories', []):
        if keyword_lower in cat['name'].lower():
            results.append({'type': 'category', 'name': cat['name'], 'url': cat['url']})
    for detail in policies.get('details', []):
        if keyword_lower in detail['title'].lower() or keyword_lower in detail['content'].lower():
            results.append({'type': 'detail', 'title': detail['title'], 'content': detail['content']})
    return results

def get_specific_policies():
    return {
        'Admission Process': 'Applications will be invited through advertisements.',
        'Attendance Policy': 'Students must attend all classes.',
        'Transfer of Credits': 'Credits may be transferred from recognized institutions.',
        'Medium of Instructions': 'English is the medium of instruction.',
        'Harassment Policy': 'HEC Sexual Harassment Policy is enforced.',
        'Disability Policy': 'Equal opportunities for students with disabilities.',
        'QEC Policy': 'Quality standards are maintained.'
    }
