## Installation Instructions

If you are new to Python or Jupyter, follow these steps in a terminal from the project folder.

1. Open the project folder in VS Code or GitHub Codespaces.
2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate it:

```bash
source .venv/bin/activate
```

4. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Run the Streamlit app

From the project folder, run:

```bash
```

In GitHub Codespaces, open the forwarded port shown by Streamlit. In the Ports panel, make the port **Public**, then select **Open in Browser**. Enter a ticker such as `MU` or `GOOG`, choose an analysis, and click **Run**.

## Save and view previous analyses

After an analysis is displayed, click **Save Analysis**. Nimbus writes a Markdown file
to `analyses-data/` at the project root. The filename includes the ticker, analysis
type, and a UTC timestamp. The folder is created automatically and is ignored by Git,
so saved analyses remain local to the machine running the app.

The **Previous Analyses** section lists saved files newest first. Select one and click
**Show** to open its rendered Markdown in a pop-up. Selecting a file alone does not
open it. To verify the feature in Codespaces:

1. Run the app using the command above and save an analysis.
2. Confirm that a new `.md` file appears in `analyses-data/`.
3. Refresh the app, select the file under **Previous Analyses**, and click **Show**.

The same steps work on an EC2 instance after cloning the project, installing
`requirements.txt`, and starting Streamlit from any directory. Storage is resolved
relative to `src/`, not the launch directory, and uses the instance's existing disk;
no EBS volume or CloudFormation change is required. Files saved on Codespaces are
not automatically copied to EC2 (or vice versa).

5. Start Jupyter Notebook:

```bash
jupyter notebook
```

6. In the browser, open the notebook files inside the `notebooks/` folder and run the cells one by one.

If you are using VS Code, you can also open a notebook and run the cells from the editor instead of starting Jupyter in the browser.

## Code Walkthrough

This repository is a beginner-friendly starter project for working with financial data using Python. The notebooks demonstrate the original data-fetching logic, while `src/analysis.py` contains reusable functions and `src/app.py` displays their results in Streamlit.

### Main folders and files

- `lessons/` — lesson notes and step-by-step instructions for the course.
- `notebooks/` — interactive Python notebooks used for exploring stock data.
- `requirements.txt` — lists the Python libraries the project needs.
- `README.md` — project overview and course context.

### Important notebooks

- `notebooks/filings.ipynb` — looks up company financial statements such as income statements, balance sheets, and cash flow. It uses `yfinance` to fetch the latest financial data.
- `notebooks/news.ipynb` — pulls recent news for a stock ticker and prints article titles and summaries.
- `notebooks/stock_price_ratings.ipynb` — gets the latest stock price and analyst recommendation data for a company.

### How the application works

The project starts by installing the needed libraries from `requirements.txt`. Then you open a notebook in `notebooks/` and run each code cell. Each notebook defines a small function, such as `get_financials()` or `get_news()`, and then calls that function with a stock ticker like `MU` or `GOOG`.

The code uses `yfinance`, which connects to Yahoo Finance and retrieves real market data. The notebook then prints the results so you can inspect the information in a simple, readable way. This is the foundation for building a larger app later, where the same data could be displayed in a web interface or dashboard.

 # Cloud Computing for Economics: Starter Repo 

  This repository contains the starter code and lesson materials for building a Python financial-data application and deploying it to AWS.

  Students will use GitHub Codespaces, Python, Jupyter notebooks, Streamlit, Git, and AWS CloudFormation.

  ## Learning outcomes

  By the end of the course, you will be able to:

   1.  Build and deploy an analytics application with a simple Front End / back-end (using AI)
   2.  Host and share the application on a cloud platform (e.g., AWS EC2 or similar) so that others can access it securely over the web
   3.  Integrate data sources and APIs into the app to enable interactive, real-time analytics
   4.  Apply cloud architecture best practices, ensuring the app demonstrates scalability, performance efficiency, and basic security
   5.  Showcase your work on GitHub as part of a personal portfolio, demonstrating practical cloud and analytics skills through a shareable, explorable repository

  
  ## Repository structure

  ```text
  .
  ├── lessons/          # Step-by-step course instructions
  ├── notebooks/        # Starter financial-data notebooks
  ├── requirements.txt  # Python dependencies
  └── README.md         # Course overview