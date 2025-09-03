import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { fetchCompanyAnalysis } from '../../services/api'

export const getCompanyAnalysis = createAsyncThunk(
  'analysis/getCompanyAnalysis',
  async (companyId, { rejectWithValue }) => {
    try {
      const response = await fetchCompanyAnalysis(companyId)
      console.log('API Response:', response.data) // Debug point
      return response.data
    } catch (error) {
      console.error('API Error:', error)
      return rejectWithValue(error.response?.data || {message: 'Network error'})
    }
  }
)

const analysisSlice = createSlice({
  name: 'analysis',
  initialState: {
    data: null,
    loading: false,
    error: null,
  },
  reducers: {
    clearAnalysis: (state) => {
      state.data = null
      state.loading= false
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(getCompanyAnalysis.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(getCompanyAnalysis.fulfilled, (state, action) => {
        state.loading = false
        state.data = action.payload
        state.error =  null
      })
      .addCase(getCompanyAnalysis.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })
  },
})

export const { clearAnalysis } = analysisSlice.actions
export default analysisSlice.reducer