let originalTrendData = null;


/* =========================================
   MAIN TREND CHART FUNCTION
========================================= */

function updateTrendChart(data) {

    originalTrendData = data;

    renderTrendChart();
}


/* =========================================
   RENDER CHART
========================================= */

function renderTrendChart() {

    if (!originalTrendData) {
        console.error("Trend data is not available.");
        return;
    }

    const graphType =
        document.getElementById("trendGraphType").value;

    const metric =
        document.getElementById("trendMetric").value;

    const dateRange =
        document.getElementById("trendDateRange").value;


    /* =====================================
       GET ORIGINAL DATA
    ===================================== */

    let dates = [...originalTrendData.dates];
    let total = [...originalTrendData.total];
    let fraud = [...originalTrendData.fraud];
    let safe = [...originalTrendData.safe];


    /* =====================================
       DATE RANGE FILTER
    ===================================== */

    if (dateRange !== "all") {

        const days = parseInt(dateRange);

        dates = dates.slice(-days);
        total = total.slice(-days);
        fraud = fraud.slice(-days);
        safe = safe.slice(-days);
    }


    /* =====================================
       CREATE TRACES
    ===================================== */

    const traces = [];


    /* =====================================
       LINE / AREA / SCATTER
    ===================================== */

    if (
        graphType === "line" ||
        graphType === "area" ||
        graphType === "scatter"
    ) {

        let mode = "lines+markers";

        if (graphType === "scatter") {
            mode = "markers";
        }


        /* TOTAL */

        if (metric === "all" || metric === "total") {

            traces.push({

                x: dates,
                y: total,

                type: "scatter",
                mode: mode,

                name: "Total Transactions",

                line: {
                    color: "#6C3CE1",
                    width: 3
                },

                marker: {
                    color: "#6C3CE1",
                    size: 6
                },

                fill:
                    graphType === "area"
                        ? "tozeroy"
                        : "none",

                hovertemplate:
                    "<b>Total Transactions</b><br>" +
                    "Date: %{x}<br>" +
                    "Transactions: %{y}<extra></extra>"
            });
        }


        /* FRAUD */

        if (metric === "all" || metric === "fraud") {

            traces.push({

                x: dates,
                y: fraud,

                type: "scatter",
                mode: mode,

                name: "Fraudulent",

                line: {
                    color: "#FF6B6B",
                    width: 3
                },

                marker: {
                    color: "#FF6B6B",
                    size: 6
                },

                fill:
                    graphType === "area"
                        ? "tozeroy"
                        : "none",

                hovertemplate:
                    "<b>Fraudulent</b><br>" +
                    "Date: %{x}<br>" +
                    "Fraud: %{y}<extra></extra>"
            });
        }


        /* SAFE */

        if (metric === "all" || metric === "safe") {

            traces.push({

                x: dates,
                y: safe,

                type: "scatter",
                mode: mode,

                name: "Safe",

                line: {
                    color: "#00D4AA",
                    width: 3
                },

                marker: {
                    color: "#00D4AA",
                    size: 6
                },

                fill:
                    graphType === "area"
                        ? "tozeroy"
                        : "none",

                hovertemplate:
                    "<b>Safe Transactions</b><br>" +
                    "Date: %{x}<br>" +
                    "Safe: %{y}<extra></extra>"
            });
        }
    }


    /* =====================================
       BAR CHART
    ===================================== */

    if (graphType === "bar") {

        if (metric === "all" || metric === "total") {

            traces.push({

                x: dates,
                y: total,

                type: "bar",

                name: "Total Transactions",

                marker: {
                    color: "#6C3CE1"
                },

                hovertemplate:
                    "<b>Total Transactions</b><br>" +
                    "Date: %{x}<br>" +
                    "Transactions: %{y}<extra></extra>"
            });
        }


        if (metric === "all" || metric === "fraud") {

            traces.push({

                x: dates,
                y: fraud,

                type: "bar",

                name: "Fraudulent",

                marker: {
                    color: "#FF6B6B"
                },

                hovertemplate:
                    "<b>Fraudulent</b><br>" +
                    "Date: %{x}<br>" +
                    "Fraud: %{y}<extra></extra>"
            });
        }


        if (metric === "all" || metric === "safe") {

            traces.push({

                x: dates,
                y: safe,

                type: "bar",

                name: "Safe",

                marker: {
                    color: "#00D4AA"
                },

                hovertemplate:
                    "<b>Safe Transactions</b><br>" +
                    "Date: %{x}<br>" +
                    "Safe: %{y}<extra></extra>"
            });
        }
    }


    /* =====================================
       LAYOUT
    ===================================== */

    const layout = {

        template: "plotly_dark",

        margin: {
            l: 55,
            r: 25,
            t: 25,
            b: 70
        },

        paper_bgcolor: "rgba(0,0,0,0)",

        plot_bgcolor: "rgba(0,0,0,0)",


        xaxis: {

            title: {
                text: "Date",
                font: {
                    color: "#B8B8D0"
                }
            },

            gridcolor:
                "rgba(255,255,255,0.05)",

            tickfont: {
                color: "#7A7A9A"
            },

            tickangle: -45,

            rangeslider: {
                visible: true
            }
        },


        yaxis: {

            title: {
                text: "Number of Transactions",
                font: {
                    color: "#B8B8D0"
                }
            },

            gridcolor:
                "rgba(255,255,255,0.05)",

            tickfont: {
                color: "#7A7A9A"
            },

            zeroline: false
        },


        hovermode: "x unified",


        legend: {

            orientation: "h",

            y: -0.30,

            x: 0,

            font: {
                color: "#B8B8D0"
            }
        },


        barmode: "group"
    };


    /* =====================================
       PLOTLY CONFIG
    ===================================== */

    const config = {

        responsive: true,

        displaylogo: false,

        modeBarButtonsToRemove: [
            "lasso2d",
            "select2d"
        ],

        modeBarButtonsToAdd: [
            "resetScale2d"
        ]
    };


    /* =====================================
       DRAW CHART
    ===================================== */

    Plotly.react(
        "trendChart",
        traces,
        layout,
        config
    );
}


