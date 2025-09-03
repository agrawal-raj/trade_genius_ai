// components/AdminPanel.js
import React, { useState } from 'react'
import { 
  triggerFetchCompanies, 
  triggerPreprocessData, 
  triggerAnalyzeData, 
  triggerAnalyzeAndStoreData 
} from '../services/api'

const AdminPanel = () => {
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  const handleAction = async (action) => {
    setLoading(true)
    setMessage('')
    
    try {
      let response
      switch (action) {
        case 'fetch':
          response = await triggerFetchCompanies()
          break
        case 'preprocess':
          response = await triggerPreprocessData()
          break
        case 'analyze':
          response = await triggerAnalyzeData()
          break
        case 'analyze_and_store':
          response = await triggerAnalyzeAndStoreData()
          break
        default:
          break
      }
      
      setMessage(response.data.message || 'Action completed successfully')
    } catch (error) {
      setMessage(error.response?.data?.message || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4">Data Management</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <button
          onClick={() => handleAction('fetch')}
          disabled={loading}
          className="bg-blue-500 text-white px-4 py-2 rounded disabled:bg-blue-300"
        >
          Fetch Companies Data
        </button>
        
        <button
          onClick={() => handleAction('preprocess')}
          disabled={loading}
          className="bg-green-500 text-white px-4 py-2 rounded disabled:bg-green-300"
        >
          Preprocess Data
        </button>
        
        <button
          onClick={() => handleAction('analyze')}
          disabled={loading}
          className="bg-purple-500 text-white px-4 py-2 rounded disabled:bg-purple-300"
        >
          Analyze Data
        </button>
        
        <button
          onClick={() => handleAction('analyze_and_store')}
          disabled={loading}
          className="bg-red-500 text-white px-4 py-2 rounded disabled:bg-red-300"
        >
          Analyze and Store in DB
        </button>
      </div>
      
      {loading && <p className="text-gray-600">Processing...</p>}
      {message && <p className="text-gray-800">{message}</p>}
    </div>
  )
}

export default AdminPanel