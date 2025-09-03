import React from 'react'
import { Link } from 'react-router-dom'

const Navigation = () => {
  return (
    <nav className="bg-blue-600 text-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <Link to="/" className="text-xl font-bold">
            Blue Mutual Fund
          </Link>
          <div className="space-x-4">
            <Link to="/" className="hover:text-blue-200 transition-colors">
              Home
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navigation