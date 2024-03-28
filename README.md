<p align="center">
  <img width="460" height="300" src="https://github.com/rakshit-ayachit/Chandlery/assets/129822642/36c68c20-5485-4e4e-bb36-6fdd70c33582">
</p>

# Chandlery: Illuminating Market Signals

**[Chandlery](https://huggingface.co/spaces/rakadon/Chandlery-app)** is a Python tool designed for comprehensive candlestick pattern analysis to Zerodha's stock market data. By employing an alternative approach to accessing Zerodha's data, Chandlery empowers users to perform in-depth analysis of candlestick patterns without direct API integration. This tool facilitates historical data retrieval, pattern identification, and signal significance analysis, enabling users to make informed decisions in stock trading based on advanced technical analysis techniques. Chandlery provides a user-friendly interface for visualizing candlestick patterns, offering valuable insights into stock market trends and potential trading opportunities.

Check it out here: **[Chandlery](https://huggingface.co/spaces/rakadon/Chandlery-app)**

## Table of Contents

- [Key Features](#key-features)
- [Significance and Impact](#significance-and-impact)
- [Prerequisites](#prerequisites)
- [Getting Started and Running the Application](#getting-started-and-running-the-application)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [Contributors and Contact](#contributors-and-contact)
- [Project Status](#project-status)
- [License](#license)
- [Disclaimer](#disclaimer)
  
## Key Features
- **Candlestick pattern identification**
- **Historical data retrieval for specified stocks**
- **Signal significance analysis**
- **User-friendly interface for pattern visualization**

## Significance and Impact
The significance and impact of the project lie in its ability to democratize access to valuable stock market data and technical analysis tools. By utilizing Zerodha's data, Chandlery enables users, particularly traders and investors, to perform sophisticated candlestick pattern analysis without direct API integration. This access fosters greater inclusivity, allowing a wider range of individuals to harness the power of advanced technical analysis for making informed decisions in stock trading.

Additionally, Chandlery's capability to retrieve historical data, identify patterns, and analyze signal significance contributes to a more informed and data-driven approach to trading. This empowers users to spot trends, understand market behavior, and potentially capitalize on emerging opportunities in the stock market.

Overall, the project's impact lies in democratizing access to sophisticated technical analysis tools, fostering a more level playing field in the realm of stock trading, and empowering users with the insights necessary to make informed decisions in their investment strategies.

## Prerequisites

Before you get started, make sure you have the following prerequisites installed on your system:

- **Python**: You can download Python from the [official Python website](https://www.python.org/downloads/).
- **Git**: To clone the repository, you'll need Git. You can download it from [here](https://git-scm.com/downloads).
- **Zerodha-Kite Account**: Access to a [Zerodha account](https://kite.zerodha.com/) is required to obtain the necessary authentication tokens for data access.
- **Easy Cookie Editor Google Extension**: : Install the [Easy Cookie Editor extension](https://chromewebstore.google.com/detail/easy-cookie-editor/lidhbccbajehjnpfjpnamoiemcnhhnki) on your Google Chrome browser. This extension facilitates the management and editing of cookies, which is crucial for authentication.

## Getting Started and Running the Application

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/rakshit-ayachit/Chandlery.git

2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt


3. **Login to your Kite-Zerodha account and open the Easy Cookie Editor extension and copy the value of the enctoken into the enctoken.txt:**

4. **Run the application:**
   ```bash
   python -m run chandlery_stream.py
5. **Select a stock, interval, and duration to analyze candlestick patterns.**

## Screenshots
![chandlery_stream · Streamlit - Google Chrome 12_29_2023 7_48_05 PM](https://github.com/rakshit-ayachit/Chandlery/assets/129822642/c8771405-d612-4dc1-8260-98cb3660148a)
![chandlery_stream · Streamlit - Google Chrome 12_29_2023 7_48_25 PM](https://github.com/rakshit-ayachit/Chandlery/assets/129822642/9301282c-e11d-4506-9d47-316ce73328f4)


## Contributing

 We welcome your contributions to [Chandlery](https://github.com/rakshit-ayachit/Chandlery)! Start by forking the repository, cloning it to your local machine, creating a new branch, making your changes, and committing them. Then, push your changes to your fork on GitHub and create a pull request. Your contributions will be reviewed and, once approved, merged into the main project. Thank you for your help!

## Contact

Feel free to contact me ([Rakshit Ayachit](mailto:rakshit@ayachit@gmail.com)) for further information or support regarding this project.


## Project Status

This project is currently under active development, and new features and improvements are being added regularly. While it is functional, there may be occasional updates that could affect usage. We appreciate your understanding and patience as we work to enhance this application. If you encounter any issues or have suggestions, please [open an issue](https://github.com/rakshit-ayachit/Chandlery/issues). Your feedback is valuable to us!


## License

This project is licensed under the [MIT LICENSE](LICENSE).

## Disclaimer
Please note that **[Chandlery](https://huggingface.co/spaces/rakadon/Chandlery-app)** is currently under development and may not fully function for all market scenarios, particularly for sideways trends. It is intended for personal use only and should not be considered as a professional trading strategy or financial advice. Users are encouraged to seek guidance from financial experts before executing any trades based on the information provided by this application. The developer cannot be held responsible for any financial losses incurred by using this app.

       


