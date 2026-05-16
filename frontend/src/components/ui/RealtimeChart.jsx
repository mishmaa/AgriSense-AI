import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from 'recharts';

const tooltipStyle = {
  border: '1px solid rgba(18, 183, 106, 0.22)',
  borderRadius: 8,
  background: 'rgba(6, 16, 13, 0.92)',
  color: '#eafff5'
};

export default function RealtimeChart({ data, type = 'area', dataKey = 'moisture', secondaryKey, height = 280 }) {
  const common = (
    <>
      <CartesianGrid strokeDasharray="3 3" stroke="rgba(148, 163, 184, 0.22)" />
      <XAxis dataKey="time" tickLine={false} axisLine={false} tick={{ fill: '#94a3b8', fontSize: 12 }} />
      <YAxis tickLine={false} axisLine={false} tick={{ fill: '#94a3b8', fontSize: 12 }} width={34} />
      <Tooltip contentStyle={tooltipStyle} />
    </>
  );

  return (
    <div className="min-h-[220px] w-full min-w-0" style={{ height }}>
      <ResponsiveContainer width="100%" height={height} minWidth={0} minHeight={220}>
        {type === 'bar' ? (
          <BarChart data={data}>
            {common}
            <Bar dataKey={dataKey} fill="#12b76a" radius={[6, 6, 0, 0]} />
          </BarChart>
        ) : type === 'line' ? (
          <LineChart data={data}>
            {common}
            <Line dataKey={dataKey} type="monotone" stroke="#34d987" strokeWidth={3} dot={false} />
            {secondaryKey && <Line dataKey={secondaryKey} type="monotone" stroke="#38bdf8" strokeWidth={3} dot={false} />}
          </LineChart>
        ) : (
          <AreaChart data={data}>
            <defs>
              <linearGradient id="chartFill" x1="0" x2="0" y1="0" y2="1">
                <stop offset="5%" stopColor="#34d987" stopOpacity={0.45} />
                <stop offset="95%" stopColor="#34d987" stopOpacity={0.02} />
              </linearGradient>
            </defs>
            {common}
            <Area dataKey={dataKey} type="monotone" stroke="#34d987" strokeWidth={3} fill="url(#chartFill)" />
          </AreaChart>
        )}
      </ResponsiveContainer>
    </div>
  );
}
