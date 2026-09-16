function updateDonutChart(data) {

    console.log(
        "DONUT CHART DATA:",
        data
    );

    if (!Array.isArray(data)) {

        console.error(
            "Donut chart data must be an array:",
            data
        );

        return;
    }

    if (data.length === 0) {

        console.error(
            "No donut chart data available"
        );

        return;
    }


    const colors = {
        "Safe Transactions": "#00D4AA",
        "Fraud Transactions": "#FF6B6B"
    };


    const trace = {

        values: data.map(
            d => Number(d.count)
        ),

        labels: data.map(
            d => d.label
        ),

        type: "pie",

        hole: 0.5,

        marker: {
            colors: data.map(
                d =>
                    colors[d.label] ||
                    "#7A7A9A"
            )
        },

        textinfo: "label+percent",

        hoverinfo: "label+value+percent",

        textposition: "inside",

        textfont: {
            color: "white",
            size: 14
        }
    };


    const total = data.reduce(
        (sum, d) =>
            sum + Number(d.count),
        0
    );


    const layout = {

        template: "plotly_dark",

        margin: {
            l: 20,
            r: 20,
            t: 20,
            b: 60
        },

        paper_bgcolor:
            "rgba(0,0,0,0)",

        plot_bgcolor:
            "rgba(0,0,0,0)",

        showlegend: true,

        legend: {

            orientation: "h",

            y: -0.15,

            font: {
                color: "#B8B8D0"
            }
        },

        annotations: [

            {
                font: {
                    size: 16,
                    color: "white"
                },

                showarrow: false,

                text:
                    `Total<br>${total}`
            }
        ]
    };


    Plotly.newPlot(
        "donutChart",
        [trace],
        layout,
        {
            responsive: true,
            displaylogo: false
        }
    );
}


/* ==========================================
   GET DATA FROM DJANGO
========================================== */

const donutChartElement =
    document.getElementById(
        "donut-chart-data"
    );


if (donutChartElement) {

    const donutChartData =
        JSON.parse(
            donutChartElement.textContent
        );

    console.log(
        "Parsed Donut Chart:",
        donutChartData
    );

    updateDonutChart(
        donutChartData
    );

} else {

    console.error(
        "donut-chart-data element NOT FOUND"
    );
}




    function updateLocationChart(data) {

    console.log("TOP FRAUD LOCATION DATA:", data);

    if (!Array.isArray(data)) {
        console.error(
            "Location chart data must be an array:",
            data
        );
        return;
    }

    if (data.length === 0) {
        console.error(
            "No fraud location data available"
        );
        return;
    }

    const locations = data.map(
        d => d.location
    );

    const counts = data.map(
        d => Number(d.fraud_count)
    );

    const trace = {

        y: locations,

        x: counts,

        type: "bar",

        orientation: "h",

        marker: {
            color: counts,
            colorscale: [
                [0, "#6C3CE1"],
                [0.5, "#8B6FE8"],
                [1, "#FF6B6B"]
            ],
            showscale: false
        },

        text: counts,

        textposition: "outside",

        textfont: {
            color: "white"
        },

        hovertemplate:
            "<b>%{y}</b><br>" +
            "Fraud Count: %{x}" +
            "<extra></extra>"
    };

    const layout = {

        template: "plotly_dark",

        margin: {
            l: 80,
            r: 50,
            t: 20,
            b: 50
        },

        paper_bgcolor:
            "rgba(0,0,0,0)",

        plot_bgcolor:
            "rgba(0,0,0,0)",

        showlegend: false,

        xaxis: {

            gridcolor:
                "rgba(255,255,255,0.05)",

            tickfont: {
                color: "#7A7A9A"
            },

            title: "Fraud Count",

            titlefont: {
                color: "#7A7A9A"
            }
        },

        yaxis: {

            gridcolor:
                "rgba(255,255,255,0.05)",

            tickfont: {
                color: "#7A7A9A"
            },

            automargin: true,

            autorange: "reversed"
        }
    };

    Plotly.newPlot(
        "locationChart",
        [trace],
        layout,
        {
            responsive: true,
            displaylogo: false
        }
    );
}


/* ==========================================
   GET TOP FRAUD LOCATION DATA
========================================== */

const locationChartElement =
    document.getElementById(
        "location-chart-data"
    );

if (locationChartElement) {

    const locationChartData =
        JSON.parse(
            locationChartElement.textContent
        );

    console.log(
        "Parsed Location Chart:",
        locationChartData
    );

    updateLocationChart(
        locationChartData
    );

} else {

    console.error(
        "location-chart-data element NOT FOUND"
    );
}



    function changeGrowthChart() {

    const selection =
        document.getElementById("growthSelection").value;

    const data =
        JSON.parse(
            document.getElementById(
                "area-chart-data"
            ).textContent
        );

    updateAreaChart(data, selection);
}


