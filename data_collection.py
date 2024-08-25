from playwright.sync_api import sync_playwright
import json
import time

def format_email(email):
    if email:
        return email.replace('ATharvardDOTedu', '@harvard.edu').replace('AT', '@').replace('DOT', '.')
    return 'N/A'

def scrape_faculty_profiles():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # URL of the Harvard Kennedy School faculty page
        url = 'https://www.hks.harvard.edu/faculty-profiles'
        page.goto(url)

        # Wait for the content to load
        page.wait_for_selector('.views-row')

        # Initialize a list to store faculty data
        faculty_list = []

        # Extract profile URLs
        faculty_elements = page.query_selector_all('.views-row a')
        profile_urls = [elem.get_attribute('href') for elem in faculty_elements if elem.get_attribute('href')]

        # Full URL format
        base_url = 'https://www.hks.harvard.edu'

        # Scrape each faculty profile
        for relative_url in profile_urls:
            profile_url = base_url + relative_url
            print(f"Scraping profile URL: {profile_url}")  # Debug print
            page.goto(profile_url)

            # Wait for some content to load, or use a more generic selector
            try:
                page.wait_for_selector('body', timeout=30000)  # Wait for the page body to be visible
                # Extract faculty details
                name = page.query_selector('h1').inner_text().strip() if page.query_selector('h1') else 'N/A'
                department = page.query_selector('.department').inner_text().strip() if page.query_selector('.department') else 'N/A'
                email_tag = page.query_selector('a[href^=mailto]')
                email = email_tag.get_attribute('href').replace('mailto:', '').strip() if email_tag else 'N/A'

                # Format email
                email = format_email(email)

                faculty_list.append({
                    'name': name,
                    'department': department,
                    'email': email,
                    'profile_url': profile_url,
                    'ratings': []  # Initialize ratings
                })

            except Exception as e:
                print(f"Error scraping {profile_url}: {e}")

            # Optionally add a delay to avoid overloading the server
            time.sleep(1)

        # Save faculty data to JSON file
        with open('harvard_faculty.json', 'w') as f:
            json.dump(faculty_list, f, indent=4)

        print("Faculty data has been successfully scraped and saved to 'harvard_faculty.json'.")

        # Close the browser
        browser.close()

if __name__ == "__main__":
    scrape_faculty_profiles()


