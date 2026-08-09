import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import "./TrendCard.css";

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="trend-tip">
      <div className="trend-tip__label">{label}</div>
      <div>₹{payload[0].value.toLocaleString("en-IN")}</div>
    </div>
  );
}

export default function TrendCard({ data }) {
  const trimmed = data ? data.slice(-16) : [];

  return (
    <div className="trend-card">
      <h2 className="trend-card__title">Sales Trend</h2>
      {!data || data.length === 0 ? (
        <p className="trend-card__empty">Waiting for sales data...</p>
      ) : (
        <ResponsiveContainer width="100%" height={170}>
          <LineChart data={trimmed} margin={{ top: 4, right: 4, left: -18, bottom: 0 }}>
            <CartesianGrid stroke="#e4ddcd" strokeDasharray="3 3" vertical={false} />
            <XAxis
              dataKey="minute"
              tick={{ fill: "#726d60", fontSize: 9, fontFamily: "JetBrains Mono" }}
              axisLine={{ stroke: "#e4ddcd" }}
              tickLine={false}
              tickFormatter={(v) => v?.split(" ")[1] || v}
            />
            <YAxis
              tick={{ fill: "#726d60", fontSize: 10, fontFamily: "JetBrains Mono" }}
              axisLine={false}
              tickLine={false}
              width={46}
            />
            <Tooltip content={<CustomTooltip />} />
            <Line
              type="monotone"
              dataKey="revenue"
              stroke="#ff5b2e"
              strokeWidth={2.5}
              dot={false}
              activeDot={{ r: 4, fill: "#ff5b2e" }}
            />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}
