import "./RegionPanel.css";

export default function RegionPanel({ regions }) {
  const max = regions?.length ? Math.max(...regions.map((r) => r.revenue)) : 0;

  return (
    <div className="region-panel">
      <h2 className="region-panel__title">Top Regions</h2>

      {!regions || regions.length === 0 ? (
        <p className="region-panel__empty">Waiting for sales data...</p>
      ) : (
        <ul className="region-panel__list">
          {regions.slice(0, 6).map((r) => (
            <li key={r.region} className="region-panel__row">
              <span className="region-panel__name">{r.region}</span>
              <span className="region-panel__track">
                <span
                  className="region-panel__fill"
                  style={{ width: `${max ? (r.revenue / max) * 100 : 0}%` }}
                />
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
