from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from pdfkit.api import configuration
import pdfkit
import time
import os
import re
import shutil
import pandas as pd

# This application will crawl through the Press Releases published
# on the ACLU website and download each as a PDF.
# Then it will organize PDFs into folders by YYYY_MM and create
# a manifest of key metadata.


def MakeDate(date):
    month_dict = {
        "January": "01",
        "February": "02",
        "March": "03",
        "April": "04",
        "May": "05",
        "June": "06",
        "July": "07",
        "August": "08",
        "September": "09",
        "October": "10",
        "November": "11",
        "December": "12",
    }

    char_list = date.split()
    month = month_dict.get(char_list[0])
    day = char_list[1].replace(',', '')
    if int(day) < 10:
        day = f"0{day}"
    else:
        pass

    format_date = f"{char_list[2]}_{month}_{day}"
    return format_date


def MakeManifest(date, article):
    char_list = date.split()

    year = char_list[2]
    month = char_list[0]
    day = char_list[1].replace(',', '')
    if int(day) < 10:
        day = f"0{day}"
    else:
        pass
    output_manifest["Year"].append(year)
    output_manifest["Month"].append(month)
    output_manifest["Day"].append(day)
    output_manifest["Title"].append(article)


def OrganizeOutputs(directory):

    cwd = os.getcwd()
    src = os.path.join(cwd, directory)
    pdfs = os.listdir(src)

    for p in pdfs:
        destination = os.path.join(src, p[0:7])
        p_filepath = os.path.join(src, p)
        if p == f"output_manifest_{tyear}.csv" or p == f"error_log_{tyear}.csv":
            pass
        elif not os.path.exists(destination):
            os.makedirs(destination)
            shutil.move(p_filepath, destination)

        elif os.path.exists(destination):
            shutil.move(p_filepath, destination)
        else:
            pass


def LogError(issue, article):
    error_log["Issue"].append(issue)
    error_log["Article"].append(article)


def ReturnHome():
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.back()


tyear = input("Enter the year: ")
start_pg = input("Enter the start page: ")
end_pg = input("Enter the end page: ")

# Initiate webdriver...............
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(
    r".\chromedriver_win32\chromedriver.exe", options=chrome_options)

# Declare manifest for later printing to csv...............
output_manifest = {
    "Year": [], "Month": [], "Day": [], "Title": []
}

error_log = {"Issue": [], "Article": []}


output_folder = f"Press_Releases_{tyear}-{start_pg}-{end_pg}"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Page turner...............SET RANGE OF PAGES TO DOWNLOAD...............
for x in range(int(start_pg), int(end_pg)):

    url = f'https://www.aclu.org/search/a?page={str(x)}&f%5B0%5D=type%3Apress_release&f%5B1%5D=field_date%3A{tyear}'
    driver.get(url)

# Search for links on page...............
    links = driver.find_elements_by_tag_name('h3.title')

    articles = []

    for link in links:
        articles.append(link.text)

    for article in articles[0:11]:
        time.sleep(2)
        try:
            driver.find_element_by_link_text(article).click()
            time.sleep(2)

            driver.find_element_by_partial_link_text('Print').click()

            driver.switch_to.window(driver.window_handles[-1])

            # Scrape elements................

            print_view_url = driver.current_url

            field_date = driver.find_element_by_xpath(
                '/html/body/div[3]/article/div[1]').text
            header = driver.find_element_by_xpath(
                '/html/body/div[3]/article/header/h2').text

            # Create output pdf filename..........

            original_title = header.replace(' [1]', '')

            export_title = re.sub('[^a-zA-Z0-9 \n\.]', '', original_title)

            pdf_title = f"{MakeDate(field_date)} {export_title}.pdf"

            pdf_path = os.path.join(output_folder, pdf_title)

            # pdf printer .....................
            print("Now printing...")
            print("Page: " + str(x))
            print(print_view_url)
            print(pdf_title)

            path_wkhtmltopdf = r'.\wkhtmltopdf\bin\wkhtmltopdf.exe'

            config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
            try:
                pdfkit.from_url(print_view_url, pdf_path, configuration=config)

                # Log to output_manifest
                MakeManifest(field_date, original_title)
            except:
                print("NotLoggedToOutputManifest= " + pdf_title)
                issue = "NotLoggedToOutputManifest"
                LogError(issue, pdf_title)
                ReturnHome()
                continue

            # Take us back to the top..............
            ReturnHome()

        except NoSuchElementException:
            print("NoSuchElementException= " + article)
            issue = "NoSuchElement"
            LogError(issue, article)
            continue

# Print output_manifest CSV with metadata..............
df = pd.DataFrame(output_manifest)
df_error = pd.DataFrame(error_log)
print(df)

csv_path = os.path.join(output_folder, f"output_manifest_{tyear}.csv")
error_log_path = os.path.join(output_folder, f"error_log_{tyear}.csv")

df.to_csv(csv_path, index=False, encoding='utf-8-sig')
df_error.to_csv(error_log_path, index=False, encoding='utf-8-sig')

OrganizeOutputs(output_folder)
