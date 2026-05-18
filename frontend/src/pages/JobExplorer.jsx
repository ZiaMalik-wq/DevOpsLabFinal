import { useState, useEffect, useMemo } from 'react';
import { HiOutlineSearch, HiOutlineLocationMarker, HiOutlineOfficeBuilding, HiOutlineCalendar, HiOutlineCurrencyDollar } from 'react-icons/hi';
import { fetchJobs } from '../services/api';

export default function JobExplorer() {
  const [allJobs, setAllJobs] = useState([]);
  const [search, setSearch] = useState('');
  const [locFilter, setLocFilter] = useState('All');
  const [sourceFilter, setSourceFilter] = useState('All');
  const [selectedJob, setSelectedJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchJobs();
        setAllJobs(data);
        setSelectedJob(data[0] || null);
      } catch (err) {
        console.error("Failed to load jobs:", err);
        setError("Could not link to backend APIs. Please ensure backend is running.");
        setAllJobs([]);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const locations = ['All', ...new Set(allJobs.map(j => j.location))];
  const sources = ['All', ...new Set(allJobs.map(j => j.source))];

  const filtered = useMemo(() => {
    return allJobs.filter(j => {
      const matchSearch = j.title.toLowerCase().includes(search.toLowerCase()) ||
                          j.company.toLowerCase().includes(search.toLowerCase()) ||
                          j.skills.some(s => s.toLowerCase().includes(search.toLowerCase()));
      const matchLoc = locFilter === 'All' || j.location === locFilter;
      const matchSource = sourceFilter === 'All' || j.source === sourceFilter;
      return matchSearch && matchLoc && matchSource;
    });
  }, [allJobs, search, locFilter, sourceFilter]);

  // Skill frequency from filtered results
  const skillFreq = useMemo(() => {
    const freq = {};
    filtered.forEach(j => j.skills.forEach(s => { freq[s] = (freq[s] || 0) + 1; }));
    return Object.entries(freq).sort((a, b) => b[1] - a[1]).slice(0, 15);
  }, [filtered]);

  if (loading) return <div className="animate-in"><div className="card" style={{ padding: 40, textAlign: 'center' }}>Loading jobs…</div></div>;
  if (error) return <div className="animate-in"><div className="card" style={{ padding: 40, textAlign: 'center', color: 'red' }}>{error}</div></div>;

  return (
    <div className="animate-in">
      {/* Filters */}
      <div className="filters-row">
        <div className="search-box">
          <HiOutlineSearch />
          <input
            placeholder="Search roles, companies, skills…"
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
        </div>
        <select className="input" value={locFilter} onChange={e => setLocFilter(e.target.value)} style={{ width: 160 }}>
          {locations.map(l => <option key={l} value={l}>{l === 'All' ? 'All Locations' : l}</option>)}
        </select>
        <select className="input" value={sourceFilter} onChange={e => setSourceFilter(e.target.value)} style={{ width: 160 }}>
          {sources.map(s => <option key={s} value={s}>{s === 'All' ? 'All Sources' : s}</option>)}
        </select>
        <span style={{ marginLeft: 'auto', fontSize: '0.82rem', color: 'hsl(220,10%,45%)' }}>
          {filtered.length} jobs found
        </span>
      </div>

      <div className="two-col" style={{ alignItems: 'start' }}>
        {/* Jobs table */}
        <div className="card" style={{ overflow: 'auto', maxHeight: 600 }}>
          <table className="data-table">
            <thead>
              <tr>
                <th>Role</th>
                <th>Company</th>
                <th>Location</th>
                <th>Source</th>
                <th>Skills</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map(j => (
                <tr
                  key={j.id}
                  onClick={() => setSelectedJob(j)}
                  style={{
                    cursor: 'pointer',
                    background: selectedJob?.id === j.id ? 'hsla(250,90%,65%,0.08)' : undefined,
                  }}
                >
                  <td style={{ fontWeight: 500, whiteSpace: 'nowrap' }}>{j.title}</td>
                  <td style={{ color: 'hsl(220,12%,65%)' }}>{j.company}</td>
                  <td style={{ color: 'hsl(220,12%,65%)', whiteSpace: 'nowrap' }}>{j.location}</td>
                  <td><span className="skill-tag">{j.source}</span></td>
                  <td style={{ maxWidth: 180 }}>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
                      {j.skills.slice(0, 3).map(s => <span className="skill-tag" key={s}>{s}</span>)}
                      {j.skills.length > 3 && <span className="skill-tag" style={{ opacity: 0.6 }}>+{j.skills.length - 3}</span>}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Detail panel + skill freq */}
        <div>
          {selectedJob && (
            <div className="detail-panel" style={{ marginBottom: 20 }}>
              <h3>{selectedJob.title}</h3>
              <p className="company">
                <HiOutlineOfficeBuilding style={{ verticalAlign: 'middle', marginRight: 4 }} />
                {selectedJob.company}
                <span style={{ margin: '0 8px', color: 'hsl(225,15%,25%)' }}>|</span>
                <HiOutlineLocationMarker style={{ verticalAlign: 'middle', marginRight: 4 }} />
                {selectedJob.location}
              </p>

              <div style={{ display: 'flex', gap: 16, marginBottom: 16, flexWrap: 'wrap' }}>
                <span style={{ fontSize: '0.82rem', color: 'hsl(220,10%,45%)', display: 'flex', alignItems: 'center', gap: 4 }}>
                  <HiOutlineCurrencyDollar /> {selectedJob.salary}
                </span>
                <span style={{ fontSize: '0.82rem', color: 'hsl(220,10%,45%)', display: 'flex', alignItems: 'center', gap: 4 }}>
                  <HiOutlineCalendar /> {selectedJob.posted}
                </span>
                <span className="skill-tag">{selectedJob.source}</span>
              </div>

              <p className="description">{selectedJob.description}</p>

              <h4 style={{ fontSize: '0.82rem', fontWeight: 600, color: 'hsl(220,10%,45%)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 8 }}>
                Extracted Skills
              </h4>
              <div className="skills-list">
                {selectedJob.skills.map(s => (
                  <span className="skill-tag" key={s} style={{ fontSize: '0.78rem', padding: '4px 10px' }}>{s}</span>
                ))}
              </div>
            </div>
          )}

          {/* Skill frequency summary */}
          <div className="card">
            <h3 style={{ marginBottom: 14, fontSize: '0.95rem' }}>📊 Skill Frequency (Filtered Results)</h3>
            {skillFreq.map(([skill, count]) => (
              <div key={skill} style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8 }}>
                <span style={{ width: 130, fontSize: '0.82rem', fontWeight: 500 }}>{skill}</span>
                <div style={{
                  flex: 1, height: 6, background: 'hsl(225,18%,15%)', borderRadius: 3, overflow: 'hidden'
                }}>
                  <div style={{
                    width: `${(count / filtered.length) * 100}%`, height: '100%',
                    background: 'linear-gradient(90deg, hsl(250,90%,65%), hsl(190,80%,55%))',
                    borderRadius: 3, transition: 'width 0.5s ease',
                  }} />
                </div>
                <span style={{ width: 40, fontSize: '0.78rem', color: 'hsl(220,10%,45%)', textAlign: 'right' }}>
                  {count}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
