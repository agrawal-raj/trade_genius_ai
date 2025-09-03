import React from 'react'
import { Bar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

const ReturnsChart = ({ salesData, profitData, roeData }) => {
  if (!salesData || !profitData || !roeData){
    return null
  }
  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Performance Metrics Over Time',
      },
    },
  }

  const data = {
    labels: ['3 Years', '5 Years', '10 Years'],
    datasets: [
      {
        label: 'Sales Growth',
        data: [salesData['3_years'], salesData['5_years'], salesData['10_years']],
        backgroundColor: 'rgba(54, 162, 235, 0.5)',
      },
      {
        label: 'Profit Growth',
        data: [profitData['3_years'], profitData['5_years'], profitData['10_years']],
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
      },
      {
        label: 'ROE',
        data: [roeData['3_years'], roeData['5_years'], roeData['10_years']],
        backgroundColor: 'rgba(153, 102, 255, 0.5)',
      },
    ],
  }

  return <Bar options={options} data={data} />
}

export default ReturnsChart