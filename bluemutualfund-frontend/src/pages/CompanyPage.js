import React, { useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { getCompanyAnalysis, clearAnalysis } from '../store/slices/analysisSlice'
import CompanyAnalysis from '../components/CompanyAnalysis'
import LoadingSpinner from '../components/LoadingSpinner'

const CompanyPage = () => {
  const { companyId } = useParams()
  const dispatch = useDispatch()
  const { data, loading, error } = useSelector((state) => state.analysis)

  useEffect(() => {

    dispatch(getCompanyAnalysis(companyId))
    
    return () => {
      dispatch(clearAnalysis())
    }
  }, [dispatch, companyId])

  
  // // Add debug logging
  // useEffect(() => {
  //   if (data) {
  //     console.log('Received data:', data)
  //   }
  //   if (error) {
  //     console.error('Error:', error)
  //   }
  // }, [data, error])


  if (loading) return <LoadingSpinner />
  // if (error) return <div className="text-red-500 text-center">Error: {error.message}</div>
  if (error) return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className='max-w-6xl mx-auto'>
        <Link 
          to="/" 
          className="inline-flex items-center text-blue-600 hover:text-blue-800 mb-6 font-medium"
        >
          ← Back to Companies
        </Link>
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          Error: {error.message || 'Failed to load company analysis'}
          {/* <br />
          <small>Company ID: {companyId}</small> */}
        </div>
      </div>
    </div>
  )// temporary check code


  return (
    <div className='min-h-screen bg-gray-100 p-4'>
      <div className='max-w-6xl- mx-auto'>
        <Link 
          to="/" 
          className="inline-flex items-center text-blue-600 hover:text-blue-800 mb-6 font-medium"
        >
          ← Back to Companies
        </Link>
        
        {data ? (
          <CompanyAnalysis data={data} />
        ) : (
          <div className="bg-white rounded-lg shadow-md p-6 text-center text-gray-500">
            No analysis available for this company.
          </div>
        )}
      </div>
    </div>
  )
}

export default CompanyPage