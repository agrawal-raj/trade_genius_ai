import { configureStore } from '@reduxjs/toolkit'
import companiesReducer from './slices/companiesSlice'
import analysisReducer from './slices/analysisSlice'

export const store = configureStore({
  reducer: {
    companies: companiesReducer,
    analysis: analysisReducer,
  },
})

export default store