function updateAreaChart(data, selection = "both") {

    console.log("CUMULATIVE GROWTH DATA:", data);
    console.log("Selected:", selection);

    if (
        !data ||
        !Array.isArray(data.dates) ||
        !Array.isArray(data.total) ||
        !Array.isArray(data.fraud)
    ) {
        console.error("Invalid cumulative growth data:", data);
        return;
    }

    const traces = [];

    // =========================
    // TOTAL TRANSACTIONS
    // =========================

    if (selection === "total" || selection === "both") {

        traces.push({
            x: data.dates,
            y: data.total,
            type: "scatter",
            mode: "lines",
            name: "Total Transactions",

            fill: "tozeroy",

            line: {
                color: "#6C3CE1",
                width: 2
            },

            fillcolor:
                "rgba(108, 60, 225, 0.3)",

            hovertemplate:
                "<b>%{x}</b><br>" +
                "Cumulative Total: %{y}" +
                "<extra></extra>"
        });
    }


    // =========================
    // FRAUDULENT TRANSACTIONS
    // =========================

    if (selection === "fraud" || selection === "both") {

        traces.push({
            x: data.dates,
            y: data.fraud,
            type: "scatter",
            mode: "lines",
            name: "Fraudulent",

            fill: "tozeroy",

            line: {
                color: "#FF6B6B",
                width: 2
            },

            fillcolor:
                "rgba(255, 107, 107, 0.3)",

            hovertemplate:
                "<b>%{x}</b><br>" +
                "Cumulative Fraud: %{y}" +
                "<extra></extra>"
        });
    }


    // =========================
    // LAYOUT
    // =========================

    const layout = {

        template: "plotly_dark",

        margin: {
            l: 50,
            r: 20,
            t: 20,
            b: 50
        },

        paper_bgcolor:
            "rgba(0,0,0,0)",

        plot_bgcolor:
            "rgba(0,0,0,0)",

        xaxis: {

            gridcolor:
                "rgba(255,255,255,0.05)",

            tickfont: {
                color: "#7A7A9A"
            },

            tickangle: -45
        },

        yaxis: {

            gridcolor:
                "rgba(255,255,255,0.05)",

            tickfont: {
                color: "#7A7A9A"
            },

            title: "Cumulative Count",

            titlefont: {
                color: "#7A7A9A"
            }
        },

        hovermode: "x unified",

        legend: {

            orientation: "h",

            y: -0.15,

            font: {
                color: "#B8B8D0"
            }
        }
    };


    // =========================
    // CREATE CHART
    // =========================

    Plotly.newPlot(
        "areaChart",
        traces,
        layout,
        {
            responsive: true,
            displaylogo: false
        }
    );
}


// =========================
// GET DJANGO DATA
// =========================

const areaChartElement =
    document.getElementById("area-chart-data");

if (areaChartElement) {

    const areaChartData =
        JSON.parse(
            areaChartElement.textContent
        );

    console.log(
        "Parsed Cumulative Growth:",
        areaChartData
    );

    // Selection exists in JS,
    // but nothing is displayed in browser.
    updateAreaChart(
        areaChartData,
        "both"
    );

} else {

    console.error(
        "area-chart-data element NOT FOUND"
    );
}


    function updateRadarChart(data) {

    console.log(
        "TRANSACTION TYPE DATA:",
        data
    );

    if (
        !data ||
        !Array.isArray(data.labels) ||
        !Array.isArray(data.total) ||
        !Array.isArray(data.fraud)
    ) {
        console.error(
            "Invalid transaction type data:",
            data
        );

        return;
    }

    if (data.labels.length === 0) {

        console.error(
            "No transaction type data available"
        );

        return;
    }


    // ==================================
    // TOTAL TRANSACTIONS
    // ==================================

    const trace1 = {

        type: "scatterpolar",

        r: data.total,

        theta: data.labels,

        fill: "toself",

        name: "Total",

        line: {
            color: "#6C3CE1",
            width: 2
        },

        fillcolor:
            "rgba(108, 60, 225, 0.2)",

        hovertemplate:
            "<b>%{theta}</b><br>" +
            "Total: %{r}" +
            "<extra></extra>"
    };


    // ==================================
    // FRAUDULENT TRANSACTIONS
    // ==================================

    const trace2 = {

        type: "scatterpolar",

        r: data.fraud,

        theta: data.labels,

        fill: "toself",

        name: "Fraudulent",

        line: {
            color: "#FF6B6B",
            width: 2
        },

        fillcolor:
            "rgba(255, 107, 107, 0.2)",

        hovertemplate:
            "<b>%{theta}</b><br>" +
            "Fraud: %{r}" +
            "<extra></extra>"
    };


    // ==================================
    // LAYOUT
    // ==================================

    const layout = {

        template: "plotly_dark",

        margin: {
            l: 40,
            r: 40,
            t: 20,
            b: 40
        },

        paper_bgcolor:
            "rgba(0,0,0,0)",

        plot_bgcolor:
            "rgba(0,0,0,0)",

        polar: {

            radialaxis: {

                gridcolor:
                    "rgba(255,255,255,0.05)",

                tickfont: {
                    color: "#7A7A9A"
                },

                visible: true
            },

            angularaxis: {

                gridcolor:
                    "rgba(255,255,255,0.05)",

                tickfont: {
                    color: "#7A7A9A"
                }
            }
        },

        legend: {

            orientation: "h",

            y: -0.15,

            font: {
                color: "#B8B8D0"
            }
        }
    };


    // ==================================
    // CREATE RADAR CHART
    // ==================================

    Plotly.newPlot(
        "radarChart",
        [trace1, trace2],
        layout,
        {
            responsive: true,
            displaylogo: false
        }
    );
}


    const radarChartElement =
    document.getElementById(
        "radar-chart-data"
    );

