document.addEventListener('DOMContentLoaded', () => {
    let data = []; // This will store the fetched transaction data

    // Fetch data from the normalized_data.json file
    fetch('../normalized_data.json')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(fetchedData => {
            data = fetchedData; // Store the fetched data
            updateCharts(); // Initialize the charts
            displayTransactionDetails(data); // Display transaction details
        })
        .catch(error => console.error("Error loading JSON data:", error));

    // Chart.js configurations
    const totalVolumeCtx = document.getElementById('total-volume-chart').getContext('2d');
    const monthlySummaryCtx = document.getElementById('monthly-summary-chart').getContext('2d');
    const paymentDepositCtx = document.getElementById('payment-deposit-distribution-chart').getContext('2d');

    let totalVolumeChart = null;
    let monthlySummaryChart = null;
    let paymentDepositChart = null;

    // Update charts based on selected filters
    function updateCharts() {
        const selectedType = document.getElementById('type').value || 'all';
        const startDate = document.getElementById('start-date').value || null;
        const endDate = document.getElementById('end-date').value || null;
        const minAmount = parseFloat(document.getElementById('min-amount').value) || 0;
        const maxAmount = parseFloat(document.getElementById('max-amount').value) || Infinity;

        const filteredData = filterData(data, selectedType, startDate, endDate, minAmount, maxAmount);

        updateTotalVolumeChart(filteredData);
        updateMonthlySummaryChart(filteredData);
        updatePaymentDepositChart(filteredData);

        displayTransactionDetails(filteredData);
    }

    // Filter data based on user input
    function filterData(data, selectedType, startDate, endDate, minAmount, maxAmount) {
        return data.filter(item =>
            (selectedType === "all" || item.category === selectedType) &&
            (!startDate || new Date(item.date) >= new Date(startDate)) &&
            (!endDate || new Date(item.date) <= new Date(endDate)) &&
            (item.amount >= minAmount && item.amount <= maxAmount)
        );
    }

    // Update Total Transaction Volume by Type chart
    function updateTotalVolumeChart(filteredData) {
        const totalVolume = {};
        filteredData.forEach(item => {
            totalVolume[item.category] = (totalVolume[item.category] || 0) + item.amount;
        });
        const totalVolumeLabels = Object.keys(totalVolume);
        const totalVolumeValues = Object.values(totalVolume);
        if (totalVolumeChart) totalVolumeChart.destroy();
        totalVolumeChart = new Chart(totalVolumeCtx, {
            type: 'bar',
            data: {
                labels: totalVolumeLabels,
                datasets: [{
                    label: 'Total Transaction Volume',
                    data: totalVolumeValues,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }

    // Update Monthly Summary of Transactions chart
    function updateMonthlySummaryChart(filteredData) {
        const monthlySummary = {};
        filteredData.forEach(item => {
            const date = new Date(item.date);
            const yearMonth = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
            monthlySummary[yearMonth] = (monthlySummary[yearMonth] || 0) + item.amount;
        });
        const monthlyLabels = Object.keys(monthlySummary).sort();
        const monthlyValues = Object.values(monthlySummary);
        if (monthlySummaryChart) monthlySummaryChart.destroy();
        if (monthlyLabels.length > 0) {
            monthlySummaryChart = new Chart(monthlySummaryCtx, {
                type: 'line',
                data: {
                    labels: monthlyLabels,
                    datasets: [{
                        label: 'Monthly Transaction Summary',
                        data: monthlyValues,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        fill: false
                    }]
                },
                options: {
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        } else {
            monthlySummaryCtx.clearRect(0, 0, monthlySummaryCtx.canvas.width, monthlySummaryCtx.canvas.height);
        }
    }

    // Update Distribution of Payments and Deposits chart
    function updatePaymentDepositChart(filteredData) {
        const paymentDepositData = filteredData.reduce((acc, item) => {
            if (item.category === "Payments to Code Holders" || item.category === "Bank Deposits") {
                acc[item.category] = (acc[item.category] || 0) + item.amount;
            }
            return acc;
        }, {});
        const paymentDepositLabels = Object.keys(paymentDepositData);
        const paymentDepositValues = Object.values(paymentDepositData);
        if (paymentDepositChart) paymentDepositChart.destroy();
        if (paymentDepositLabels.length > 0) {
            paymentDepositChart = new Chart(paymentDepositCtx, {
                type: 'pie',
                data: {
                    labels: paymentDepositLabels,
                    datasets: [{
                        data: paymentDepositValues,
                        backgroundColor: ['#FF6384', '#36A2EB']
                    }]
                },
                options: {
                    plugins: {
                        legend: { display: true }
                    }
                }
            });
        } else {
            paymentDepositCtx.clearRect(0, 0, paymentDepositCtx.canvas.width, paymentDepositCtx.canvas.height);
        }
    }

    // Display detailed transactions
    function displayTransactionDetails(filteredData) {
        const detailsList = document.getElementById('transactions');
        detailsList.innerHTML = ''; // Clear previous content

        const groupedData = filteredData.reduce((acc, item) => {
            if (!acc[item.category]) {
                acc[item.category] = [];
            }
            acc[item.category].push(item);
            return acc;
        }, {});

        Object.keys(groupedData).forEach(category => {
            const categoryContainer = document.createElement('div');
            categoryContainer.classList.add('category-container');
            const categoryTitle = document.createElement('h3');
            categoryTitle.textContent = category;
            categoryContainer.appendChild(categoryTitle);

            groupedData[category].forEach(item => {
                const li = document.createElement('li');
                li.classList.add('transaction-item');
                let details = `<strong>${item.category}</strong>: ${item.amount} RWF`;
                if (item.sender) details += `, <strong>Sender:</strong> ${item.sender}`;
                if (item.recipient) details += `, <strong>Recipient:</strong> ${item.recipient}`;
                if (item.transaction_id) details += `, <strong>Transaction ID:</strong> ${item.transaction_id}`;
                if (item.agent_name) details += `, <strong>Agent:</strong> ${item.agent_name} (${item.agent_phone})`;
                if (item.bundle_size) details += `, <strong>Bundle Size:</strong> ${item.bundle_size}GB`;
                if (item.message_body) details += `, <strong>Message:</strong> ${item.message_body}`;
                li.innerHTML = details;
                categoryContainer.appendChild(li);
            });

            detailsList.appendChild(categoryContainer);
        });
    }

    // Event listeners for filters
    document.getElementById('type').addEventListener('change', updateCharts);
    document.getElementById('start-date').addEventListener('change', updateCharts);
    document.getElementById('end-date').addEventListener('change', updateCharts);
    document.getElementById('min-amount').addEventListener('change', updateCharts);
    document.getElementById('max-amount').addEventListener('change', updateCharts);
});