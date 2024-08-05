import csv
import re

# Function to extract name and link from a line
def extract_name_and_link(line):
    match = re.search(r'<a href="(.*?)">(.*?)</a>', line)
    if match:
        link = match.group(1)
        name = match.group(2)
        return name, link
    return None, None

# Function to convert text file to CSV
def convert_txt_to_csv(input_file, output_file):
    with open(input_file, 'r') as txt_file, open(output_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Name', 'Link'])  # Write header

        for line in txt_file:
            name, link = extract_name_and_link(line.strip())
            if name and link:
                csv_writer.writerow([name, link])


input_directory = 'C:\\vscode\\2024-html-scraper\\textdocs\\'
output_directory = 'C:\\vscode\\2024-html-scraper\\csvfiles\\'

category_names = ['1_vectored_thrust', '2_hover_bikes_personal_flying_devices', '3_lift_cruise', '4_wingless', '5_electric_rotorcraft']

for category_name in category_names:
    input_file = input_directory + category_name + '.txt'
    output_file = output_directory + category_name + '.csv'
    convert_txt_to_csv(input_file, output_file)