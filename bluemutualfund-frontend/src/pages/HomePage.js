import React, { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { getCompanies } from '../store/slices/companiesSlice'
// import CompanyList from '../components/CompanyList'
import LoadingSpinner from '../components/LoadingSpinner'
import EmptyState from '../components/EmptyState'

const HomePage = () => {
  const dispatch = useDispatch()
    const companiesState = useSelector((state) => state.companies)

  // const { companies, loading, error } = useSelector((state) => state.companies)

  const companies = companiesState?.companies || []
  const loading = companiesState?.loading || false
  const error = companiesState?.loading || null

  useEffect(() => {
    dispatch(getCompanies())
  }, [dispatch])

  if (loading) return <LoadingSpinner />
  if (error) return <div className="text-red-500 text-center">Error: {error.message}</div>

  return (
    <div className='min-h-screen bg-gray-100 p-4'>
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">Financial Companies Analysis</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {companies && companies.length>  0 ?( 
            companies.map((company) => (
            <Link 
              key={company.id} 
              to={`/company/${company.id}`}
              className="block bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow"
            >
              <div className="p-6">
                <div className="flex items-center mb-4">
                  {company.company_logo && (
                    <img 
                      src={company.company_logo} 
                      alt={company.company_name}
                      className="w-12 h-12 rounded-full mr-4 object-contain"
                    />
                  )}
                  <div>
                    <h2 className="text-xl font-semibold text-gray-800">{company.company_name}</h2>
                    <p className="text-gray-600 text-sm">ID: {company.id}</p>
                  </div>
                </div>
                
                {company.roe_percentage && (
                  <div className="mt-4">
                    <span className="inline-block bg-blue-100 text-blue-800 text-xs font-semibold px-2 py-1 rounded">
                      ROE: {company.roe_percentage}%
                    </span>
                  </div>
                )}
                
                <div className="mt-4 text-blue-600 font-medium">
                  View Analysis →
                </div>
              </div>
            </Link>
          ))
        ) : (
            <div className="col-span-full">
              <EmptyState 
                message="No companies available. Please check your data connection or try refreshing."
                actionText="Refresh Data"
                onAction={() => dispatch(getCompanies())}
              />
            </div>
          )}
        
        </div>
      </div>
    </div>
  )
}


export default HomePage