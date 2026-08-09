import "./TreadBars.css";

export default function TreadBars({ categories }) {
  const max = categories?.length ? Math.max(...categories.map((c) => c.revenue)) : 0;

  return (
    <div className="tread-card">
      <h2 className="tread-card__title">Sales by Type</h2>

      {!categories || categories.length === 0 ? (
        <p className="tread-card__empty">Waiting for sales data...</p>
      ) : (
        <ul className="tread-card__list">
          {categories.map((c) => (
            <li key={c.category} className="tread-card__row">
              <span className="tread-card__label">{c.category}</span>
              <span className="tread-card__track">
                <span
                  className="tread-card__fill"
                  style={{ width: `${max ? (c.revenue / max) * 100 : 0}%` }}
                >
                  <span className="tread-card__notches" aria-hidden="true" />
                </span>
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
