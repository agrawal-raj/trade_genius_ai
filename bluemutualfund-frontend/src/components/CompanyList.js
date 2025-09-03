import React from 'react'
import { Link } from 'react-router-dom'
import CompanyCard from './CompanyCard'

const CompanyList = ({ companies }) => {
  if (!companies || companies.length === 0) {
    return (
      <div className="text-center text-gray-500 py-12">
        No companies available. Please try refreshing the data.
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {companies.map((company) => (
        <Link 
          key={company.id} 
          to={`/company/${company.id}`}
          className="block transition-transform hover:scale-105"
        >
          <CompanyCard company={company} />
        </Link>
      ))}
    </div>
  )
}

export default CompanyList