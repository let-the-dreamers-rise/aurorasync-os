import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'
import { cn } from '@/utils/cn'
import Card from './ui/Card'

const ForecastGraph = ({ data, title, type = 'line', className }) => {
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="glass border border-aurora-bg-tertiary rounded-lg p-3">
          <p className="text-sm font-medium text-aurora-text-primary mb-2">{label}</p>
          {payload.map((entry, index) => (
            <div key={index} className="flex items-center gap-2">
              <div
                className="w-3 h-3 rounded-full"
                style={{ backgroundColor: entry.color }}
              />
              <span className="text-xs text-aurora-text-secondary">
                {entry.name}: {entry.value}
              </span>
            </div>
          ))}
        </div>
      )
    }
    return null
  }

  return (
    <Card className={cn('', className)}>
      {title && (
        <h3 className="text-lg font-semibold text-aurora-text-primary mb-4">{title}</h3>
      )}
      <ResponsiveContainer width="100%" height={300}>
        {type === 'line' ? (
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1a1f2e" />
            <XAxis
              dataKey="date"
              stroke="#6b7280"
              style={{ fontSize: '12px' }}
            />
            <YAxis
              stroke="#6b7280"
              style={{ fontSize: '12px' }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend
              wrapperStyle={{ fontSize: '12px', color: '#9ca3af' }}
            />
            <Line
              type="monotone"
              dataKey="value"
              stroke="#00d4ff"
              strokeWidth={2}
              dot={{ fill: '#00d4ff', r: 4 }}
              activeDot={{ r: 6 }}
            />
            {data[0]?.forecast !== undefined && (
              <Line
                type="monotone"
                dataKey="forecast"
                stroke="#a855f7"
                strokeWidth={2}
                strokeDasharray="5 5"
                dot={{ fill: '#a855f7', r: 4 }}
              />
            )}
          </LineChart>
        ) : (
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1a1f2e" />
            <XAxis
              dataKey="date"
              stroke="#6b7280"
              style={{ fontSize: '12px' }}
            />
            <YAxis
              stroke="#6b7280"
              style={{ fontSize: '12px' }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend
              wrapperStyle={{ fontSize: '12px', color: '#9ca3af' }}
            />
            <Bar
              dataKey="value"
              fill="#00d4ff"
              radius={[4, 4, 0, 0]}
            />
            {data[0]?.forecast !== undefined && (
              <Bar
                dataKey="forecast"
                fill="#a855f7"
                radius={[4, 4, 0, 0]}
              />
            )}
          </BarChart>
        )}
      </ResponsiveContainer>
    </Card>
  )
}

export default ForecastGraph
