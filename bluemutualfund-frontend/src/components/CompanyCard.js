import React from 'react'

const CompanyCard = ({ company }) => {
  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow">
      <div className="p-6">
        <div className="flex items-center mb-4">
          {company.company_logo && (
            <img 
              src={company.company_logo} 
              alt={company.company_name}
              className="w-12 h-12 rounded-full mr-4 object-contain"
            />
          )}
          <h2 className="text-xl font-semibold text-gray-800">{company.company_name}</h2>
        </div>
        
        <div className="text-gray-600 mb-4">
          <p className="truncate">ID: {company.id}</p>
          {company.roe_percentage && (
            <p>ROE: {company.roe_percentage}%</p>
          )}
        </div>
        
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-500">View Analysis →</span>
          {company.website && (
            <a 
              href={company.website} 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-blue-600 hover:text-blue-800 text-sm"
              onClick={(e) => e.stopPropagation()}
            >
              Website
            </a>
          )}
        </div>
      </div>
    </div>
  )
}

export default CompanyCard