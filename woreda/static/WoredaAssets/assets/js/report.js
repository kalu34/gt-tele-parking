const today_money = document.querySelector("#today_money");
const monthly_income = document.querySelector("#monthly_income");
const total_user = document.querySelector("#total_user");
const monthly_user = document.querySelector("#monthly_user");


window.addEventListener("load", () => {
  // Fetching Data For Income Today
  fetch(`${window.API_URL}/ApprovedParkingRequest/day/`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json", // Important for most API requests
    },
  })
    .then((response) => response.json())
    .then((data) => {
      const total_value = data.reduce((total, item) => total + parseFloat(item.amount), 0);
      today_money.textContent = `${total_value} Birr`;
    })
    .catch((error) => {
      console.error("An error occurred", error);
    });

  // Fetching Data For Monthly Income
  fetch(`${window.API_URL}/ApprovedParkingRequest/month/`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json", // Important for most API requests
    },
  })
    .then((response) => response.json())
    .then((data) => {
      const total_value = data.reduce((total, item) => total + parseFloat(item.amount), 0);
      monthly_income.textContent = `${total_value} Birr`;
    });

  //  Fetching Data For User
  fetch(`${window.API_URL}/TotalUser/day/`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json", // Important for most API requests
    },
  })
    .then((response) => response.json())
    .then((data) => {
      total_user.textContent = data.length;
    });

  //  Fetching Data For Monthly User
  fetch(`${window.API_URL}/TotalUser/month/`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json", // Important for most API requests
    },
  })
    .then((response) => response.json())
    .then((data) => {
      monthly_user.textContent = data.length;
    })
    .catch((error) => {
      console.error("Error Fetching Data", error);
    });

  //  Working On Weekly Inocme
  fetch(`${window.API_URL}/TotalIncome/month/`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json", // Important for most API requests
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.length > 0) {
        try {
          // Convert date strings to Date objects and keep relevant fields
          const transferredData = data.map((item) => ({
            amount: Number(item.amount), // Ensure the amount is a number
            date: new Date(item.date), // Convert date string to Date object
          }));

          // Get current date and 7 days ago
          const now = new Date();
          const sevenDaysAgo = new Date();
          sevenDaysAgo.setDate(now.getDate() - 7);

          // Filter data to include only entries from the last 7 days
          const filteredData = transferredData.filter((item) => item.date >= sevenDaysAgo && item.date <= now);

          // Sum the amounts for the same date
          const summedData = filteredData.reduce((acc, item) => {
            // Format date as "YYYY-MM-DD" for easier grouping
            const dateKey = item.date.toISOString().split("T")[0];

            // Sum amounts for the same date
            if (acc[dateKey]) {
              acc[dateKey].amount += item.amount;
            } else {
              acc[dateKey] = { date: dateKey, amount: item.amount };
            }
            return acc;
          }, {});

          // Convert summed data to an array
          const finalData = Object.values(summedData);

          if (finalData.length === 0) {
            console.log("No data available within the last 7 days.");
          } else {
            // Prepare chart data
            const chartData = prepareChartData(finalData);

            // Chart.js setup
            const ctx = document.getElementById("chart-bars").getContext("2d");

            new Chart(ctx, {
              type: "bar",
              data: {
                labels: chartData.labels, // Labels (dates)
                datasets: [
                  {
                    label: "Amount", // Label for dataset
                    tension: 0.4,
                    borderWidth: 0,
                    borderRadius: 4,
                    borderSkipped: false,
                    backgroundColor: "#43A047", // Green bars
                    data: chartData.data, // Data for the bars (summed amounts)
                    barThickness: "flex",
                  },
                ],
              },
              options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                  legend: { display: false },
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
                      borderDash: [5, 5],
                      color: "#e5e5e5",
                    },
                    ticks: {
                      suggestedMin: 0,
                      suggestedMax: Math.max(...chartData.data) + 500, // Dynamic max based on data
                      beginAtZero: true,
                      padding: 10,
                      font: { size: 14, lineHeight: 2 },
                      color: "#737373",
                    },
                  },
                  x: {
                    grid: {
                      drawBorder: false,
                      display: false,
                      drawOnChartArea: false,
                      drawTicks: false,
                      borderDash: [5, 5],
                    },
                    ticks: {
                      display: true,
                      color: "#737373",
                      padding: 10,
                      font: { size: 14, lineHeight: 2 },
                    },
                  },
                },
              },
            });
          }
        } catch (error) {
          console.error("Error processing data or rendering chart:", error);
        }
      } else {
        console.log("No data available.");
      }
    })
    .catch((error) => {
      console.error("Error fetching data:", error); // Handle any fetch-related errors
    });

  // Working On Weekly User

  fetch(`${window.API_URL}/TotalUser/month/`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json", // Important for most API requests
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.length > 0) {
        try {
          // Convert date strings to Date objects and keep relevant fields
          const transferredData = data.map((item) => ({
            amount: Number(1), // Ensure the amount is a number
            date: new Date(item.date), // Convert date string to Date object
          }));

          // Get current date and 7 days ago
          const now = new Date();
          const sevenDaysAgo = new Date();
          sevenDaysAgo.setDate(now.getDate() - 7);


          // Filter data to include only entries from the last 7 days
          const filteredData = transferredData.filter((item) => item.date >= sevenDaysAgo && item.date <= now);
          
          // Sum the amounts for the same date
          const summedData = filteredData.reduce((acc, item) => {
            // Format date as "YYYY-MM-DD" for easier grouping
            const dateKey = item.date.toISOString().split("T")[0];

            // Sum amounts for the same date
            if (acc[dateKey]) {
              acc[dateKey].amount += 1;
            } else {
              acc[dateKey] = { date: dateKey, amount: item.amount };
            }
            return acc;
          }, {});

          // Convert summed data to an array
          const finalData = Object.values(summedData);

          if (finalData.length !== 0) {
            console.log("No data available within the last 7 days.");
          } else {
            // Prepare chart data
            const chartData = prepareChartData(finalData);

            var ctx2 = document.getElementById("chart-line").getContext("2d");

            new Chart(ctx2, {
              type: "line",
              data: {
                labels: chartData.labels,
                datasets: [
                  {
                    label: "Sales",
                    tension: 0,
                    borderWidth: 2,
                    pointRadius: 3,
                    pointBackgroundColor: "#43A047",
                    pointBorderColor: "transparent",
                    borderColor: "#43A047",
                    backgroundColor: "transparent",
                    fill: true,
                    data: chartData.data,
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
                    callbacks: {
                      title: function (context) {
                        const fullMonths = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
                        return fullMonths[context[0].dataIndex];
                      },
                    },
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
                      color: "#e5e5e5",
                    },
                    ticks: {
                      display: true,
                      color: "#737373",
                      padding: 10,
                      font: {
                        size: 12,
                        lineHeight: 2,
                      },
                    },
                  },
                  x: {
                    grid: {
                      drawBorder: false,
                      display: false,
                      drawOnChartArea: false,
                      drawTicks: false,
                      borderDash: [5, 5],
                    },
                    ticks: {
                      display: true,
                      color: "#737373",
                      padding: 10,
                      font: {
                        size: 12,
                        lineHeight: 2,
                      },
                    },
                  },
                },
              },
            });

          }
        } catch (error) {
          console.error("Error processing data or rendering chart:", error);
        }
      } else {
        console.log("No data available.");
      }
    })
    .catch((error) => {
      console.error("Error fetching data:", error); // Handle any fetch-related errors
    });

  // Function to map the `finalData` to the Chart.js data format
  function prepareChartData(data) {
    // Extract labels (days of the week) and data (amounts)
    const labels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    const amounts = new Array(7).fill(0); // Initialize an array for the 7 days

    // Loop through the data and map the amounts to the corresponding day of the week
    data.forEach((item) => {
      const itemDate = new Date(item.date);
      const dayOfWeek = itemDate.getDay(); // Get day of the week (0 = Sunday, 6 = Saturday)
      amounts[dayOfWeek] += item.amount; // Sum the amounts for the same day of the week
    });

    return {
      labels: labels, // Days of the week (labels)
      data: amounts, // Amounts for each day of the week
    };
  }
});
