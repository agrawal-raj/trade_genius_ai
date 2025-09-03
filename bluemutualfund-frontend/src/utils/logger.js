import { store } from '../store'

const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
}

class Logger {
  constructor() {
    this.logFile = []
  }

  log(message, color = 'reset') {
    const timestamp = new Date().toISOString()
    const coloredMessage = `${colors[color]}${message}${colors.reset}`
    const logEntry = `[${timestamp}] ${message}`

    console.log(coloredMessage)
    this.logFile.push(logEntry)
  }

  logCompanyProcessing(companyId, companyName) {
    this.log(`Processing: ${companyName} (ID: ${companyId})`, 'blue')
  }

  logPros(pros) {
    if (pros && pros.length > 0) {
      this.log('Pros:', 'green')
      pros.forEach(pro => this.log(`  ✔ ${pro}`, 'green'))
    }
  }

  logCons(cons) {
    if (cons && cons.length > 0) {
      this.log('Cons:', 'red')
      cons.forEach(con => this.log(`  ✖ ${con}`, 'red'))
    }
  }

  logError(error) {
    this.log(`Error: ${error.message || error}`, 'red')
  }

  logSuccess(message) {
    this.log(message, 'green')
  }

  saveToFile() {
    // In a real implementation, this would save to a file
    // For now, we'll just keep it in memory
    console.log('Log would be saved to file with', this.logFile.length, 'entries')
  }

  // Subscribe to Redux store for real-time logging
  subscribeToStore() {
    let previousState = store.getState()

    store.subscribe(() => {
      const currentState = store.getState()
      
      // Log companies loading state - FIXED: Use correct state structure
      if (currentState.companies.loading !== previousState.companies.loading) {
        if (currentState.companies.loading) {
          this.log('Fetching companies data...', 'yellow')
        } else {
          // FIX: Use companies instead of items and add safety check
          const companiesCount = currentState.companies.companies?.length || 0
          this.log(`Companies data loaded: ${companiesCount} companies`, 'green')
        }
      }

      // Log analysis loading state
      if (currentState.analysis.loading !== previousState.analysis.loading) {
        if (currentState.analysis.loading) {
          this.log('Fetching company analysis...', 'yellow')
        } else if (currentState.analysis.data) {
          this.log('Company analysis loaded successfully', 'green')
        }
      }

      // Log errors
      if (currentState.companies.error !== previousState.companies.error && currentState.companies.error) {
        this.logError(currentState.companies.error)
      }

      if (currentState.analysis.error !== previousState.analysis.error && currentState.analysis.error) {
        this.logError(currentState.analysis.error)
      }

      previousState = currentState
    })
  }
}

export const logger = new Logger()