// Get the current year
const currentYear = new Date().getFullYear();

// Set the current year as the selected option in the select element
var selectElement = document.getElementById("year-select");
selectElement.value = currentYear;
const accessTokens = document.cookie
.split("; ")
.find((row) => row.startsWith("access_token="))
?.split("=")[1];

if (!accessTokens) {
console.error("No access token found in cookie. Redirecting to login.");
window.location.href = "user_login"; // Redirect after logout
}
const selectedYearReport = document.querySelector("#yearSelectReport");
const selectedMonthReport = document.querySelector("#monthSelectReport");

const totalValues = document.querySelector("#tatal_value");

// Function to update the chart with data
function updateChart(selectedYear) {
  fetch(`${window.API_URL}/CityReportDashboard/${selectedYear}/`, {
    headers: {
      Authorization: `Bearer ${accessTokens}`,
      "Content-Type": "application/json", // Important for most API requests
    },
  })
    .then((response) => response.json())
    .then((data) => {
      const totalPaymentsList = data.map((item) => item.total_payments);
      const totalUserList = data.map((item) => item.total_customers);

      // Update the chart with the new data
      chart1.data.datasets[0].data = totalPaymentsList;
      chart1.data.datasets[1].data = totalUserList;

      chart1.update();
    });
}

function updateChart2(selectedYear, selectedMonth) {
  fetch(`${window.API_URL}/YearlyPaymentSerializer/${selectedYear}/${selectedMonth}`, {
    headers: {
      Authorization: `Bearer ${accessTokens}`,
      "Content-Type": "application/json", // Important for most API requests
    },
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      const totalPaymentsList = data.map((item) => item.total_payments);
      const totalUserList = data.map((item) => item.total_customers);
      const monthDay = [];
      let totalValue = 0;
      data.map((item) => {
        monthDay.push(`${item.day}-${item.month}`);
        totalValue += item.total_payments;
      });
      totalValues.textContent = ` ${totalValue} Birr`;
      // Update the chart with the new data
      chart2.data.datasets[0].data = totalPaymentsList;
      chart2.data.datasets[1].data = totalUserList;
      chart2.data.labels = monthDay;
      chart2.update();
    });
}

// Event listener for select element change
selectElement.addEventListener("change", function () {
  let selectedYear = selectElement.value;
  updateChart(selectedYear);
});

// Another Event Listern
selectedYearReport.addEventListener("change", function () {
  updateChart2(selectedYearReport.value, selectedMonthReport.value);
});

selectedMonthReport.addEventListener("change", function () {
  updateChart2(selectedYearReport.value, selectedMonthReport.value);
});

// Make initial fetch request with the current year
updateChart(currentYear);
updateChart2(selectedYearReport.value, selectedMonthReport.value);

// Chart 1 ---------------
var ctx = document.getElementById("chart-bars").getContext("2d");
var chart1 = new Chart(ctx, {
  type: "bar",
  data: {
    labels: ["Ja", "Fe", "Mc", "Ap", "Ma", "Ju", "ji", "Au", "Se", "Oc", "No", "De"],
    datasets: [
      {
        label: "Total Income",
        tension: 0.4,
        borderWidth: 0,
        borderSkipped: false,
        backgroundColor: "#2ca8ff",
        data: [],
        maxBarThickness: 6,
      },
      {
        label: "Total Customer",
        tension: 0.4,
        borderWidth: 0,
        borderSkipped: false,
        backgroundColor: "#7c3aed",
        data: [],
        maxBarThickness: 6,
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        backgroundColor: "#fff",
        titleColor: "#1e293b",
        bodyColor: "#1e293b",
        borderColor: "#e9ecef",
        borderWidth: 1,
        usePointStyle: true,
      },
    },
    interaction: {
      intersect: false,
      mode: "index",
    },
    scales: {
      y: {
        stacked: true,
        grid: {
          drawBorder: false,
          display: true,
          drawOnChartArea: true,
          drawTicks: false,
          borderDash: [4, 4],
        },
        ticks: {
          beginAtZero: true,
          padding: 10,
          font: {
            size: 12,
            family: "Noto Sans",
            style: "normal",
            lineHeight: 2,
          },
          color: "#64748B",
        },
      },
      x: {
        stacked: true,
        grid: {
          drawBorder: false,
          display: false,
          drawOnChartArea: false,
          drawTicks: false,
        },
        ticks: {
          font: {
            size: 12,
            family: "Noto Sans",
            style: "normal",
            lineHeight: 2,
          },
          color: "#64748B",
        },
      },
    },
  },
});

