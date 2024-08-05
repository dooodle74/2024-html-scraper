import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_image_urls_from_pages(csv_file):
    # Read the CSV file
    data = pd.read_csv(csv_file)

    images = []

    # Loop through each row in the CSV
    count = 0
    for index, row in data.iterrows():
        title = row['Name']
        page_link = row['Link']

        # Send a GET request to the URL
        response = requests.get(page_link)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the div with the specific class
            target_div = soup.find('div', class_='col-lg-12 col-md-4 col-6')
            
            # Check if the div was found
            if target_div:
                # Find the first <img> tag within the div
                img_tag = target_div.find('img')
                
                if img_tag and 'src' in img_tag.attrs:
                    img_url = img_tag['src']
                    
                    # If the image URL is relative, make it absolute
                    if not img_url.startswith(('http://', 'https://')):
                        img_url = requests.compat.urljoin(page_link, img_url)
                    
                    # Append the title and image URL to the list
                    images.append((title, img_url))
                    count += 1
                else:
                    print(f'No image found for title: {title}')
            else:
                print(f'Target div not found for title: {title}')
        else:
            print(f'Failed to retrieve the webpage for title: {title}')
        
    fill = 4 -  (count % 4)
    if fill != 4:
        for x in range (fill):
            images.append(('',''))
    
    return images

def generate_html(images, output_file, pageTitle, pageSubtitle):
    # Start the HTML file
    html_content = '''
    <html>
    <head>
        <style>
            body {
                max-width: 90%;
                margin: 40px auto;
            }
            .gallery {
                display: flex;
                flex-wrap: wrap;
            }
            .gallery-item {
                flex: 1 1 23%;
                margin: 1%;
                text-align: center;
            }
            .gallery-item img {
                max-width: 100%;
                height: auto;
            }
        </style>
    </head>
    <body>
    '''

    html_content += f'''
    <h2>{pageTitle}</h2>
    <p>{pageSubtitle}</p>
        <div class="gallery">
    '''

    # Add images to the HTML
    for title, img_url in images:
        html_content += f'''
        <div class="gallery-item">
            <h3>{title}</h3>
            <img src="{img_url}" alt="{title}">
        </div>
        '''
    
    # End the HTML file
    html_content += '''
        </div>
    </body>
    </html>
    '''

    # Write the HTML content to the output file
    with open(output_file, 'w') as file:
        file.write(html_content)
    
    print(f'HTML file generated successfully: {output_file}')


input_directory = 'C:\\vscode\\2024-html-scraper\\csvfiles\\'
output_directory = 'C:\\vscode\\2024-html-scraper\\pdfs\\'
category_names = ['1_vectored_thrust', '2_hover_bikes_personal_flying_devices', '3_lift_cruise', '4_wingless', '5_electric_rotorcraft']

category_titles = [('Vectored Thrust', 'An eVTOL aircraft that uses any of its thrusters for lift and cruise.'),
                   ('Hover Bikes/Personal Flying Devices', 'These single-person eVTOL aircraft are considered to be in the general class of hover bikes or personal flying devices with the primary differentiation being that the pilot sits on a saddle or is standing, or something similar. Nearly all are multicopter-type wingless configurations.'),
                   ('Lift + Cruise', 'Completely independent thrusters used for cruise vs. for lift without any thrust vectoring.'),
                   ('Wingless (Multicopter)', 'No thruster for cruise – only for lift.'),
                   ('Electric Rotorcraft', 'An eVTOL aircraft that utilizes a rotor, such as an electric helicopter or electric autogyro.')
                   ]

for i in range (5):
    category_name = category_names[i]
    title = category_titles[i][0]
    subtitle = category_titles[i][1]

    csv_file = input_directory + category_name + '.csv'

    # Fetch image URLs from the pages
    images = fetch_image_urls_from_pages(csv_file)

    # Generate HTML file
    output_file = output_directory + category_name + '.html'
    generate_html(images, output_file, title, subtitle)