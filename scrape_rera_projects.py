import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_project_details(project_url):
    response = requests.get(project_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    details = {}
    
    #Locating and extracting the required details
    details['GSTIN No'] = soup.find('span', id='ContentPlaceHolder1_lblGSTINNo').text.strip() if soup.find('span', id='ContentPlaceHolder1_lblGSTINNo') else "N/A"
    details['PAN No'] = soup.find('span', id='ContentPlaceHolder1_lblPan').text.strip() if soup.find('span', id='ContentPlaceHolder1_lblPan') else "N/A"
    details['Name'] = soup.find('span', id='ContentPlaceHolder1_lblPromoterName').text.strip() if soup.find('span', id='ContentPlaceHolder1_lblPromoterName') else "N/A"
    details['Permanent Address'] = soup.find('span', id='ContentPlaceHolder1_lblAddress').text.strip() if soup.find('span', id='ContentPlaceHolder1_lblAddress') else "N/A"
    
    return details

def main():
    base_url = "https://hprera.nic.in/PublicDashboard"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    project_links = []
    
    #Locating table containing registered projects
    table = soup.find('table', {'id': 'ContentPlaceHolder1_gvProjects'})
    rows = table.find_all('tr')
    
    #Get the first 6 project links"
    for row in rows[:6]: 
        view_application_link = row.find('a', text='View Application', href=True)
        if view_application_link:
            project_url = "https://hprera.nic.in/" + view_application_link['href']
            project_links.append(project_url)
    
    project_data = []
    
    for link in project_links:
        project_data.append(get_project_details(link))
    
    #Save as CSV
    df = pd.DataFrame(project_data)
    df.to_csv('registered_projects.csv', index=False)
    print("Data saved to registered_projects.csv")

if __name__ == "__main__":
    main()
