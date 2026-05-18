import { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  RadialLinearScale, PointElement, LineElement,
  Filler, Tooltip, Legend,
} from 'chart.js';
import { Radar } from 'react-chartjs-2';
import { HiOutlinePlus, HiOutlineX, HiOutlineCheck, HiOutlineExclamation, HiOutlineClock } from 'react-icons/hi';
import { fetchUser, fetchSkillTrends, fetchGapAnalysis, fetchMatchScore, addUserSkill, updateUserSkill, deleteUserSkill } from '../services/api';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

export default function Profile() {
  const [user, setUser] = useState(null);
  const [skills, setSkills] = useState([]);
  const [trends, setTrends] = useState([]);
  const [gap, setGap] = useState({ matched: [], missing: [], outdated: [] });
  const [matchScore, setMatchScore] = useState(0);
  const [newSkill, setNewSkill] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  async function loadAll() {
    try {
      const [u, t, g, m] = await Promise.all([
        fetchUser(),
        fetchSkillTrends(),
        fetchGapAnalysis(),
        fetchMatchScore(),
      ]);
      setUser(u);
      setSkills(u.skills || []);
      setTrends(t);
      setGap(g);
      setMatchScore(m.score);
    } catch (err) {
      console.error("Failed to load profile data:", err);
      setError("Could not load profile from backend.");
      setGap({ matched: [], missing: [], outdated: [] });
      setMatchScore(0);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { loadAll(); }, []);

  // Radar data
  const marketDemand = {};
  trends.forEach(s => { marketDemand[s.name] = s.demand?.[s.demand.length - 1] || 50; });
  const radarSkills = skills.slice(0, 8);
  const maxDemand = Math.max(...Object.values(marketDemand), 1);

  const radarData = {
    labels: radarSkills.map(s => s.name),
    datasets: [
      {
        label: 'Your Proficiency',
        data: radarSkills.map(s => s.proficiency),
        backgroundColor: 'hsla(250,90%,65%,0.15)',
        borderColor: 'hsl(250,90%,65%)',
        borderWidth: 2,
        pointBackgroundColor: 'hsl(250,90%,65%)',
      },
      {
        label: 'Market Demand',
        data: radarSkills.map(s => ((marketDemand[s.name] || 50) / maxDemand) * 100),
        backgroundColor: 'hsla(155,70%,50%,0.1)',
        borderColor: 'hsl(155,70%,50%)',
        borderWidth: 2,
        pointBackgroundColor: 'hsl(155,70%,50%)',
      },
    ],
  };

  const radarOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      r: {
        beginAtZero: true,
        max: 100,
        ticks: { color: 'hsl(220,10%,45%)', backdropColor: 'transparent', font: { size: 9 } },
        grid: { color: 'hsla(225,15%,20%,0.5)' },
        pointLabels: { color: 'hsl(220,12%,65%)', font: { family: 'Inter', size: 11 } },
        angleLines: { color: 'hsla(225,15%,20%,0.4)' },
      },
    },
    plugins: {
      legend: {
        labels: { color: 'hsl(220,12%,65%)', font: { family: 'Inter', size: 11 }, usePointStyle: true, pointStyle: 'circle' },
      },
      tooltip: {
        backgroundColor: 'hsl(225,22%,11%)',
        borderColor: 'hsl(225,15%,20%)',
        borderWidth: 1,
        padding: 12,
        cornerRadius: 8,
      },
    },
  };

  const handleAddSkill = async () => {
    const trimmed = newSkill.trim();
    if (!trimmed || skills.find(s => s.name.toLowerCase() === trimmed.toLowerCase())) return;
    try {
      await addUserSkill(trimmed, 50);
      setNewSkill('');
      await loadAll(); // Refresh everything
    } catch {
      // Fallback local
      setSkills([...skills, { name: trimmed, proficiency: 50 }]);
      setNewSkill('');
    }
  };

  const handleRemoveSkill = async (name) => {
    try {
      await deleteUserSkill(name);
      await loadAll();
    } catch {
      setSkills(skills.filter(s => s.name !== name));
    }
  };

  const handleUpdateProficiency = async (name, val) => {
    // Optimistic local update
    setSkills(skills.map(s => s.name === name ? { ...s, proficiency: Number(val) } : s));
    try {
      await updateUserSkill(name, Number(val));
    } catch { /* already updated locally */ }
  };

  // SVG Gauge
  const circumference = 2 * Math.PI * 70;
  const dashOffset = circumference - (matchScore / 100) * circumference;

  if (loading) return <div className="animate-in"><div className="card" style={{ padding: 40, textAlign: 'center' }}>Loading profile…</div></div>;
  if (error) return <div className="animate-in"><div className="card" style={{ padding: 40, textAlign: 'center', color: 'red' }}>{error}</div></div>;

  const profile = user || { name: 'Unknown', university: '', degree: '', semester: '' };

  return (
    <div className="animate-in">
      {/* Profile header */}
      <div className="profile-header">
        <div className="profile-avatar">
          {profile.name.split(' ').map(n => n[0]).join('')}
        </div>
        <div className="profile-info">
          <h2>{profile.name}</h2>
          <p>{profile.university}</p>
          <p>{profile.degree} · Semester {profile.semester}</p>
        </div>
      </div>

      <div className="two-col" style={{ marginBottom: 24 }}>
        {/* Skill management */}
        <div className="card">
          <h3 style={{ marginBottom: 16 }}>🎯 Your Skills</h3>
          <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
            <input
              className="input"
              placeholder="Add a skill…"
              value={newSkill}
              onChange={e => setNewSkill(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleAddSkill()}
            />
            <button className="btn btn-primary" onClick={handleAddSkill}>
              <HiOutlinePlus /> Add
            </button>
          </div>

          <div style={{ maxHeight: 340, overflowY: 'auto' }}>
            {skills.map(s => (
              <div className="skill-bar" key={s.name}>
                <span className="skill-bar-name">{s.name}</span>
                <div className="skill-bar-track">
                  <div className="skill-bar-fill" style={{ width: `${s.proficiency}%` }} />
                </div>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={s.proficiency}
                  onChange={e => handleUpdateProficiency(s.name, e.target.value)}
                  style={{ width: 60, accentColor: 'hsl(250,90%,65%)' }}
                />
                <span className="skill-bar-value">{s.proficiency}%</span>
                <button
                  className="btn-icon"
                  onClick={() => handleRemoveSkill(s.name)}
                  style={{ width: 28, height: 28, minWidth: 28, fontSize: '0.8rem' }}
                >
                  <HiOutlineX />
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Radar Chart + Gauge */}
        <div className="card">
          <h3 style={{ marginBottom: 16 }}>📊 Skills vs Market Demand</h3>
          <div className="chart-container" style={{ height: 300 }}>
            <Radar data={radarData} options={radarOptions} />
          </div>

          <div className="gauge-container" style={{ marginTop: 24 }}>
            <div className="gauge-ring">
              <svg width="160" height="160">
                <circle cx="80" cy="80" r="70" stroke="hsl(225,15%,20%)" strokeWidth="8" fill="none" />
                <circle
                  cx="80" cy="80" r="70"
                  stroke={matchScore >= 70 ? 'hsl(155,70%,50%)' : matchScore >= 40 ? 'hsl(38,90%,55%)' : 'hsl(0,75%,60%)'}
                  strokeWidth="8"
                  fill="none"
                  strokeDasharray={circumference}
                  strokeDashoffset={dashOffset}
                  strokeLinecap="round"
                  style={{ transition: 'stroke-dashoffset 0.8s ease' }}
                />
              </svg>
              <span className="gauge-value" style={{ color: matchScore >= 70 ? 'hsl(155,70%,50%)' : matchScore >= 40 ? 'hsl(38,90%,55%)' : 'hsl(0,75%,60%)' }}>
                {matchScore}%
              </span>
            </div>
            <span className="gauge-label">Market Match Score</span>
          </div>
        </div>
      </div>

      {/* Gap analysis */}
      <div className="three-col">
        <div className="card">
          <h3 style={{ marginBottom: 14, display: 'flex', alignItems: 'center', gap: 8 }}>
            <HiOutlineCheck style={{ color: 'hsl(155,70%,50%)' }} /> Matched Skills ({gap.matched.length})
          </h3>
          <div className="gap-list">
            {gap.matched.map(s => (
              <div className="gap-item matched" key={s.name}>
                <span className="gap-item-name">{s.name}</span>
                <span className="gap-item-status">✓ Matched ({s.proficiency}%)</span>
              </div>
            ))}
          </div>
        </div>

        <div className="card">
          <h3 style={{ marginBottom: 14, display: 'flex', alignItems: 'center', gap: 8 }}>
            <HiOutlineExclamation style={{ color: 'hsl(0,75%,60%)' }} /> Missing Skills ({gap.missing.length})
          </h3>
          <div className="gap-list">
            {gap.missing.map(s => (
              <div className="gap-item missing" key={s.name}>
                <span className="gap-item-name">{s.name}</span>
                <span className="gap-item-status">✗ Missing</span>
              </div>
            ))}
          </div>
        </div>

        <div className="card">
          <h3 style={{ marginBottom: 14, display: 'flex', alignItems: 'center', gap: 8 }}>
            <HiOutlineClock style={{ color: 'hsl(38,90%,55%)' }} /> Needs Improvement ({gap.outdated.length})
          </h3>
          <div className="gap-list">
            {gap.outdated.length === 0 ? (
              <p style={{ color: 'hsl(220,10%,45%)', fontSize: '0.85rem' }}>No outdated skills detected</p>
            ) : (
              gap.outdated.map(s => (
                <div className="gap-item outdated" key={s.name}>
                  <span className="gap-item-name">{s.name}</span>
                  <span className="gap-item-status">⚠ Low ({s.proficiency}%)</span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
