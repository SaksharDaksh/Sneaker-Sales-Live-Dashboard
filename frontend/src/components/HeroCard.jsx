import { AreaChart, Area, ResponsiveContainer } from "recharts";
import heroSneaker from "../assets/hero-sneaker.jpg";
import "./HeroCard.css";

function formatINR(n) {
  if (n === undefined || n === null) return "—";
  if (n >= 100000) return "₹" + (n / 100000).toFixed(2) + "L";
  return "₹" + Number(n).toLocaleString("en-IN");
}

export default function HeroCard({ revenue, trend, topRegion, topRegionShare }) {
  const sparkData = trend ? trend.slice(-16) : [];

  return (
    <div className="hero-card">
      <img
        src={heroSneaker}
        alt=""
        className="hero-card__photo"
        aria-hidden="true"
      />
      <div className="hero-card__scrim" aria-hidden="true" />

      <div className="hero-card__content">
        <div className="hero-card__eyebrow">Total Revenue</div>
        <div className="hero-card__figure">{formatINR(revenue)}</div>

        <div className="hero-card__spark" aria-hidden="true">
          {sparkData.length > 1 && (
            <ResponsiveContainer width="100%" height={48}>
              <AreaChart data={sparkData}>
                <defs>
                  <linearGradient id="sparkFill" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#ffb020" stopOpacity={0.6} />
                    <stop offset="100%" stopColor="#ffb020" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <Area
                  type="monotone"
                  dataKey="revenue"
                  stroke="#ffb020"
                  strokeWidth={2}
                  fill="url(#sparkFill)"
                />
              </AreaChart>
            </ResponsiveContainer>
          )}
        </div>

        <div className="hero-card__stats">
          <div className="hero-card__stat">
            <span className="hero-card__stat-dot" />
            <span>
              <strong>{topRegionShare}</strong> from {topRegion || "—"}
            </span>
          </div>
          <div className="hero-card__stat">
            <span className="hero-card__stat-dot hero-card__stat-dot--dark" />
            <span>Live order feed, refreshing every 5s</span>
          </div>
        </div>
      </div>
    </div>
  );
}