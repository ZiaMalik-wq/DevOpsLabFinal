import { useState, useEffect } from 'react';
import { HiOutlineStar, HiOutlineClock, HiOutlineAcademicCap, HiOutlineExternalLink } from 'react-icons/hi';
import { fetchRecommendations } from '../services/api';

const priorityConfig = {
  critical: { label: 'Critical', color: 'hsl(0,75%,60%)', bg: 'hsla(0,75%,60%,0.12)' },
  high:     { label: 'High',     color: 'hsl(38,90%,55%)', bg: 'hsla(38,90%,55%,0.12)' },
  medium:   { label: 'Medium',   color: 'hsl(250,90%,65%)', bg: 'hsla(250,90%,65%,0.12)' },
  low:      { label: 'Low',      color: 'hsl(155,70%,50%)', bg: 'hsla(155,70%,50%,0.12)' },
};

export default function Roadmap() {
  const [recommended, setRecommended] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchRecommendations();
        setRecommended(data);
      } catch {
        setRecommended([]);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <div className="animate-in"><div className="card" style={{ padding: 40, textAlign: 'center' }}>Loading roadmap…</div></div>;

  const totalWeeks = recommended.reduce((sum, c) => sum + parseInt(c.duration), 0);
  const avgRating = recommended.length > 0 ? (recommended.reduce((s, c) => s + c.rating, 0) / recommended.length).toFixed(1) : '0.0';

  return (
    <div className="animate-in">
      {/* Summary stats */}
      <div className="stat-grid" style={{ marginBottom: 28 }}>
        <div className="card stat-card">
          <div className="stat-card-icon"><HiOutlineAcademicCap /></div>
          <h3>Courses Recommended</h3>
          <div className="stat-value">{recommended.length}</div>
          <div className="stat-change positive">Personalized for your gaps</div>
        </div>
        <div className="card stat-card">
          <div className="stat-card-icon"><HiOutlineClock /></div>
          <h3>Total Learning Time</h3>
          <div className="stat-value">{totalWeeks} weeks</div>
          <div className="stat-change positive">Self-paced learning</div>
        </div>
        <div className="card stat-card">
          <div className="stat-card-icon"><HiOutlineStar /></div>
          <h3>Avg Course Rating</h3>
          <div className="stat-value">{avgRating}</div>
          <div className="stat-change positive">Top-rated courses</div>
        </div>
        <div className="card stat-card">
          <div className="stat-card-icon">🎯</div>
          <h3>Critical Gaps</h3>
          <div className="stat-value">{recommended.filter(c => c.priority === 'critical').length}</div>
          <div className="stat-change negative">Requires immediate attention</div>
        </div>
      </div>

      {/* Priority legend */}
      <div className="card" style={{ marginBottom: 24, padding: '16px 24px' }}>
        <div style={{ display: 'flex', gap: 24, alignItems: 'center', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'hsl(220,12%,65%)' }}>Priority Levels:</span>
          {Object.entries(priorityConfig).map(([key, cfg]) => (
            <span key={key} style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: '0.82rem' }}>
              <span style={{ width: 10, height: 10, borderRadius: '50%', background: cfg.color, display: 'inline-block', boxShadow: `0 0 8px ${cfg.bg}` }} />
              {cfg.label}
            </span>
          ))}
        </div>
      </div>

      {/* Timeline */}
      <div className="roadmap-timeline">
        {recommended.map((course, i) => (
          <div className="roadmap-item" key={course.id} style={{ animationDelay: `${0.1 * i}s` }}>
            <div className={`roadmap-dot ${course.priority}`}>
              {i + 1}
            </div>
            <div className="card roadmap-card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 12 }}>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 4 }}>
                    <span style={{ fontSize: '1.4rem' }}>{course.icon}</span>
                    <h4>{course.title}</h4>
                  </div>
                  <p className="provider">{course.provider} · {course.platform}</p>
                  <p style={{ fontSize: '0.85rem', color: 'hsl(220,12%,65%)' }}>
                    Fills gap: <strong style={{ color: 'hsl(250,90%,75%)' }}>{course.skill}</strong>
                    {course.growth > 0 && (
                      <span style={{ marginLeft: 12, color: 'hsl(155,70%,50%)' }}>
                        Market growth: +{course.growth}%
                      </span>
                    )}
                  </p>
                </div>
                <span
                  style={{
                    padding: '4px 12px',
                    borderRadius: 20,
                    fontSize: '0.72rem',
                    fontWeight: 600,
                    background: (priorityConfig[course.priority] || priorityConfig.medium).bg,
                    color: (priorityConfig[course.priority] || priorityConfig.medium).color,
                    textTransform: 'uppercase',
                    letterSpacing: '0.04em',
                  }}
                >
                  {(priorityConfig[course.priority] || priorityConfig.medium).label}
                </span>
              </div>

              <div className="roadmap-meta">
                <span><HiOutlineClock /> {course.duration}</span>
                <span><HiOutlineStar /> {course.rating}</span>
                <span><HiOutlineAcademicCap /> {course.level}</span>
                <a href={course.url} style={{ display: 'flex', alignItems: 'center', gap: 4, color: 'hsl(250,90%,75%)', fontSize: '0.78rem' }}>
                  <HiOutlineExternalLink /> View Course
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
