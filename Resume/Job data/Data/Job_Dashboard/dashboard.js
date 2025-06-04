async function loadChart(id, jsonFile) {
  const res = await fetch(jsonFile);
  const fig = await res.json();
  Plotly.newPlot(id, fig.data, fig.layout);
}

loadChart("barChart2024", "bar_data_2024.json");
loadChart("barChart2025", "bar_data_2025.json");
loadChart("scatterPlot", "scatter_data.json");
loadChart("weeklyLine", "weekly_line_data.json");