/* =========================================
   LOAD DJANGO DATA
========================================= */

const trendChartElement =
    document.getElementById("trend-chart-data");


if (trendChartElement) {

    const trendChartData =
        JSON.parse(
            trendChartElement.textContent
        );

    updateTrendChart(trendChartData);

} else {

    console.error(
        "trend-chart-data element was not found."
    );


}



function updateTypeChart(data) {

    console.log("TYPE CHART DATA:", data);

    if (!data || data.length === 0) {

        console.error(
            "No data available for Fraud by Transaction Type"
        );

        return;
    }


    const types = data.map(
        d => d.transaction_type
    );

    const total = data.map(
        d => Number(d.total)
    );

    const fraud = data.map(
        d => Number(d.fraud)
    );


    const trace1 = {

        x: types,

        y: total,

        type: "bar",

        name: "Total",

        marker: {
            color: "#6C3CE1"
        }
    };


    const trace2 = {

        x: types,

        y: fraud,

        type: "bar",

        name: "Fraudulent",

        marker: {
            color: "#FF6B6B"
        }
    };


    const layout = {

        template: "plotly_dark",

        paper_bgcolor: "rgba(0,0,0,0)",

        plot_bgcolor: "rgba(0,0,0,0)",

        margin: {
            l: 60,
            r: 20,
            t: 30,
            b: 70
        },

        barmode: "group",

        xaxis: {

            title: "Transaction Type",

            gridcolor:
                "rgba(255,255,255,0.05)",

            tickfont: {
                color: "#7A7A9A"
            }
        },

        yaxis: {

            title: "Transactions",

            gridcolor:
                "rgba(255,255,255,0.05)",

            tickfont: {
                color: "#7A7A9A"
            }
        },

        legend: {

            orientation: "h",

            y: -0.25,

            font: {
                color: "#B8B8D0"
            }
        }
    };


    const config = {

        responsive: true,

        displaylogo: false
    };


    Plotly.newPlot(
        "typeChart",
        [trace1, trace2],
        layout,
        config
    );
}

    const typeChartElement =
    document.getElementById("type-chart-data");


if (typeChartElement) {

    const typeChartData =
        JSON.parse(
            typeChartElement.textContent
        );

    console.log(
        "Parsed Type Chart:",
        typeChartData
    );

    updateTypeChart(
        typeChartData
    );

} else {

    console.error(
        "type-chart-data element NOT FOUND"
    );
}



    function updateLocationChart(data) {

    console.log("LOCATION CHART DATA:", data);

    if (!Array.isArray(data)) {
        console.error(
            "Location chart data must be an array:",
            data
        );
        return;
    }

    if (data.length === 0) {
        console.error(
            "No location data available"
        );
        return;
    }

    const locations = data.map(
        d => d.location
    );

    const total = data.map(
        d => Number(d.total)
    );

    const fraud = data.map(
        d => Number(d.fraud)
    );

    const trace1 = {
        x: locations,
        y: total,
        type: "bar",
        name: "Total",
        marker: {
            color: "#6C3CE1"
        }
    };

    const trace2 = {
        x: locations,
        y: fraud,
        type: "bar",
        name: "Fraudulent",
        marker: {
            color: "#FF6B6B"
        }
    };

    const layout = {

        template: "plotly_dark",

        margin: {
            l: 60,
            r: 20,
            t: 30,
            b: 70
        },

        paper_bgcolor: "rgba(0,0,0,0)",

        plot_bgcolor: "rgba(0,0,0,0)",

        barmode: "group",

        xaxis: {
            title: "Location",
            gridcolor: "rgba(255,255,255,0.05)",
            tickfont: {
                color: "#7A7A9A"
            }
        },

        yaxis: {
            title: "Transactions",
            gridcolor: "rgba(255,255,255,0.05)",
            tickfont: {
                color: "#7A7A9A"
            },
            zeroline: false
        },

        hovermode: "x unified",

        legend: {
            orientation: "h",
            y: -0.25,
            font: {
                color: "#B8B8D0"
            }
        }
    };

    const config = {
        responsive: true,
        displaylogo: false
    };

    Plotly.newPlot(
        "locationChart",
        [trace1, trace2],
        layout,
        config
    );
}


    const locationChartElement =
    document.getElementById("location-chart-data");

