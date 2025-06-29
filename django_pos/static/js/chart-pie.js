// Set modern default font family and styling
// Ensure compatibility with different Chart.js versions
if (typeof Chart !== "undefined") {
  // Initialize defaults if they don't exist
  Chart.defaults = Chart.defaults || {};
  Chart.defaults.font = Chart.defaults.font || {};

  // Set font properties
  Chart.defaults.font.family =
    Chart.defaults.font.family ||
    "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
  Chart.defaults.color = Chart.defaults.color || "#64748b";
  Chart.defaults.font.size = Chart.defaults.font.size || 12;
} else {
  console.error(
    "Chart.js is not loaded. Please ensure Chart.js is properly included."
  );
}

// Modern Doughnut Chart Configuration
function initializePieChart() {
  if (typeof Chart === "undefined") {
    console.error("Chart.js is not loaded. Cannot initialize pie chart.");
    return;
  }

  var ctx = document.getElementById("myPieChart");
  if (!ctx) {
    console.error('Canvas element with id "myPieChart" not found.');
    return;
  }

  var myPieChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: JSON.parse(document.getElementById("top_products_names").value),
      datasets: [
        {
          data: JSON.parse(
            document.getElementById("top_products_quantity").value
          ),
          backgroundColor: [
            "rgba(59, 130, 246, 0.9)", // Blue
            "rgba(34, 197, 94, 0.9)", // Green
            "rgba(168, 85, 247, 0.9)", // Purple
            "rgba(251, 146, 60, 0.9)", // Orange
            "rgba(236, 72, 153, 0.9)", // Pink
            "rgba(14, 165, 233, 0.9)", // Sky
          ],
          borderColor: [
            "rgba(59, 130, 246, 1)",
            "rgba(34, 197, 94, 1)",
            "rgba(168, 85, 247, 1)",
            "rgba(251, 146, 60, 1)",
            "rgba(236, 72, 153, 1)",
            "rgba(14, 165, 233, 1)",
          ],
          borderWidth: 3,
          hoverBackgroundColor: [
            "rgba(59, 130, 246, 1)",
            "rgba(34, 197, 94, 1)",
            "rgba(168, 85, 247, 1)",
            "rgba(251, 146, 60, 1)",
            "rgba(236, 72, 153, 1)",
            "rgba(14, 165, 233, 1)",
          ],
          hoverBorderColor: "#ffffff",
          hoverBorderWidth: 4,
          hoverOffset: 8,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "65%",
      plugins: {
        legend: {
          display: true,
          position: "bottom",
          labels: {
            usePointStyle: true,
            pointStyle: "circle",
            padding: 20,
            font: {
              size: 12,
              weight: "500",
            },
            generateLabels: function (chart) {
              const data = chart.data;
              if (data.labels.length && data.datasets.length) {
                const dataset = data.datasets[0];
                const total = dataset.data.reduce(
                  (sum, value) => sum + value,
                  0
                );

                return data.labels.map((label, i) => {
                  const value = dataset.data[i];
                  const percentage = ((value / total) * 100).toFixed(1);

                  return {
                    text: `${label} (${percentage}%)`,
                    fillStyle: dataset.backgroundColor[i],
                    strokeStyle: dataset.borderColor[i],
                    lineWidth: dataset.borderWidth,
                    index: i,
                  };
                });
              }
              return [];
            },
          },
        },
        tooltip: {
          backgroundColor: "rgba(255, 255, 255, 0.95)",
          titleColor: "#1f2937",
          bodyColor: "#4b5563",
          borderColor: "rgba(229, 231, 235, 1)",
          borderWidth: 1,
          cornerRadius: 12,
          displayColors: true,
          padding: 16,
          titleFont: {
            size: 14,
            weight: "600",
          },
          bodyFont: {
            size: 13,
            weight: "500",
          },
          callbacks: {
            title: function (tooltipItems) {
              return tooltipItems[0].label;
            },
            label: function (context) {
              const total = context.dataset.data.reduce(
                (sum, value) => sum + value,
                0
              );
              const percentage = ((context.parsed / total) * 100).toFixed(1);
              return `Sales: ${context.parsed} units (${percentage}%)`;
            },
          },
        },
      },
      animation: {
        animateRotate: true,
        animateScale: true,
        duration: 1000,
        easing: "easeOutQuart",
      },
      interaction: {
        intersect: false,
      },
    },
  });
}

// Initialize the chart when the page loads
document.addEventListener("DOMContentLoaded", function () {
  initializePieChart();
});
