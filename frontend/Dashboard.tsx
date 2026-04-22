import Watchlist from "../components/Watchlist";
import Chart from "../components/Chart";
import Navbar from "../components/Navbar";

export default function Dashboard() {
  return (
    <div>
      <Navbar />
      <div style={{ display: "flex" }}>
        <Watchlist />
        <Chart symbol="BTCUSDT" />
      </div>
    </div>
  );
}