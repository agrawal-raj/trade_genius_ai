// components/CompanyAnalysis.js
import React from 'react'
import ProsConsBadges from './ProsConsBadges'
// Remove the unused import:
// import ReturnsChart from './ReturnsChart'  // ← Remove this line

const CompanyAnalysis = ({ data }) => {
  // Check if data exists and has the expected structure
  if (!data || !data.company) {
    return (
      <div className="bg-white rounded-xl shadow-md p-6">
        <div className="text-center text-gray-500">
          No company data available.
        </div>
      </div>
    )
  }

  const { company, analysis, pros, cons } = data

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">

      <div className = 'bg-gradient-to-r from-blue-600 to-blue-800 text-white- p-6'>
      <div className="flex items-center mb-6">
        {company.company_logo && (
          <img 
            src={company.company_logo} 
            alt={company.company_name}
            className="w-20 h-20 rounded-full mr-6 object-contain bg-white p-1"
          />
        )}
        <div>
          <h1 className="text-3xl font-bold">{company.company_name}</h1>
          <p className="text-blue-100 mt-1">ID: {company.id}</p>
          {company.roe_percentage && (
            <div className = "flex items-center mt-2">
              <span className="bg-blue-500 text-xs font-semibold px-2 py-1 rounded">ROE: {company.roe_percentage}%
              </span>
            </div>
          )}
        </div>
      </div>
    </div>

      {/* Analysis Section */}
      <div className="p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-6 border-b pb-2">Financial Analysis</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {/* Sales Growth */}
          <div className="bg-gray-50 rounded-lg p-5 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-700 mb-3 flex items-center">
              <span className="w-3 h-3 bg-blue-500 rounded-full mr-2"></span>
              Sales Growth
            </h3>
            <div className="space-y-2">
              {analysis.compounded_sales_growth && analysis.compounded_sales_growth['3_years'] && (
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">3 Years</span>
                  <span className={`text-lg font-bold ${analysis.compounded_sales_growth['3_years'] >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {analysis.compounded_sales_growth['3_years']}%
                  </span>
                </div>
              )}
              {analysis.compounded_sales_growth && analysis.compounded_sales_growth['5_years'] && (
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">5 Years</span>
                  <span className={`text-lg font-bold ${analysis.compounded_sales_growth['5_years'] >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {analysis.compounded_sales_growth['5_years']}%
                  </span>
                </div>
              )}
              {analysis.compounded_sales_growth && analysis.compounded_sales_growth['10_years'] && (
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">10 Years</span>
                  <span className={`text-lg font-bold ${analysis.compounded_sales_growth['10_years'] >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {analysis.compounded_sales_growth['10_years']}%
                  </span>
                </div>
              )}
            </div>
          </div>

          {/* Profit Growth */}
          <div className="bg-gray-50 rounded-lg p-5 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-700 mb-3 flex items-center">
              <span className="w-3 h-3 bg-green-500 rounded-full mr-2"></span>
              Profit Growth
            </h3>
            <div className="space-y-2">
              {analysis.compounded_profit_growth && analysis.compounded_profit_growth['3_years'] && (
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">3 Years</span>
                  <span className={`text-lg font-bold ${analysis.compounded_profit_growth['3_years'] >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {analysis.compounded_profit_growth['3_years']}%
                  </span>
                </div>
              )}
              {analysis.compounded_profit_growth && analysis.compounded_profit_growth['5_years'] && (
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">5 Years</span>
                  <span className={`text-lg font-bold ${analysis.compounded_profit_growth['5_years'] >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {analysis.compounded_profit_growth['5_years']}%
                  </span>
                </div>
              )}
              {analysis.compounded_profit_growth && analysis.compounded_profit_growth['10_years'] && (
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">10 Years</span>
                  <span className={`text-lg font-bold ${analysis.compounded_profit_growth['10_years'] >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {analysis.compounded_profit_growth['10_years']}%
                  </span>
                </div>
              )}
            </div>
          </div>

          {/* Return on Equity */}
          <div className="bg-gray-50 rounded-lg p-5 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-700 mb-3 flex items-center">
              <span className="w-3 h-3 bg-purple-500 rounded-full mr-2"></span>
              Return on Equity
            </h3>
            <div className="space-y-2">
              {analysis.return_on_equity && analysis.return_on_equity['3_years'] && (
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">3 Years</span>
                  <span className="text-lg font-bold text-purple-600">
                    {analysis.return_on_equity['3_years']}%
                  </span>
                </div>
              )}
              {analysis.return_on_equity && analysis.return_on_equity['5_years'] && (
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">5 Years</span>
                  <span className="text-lg font-bold text-purple-600">
                    {analysis.return_on_equity['5_years']}%
                  </span>
                </div>
              )}
              {analysis.return_on_equity && analysis.return_on_equity['10_years'] && (
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">10 Years</span>
                  <span className="text-lg font-bold text-purple-600">
                    {analysis.return_on_equity['10_years']}%
                  </span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Pros and Cons Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <ProsConsBadges title="Pros" items={pros} type="pros" />
          <ProsConsBadges title="Cons" items={cons} type="cons" />
        </div>
      </div>
    </div>
  )
}

export default CompanyAnalysis