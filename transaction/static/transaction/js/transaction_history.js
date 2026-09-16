   // ============================================================
// MAIN DASHBOARD - CHARTS
// ============================================================

function updateCharts() {
    console.log("updateCharts() called");

    // ============================================================
    // 1. VOLUME CHART - BAR CHART
    // ============================================================

    const volumeData = [
        {% for item in metric.transaction_volume %}
        {
            date: "{{ item.date|date:'Y-m-d' }}",
            total: {{ item.total_transactions }}
        }{% if not forloop.last %},{% endif %}
        {% endfor %}
    ];

    console.log("Volume Data:", volumeData);

    const volumeTrace = {
        x: volumeData.map(item => item.date),
        y: volumeData.map(item => item.total),
        type: "bar",
        name: "Transactions",
        hovertemplate: "<b>%{x}</b><br>Transactions: %{y:,}<extra></extra>",
        marker: {
            color: '#6C3CE1',
            opacity: 0.9,
            line: {
                color: 'rgba(255,255,255,0.1)',
                width: 1
            }
        }
    };

    const volumeLayout = {
        template: "plotly_dark",
        height: 350,
        margin: { l: 55, r: 20, t: 15, b: 90 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        xaxis: {
            title: "",
            showgrid: false,
            tickangle: -35,
            tickfont: { size: 10, color: "#8A8AA3" },
            linecolor: "rgba(255,255,255,0.1)",
            tickmode: "auto",
            nticks: 10
        },
        yaxis: {
            title: "Transactions",
            rangemode: "tozero",
            showgrid: true,
            gridcolor: "rgba(255,255,255,0.06)",
            zeroline: false,
            tickfont: { size: 11, color: "#8A8AA3" },
            titlefont: { size: 13, color: "#FFFFFF" }
        },
        hovermode: "x",
        showlegend: false
    };

    Plotly.newPlot("volumeChart", [volumeTrace], volumeLayout, {
        responsive: true,
        displayModeBar: false
    });

    // ============================================================
    // 2. STATUS CHART - DONUT CHART
    // ============================================================

    const statusData = [{
        labels: ["Safe", "Fraud"],
        values: [
            {{ metric.total_safe }},
            {{ metric.total_fraud }}
        ],
        type: "pie",
        hole: 0.60,
        rotation: 90,
        textinfo: "label+percent",
        textposition: "outside",
        textfont: { size: 12, color: "#FFFFFF" },
        marker: {
            colors: ['#00D4AA', '#FF6B6B']
        },
        hovertemplate: "<b>%{label}</b><br>Transactions: %{value:,}<br>Percentage: %{percent}<extra></extra>"
    }];

    const statusLayout = {
        template: "plotly_dark",
        height: 400,
        margin: { l: 80, r: 80, t: 10, b: 110 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        showlegend: true,
        legend: {
            orientation: "h",
            y: -0.05,
            x: 0.5,
            xanchor: "center",
            font: { size: 12, color: "#B8B8D0" }
        }
    };

    Plotly.newPlot("statusChart", statusData, statusLayout, {
        responsive: true,
        displayModeBar: false
    });

    // ============================================================
    // 3. AMOUNT CHART - BAR CHART
    // ============================================================

    const amountData = [{
        x: [
            {% for item in metric.amount_ranges %}
                "{{ item.label }}"{% if not forloop.last %},{% endif %}
            {% endfor %}
        ],
        y: [
            {% for item in metric.amount_ranges %}
                {{ item.count }}{% if not forloop.last %},{% endif %}
            {% endfor %}
        ],
        type: "bar",
        text: [
            {% for item in metric.amount_ranges %}
                "{{ item.count }}"{% if not forloop.last %},{% endif %}
            {% endfor %}
        ],
        textposition: "outside",
        marker: {
            color: '#8B6FE8',
            opacity: 0.8,
            line: {
                color: 'rgba(255,255,255,0.1)',
                width: 1
            }
        },
        hovertemplate: "<b>%{x}</b><br>Transactions: %{y:,}<extra></extra>"
    }];

    const amountLayout = {
        template: "plotly_dark",
        height: 350,
        margin: { l: 65, r: 25, t: 30, b: 100 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        showlegend: false,
        xaxis: {
            title: {
                text: "Amount Range",
                font: { color: "#FFFFFF", size: 13 }
            },
            tickfont: { color: "#FFFFFF", size: 11 },
            tickangle: -20,
            showgrid: false,
            zeroline: false
        },
        yaxis: {
            title: {
                text: "Number of Transactions",
                font: { color: "#FFFFFF", size: 13 }
            },
            tickfont: { color: "#FFFFFF", size: 11 },
            showgrid: true,
            gridcolor: "rgba(255,255,255,0.06)",
            zeroline: false,
            rangemode: "tozero"
        },
        hovermode: "closest"
    };

    Plotly.newPlot("amountChart", amountData, amountLayout, {
        responsive: true,
        displayModeBar: false
    });

    // ============================================================
    // 4. TYPE CHART - GROUPED BAR CHART
    // ============================================================

    const typeData = [
        {% for item in metric.transaction_type_data %}
        {
            transaction_type: "{{ item.transaction_type|escapejs }}",
            total_transactions: {{ item.total_transactions }},
            fraud_transactions: {{ item.fraud_transactions }}
        }{% if not forloop.last %},{% endif %}
        {% endfor %}
    ];

    const typeTraces = [{
        x: typeData.map(item => item.transaction_type),
        y: typeData.map(item => item.total_transactions),
        type: "bar",
        name: "Total Transactions",
        marker: { color: '#6C3CE1' },
        hovertemplate: "<b>%{x}</b><br>Total Transactions: %{y:,}<extra></extra>"
    }, {
        x: typeData.map(item => item.transaction_type),
        y: typeData.map(item => item.fraud_transactions),
        type: "bar",
        name: "Fraudulent Transactions",
        marker: { color: '#FF6B6B' },
        hovertemplate: "<b>%{x}</b><br>Fraudulent Transactions: %{y:,}<extra></extra>"
    }];

    const typeLayout = {
        template: "plotly_dark",
        height: 400,
        margin: { l: 70, r: 30, t: 25, b: 90 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        barmode: "group",
        xaxis: {
            title: {
                text: "Transaction Type",
                font: { color: "#FFFFFF", size: 13 }
            },
            tickfont: { color: "#B8B8D0", size: 11 },
            showgrid: false,
            zeroline: false
        },
        yaxis: {
            title: {
                text: "Number of Transactions",
                font: { color: "#FFFFFF", size: 13 }
            },
            tickfont: { color: "#B8B8D0", size: 11 },
            gridcolor: "rgba(255,255,255,0.06)",
            zeroline: false,
            rangemode: "tozero"
        },
        legend: {
            orientation: "h",
            x: 0.5,
            xanchor: "center",
            y: -0.25,
            font: { color: "#B8B8D0", size: 12 }
        },
        hovermode: "x unified"
    };

    Plotly.newPlot("typeChart", typeTraces, typeLayout, {
        responsive: true,
        displayModeBar: false
    });
}


// ============================================================
// PAGE LOAD
// ============================================================

document.addEventListener("DOMContentLoaded", function() {
    console.log("PAGE LOADED");

    if (typeof Plotly === "undefined") {
        console.error("Plotly NOT loaded");
        return;
    }

    console.log("Plotly loaded");
    updateCharts();
});


// ============================================================
// TRANSACTION HISTORY TABLE
// ============================================================

let transactionHistoryData = [];
let transactionHistoryCurrentPage = 1;
let transactionHistoryPageSize = 10;


document.addEventListener("DOMContentLoaded", function() {
    loadTransactionHistory();
});


function loadTransactionHistory() {
    const element = document.getElementById("transaction-history-data");

    if (!element) {
        console.error("transaction-history-data NOT FOUND");
        return;
    }

    console.log("RAW JSON:", element.textContent);

    try {
        const data = JSON.parse(element.textContent);
        console.log("PARSED DATA:", data);

        if (!Array.isArray(data)) {
            console.error("Expected array but received:", data);
            transactionHistoryData = [];
        } else {
            transactionHistoryData = data;
        }

        console.log("TOTAL TRANSACTIONS:", transactionHistoryData.length);
        renderTransactionHistoryTable();

    } catch (error) {
        console.error("JSON PARSE ERROR:", error);
        transactionHistoryData = [];
        renderTransactionHistoryTable();
    }
}


function renderTransactionHistoryTable() {
    const tableBody = document.getElementById("tableBody");

    if (!tableBody) {
        console.error("tableBody NOT FOUND");
        return;
    }

    const start = (transactionHistoryCurrentPage - 1) * transactionHistoryPageSize;
    const end = start + transactionHistoryPageSize;
    const pageData = transactionHistoryData.slice(start, end);

    tableBody.innerHTML = "";

    if (pageData.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="8" style="text-align:center; padding:40px; color: #7A7A9A;">
                    <i class="fas fa-inbox" style="font-size:40px; display:block; margin-bottom:10px;"></i>
                    No transactions found
                </td>
            </tr>
        `;
        updateTransactionHistoryPageInfo();
        updateTransactionHistoryPagination();
        return;
    }

    pageData.forEach(function(transaction) {
        const amount = Number(transaction.amount) || 0;

        const status = transaction.is_fraud
            ? `<span class="status-badge fraud"><i class="fas fa-exclamation-circle"></i> Fraud</span>`
            : `<span class="status-badge safe"><i class="fas fa-check-circle"></i> Safe</span>`;

        const row = document.createElement("tr");
        row.innerHTML = `
            <td><strong>${transaction.transaction_id || "-"}</strong></td>
            <td>${transaction.customer_id || "-"}</td>
            <td>$${amount.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
            <td>${transaction.transaction_type || "-"}</td>
            <td>${transaction.location || "-"}</td>
            <td>${status}</td>
            <td>${transaction.timestamp || "-"}</td>
            <td>
                <button type="button" class="action-btn" onclick="viewTransaction('${transaction.transaction_id}')">
                    <i class="fas fa-eye"></i>
                </button>
            </td>
        `;
        tableBody.appendChild(row);
    });

    updateTransactionHistoryPageInfo();
    updateTransactionHistoryPagination();
}


function updateTransactionHistoryPageInfo() {
    const pageInfo = document.getElementById("pageInfo");
    if (!pageInfo) return;

    const total = transactionHistoryData.length;
    if (total === 0) {
        pageInfo.textContent = "Showing 0-0 of 0";
        return;
    }

    const start = (transactionHistoryCurrentPage - 1) * transactionHistoryPageSize + 1;
    const end = Math.min(transactionHistoryCurrentPage * transactionHistoryPageSize, total);
    pageInfo.textContent = `Showing ${start}-${end} of ${total}`;
}


function updateTransactionHistoryPagination() {
    const pageNumbers = document.getElementById("pageNumbers");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");

    if (!pageNumbers) return;

    const totalPages = Math.ceil(transactionHistoryData.length / transactionHistoryPageSize);
    pageNumbers.innerHTML = "";

    if (prevBtn) {
        prevBtn.disabled = transactionHistoryCurrentPage <= 1;
    }

    if (nextBtn) {
        nextBtn.disabled = transactionHistoryCurrentPage >= totalPages;
    }

    if (totalPages === 0) return;

    const maxVisible = 5;
    let startPage = Math.max(1, transactionHistoryCurrentPage - Math.floor(maxVisible / 2));
    let endPage = Math.min(totalPages, startPage + maxVisible - 1);

    if (endPage - startPage < maxVisible - 1) {
        startPage = Math.max(1, endPage - maxVisible + 1);
    }

    if (startPage > 1) {
        addPageButton(pageNumbers, 1);
        if (startPage > 2) addDots(pageNumbers);
    }

    for (let page = startPage; page <= endPage; page++) {
        addPageButton(pageNumbers, page);
    }

    if (endPage < totalPages) {
        if (endPage < totalPages - 1) addDots(pageNumbers);
        addPageButton(pageNumbers, totalPages);
    }
}


function addPageButton(container, page) {
    const button = document.createElement("button");
    button.textContent = page;
    button.className = "page-number";
    if (page === transactionHistoryCurrentPage) {
        button.classList.add("active");
    }
    button.onclick = function() {
        goToTransactionHistoryPage(page);
    };
    container.appendChild(button);
}


function addDots(container) {
    const span = document.createElement("span");
    span.textContent = "...";
    container.appendChild(span);
}


function goToTransactionHistoryPage(page) {
    const totalPages = Math.ceil(transactionHistoryData.length / transactionHistoryPageSize);
    if (page < 1 || page > totalPages) return;
    transactionHistoryCurrentPage = page;
    renderTransactionHistoryTable();
}


function prevTransactionHistoryPage() {
    if (transactionHistoryCurrentPage > 1) {
        transactionHistoryCurrentPage--;
        renderTransactionHistoryTable();
    }
}


function nextTransactionHistoryPage() {
    const totalPages = Math.ceil(transactionHistoryData.length / transactionHistoryPageSize);
    if (transactionHistoryCurrentPage < totalPages) {
        transactionHistoryCurrentPage++;
        renderTransactionHistoryTable();
    }
}


function changeTransactionHistoryPageSize() {
    const select = document.getElementById("transactionHistoryPageSize");
    if (!select) return;
    transactionHistoryPageSize = parseInt(select.value, 10);
    transactionHistoryCurrentPage = 1;
    renderTransactionHistoryTable();
}


function viewTransaction(transactionId) {
    alert(`Viewing transaction: ${transactionId}\nThis would open a detailed view modal.`);
}


// ============================================================
// FRAUD CASES TABLE
// ============================================================

let fraudCases = [];
let currentPage = 1;
let pageSize = 10;


function loadFraudCases() {
    const element = document.getElementById("fraud-cases-data");

    if (!element) {
        console.error("fraud-cases-data NOT FOUND");
        return;
    }

    try {
        const data = JSON.parse(element.textContent);
        fraudCases = Array.isArray(data) ? data : [];
        console.log("Fraud Cases Loaded:", fraudCases.length);
        renderFraudTable();
        updateFraudPagination();
    } catch (error) {
        console.error("Error loading fraud cases:", error);
        fraudCases = [];
        renderFraudTable();
        updateFraudPagination();
    }
}


function renderFraudTable() {
    const tableBody = document.getElementById("fraudTableBody");

    if (!tableBody) {
        console.error("fraudTableBody NOT FOUND");
        return;
    }

    const start = (currentPage - 1) * pageSize;
    const end = start + pageSize;
    const pageData = fraudCases.slice(start, end);

    tableBody.innerHTML = "";

    if (pageData.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="8" style="text-align:center; padding:40px; color: #7A7A9A;">
                    <i class="fas fa-inbox" style="font-size:40px; display:block; margin-bottom:10px;"></i>
                    No fraud cases found
                </td>
            </tr>
        `;
        updateFraudPageInfo();
        return;
    }

    pageData.forEach(function(caseItem) {
        const statusColors = {
            'Confirmed': 'confirmed',
            'Under Review': 'review',
            'False Positive': 'false-positive'
        };

        const row = document.createElement("tr");
        row.innerHTML = `
            <td><span class="case-id">${caseItem.case_id || "-"}</span></td>
            <td><span class="tx-id">${caseItem.transaction_id || "-"}</span></td>
            <td>${caseItem.customer_id || "-"}</td>
            <td class="amount">$${(caseItem.fraud_amount || 0).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
            <td><span class="type-badge">${caseItem.fraud_type || "-"}</span></td>
            <td><span class="status-badge ${statusColors[caseItem.status] || 'review'}">${caseItem.status || "-"}</span></td>
            <td>${caseItem.detection_time || "-"}</td>
            <td>${caseItem.investigator || "Unassigned"}</td>
        `;
        tableBody.appendChild(row);
    });

    updateFraudPageInfo();
}


function updateFraudPageInfo() {
    const pageInfo = document.getElementById("fraudPageInfo");
    if (!pageInfo) return;

    const total = fraudCases.length;
    if (total === 0) {
        pageInfo.textContent = "Showing 0-0 of 0";
        return;
    }

    const start = (currentPage - 1) * pageSize + 1;
    const end = Math.min(currentPage * pageSize, total);
    pageInfo.textContent = `Showing ${start}-${end} of ${total}`;
}


function updateFraudPagination() {
    const pageNumbers = document.getElementById("fraudPageNumbers");
    const prevBtn = document.getElementById("fraudPrevBtn");
    const nextBtn = document.getElementById("fraudNextBtn");

    if (!pageNumbers) return;

    const totalPages = Math.ceil(fraudCases.length / pageSize);
    pageNumbers.innerHTML = "";

    if (prevBtn) {
        prevBtn.disabled = currentPage <= 1;
    }

    if (nextBtn) {
        nextBtn.disabled = currentPage >= totalPages;
    }

    if (totalPages === 0) return;

    const maxVisible = 5;
    let startPage = Math.max(1, currentPage - Math.floor(maxVisible / 2));
    let endPage = Math.min(totalPages, startPage + maxVisible - 1);

    if (endPage - startPage < maxVisible - 1) {
        startPage = Math.max(1, endPage - maxVisible + 1);
    }

    if (startPage > 1) {
        addFraudPageButton(pageNumbers, 1);
        if (startPage > 2) addFraudDots(pageNumbers);
    }

    for (let page = startPage; page <= endPage; page++) {
        addFraudPageButton(pageNumbers, page);
    }

    if (endPage < totalPages) {
        if (endPage < totalPages - 1) addFraudDots(pageNumbers);
        addFraudPageButton(pageNumbers, totalPages);
    }
}


function addFraudPageButton(container, page) {
    const button = document.createElement("button");
    button.textContent = page;
    button.className = "page-number";
    if (page === currentPage) {
        button.classList.add("active");
    }
    button.onclick = function() {
        goToFraudPage(page);
    };
    container.appendChild(button);
}


function addFraudDots(container) {
    const span = document.createElement("span");
    span.textContent = "...";
    container.appendChild(span);
}


function goToFraudPage(page) {
    const totalPages = Math.ceil(fraudCases.length / pageSize);
    if (page < 1 || page > totalPages) return;
    currentPage = page;
    renderFraudTable();
    updateFraudPagination();
}


function prevFraudPage() {
    if (currentPage > 1) {
        currentPage--;
        renderFraudTable();
        updateFraudPagination();
    }
}


function nextFraudPage() {
    const totalPages = Math.ceil(fraudCases.length / pageSize);
    if (currentPage < totalPages) {
        currentPage++;
        renderFraudTable();
        updateFraudPagination();
    }
}


function changeFraudPageSize() {
    const select = document.getElementById("fraudPageSize");
    if (!select) return;
    pageSize = parseInt(select.value, 10);
    currentPage = 1;
    renderFraudTable();
    updateFraudPagination();
}


// ============================================================
// INITIALIZE FRAUD CASES
// ============================================================

document.addEventListener("DOMContentLoaded", function() {
    loadFraudCases();
});


// ============================================================
// EXPORT FUNCTIONS
// ============================================================

function exportTransactionHistory() {
    if (transactionHistoryData.length === 0) {
        alert('No data to export');
        return;
    }

    const headers = ['Transaction ID', 'Customer ID', 'Amount', 'Type', 'Location', 'Status', 'Timestamp'];
    const rows = transactionHistoryData.map(tx => [
        tx.transaction_id || '',
        tx.customer_id || '',
        tx.amount || 0,
        tx.transaction_type || '',
        tx.location || '',
        tx.is_fraud ? 'Fraud' : 'Safe',
        tx.timestamp || ''
    ]);

    let csv = headers.join(',') + '\n';
    rows.forEach(row => {
        csv += row.join(',') + '\n';
    });

    downloadCSV(csv, 'transaction_history.csv');
}


function exportFraudCases() {
    if (fraudCases.length === 0) {
        alert('No data to export');
        return;
    }

    const headers = ['Case ID', 'Transaction ID', 'Customer ID', 'Amount', 'Fraud Type', 'Status', 'Detection Time', 'Investigator'];
    const rows = fraudCases.map(c => [
        c.case_id || '',
        c.transaction_id || '',
        c.customer_id || '',
        c.fraud_amount || 0,
        c.fraud_type || '',
        c.status || '',
        c.detection_time || '',
        c.investigator || 'Unassigned'
    ]);

    let csv = headers.join(',') + '\n';
    rows.forEach(row => {
        csv += row.join(',') + '\n';
    });

    downloadCSV(csv, 'fraud_cases.csv');
}


function downloadCSV(csv, filename) {
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}


// ============================================================
// REFRESH FUNCTIONS
// ============================================================

function refreshDashboard() {
    const btn = document.querySelector('.btn-refresh');
    if (btn) {
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
        btn.disabled = true;
    }

    location.reload();
}


// ============================================================
// WINDOW RESIZE - RESIZE CHARTS
// ============================================================

let resizeTimeout;

window.addEventListener('resize', function() {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(function() {
        const chartIds = ['volumeChart', 'statusChart', 'amountChart', 'typeChart'];
        chartIds.forEach(function(id) {
            const el = document.getElementById(id);
            if (el && typeof Plotly !== 'undefined') {
                Plotly.Plots.resize(el);
            }
        });
    }, 300);
});


// ============================================================
// KEYBOARD SHORTCUTS
// ============================================================

document.addEventListener('keydown', function(e) {
    // Ctrl + R = Refresh
    if (e.ctrlKey && e.key === 'r') {
        e.preventDefault();
        refreshDashboard();
    }

    // Escape = Close modals
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal').forEach(function(modal) {
            modal.style.display = 'none';
        });
    }
});


// ============================================================
// UTILITY FUNCTIONS
// ============================================================

function formatCurrency(amount) {
    return '$' + Number(amount).toLocaleString(undefined, {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}


function formatDate(dateString) {
    if (!dateString) return '-';
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch (e) {
        return dateString;
    }
}


function getStatusColor(status) {
    const colors = {
        'safe': '#00D4AA',
        'fraud': '#FF6B6B',
        'pending': '#FFB432',
        'suspicious': '#FF8A8A',
        'Confirmed': '#00D4AA',
        'Under Review': '#FFB432',
        'False Positive': '#FF6B6B'
    };
    return colors[status] || '#7A7A9A';
}


function getStatusIcon(status) {
    const icons = {
        'safe': 'fa-check-circle',
        'fraud': 'fa-exclamation-circle',
        'pending': 'fa-clock',
        'suspicious': 'fa-exclamation-triangle',
        'Confirmed': 'fa-check-circle',
        'Under Review': 'fa-clock',
        'False Positive': 'fa-times-circle'
    };
    return icons[status] || 'fa-circle';
}


// ============================================================
// LOGOUT
// ============================================================

function logoutUser() {
    if (confirm('Are you sure you want to logout?')) {
        window.location.href = '/logout/';
    }
}


// ============================================================
// NOTIFICATION TOAST (Optional - Simple Version)
// ============================================================

function showToast(message, type) {
    // Simple alert fallback
    console.log(`[${type || 'info'}] ${message}`);

    // You can implement a simple toast notification here if needed
    // Or use the browser's native notification
    if (typeof Notification !== 'undefined' && Notification.permission === 'granted') {
        new Notification('Fraud Detection System', {
            body: message,
            icon: '/static/images/logo.png'
        });
    }
}


console.log("✅ Dashboard JavaScript loaded successfully!");
console.log("ℹ️ Use Ctrl+R to refresh");