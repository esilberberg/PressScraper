# PressScraper

ABOUT:

PressScraper v3.0 crawls through the pages of Press Releases published on the ACLU website and downloads each as a PDF. PDFs are downloaded to the folder "Press_Releases_YYYY" which is created when the script starts. These PDFs are named according to ACLU Archives and Records department convetion of "YYYY_MM title of release.pdf." After completing the downloads, the app organizes the PDFs into folders by month, creates a manifest (CSV file) containing key metadata, and an error log (CSV file).

----------------------------------------------------

DEPENDENCIES:

chromedriver_win32 and wkhtmltopdf must be in the same director as press_scraper.py.

chromedriver_win32 documentation = https://chromedriver.chromium.org/home

wkhtmltopdf documentation = https://wkhtmltopdf.org/

----------------------------------------------------

USAGE NOTES:

On running, the script will prompt for year, start page, and end page. Remember, if you select pages 1-21, the program will download all documents on page 20 and stop once it reaches page 21, thus nothing on page 21 will download.

It is advisable to download in 30 page batches. This way if there is an issue, you won't loose the organization, manifest, and error log which are produced at the end of the program.

----------------------------------------------------

ERROR LOG:

NoSuchElement, This means that the chromedriver could not find the press release link on the website. User should search for this article on the ACLU website and manually download and catalog.

NotLoggedToOutputManifest, Sometimes wkhtmltopdf did create a PDF and failed to register the download on the output_manifest. Sometimes the entire print to PDF process failed. Either way, users should verify that the PDF did download and see if it was logged to the output_manifest. Users will need to download and catalog or simply catalog these articles.
