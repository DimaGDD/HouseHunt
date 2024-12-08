using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Support.UI;
using AngleSharp.Html.Parser;

class Program
{
    static void Main(string[] args)
    {
        var options = new ChromeOptions();
        options.AddArgument("--disable-blink-features=AutomationControlled");
        options.AddArgument("--disable-extensions");
        options.AddArgument("--disable-images");
        options.AddArgument("--no-sandbox");
        options.AddArgument("--disable-webgl");
        options.AddArgument("--disable-software-rasterizer");
        options.AddArgument("--disable-gpu");
        //options.AddArgument("--headless");
        options.AddArgument("--enable-unsafe-swiftshader");
        options.AddArgument("--disable-webrtc");
        options.AddArgument("--use-gl=desktop");
        options.AddArgument("--ignore-certificate-errors");
        options.AddArgument("--disable-web-security");
        options.AddArgument("--allow-running-insecure-content");
        options.AddArgument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.95 Safari/537.36");
        //options.AddArgument("--proxy-server=http://<proxy_address>:<proxy_port>");


        using (var driver = new ChromeDriver(options))
        {
            string url = "https://www.avito.ru/rostov-na-donu/kvartiry?context=H4sIAAAAAAAA_wEjANz_YToxOntzOjg6ImZyb21QYWdlIjtzOjc6ImNhdGFsb2ciO312FITcIwAAAA&district=349-350-351-353-354-355-356-357";
            driver.Manage().Timeouts().PageLoad = TimeSpan.FromSeconds(120);
            driver.Navigate().GoToUrl(url);
            Thread.Sleep(5000);

            var houses = new List<HouseData>();

            // Create CSV file
            string filePath = "houses.csv";
            using (var writer = new StreamWriter(filePath))
            {
                writer.WriteLine("Room_number,Squares,Living_squares,Floor,Place,Price");

                ScrollPage(driver);
                ParseData(driver, houses);

                // Navigate through pages
                while (true)
                {
                    var nextButton = driver.FindElements(By.CssSelector("a.styles-module-item-QkAj5.styles-module-item_arrow-gwJ04.styles-module-item_size_s-hLYd4.styles-module-item_link-rcqQ0"))
                                        .LastOrDefault();

                    if (nextButton != null)
                    {
                        nextButton.Click();
                        Thread.Sleep(5000);
                        ScrollPage(driver);
                        ParseData(driver, houses);
                    }
                    else
                    {
                        break;
                    }
                }

                // Write data to CSV
                foreach (var house in houses)
                {
                    writer.WriteLine($"{house.Rooms},{house.TotalArea},{house.LivingArea},{house.Floor},{house.Place},{house.Price}");
                }
            }

            Console.WriteLine("Data scraping completed. Check houses.csv.");
        }
    }

    static void ScrollPage(IWebDriver driver)
    {
        var js = (IJavaScriptExecutor)driver;
        long lastHeight = (long)js.ExecuteScript("return document.body.scrollHeight");

        while (true)
        {
            js.ExecuteScript("window.scrollTo(0, document.body.scrollHeight);");
            Thread.Sleep(300);
            long newHeight = (long)js.ExecuteScript("return document.body.scrollHeight");

            if (newHeight == lastHeight)
                break;

            lastHeight = newHeight;
        }
    }

    static void ParseData(IWebDriver driver, List<HouseData> houses)
    {
        var parser = new HtmlParser();
        var html = driver.PageSource;
        var document = parser.ParseDocument(html);

        var houseLinks = document.QuerySelectorAll("a.iva-item-sliderLink-Fvfau")
                                 .Select(link => link.GetAttribute("href"))
                                 .Where(href => !string.IsNullOrEmpty(href))
                                 .ToList();

        foreach (var link in houseLinks)
        {
            driver.Navigate().GoToUrl(link.StartsWith("http") ? link : $"https://www.avito.ru{link}");
            Thread.Sleep(3000);

            var detailHtml = driver.PageSource;
            var detailDocument = parser.ParseDocument(detailHtml);

            var houseData = new HouseData();

            // Parse parameters
            var paramsList = detailDocument.QuerySelectorAll("li.params-paramsList__item-_2Y2O");
            foreach (var param in paramsList)
            {
                var label = param.QuerySelector("span")?.TextContent.Trim();
                var value = param.TextContent.Split(":")[1]?.Trim();

                if (label == null || value == null)
                    continue;

                if (label.Contains("Количество комнат"))
                    houseData.Rooms = value.Contains("студия") ? 0 : int.Parse(value.Split(' ')[0]);
                else if (label.Contains("Общая площадь"))
                    houseData.TotalArea = float.Parse(value.Replace("\u00A0", "").Replace("м²", "").Trim());
                else if (label.Contains("Жилая площадь"))
                    houseData.LivingArea = float.Parse(value.Replace("\u00A0", "").Replace("м²", "").Trim());
                else if (label.Contains("Этаж"))
                    houseData.Floor = int.Parse(value.Split(' ')[0]);
            }

            // Parse price and place
            var priceElement = detailDocument.QuerySelector("span.styles-module-size_xxxl-GRUMY");
            houseData.Price = priceElement?.TextContent.Replace("\xa0", "").Trim() ?? "N/A";

            var placeElement = detailDocument.QuerySelectorAll("span")
                                              .FirstOrDefault(x => x.TextContent.Contains("р-н"));
            houseData.Place = placeElement?.TextContent.Split()[1] ?? "N/A";

            houses.Add(houseData);
        }
    }
}

public class HouseData
{
    public int Rooms { get; set; } = -1;
    public float TotalArea { get; set; } = -1;
    public float LivingArea { get; set; } = -1;
    public int Floor { get; set; } = -1;
    public string Place { get; set; } = "N/A";
    public string Price { get; set; } = "N/A";
}