// chart 2 ---------------
var ctx2 = document.getElementById("chart-line").getContext("2d");

var gradientStroke1 = ctx2.createLinearGradient(0, 230, 0, 50);

gradientStroke1.addColorStop(1, "rgba(45,168,255,0.2)");
gradientStroke1.addColorStop(0.2, "rgba(45,168,255,0.0)");
gradientStroke1.addColorStop(0, "rgba(45,168,255,0)"); //blue colors

var gradientStroke2 = ctx2.createLinearGradient(0, 230, 0, 50);

gradientStroke2.addColorStop(1, "rgba(119,77,211,0.4)");
gradientStroke2.addColorStop(0.7, "rgba(119,77,211,0.1)");
gradientStroke2.addColorStop(0, "rgba(119,77,211,0)"); //purple colors

var chart2 = new Chart(ctx2, {
  plugins: [
    {
      beforeInit(chart) {
        const originalFit = chart.legend.fit;
        chart.legend.fit = function fit() {
          originalFit.bind(chart.legend)();
          this.height += 40;
        };
      },
    },
  ],
  type: "line",
  data: {
    labels: [],
    datasets: [
      {
        label: "Volume",
        tension: 0,
        borderWidth: 2,
        pointRadius: 3,
        borderColor: "#2ca8ff",
        pointBorderColor: "#2ca8ff",
        pointBackgroundColor: "#2ca8ff",
        backgroundColor: gradientStroke1,
        fill: true,
        data: [],
        maxBarThickness: 6,
      },
      {
        label: "Trade",
        tension: 0,
        borderWidth: 2,
        pointRadius: 3,
        borderColor: "#832bf9",
        pointBorderColor: "#832bf9",
        pointBackgroundColor: "#832bf9",
        backgroundColor: gradientStroke2,
        fill: true,
        data: [],
        maxBarThickness: 6,
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: "top",
        align: "end",
        labels: {
          boxWidth: 6,
          boxHeight: 6,
          padding: 20,
          pointStyle: "circle",
          borderRadius: 50,
          usePointStyle: true,
          font: {
            weight: 400,
          },
        },
      },
      tooltip: {
        backgroundColor: "#fff",
        titleColor: "#1e293b",
        bodyColor: "#1e293b",
        borderColor: "#e9ecef",
        borderWidth: 1,
        pointRadius: 2,
        usePointStyle: true,
        boxWidth: 8,
      },
    },
    interaction: {
      intersect: false,
      mode: "index",
    },
    scales: {
      y: {
        grid: {
          drawBorder: false,
          display: true,
          drawOnChartArea: true,
          drawTicks: false,
          borderDash: [4, 4],
        },
        ticks: {
          callback: function (value, index, ticks) {
            return parseInt(value).toLocaleString() + " EUR";
          },
          display: true,
          padding: 10,
          color: "#b2b9bf",
          font: {
            size: 12,
            family: "Noto Sans",
            style: "normal",
            lineHeight: 2,
          },
          color: "#64748B",
        },
      },
      x: {
        grid: {
          drawBorder: false,
          display: false,
          drawOnChartArea: false,
          drawTicks: false,
          borderDash: [4, 4],
        },
        ticks: {
          display: true,
          color: "#b2b9bf",
          padding: 20,
          font: {
            size: 12,
            family: "Noto Sans",
            style: "normal",
            lineHeight: 2,
          },
          color: "#64748B",
        },
      },
    },
  },
});

const sycnBtn = document.getElementById('sync')

sycnBtn.addEventListener('click', function(){
  window.location.reload()
})


function downloadDivAsPDF(divId, filename = "download.pdf") {
  const { jsPDF } = window.jspdf; // Get jsPDF from the global scope.
  const divElement = document.getElementById(divId);

  if (!divElement) {
    console.error("Div element with ID '" + divId + "' not found.");
    return;
  }

  const pdf = new jsPDF();

  pdf.html(divElement, {
    callback: function (pdf) {
      pdf.save(filename);
    },
    x: 10,
    y: 10,
  });
}

// Example usage:
// <button onclick="downloadDivAsPDF('myDivToDownload', 'myDivContent.pdf')">Download as PDF</button>
// <div id="myDivToDownload">
//   <p>This is the section to download.</p>
//   <ul>
//     <li>Item 1</li>
//     <li>Item 2</li>
//   </ul>
// </div>