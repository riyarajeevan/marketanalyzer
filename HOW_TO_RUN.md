# How to Run the App

Super simple - just follow these steps:

## Step 1: Install Dependencies

Make sure you have all the packages installed:

```bash
pip install -r requirements.txt
```

Or if you just need the new ones:

```bash
pip install streamlit plotly
```

## Step 2: Run the App

Just run this command:

```bash
streamlit run app.py
```

That's it! The app will automatically open in your browser at `http://localhost:8501`

## Alternative: Use the Script

You can also use the helper script:

```bash
./run.sh
```

Or on Windows:

```bash
streamlit run app.py
```

## What You'll See

Once it's running, you'll see a dashboard with three pages:

1. **Stock Analysis** - look at individual stocks, see price charts and returns
2. **Compare Stocks** - compare multiple stocks side by side
3. **Risk Metrics** - calculate some basic risk stuff like volatility

Just pick a page from the sidebar and start exploring!

## Troubleshooting

**Port already in use?**
- The app runs on port 8501 by default
- If it's taken, Streamlit will ask if you want to use a different port
- Or kill the process: `lsof -ti:8501 | xargs kill` (Mac/Linux)

**Import errors?**
- Make sure you installed all dependencies: `pip install -r requirements.txt`
- Check that you're in the project directory

**No data showing?**
- Make sure you have internet connection (Yahoo Finance needs it)
- Check that the ticker symbol is correct (e.g., "AAPL" not "apple")

That's it - have fun exploring!

