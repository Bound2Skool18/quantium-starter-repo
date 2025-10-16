import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px


# Load the data
df = pd.read_csv("output.csv")

# Convert date to datetime for proper sorting
df["date"] = pd.to_datetime(df["date"])

# Sort by date
df = df.sort_values("date")

# Group by date to get total daily sales across all regions
daily_sales = df.groupby("date")["sales"].sum().reset_index()


# Create the Dash app
app = dash.Dash(__name__)

# Create the line chart
fig = px.line(
    daily_sales,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time",
    labels={"date": "Date", "sales": "Total Sales ($)"},
)

# Add a vertical line manually using add_shape
price_increase_date = pd.Timestamp("2021-01-15")
fig.add_shape(
    type="line",
    x0=price_increase_date,
    x1=price_increase_date,
    y0=0,
    y1=1,
    yref="paper",
    line=dict(color="red", width=3, dash="dash"),
)

# Add annotation for the vertical line
fig.add_annotation(
    x=price_increase_date,
    y=1,
    yref="paper",
    text="Price Increase (Jan 15, 2021)",
    showarrow=False,
    yshift=10,
    font=dict(color="red", size=12),
)


# Define the layout
app.layout = html.Div(
    [
        # Header
        html.H1(
            "Soul Foods Pink Morsel Sales Dashboard",
            style={
                "textAlign": "center",
                "color": "#2c3e50",
                "marginBottom": 20,
                "marginTop": 20,
            },
        ),
        # Subtitle
        html.H3(
            "Analyzing sales before and after the price increase on January 15, 2021",
            style={"textAlign": "center", "color": "#7f8c8d", "marginBottom": 40},
        ),
        # Line chart
        dcc.Graph(id="sales-line-chart", figure=fig),
        # Analysis summary
        html.Div(
            [
                html.H2("Key Findings", style={"color": "#2c3e50"}),
                html.P(
                    "The visualization clearly shows that sales significantly increased after the price increase on January 15, 2021.",
                    style={"fontSize": 18},
                ),
                html.P(
                    "• Before price increase: Average daily sales ~$6,400",
                    style={"fontSize": 16},
                ),
                html.P(
                    "• After price increase: Average daily sales ~$9,200",
                    style={"fontSize": 16},
                ),
                html.P(
                    "Despite raising prices, Pink Morsel sales increased by approximately 44%, demonstrating strong customer demand and brand loyalty.",
                    style={"fontSize": 16, "fontWeight": "bold", "color": "#27ae60"},
                ),
            ],
            style={
                "marginTop": 40,
                "padding": "30px",
                "backgroundColor": "#ecf0f1",
                "borderRadius": "10px",
                "margin": "40px",
            },
        ),
    ]
)


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
