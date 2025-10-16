import dash
from dash import dcc, html, Input, Output
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
"""
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
"""

# Define the layout
app.layout = html.Div(
    [
        # Main container with background
        html.Div(
            [
                # Header
                html.H1(
                    "Soul Foods Pink Morsel Sales Dashboard",
                    style={
                        "textAlign": "center",
                        "color": "white",  # Changed to white text
                        "backgroundColor": "#3498db",  # Blue background
                        "padding": "30px",  # Space inside the header
                        "marginBottom": 20,
                        "marginTop": 0,  # Changed from 20 to 0
                        "borderRadius": "10px",  # Rounded corners
                        "boxShadow": "0 4px 6px rgba(0,0,0,0.1)",  # Subtle shadow
                        "fontFamily": "Arial, sans-serif",  # Clean font
                    },
                ),
                # Subtitle
                html.H3(
                    "Analyzing sales before and after the price increase on January 15, 2021",
                    style={
                        "textAlign": "center",
                        "color": "#7f8c8d",
                        "marginBottom": 40,
                    },
                ),
                html.Div(
                    [
                        html.Label(
                            "Select Region: ",
                            style={
                                "fontSize": 18,
                                "fontWeight": "bold",
                                "marginRight": 15,
                                "color": "#2c3e50",  # Add dark color
                            },
                        ),
                        dcc.RadioItems(
                            id="region-filter",
                            options=[
                                {"label": "All Regions", "value": "all"},
                                {"label": "North", "value": "north"},
                                {"label": "East", "value": "east"},
                                {"label": "South", "value": "south"},
                                {"label": "West", "value": "west"},
                            ],
                            value="all",
                            labelStyle={
                                "display": "inline-block",
                                "marginRight": 20,
                                "fontSize": 16,  # Add font size
                                "cursor": "pointer",  # Show pointer on hover
                            },
                        ),
                    ],
                    style={
                        "textAlign": "center",
                        "marginBottom": 30,
                        "backgroundColor": "white",  # White background
                        "padding": "25px",  # Space inside
                        "borderRadius": "10px",  # Rounded corners
                        "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",  # Subtle shadow
                        "maxWidth": "800px",  # Max width
                        "margin": "0 auto 30px auto",  # Center it
                    },
                ),
                # Line chart
                dcc.Graph(id="sales-line-chart"),
                # Analysis summary
                html.Div(
                    [
                        html.H2(
                            "Key Findings",
                            style={
                                "color": "#2c3e50",
                                "borderBottom": "3px solid #3498db",  # Blue underline
                                "paddingBottom": "10px",  # Space below text
                                "marginBottom": "20px",  # Space before content
                            },
                        ),
                        html.P(
                            "The visualization clearly shows that sales significantly increased after the price increase on January 15, 2021.",
                            style={
                                "fontSize": 18,
                                "lineHeight": "1.6",  # Better line spacing
                                "color": "#34495e",  # Slightly darker gray
                            },
                        ),
                        html.P(
                            "• Before price increase: Average daily sales ~$6,400",
                            style={
                                "fontSize": 16,
                                "color": "#e74c3c",  # Red for "before"
                                "fontWeight": "500",  # Medium weight
                            },
                        ),
                        html.P(
                            "• After price increase: Average daily sales ~$9,200",
                            style={
                                "fontSize": 16,
                                "color": "#27ae60",  # Green for "after"
                                "fontWeight": "500",
                            },
                        ),
                        html.P(
                            "Despite raising prices, Pink Morsel sales increased by approximately 44%, demonstrating strong customer demand and brand loyalty.",
                            style={
                                "fontSize": 16,
                                "fontWeight": "bold",
                                "color": "#27ae60",
                                "backgroundColor": "#d5f4e6",  # Light green background
                                "padding": "15px",  # Space inside
                                "borderRadius": "8px",  # Rounded corners
                                "borderLeft": "4px solid #27ae60",  # Green left border
                                "marginTop": "20px",  # Space above
                            },
                        ),
                    ],
                    style={
                        "marginTop": 40,
                        "padding": "30px",
                        "backgroundColor": "white",  # Changed to white
                        "borderRadius": "10px",
                        "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",  # Added shadow
                        "maxWidth": "900px",  # Max width
                        "margin": "40px auto",  # Center it
                    },
                ),
            ],
            style={
                "backgroundColor": "#f5f7fa",  # Light gray-blue background
                "minHeight": "100vh",  # Full viewport height
                "padding": "20px",  # Spacing around edges
            },
        )
    ]
)


@app.callback(Output("sales-line-chart", "figure"), Input("region-filter", "value"))
def update_graph(selected_region):
    if selected_region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["region"] == selected_region]

    daily_sales = filtered_df.groupby("date")["sales"].sum().reset_index()

    fig = px.line(
        daily_sales,
        x="date",
        y="sales",
        title=f"Pink Morsel Sales Over Time - {selected_region.capitalize()}",
        labels={"date": "Date", "sales": "Total Sales ($)"},
    )

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

    fig.add_annotation(
        x=price_increase_date,
        y=1,
        yref="paper",
        text="Price Increase (Jan 15, 2021)",
        showarrow=False,
        yshift=10,
        font=dict(color="red", size=12),
    )

    fig.update_layout(
        plot_bgcolor='white',                    # White background inside plot
        paper_bgcolor='white',                   # White background around plot
        font=dict(family="Arial, sans-serif", size=12, color="#2c3e50"),  # Font styling
        title=dict(
            font=dict(size=20, color="#2c3e50", family="Arial, sans-serif"),
            x=0.5,                               # Center the title
            xanchor='center'
        ),
        xaxis=dict(
            showgrid=True,                       # Show grid lines
            gridcolor='#ecf0f1',                 # Light gray grid
            showline=True,                       # Show axis line
            linecolor='#bdc3c7',                 # Gray axis line
            linewidth=2
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#ecf0f1',
            showline=True,
            linecolor='#bdc3c7',
            linewidth=2
        ),
        hovermode='x unified',                   # Better hover experience
        margin=dict(l=50, r=50, t=80, b=50),    # Margins around the plot
    )
    
    # Style the line trace
    fig.update_traces(
        line=dict(color='#3498db', width=3),    # Blue line, thicker
        hovertemplate='<b>Date</b>: %{x}<br><b>Sales</b>: $%{y:,.0f}<extra></extra>'  # Custom hover
    )

    return fig


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
