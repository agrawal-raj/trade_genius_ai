import axios from 'axios'

// const API_BASE_URL = 'https://bluemutualfund.in/server/api'
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'https://bluemutualfund.in/server/api'
// const API_BASE_URL = 'http://localhost:8000/api' 



// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('authToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('authToken')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API methods
export const fetchCompanies = async () => {
  api.get('/companies/')
  try {
    const response = await api.get('/companies/')
    return response
  }catch (error) {
    console.error("Error fetching companies:", error)
    throw error
  }
  }
  // api.get('/company.php?action=list')

export const fetchCompanyAnalysis = (companyId) => 
  api.get(`/companies/${companyId}/analysis/`)
  // api.get(`/company.php?action=analysis&id=${companyId}`)

  export const triggerFetchCompanies = () => 
  api.post('/fetch_companies/')

export const triggerPreprocessData = () => 
  api.post('/preprocess_data/')

export const triggerAnalyzeData = () => 
  api.post('/analyze_data/')

export const triggerAnalyzeAndStoreData = () => 
  api.post('/analyze_and_store_data/')
export default api