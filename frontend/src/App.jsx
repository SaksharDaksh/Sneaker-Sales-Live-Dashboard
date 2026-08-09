import { useLiveData } from "./api.js";
import HeroCard from "./components/HeroCard.jsx";
import TopSellers from "./components/TopSellers.jsx";
import RegionPanel from "./components/RegionPanel.jsx";
import TrendCard from "./components/TrendCard.jsx";
import TreadBars from "./components/TreadBars.jsx";
import "./App.css";

export default function App() {
  const revenue = useLiveData("/kpi/revenue");
  const topProducts = useLiveData("/kpi/top-products");
  const byRegion = useLiveData("/kpi/by-region");
  const byCategory = useLiveData("/kpi/by-category");
  const trend = useLiveData("/kpi/trend");

  const topRegion = byRegion.data?.[0];
  const totalRegionRevenue = byRegion.data?.reduce((sum, r) => sum + r.revenue, 0) || 0;
  const topRegionShare =
    topRegion && totalRegionRevenue
      ? `${Math.round((topRegion.revenue / totalRegionRevenue) * 100)}%`
      : "—";

  return (
    <div className="shell">
      <main className="main">
        <header className="page-header">
          <div className="page-header__brand">
            <span className="page-header__mark" aria-hidden="true">
              ◆
            </span>
            <div>
              <h1 className="page-header__title">Drop Deck</h1>
              <p className="page-header__subtitle">Sneakers Only — Live Sales Dashboard</p>
            </div>
          </div>
        </header>

        <section className="grid-top">
          <div className="reveal" style={{ "--i": 0 }}>
            <HeroCard
              revenue={revenue.data?.total_revenue}
              trend={trend.data}
              topRegion={topRegion?.region}
              topRegionShare={topRegionShare}
            />
          </div>
          <div className="reveal" style={{ "--i": 1 }}>
            <TopSellers products={topProducts.data} />
          </div>
        </section>

        <section className="grid-bottom">
          <div className="reveal" style={{ "--i": 2 }}>
            <RegionPanel regions={byRegion.data} />
          </div>
          <div className="reveal" style={{ "--i": 3 }}>
            <TrendCard data={trend.data} />
          </div>
          <div className="reveal" style={{ "--i": 4 }}>
            <TreadBars categories={byCategory.data} />
          </div>
        </section>
      </main>
    </div>
  );
}