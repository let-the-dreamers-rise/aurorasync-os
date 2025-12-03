import { motion } from 'framer-motion'
import { ChevronUp, ChevronDown, ChevronsUpDown } from 'lucide-react'
import { cn } from '@/utils/cn'
import { useState } from 'react'

const DataTable = ({ columns, data, onRowClick, className }) => {
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' })

  const handleSort = (key) => {
    let direction = 'asc'
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc'
    }
    setSortConfig({ key, direction })
  }

  const sortedData = [...data].sort((a, b) => {
    if (!sortConfig.key) return 0
    
    const aValue = a[sortConfig.key]
    const bValue = b[sortConfig.key]
    
    if (aValue < bValue) return sortConfig.direction === 'asc' ? -1 : 1
    if (aValue > bValue) return sortConfig.direction === 'asc' ? 1 : -1
    return 0
  })

  const getSortIcon = (columnKey) => {
    if (sortConfig.key !== columnKey) return ChevronsUpDown
    return sortConfig.direction === 'asc' ? ChevronUp : ChevronDown
  }

  return (
    <div className={cn('glass rounded-lg border border-aurora-bg-tertiary overflow-hidden', className)}>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-aurora-bg-tertiary">
            <tr>
              {columns.map((column) => {
                const SortIcon = getSortIcon(column.key)
                return (
                  <th
                    key={column.key}
                    className={cn(
                      'px-4 py-3 text-left text-xs font-medium text-aurora-text-muted uppercase tracking-wider',
                      column.sortable && 'cursor-pointer hover:bg-aurora-bg-hover transition-colors'
                    )}
                    onClick={() => column.sortable && handleSort(column.key)}
                  >
                    <div className="flex items-center gap-2">
                      {column.label}
                      {column.sortable && (
                        <SortIcon className="w-4 h-4" />
                      )}
                    </div>
                  </th>
                )
              })}
            </tr>
          </thead>
          <tbody className="divide-y divide-aurora-bg-tertiary">
            {sortedData.map((row, index) => (
              <motion.tr
                key={row.id || index}
                className={cn(
                  'hover:bg-aurora-bg-hover transition-colors',
                  onRowClick && 'cursor-pointer'
                )}
                onClick={() => onRowClick && onRowClick(row)}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.05 }}
              >
                {columns.map((column) => (
                  <td
                    key={column.key}
                    className="px-4 py-3 text-sm text-aurora-text-secondary"
                  >
                    {column.render ? column.render(row[column.key], row) : row[column.key]}
                  </td>
                ))}
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>
      
      {data.length === 0 && (
        <div className="p-8 text-center">
          <p className="text-aurora-text-muted">No data available</p>
        </div>
      )}
    </div>
  )
}

export default DataTable
