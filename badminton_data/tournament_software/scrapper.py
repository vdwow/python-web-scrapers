import requests
from bs4 import BeautifulSoup
import csv

def scrape_badminton_ranking(url, output_file):
    
    headers = {"User-Agent":"Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
                
        table = soup.find('table', class_='ruler')
        
        if table:
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write headers
                headers = ['Rank', 'Movement', 'Player', 'Member ID', 'Country', 'Confederation', 'Points', 'Tournaments']
                writer.writerow(headers)
                
                # Extract and write data rows
                for row in table.find_all('tr')[1:]:  # Skip the header row
                    cells = row.find_all('td')
                    if len(cells) >= 8:
                        rank = cells[0].text.strip()
                        movement = cells[1].text.strip()
                        player = cells[2].text.strip()
                        member_id = cells[2].find('a')['name'] if cells[2].find('a') else ''
                        country = cells[3].text.strip()
                        confederation = cells[4].text.strip()
                        points = cells[5].text.strip()
                        tournaments = cells[6].text.strip()
                        
                        writer.writerow([rank, movement, player, member_id, country, confederation, points, tournaments])
            
            print(f"Data has been successfully scraped and saved to {output_file}")
        else:
            print("No table found on the page.")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

# Usage
url = "https://www.tournamentsoftware.com/ranking/category.aspx?id=42307&category=472&C472FOC=&p=1&ps=100"
output_file = "badminton_rankings.csv"

scrape_badminton_ranking(url, output_file)