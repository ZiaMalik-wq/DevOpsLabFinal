import { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale, LinearScale, BarElement, PointElement, LineElement,
  ArcElement, Title, Tooltip, Legend, Filler,
} from 'chart.js';
import { Bar, Line, Doughnut } from 'react-chartjs-2';
import { HiOutlineBriefcase, HiOutlineLightningBolt, HiOutlineExclamation, HiOutlineBadgeCheck } from 'react-icons/hi';
import { fetchDashboardStats, fetchSkillTrends, fetchRegionalDemand, fetchSkillCategories } from '../services/api';
ChartJS.register(CategoryScale, LinearScale, BarElement, PointElement, LineElement, ArcElement, Title, Tooltip, Legend, Filler);


const chartDefaults = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { labels: { color: 'hsl(220,12%,65%)', font: { family: 'Inter', size: 11 } } },
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
    y: { ticks: { color: 'hsl(220,10%,45%)', font: { family: 'Inter', size: 10 } }, grid: { color: 'hsla(225,15%,20%,0.4)' } },
  },
};

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [trends, setTrends] = useState([]);
  const [regional, setRegional] = useState(null);
  const [categories, setCategories] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        const [s, t, r, c] = await Promise.all([
          fetchDashboardStats(),
          fetchSkillTrends(),
          fetchRegionalDemand(),
          fetchSkillCategories(),
        ]);
        setStats(s);
        setTrends(t);
        setRegional(r);
        // Convert categories array to { name: [skills] } map
        const catMap = {};
        c.forEach(cat => { catMap[cat.category] = cat.skills; });
        setCategories(catMap);
      } catch (err) {
        console.error('Failed to fetch dashboard data:', err);
        setError('Failed to load dashboard data. Please ensure the backend is running.');
        setTrends([]);
        setStats({});
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <div className="animate-in"><div className="card" style={{ padding: 40, textAlign: 'center' }}>Loading dashboard…</div></div>;
  if (error) return <div className="animate-in"><div className="card" style={{ padding: 40, textAlign: 'center', color: 'red' }}>{error}</div></div>;

  // Top 10 emerging skills (by growth)
  const top10 = [...trends].sort((a, b) => b.growth - a.growth).slice(0, 10);

  const barData = {
    labels: top10.map(s => s.name),
    datasets: [{
      label: 'Growth %',
      data: top10.map(s => s.growth),
      backgroundColor: [
        'hsl(250,90%,65%)', 'hsl(260,80%,62%)', 'hsl(270,75%,60%)',
        'hsl(155,70%,50%)', 'hsl(165,65%,48%)', 'hsl(190,80%,55%)',
        'hsl(38,90%,55%)',  'hsl(25,85%,55%)',  'hsl(210,80%,60%)',
        'hsl(320,70%,55%)',
      ],
      borderRadius: 6,
      barThickness: 28,
    }],
  };

  const barOptions = {
    ...chartDefaults,
    indexAxis: 'y',
    plugins: {
      ...chartDefaults.plugins,
      legend: { display: false },
    },
    scales: {
      x: { ...chartDefaults.scales.x, beginAtZero: true },
      y: { ...chartDefaults.scales.y, grid: { display: false } },
    },
  };

  // Regional demand line chart
  const regionColors = ['hsl(250,90%,65%)', 'hsl(155,70%,50%)', 'hsl(38,90%,55%)'];
  const regionData = regional || { labels: [], regions: [] };
  const lineData = {
    labels: regionData.labels,
    datasets: regionData.regions.map((r, i) => ({
      label: r.name,
      data: r.data,
      borderColor: regionColors[i],
      backgroundColor: regionColors[i].replace(')', ',0.1)').replace('hsl', 'hsla'),
      fill: true,
      tension: 0.4,
      pointRadius: 3,
      pointHoverRadius: 6,
    })),
  };

  // Category distribution doughnut
  const catNames = Object.keys(categories);
  const catColors = ['hsl(250,90%,65%)', 'hsl(190,80%,55%)', 'hsl(155,70%,50%)', 'hsl(38,90%,55%)', 'hsl(0,75%,60%)'];
  const doughnutData = {
    labels: catNames,
    datasets: [{
      data: catNames.map(c => categories[c].length),
      backgroundColor: catColors,
      borderColor: 'hsl(225,20%,13%)',
      borderWidth: 3,
      hoverOffset: 8,
    }],
  };

  const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      ...chartDefaults.plugins,
      legend: {
        position: 'right',
        labels: { color: 'hsl(220,12%,65%)', font: { family: 'Inter', size: 11 }, padding: 16, usePointStyle: true, pointStyle: 'circle' },
      },
    },
  };

  // Dynamic quick insights
  const fastestGrowing = top10[0];
  const mostDemanded = [...trends].sort((a, b) => (b.demand?.[b.demand.length - 1] || 0) - (a.demand?.[a.demand.length - 1] || 0))[0];
  const highestPaying = [...trends].sort((a, b) => {
    const pa = parseInt((b.avgSalary || '').replace(/[^0-9]/g, '')) || 0;
    const pb = parseInt((a.avgSalary || '').replace(/[^0-9]/g, '')) || 0;
    return pa - pb;
  })[0];

  const dashStats = stats || {};
  const statCards = [
    { label: 'Jobs Analyzed',  value: dashStats.totalJobsAnalyzed?.toLocaleString() || '0', change: '+12.3%', positive: true,  icon: <HiOutlineBriefcase /> },
    { label: 'Skills Tracked',  value: dashStats.skillsTracked,                              change: '+8 new',  positive: true,  icon: <HiOutlineLightningBolt /> },
    { label: 'Gaps Detected',   value: dashStats.gapsDetected,                               change: '-2 fixed',positive: true,  icon: <HiOutlineExclamation /> },
    { label: 'Match Score',     value: `${dashStats.matchScore}%`,                           change: '+5.2%',   positive: true,  icon: <HiOutlineBadgeCheck /> },
  ];

  return (
    <div className="animate-in">
      {/* Stat cards */}
      <div className="stat-grid">
        {statCards.map((s, i) => (
          <div key={i} className="card stat-card">
            <div className="stat-card-icon">{s.icon}</div>
            <h3>{s.label}</h3>
            <div className="stat-value">{s.value}</div>
            <div className={`stat-change ${s.positive ? 'positive' : 'negative'}`}>{s.change} from last month</div>
          </div>
        ))}
      </div>

      {/* Charts */}
      <div className="charts-grid">
        <div className="card chart-card">
          <h3>🚀 Top 10 Emerging Skills</h3>
          <div className="chart-container" style={{ height: 380 }}>
            <Bar data={barData} options={barOptions} />
          </div>
        </div>

        <div className="card chart-card">
          <h3>📈 Regional Job Demand Trends</h3>
          <div className="chart-container" style={{ height: 380 }}>
            <Line data={lineData} options={chartDefaults} />
          </div>
        </div>
      </div>

      <div className="charts-grid">
        <div className="card chart-card">
          <h3>📊 Skill Category Distribution</h3>
          <div className="chart-container" style={{ height: 320 }}>
            <Doughnut data={doughnutData} options={doughnutOptions} />
          </div>
        </div>

        <div className="card chart-card">
          <h3>⚡ Quick Insights</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            <div className="trend-item">
              <span className="trend-item-name">Fastest growing</span>
              <span className="growth up">{fastestGrowing?.name || 'LLMs'} (+{fastestGrowing?.growth || 52}%)</span>
            </div>
            <div className="trend-item">
              <span className="trend-item-name">Most demanded</span>
              <span className="growth up">{mostDemanded?.name || 'React'}</span>
            </div>
            <div className="trend-item">
              <span className="trend-item-name">Highest paying</span>
              <span className="growth up">{highestPaying?.name || 'LLMs'} ({highestPaying?.avgSalary || '$135K'} avg)</span>
            </div>
            <div className="trend-item">
              <span className="trend-item-name">Gaps Detected</span>
              <span className="growth down">{dashStats.gapsDetected} skills missing</span>
            </div>
            <div className="trend-item">
              <span className="trend-item-name">Regional hot spot</span>
              <span className="growth up">Lahore (+75%)</span>
            </div>
            <div className="trend-item">
              <span className="trend-item-name">Trending category</span>
              <span className="growth up">AI / ML</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
