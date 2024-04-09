const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  // Set viewport size
  await page.setViewport({ width: 800, height: 600 });

  // Navigate to the HTML file passed as an argument
  const htmlFilePath = process.argv[2];
  await page.goto(`file://${htmlFilePath}`, { waitUntil: 'networkidle0' });

  // Get the dimensions of the HTML content
  const dimensions = await page.evaluate(() => {
    const body = document.querySelector('body');
    return {
      width: body.scrollWidth,
      height: body.scrollHeight,
      deviceScaleFactor: window.devicePixelRatio,
    };
  });

  // Set the viewport to match the HTML content size
  await page.setViewport({ width: dimensions.width, height: dimensions.height, deviceScaleFactor: dimensions.deviceScaleFactor });

  // Take a screenshot of the HTML content
  await page.screenshot({ path: 'output.png', fullPage: true });

  await browser.close();
})();


import subprocess

def convert_html_to_image(html_file_path):
    try:
        subprocess.run(["node", "htmlToImage.js", html_file_path], check=True)
        print("HTML file converted to image successfully.")
    except subprocess.CalledProcessError as e:
        print("Error occurred while converting HTML to image:", e)

if __name__ == "__main__":
    html_path = input("Enter the path to the HTML file: ")
    convert_html_to_image(html_path)