if (radarChartElement) {

    const radarChartData =
        JSON.parse(
            radarChartElement.textContent
        );

    console.log(
        "Parsed Transaction Type Data:",
        radarChartData
    );

    updateRadarChart(
        radarChartData
    );

} else {

    console.error(
        "radar-chart-data element NOT FOUND"
    );
}





    function updateWaterfallData(data) {

    console.log(
        "TRANSACTION AMOUNT DATA:",
        data
    );

    if (!Array.isArray(data)) {

        console.error(
            "Invalid waterfall data:",
            data
        );

        return;
    }

    if (data.length === 0) {

        console.error(
            "No transaction amount data available"
        );

        return;
    }


    // ==================================
    // PREPARE DATA
    // ==================================

    const labels =
        data.map(
            d => d.transaction_type
        );

    const totalAmounts =
        data.map(
            d => Number(d.total_amount) || 0
        );

    const fraudAmounts =
        data.map(
            d => Number(d.fraud_amount) || 0
        );

    const netAmounts =
        data.map(
            d => Number(d.net_amount) || 0
        );


    // ==================================
    // TOTAL AMOUNT
    // ==================================

    const trace1 = {

        x: labels,

        y: totalAmounts,

        type: "bar",

        name: "Total Amount",

        marker: {
            color: "#6C3CE1"
        },

        hovertemplate:
            "<b>%{x}</b><br>" +
            "Total: $%{y:,.2f}" +
            "<extra></extra>"
    };


    // ==================================
    // FRAUD AMOUNT
    // ==================================

    const trace2 = {

        x: labels,

        y: fraudAmounts,

        type: "bar",

        name: "Fraud Amount",

        marker: {
            color: "#FF6B6B"
        },

        hovertemplate:
            "<b>%{x}</b><br>" +
            "Fraud: $%{y:,.2f}" +
            "<extra></extra>"
    };


    // ==================================
    // NET AMOUNT
    // ==================================

    const trace3 = {

        x: labels,

        y: netAmounts,

        type: "bar",

        name: "Net Amount",

        marker: {
            color: "#00D4AA"
        },

        hovertemplate:
            "<b>%{x}</b><br>" +
            "Net: $%{y:,.2f}" +
            "<extra></extra>"
    };


    // ==================================
    // LAYOUT
    // ==================================

    const layout = {

        template: "plotly_dark",

        margin: {
            l: 130,
            r: 20,
            t: 20,
            b: 60
        },

        paper_bgcolor:
            "rgba(0,0,0,0)",

        plot_bgcolor:
            "rgba(0,0,0,0)",

        barmode: "group",


        // ==================================
        // X AXIS
        // ==================================

        xaxis: {

            gridcolor:
                "rgba(255,255,255,0.05)",

            tickfont: {
                color: "#7A7A9A"
            },

            tickangle: -20,

            automargin: true
        },


        // ==================================
        // Y AXIS - LOG SCALE
        // ==================================

        yaxis: {

            type: "log",

            gridcolor:
                "rgba(255,255,255,0.05)",

            tickfont: {
                color: "#7A7A9A"
            },

            title:
                "Amount ($) - Log Scale",

            titlefont: {
                color: "#7A7A9A"
            },

            tickprefix: "$",

            exponentformat: "none",

            showexponent: "none"
        },


        // ==================================
        // HOVER
        // ==================================

        hovermode: "x unified",


        // ==================================
        // LEGEND
        // ==================================

        legend: {

            orientation: "h",

            y: -0.15,

            font: {
                color: "#B8B8D0"
            }
        }
    };


    // ==================================
    // CREATE CHART
    // ==================================

    Plotly.newPlot(
        "waterfallChart",

        [
            trace1,
            trace2,
            trace3
        ],

        layout,

        {
            responsive: true,
            displaylogo: false
        }
    );
}


// ==========================================
// GET DATA FROM DJANGO
// ==========================================

const waterfallChartElement =
    document.getElementById(
        "waterfall-chart-data"
    );


if (waterfallChartElement) {

    const waterfallChartData =
        JSON.parse(
            waterfallChartElement.textContent
        );

    console.log(
        "Parsed Transaction Amount Data:",
        waterfallChartData
    );

    updateWaterfallData(
        waterfallChartData
    );

} else {

    console.error(
        "waterfall-chart-data element NOT FOUND"
    );
}