// Set new default font family and font color for modern styling
Chart.defaults.font.family =
  "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
Chart.defaults.color = "#64748b";
Chart.defaults.font.size = 12;

function number_format(number, decimals, dec_point, thousands_sep) {
  // *     example: number_format(1234.56, 2, ',', ' ');
  // *     return: '1 234,56'
  number = (number + "").replace(",", "").replace(" ", "");
  var n = !isFinite(+number) ? 0 : +number,
    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
    sep = typeof thousands_sep === "undefined" ? "," : thousands_sep,
    dec = typeof dec_point === "undefined" ? "." : dec_point,
    s = "",
    toFixedFix = function (n, prec) {
      var k = Math.pow(10, prec);
      return "" + Math.round(n * k) / k;
    };
  // Fix for IE parseFloat(0.55).toFixed(0) = 0;
  s = (prec ? toFixedFix(n, prec) : "" + Math.round(n)).split(".");
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || "").length < prec) {
    s[1] = s[1] || "";
    s[1] += new Array(prec - s[1].length + 1).join("0");
  }
  return s.join(dec);
}

// Modern Area Chart Configuration
var ctx = document.getElementById("myAreaChart");
var myLineChart = new Chart(ctx, {
  type: "line",
  data: {
    labels: [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ],
    datasets: [
      {
        label: "Monthly Earnings",
        data: JSON.parse(document.getElementById("monthly_earnings").value),
        borderColor: "rgba(59, 130, 246, 1)",
        backgroundColor: "rgba(59, 130, 246, 0.1)",
        borderWidth: 3,
        pointBackgroundColor: "#ffffff",
        pointBorderColor: "rgba(59, 130, 246, 1)",
        pointBorderWidth: 3,
        pointRadius: 6,
        pointHoverRadius: 8,
        pointHoverBackgroundColor: "rgba(59, 130, 246, 1)",
        pointHoverBorderColor: "#ffffff",
        pointHoverBorderWidth: 3,
        tension: 0.4,
        fill: true,
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      intersect: false,
      mode: "index",
    },
    plugins: {
      legend: {
        display: true,
        position: "top",
        align: "end",
        labels: {
          usePointStyle: true,
          pointStyle: "circle",
          padding: 20,
          font: {
            size: 12,
            weight: "500",
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
        displayColors: false,
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
            return tooltipItems[0].label + " Earnings";
          },
          label: function (context) {
            return "Total: " + number_format(context.parsed.y);
          },
        },
      },
    },
    scales: {
      x: {
        grid: {
          display: true,
          color: "rgba(229, 231, 235, 0.5)",
          drawBorder: false,
        },
        ticks: {
          color: "#6b7280",
          font: {
            size: 11,
            weight: "500",
          },
          padding: 10,
        },
      },
      y: {
        beginAtZero: true,
        grid: {
          color: "rgba(229, 231, 235, 0.3)",
          drawBorder: false,
        },
        ticks: {
          color: "#6b7280",
          font: {
            size: 11,
            weight: "500",
          },
          padding: 15,
          maxTicksLimit: 6,
          callback: function (value) {
            return number_format(value);
          },
        },
      },
    },
    elements: {
      point: {
        hoverRadius: 8,
      },
    },
  },
});
