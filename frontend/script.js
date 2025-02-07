// Mock Data (Replace with data from your backend API)
const transactions = [
  { id: 1, type: "Incoming Money", amount: 5000, date: "2024-01-01", sender: "John Doe", recipient: "You" },
  { id: 2, type: "Payments", amount: 1500, date: "2024-01-02", sender: "You", recipient: "Jane Smith" },
  { id: 3, type: "Transfers", amount: 3000, date: "2024-01-03", sender: "You", recipient: "Airtime" },
  // Add more transactions as needed
];

// DOM Elements
const searchInput = document.getElementById("search");
const typeFilter = document.getElementById("typeFilter");
const filterButton = document.getElementById("filterButton");
const transactionsTable = document.getElementById("transactionsTable").getElementsByTagName("tbody")[0];

// Render Transactions Table
function renderTable(data) {
  transactionsTable.innerHTML = "";
  data.forEach(transaction => {
    const row = transactionsTable.insertRow();
    row.innerHTML = `
      <td>${transaction.id}</td>
      <td>${transaction.type}</td>
      <td>${transaction.amount}</td>
      <td>${transaction.date}</td>
      <td>${transaction.sender}</td>
      <td>${transaction.recipient}</td>
    `;
  });
}

// Filter Transactions
function filterTransactions() {
  const searchTerm = searchInput.value.toLowerCase();
  const type = typeFilter.value;

  const filtered = transactions.filter(transaction => {
    const matchesSearch = (
      transaction.id.toString().includes(searchTerm) ||
      transaction.sender.toLowerCase().includes(searchTerm) ||
      transaction.recipient.toLowerCase().includes(searchTerm)
    );
    const matchesType = type ? transaction.type === type : true;
    return matchesSearch && matchesType;
  });

  renderTable(filtered);
  renderCharts(filtered);
}

// Render Charts
function renderCharts(data) {
  const transactionTypes = [...new Set(data.map(t => t.type))];
  const amountsByType = transactionTypes.map(type => {
    return data.filter(t => t.type === type).reduce((sum, t) => sum + t.amount, 0);
  });

  // Transaction Volume Chart
  const volumeCtx = document.getElementById("transactionVolumeChart").getContext("2d");
  new Chart(volumeCtx, {
    type: "bar",
    data: {
      labels: transactionTypes,
      datasets: [{
        label: "Transaction Volume (RWF)",
        data: amountsByType,
        backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56"]
      }]
    }
  });

  // Transaction Type Distribution Chart
  const distributionCtx = document.getElementById("transactionTypeDistributionChart").getContext("2d");
  new Chart(distributionCtx, {
    type: "pie",
    data: {
      labels: transactionTypes,
      datasets: [{
        label: "Transaction Distribution",
        data: amountsByType,
        backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56"]
      }]
    }
  });
}

// Event Listeners
filterButton.addEventListener("click", filterTransactions);

// Initial Render
renderTable(transactions);
renderCharts(transactions);
