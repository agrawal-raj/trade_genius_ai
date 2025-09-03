import React from 'react'

const ProsConsBadges = ({ title, items, type }) => {
  if (!items || items.length === 0) {
    return (
      <div className='bg-white rounded-lg shadow-sm p-5 border border-gray-200'>
        <h2 className="text-xl font-semibold mb-4 text-gray-800 flex items-center">
          {type === 'pros' ? (
            <span className='w-4 h-4 bg-green-500 rounded-full mr-2'></span>
          ) : (
            <span className='w-4 h-4 bf-red-500 rounded-full mr-2'></span>
          )}
          {title}
          </h2>
        <p className="text-gray-500">No {type === 'pros' ? 'strengths' : 'weaknesses'} available.</p>
      </div>
    )
  }

  return (
    <div className='bg-white rounded-lg shadow-sm p-5 border-gray-200'>
      <h2 className="text-xl font-semibold mb-4 text-gray-800 flex items-center">
        {type === 'pros' ? (
          <span className='w-4 h-4 bg-green-500 rounded-full mr-2'></span>
        ): (
          <span className='w-4 h-4 bg-red-500 rounded-full mr-2'></span>
        )}
        {title}
        </h2>
      <div className="space-y-3">
        {items.map((item, index) => (
          <div
            key={index}
            className={`p-3 rounded-lg ${
              type === 'pros'
                ? 'bg-green-100 border-l-4 border-green-500'
                : 'bg-red-100 border-l-4 border-red-500'
            }`}
          >
            <div className="flex items-start">
              <span
                className={`mr-3 mt-1 ${
                  type === 'pros' ? 'text-green-500' : 'text-red-500'
                }`}
              >
                {type === 'pros' ? '✔' : '✖'}
              </span>
              <p
                className={
                  type === 'pros' ? 'text-green-700' : 'text-red-700'
                }
              >
                {item}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default ProsConsBadges