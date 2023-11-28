import Chart from "react-apexcharts";

function PollChart() {
  const chartData = {
    options: {
      title: {
        text: "What's your favourite season?",
        align: "left",
      },
      tooltip: {
        enabled: false,
      },
      chart: {
        id: "Twitter poll",
      },
      xaxis: {
        categories: ["Spring", "Summer", "Autumn", "Winter"],
      },
      plotOptions: {
        bar: {
          horizontal: true,
          dataLabels: {
            position: "bottom",
            enabled: false,
          },
        },
      },
      yaxis: {
        labels: {
          show: false,
        },
      },
      dataLabels: {
        enabled: true,
        textAnchor: "start",
        style: {
          colors: ["#fff"],
        },
        formatter: function (val, opt) {
          return opt.w.globals.labels[opt.dataPointIndex] + ":  " + val;
        },
        offsetX: 0,
        dropShadow: {
          enabled: true,
        },
      },
    },
    series: [
      {
        data: [10, 18, 13, 15],
      },
    ],
  };

  return (
    <Chart
      options={chartData.options}
      series={chartData.series}
      type="bar"
      width="500"
    />
  );
}

export default PollChart;
