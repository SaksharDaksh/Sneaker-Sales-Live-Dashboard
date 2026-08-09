import "./TopSellers.css";

const SWATCHES = ["#ff5b2e", "#ffb020", "#16150f", "#e64520", "#726d60"];

function formatINR(n) {
  return "₹" + Number(n).toLocaleString("en-IN", { maximumFractionDigits: 0 });
}

export default function TopSellers({ products }) {
  return (
    <div className="top-sellers">
      <h2 className="top-sellers__title">Top Selling Sneakers</h2>

      {!products || products.length === 0 ? (
        <p className="top-sellers__empty">Waiting for sales data...</p>
      ) : (
        <ul className="top-sellers__list">
          {products.slice(0, 5).map((p, i) => (
            <li key={p.product} className="top-sellers__row">
              <span
                className="top-sellers__swatch"
                style={{ background: SWATCHES[i % SWATCHES.length] }}
              />
              <div className="top-sellers__info">
                <span className="top-sellers__name">{p.product}</span>
                <span className="top-sellers__brand">{p.brand}</span>
              </div>
              <span className="top-sellers__revenue">{formatINR(p.revenue)}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
