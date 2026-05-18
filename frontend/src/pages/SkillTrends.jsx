import { useState, useEffect, useMemo } from 'react';
import {
  Chart as ChartJS,
  CategoryScale, LinearScale, PointElement, LineElement,
  Title, Tooltip, Legend, Filler,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import { HiOutlineSearch, HiOutlineTrendingUp, HiOutlineTrendingDown } from 'react-icons/hi';
import { fetchSkillTrends } from '../services/api';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler);

const MONTHS = [
  'Apr 25', 'May 25', 'Jun 25', 'Jul 25', 'Aug 25', 'Sep 25',
  'Oct 25', 'Nov 25', 'Dec 25', 'Jan 26', 'Feb 26', 'Mar 26',
];

const categoryTagClass = (cat) => {
  if (cat.includes('AI'))    return 'tag tag-ai';
  if (cat.includes('Web'))   return 'tag tag-web';
  if (cat.includes('Data'))  return 'tag tag-data';
  if (cat.includes('Cloud')) return 'tag tag-cloud';
  if (cat.includes('Sec'))   return 'tag tag-sec';
  return 'tag';
};

export default function SkillTrends() {
  const [allTrends, setAllTrends] = useState([]);
  const [search, setSearch] = useState('');
  const [catFilter, setCatFilter] = useState('All');
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchSkillTrends();
        setAllTrends(data);
        setSelected(data.find(s => s.name === 'LLMs') || data[0]);
      } catch (err) {
        console.error("Failed to load skill trends:", err);
        setError("Failed to load skill trends from backend.");
        setAllTrends([]);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const categories = ['All', ...new Set(allTrends.map(s => s.category))];

  const filtered = useMemo(() => {
    return allTrends.filter(s => {
      const matchSearch = s.name.toLowerCase().includes(search.toLowerCase());
      const matchCat = catFilter === 'All' || s.category === catFilter;
      return matchSearch && matchCat;
    });
  }, [allTrends, search, catFilter]);

  const rising = [...allTrends].sort((a, b) => b.growth - a.growth).slice(0, 8);
  const declining = [...allTrends].sort((a, b) => a.growth - b.growth).slice(0, 8);

  if (loading) return <div className="animate-in"><div className="card" style={{ padding: 40, textAlign: 'center' }}>Loading trends…</div></div>;
  if (error) return <div className="animate-in"><div className="card" style={{ padding: 40, textAlign: 'center', color: 'red' }}>{error}</div></div>;
  if (!selected) return <div className="animate-in"><div className="card" style={{ padding: 40, textAlign: 'center' }}>No data</div></div>;

  const chartData = {
    labels: MONTHS,
    datasets: [{
      label: selected.name,
      data: selected.demand,
      borderColor: 'hsl(250,90%,65%)',
      backgroundColor: 'hsla(250,90%,65%,0.08)',
      fill: true,
      tension: 0.4,
      pointRadius: 4,
      pointHoverRadius: 7,
      pointBackgroundColor: 'hsl(250,90%,65%)',
      pointBorderColor: 'hsl(225,20%,13%)',
      pointBorderWidth: 2,
    }],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: 'hsl(225,22%,11%)',
        borderColor: 'hsl(225,15%,20%)',
        borderWidth: 1,
        titleFont: { family: 'Inter', weight: '600' },
        bodyFont: { family: 'Inter' },
        padding: 12,
        cornerRadius: 8,
      },
    },
    scales: {
      x: { ticks: { color: 'hsl(220,10%,45%)', font: { family: 'Inter', size: 10 } }, grid: { color: 'hsla(225,15%,20%,0.4)' } },
      y: { ticks: { color: 'hsl(220,10%,45%)', font: { family: 'Inter', size: 10 } }, grid: { color: 'hsla(225,15%,20%,0.4)' }, beginAtZero: false },
    },
  };

  return (
    <div className="animate-in">
      {/* Filters */}
      <div className="filters-row">
        <div className="search-box">
          <HiOutlineSearch />
          <input
            placeholder="Search skills…"
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
        </div>
        <select className="input" value={catFilter} onChange={e => setCatFilter(e.target.value)} style={{ width: 200 }}>
          {categories.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
      </div>

      {/* Time series chart */}
      <div className="card chart-card" style={{ marginBottom: 20 }}>
        <h3>📈 Demand Over Time — <span style={{ color: 'hsl(250,90%,75%)' }}>{selected.name}</span></h3>
        <p style={{ fontSize: '0.8rem', color: 'hsl(220,10%,45%)', marginBottom: 16 }}>
          Category: {selected.category} &nbsp;·&nbsp; Growth: <span style={{ color: selected.growth > 0 ? 'hsl(155,70%,50%)' : 'hsl(0,75%,60%)' }}>
            {selected.growth > 0 ? '+' : ''}{selected.growth}%
          </span> &nbsp;·&nbsp; Avg Salary: {selected.avgSalary}
        </p>
        <div className="chart-container" style={{ height: 280 }}>
          <Line data={chartData} options={chartOptions} />
        </div>
      </div>

      {/* Table + Rising/Declining */}
      <div className="two-col">
        {/* Skills Table */}
        <div className="card" style={{ overflow: 'auto', maxHeight: 480 }}>
          <h3 style={{ marginBottom: 16 }}>All Tracked Skills</h3>
          <table className="data-table">
            <thead>
              <tr>
                <th>Skill</th>
                <th>Category</th>
                <th>Growth</th>
                <th>Salary</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map(s => (
                <tr
                  key={s.name}
                  onClick={() => setSelected(s)}
                  style={{ cursor: 'pointer', background: selected.name === s.name ? 'hsla(250,90%,65%,0.08)' : undefined }}
                >
                  <td style={{ fontWeight: 500 }}>{s.name}</td>
                  <td><span className={categoryTagClass(s.category)}>{s.category}</span></td>
                  <td>
                    <span style={{ color: s.growth >= 15 ? 'hsl(155,70%,50%)' : s.growth >= 5 ? 'hsl(38,90%,55%)' : 'hsl(220,12%,65%)' }}>
                      {s.growth > 0 ? '+' : ''}{s.growth}%
                    </span>
                  </td>
                  <td style={{ color: 'hsl(220,12%,65%)' }}>{s.avgSalary}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Rising / Declining */}
        <div>
          <div className="card" style={{ marginBottom: 20 }}>
            <h3 style={{ marginBottom: 14, display: 'flex', alignItems: 'center', gap: 8 }}>
              <HiOutlineTrendingUp style={{ color: 'hsl(155,70%,50%)' }} /> Rising Skills
            </h3>
            {rising.map(s => (
              <div className="trend-item" key={s.name}>
                <span className="trend-item-name">{s.name}</span>
                <span className="growth up">+{s.growth}%</span>
              </div>
            ))}
          </div>

          <div className="card">
            <h3 style={{ marginBottom: 14, display: 'flex', alignItems: 'center', gap: 8 }}>
              <HiOutlineTrendingDown style={{ color: 'hsl(0,75%,60%)' }} /> Slower Growth
            </h3>
            {declining.map(s => (
              <div className="trend-item" key={s.name}>
                <span className="trend-item-name">{s.name}</span>
                <span className={`growth ${s.growth < 5 ? 'down' : 'up'}`}>+{s.growth}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