if (locationChartElement) {

    const locationChartData =
        JSON.parse(locationChartElement.textContent);

    console.log(
        "Parsed Location Chart:",
        locationChartData
    );

    updateLocationChart(locationChartData);

} else {

    console.error(
        "location-chart-data element NOT FOUND"
    );

}




    function updateRiskChart(data) {

    console.log("RISK CHART DATA:", data);

    if (!Array.isArray(data)) {
        console.error(
            "Risk chart data must be an array:",
            data
        );
        return;
    }

    if (data.length === 0) {
        console.error(
            "No risk data available"
        );
        return;
    }

    const labels = data.map(
        d => d.label
    );

    const counts = data.map(
        d => Number(d.count)
    );

    const trace = {
        x: labels,

        y: counts,

        type: "bar",

        marker: {
            color: [
                "#00D4AA",
                "#FFB432",
                "#FF8A8A",
                "#FF6B6B"
            ],
            opacity: 0.8
        },

        text: counts,

        textposition: "outside",

        textfont: {
            color: "white"
        }
    };

    const layout = {

        template: "plotly_dark",

        margin: {
            l: 50,
            r: 20,
            t: 30,
            b: 80
        },

        paper_bgcolor: "rgba(0,0,0,0)",

        plot_bgcolor: "rgba(0,0,0,0)",

        xaxis: {
            title: "Risk Level",

            gridcolor:
                "rgba(255,255,255,0.05)",

            tickfont: {
                color: "#7A7A9A"
            },

            tickangle: -20
        },

        yaxis: {
            title: "Customers",

            gridcolor:
                "rgba(255,255,255,0.05)",

            tickfont: {
                color: "#7A7A9A"
            },

            zeroline: false
        },

        hovermode: "x unified"
    };

    const config = {
        responsive: true,
        displaylogo: false
    };

    Plotly.newPlot(
        "riskChart",
        [trace],
        layout,
        config
    );
}

    const riskChartElement =
    document.getElementById("risk-chart-data");

if (riskChartElement) {

    const riskChartData =
        JSON.parse(
            riskChartElement.textContent
        );

    console.log(
        "Parsed Risk Chart:",
        riskChartData
    );

    updateRiskChart(riskChartData);

} else {

    console.error(
        "risk-chart-data element NOT FOUND"
    );

}


    function updateAlertChart(data) {

    console.log("ALERT CHART DATA:", data);

    if (!Array.isArray(data)) {
        console.error(
            "Alert chart data must be an array:",
            data
        );
        return;
    }

    if (data.length === 0) {
        console.error(
            "No alert data available"
        );
        return;
    }

    const colors = {
        "Critical": "#FF6B6B",
        "High": "#FF8A8A",
        "Medium": "#FFB432",
        "Low": "#00D4AA"
    };

    const trace = {

        values: data.map(
            d => Number(d.count)
        ),

        labels: data.map(
            d => d.severity
        ),

        type: "pie",

        marker: {
            colors: data.map(
                d => colors[d.severity] || "#7A7A9A"
            )
        },

        textinfo: "label+percent",

        hoverinfo: "label+value+percent",

        textposition: "inside",

        textfont: {
            color: "white",
            size: 12
        }
    };

    const layout = {

        template: "plotly_dark",

        margin: {
            l: 20,
            r: 20,
            t: 20,
            b: 20
        },

        paper_bgcolor: "rgba(0,0,0,0)",

        plot_bgcolor: "rgba(0,0,0,0)",

        showlegend: true,

        legend: {
            orientation: "h",

            y: -0.1,

            font: {
                color: "#B8B8D0"
            }
        }
    };

    Plotly.newPlot(
        "alertChart",
        [trace],
        layout,
        {
            responsive: true,
            displaylogo: false
        }
    );
}

    const alertChartElement =
    document.getElementById("alert-chart-data");

if (alertChartElement) {

    const alertChartData =
        JSON.parse(
            alertChartElement.textContent
        );

    console.log(
        "Parsed Alert Chart:",
        alertChartData
    );

    updateAlertChart(alertChartData);

} else {

    console.error(
        "alert-chart-data element NOT FOUND"
    );
}

