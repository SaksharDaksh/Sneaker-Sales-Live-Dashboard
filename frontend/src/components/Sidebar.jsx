import { Home, Shuffle, BarChart2, MessageCircle } from "lucide-react";
import "./Sidebar.css";

const ITEMS = [
  { icon: Home, label: "Overview", active: true },
  { icon: Shuffle, label: "Live feed" },
  { icon: BarChart2, label: "Reports" },
  { icon: MessageCircle, label: "Notes" },
];

export default function Sidebar() {
  return (
    <nav className="sidebar" aria-label="Primary">
      <div className="sidebar__mark" aria-hidden="true">
        ◆
      </div>
      <ul className="sidebar__list">
        {ITEMS.map(({ icon: Icon, label, active }) => (
          <li key={label}>
            <button
              type="button"
              className={`sidebar__btn ${active ? "sidebar__btn--active" : ""}`}
              aria-current={active ? "page" : undefined}
              title={label}
            >
              <Icon size={18} strokeWidth={2} />
              <span className="sidebar__sr">{label}</span>
            </button>
          </li>
        ))}
      </ul>
    </nav>
  );
}
