import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { fetchCompanies } from '../../services/api'

export const getCompanies = createAsyncThunk(
  'companies/getCompanies',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetchCompanies()
      return response.data
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch companies')
    }
  }
)

const companiesSlice = createSlice({
  name: 'companies',
  initialState: {
    companies: [],
    loading: false,
    error: null,
  },
  reducers: {
    clearCompanies: (state) => {
    state.companies = []
    state.loading = false
    state.error = null
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(getCompanies.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(getCompanies.fulfilled, (state, action) => {
        state.loading = false
        state.companies = action.payload || []
      })
      .addCase(getCompanies.rejected, (state, action) => {
        state.loading = false
        state.error = []
      })
  },
})

export const { clearCompanies } = companiesSlice.actions
export default companiesSlice.reducer