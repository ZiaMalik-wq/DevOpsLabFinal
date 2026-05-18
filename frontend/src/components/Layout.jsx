import { NavLink, Outlet, useLocation } from 'react-router-dom';
import { HiOutlineChartBar, HiOutlineTrendingUp, HiOutlineUser, HiOutlineMap, HiOutlineBriefcase, HiOutlineSearch } from 'react-icons/hi';

const navItems = [
  { to: '/',         label: 'Dashboard',        icon: <HiOutlineChartBar /> },
  { to: '/trends',   label: 'Skill Trends',     icon: <HiOutlineTrendingUp /> },
  { to: '/profile',  label: 'Profile & Gaps',   icon: <HiOutlineUser /> },
  { to: '/roadmap',  label: 'Upskilling Roadmap',icon: <HiOutlineMap /> },
  { to: '/jobs',     label: 'Job Explorer',      icon: <HiOutlineBriefcase /> },
];

const pageTitles = {
  '/':        'Dashboard',
  '/trends':  'Skill Trend Analysis',
  '/profile': 'Profile & Gap Analysis',
  '/roadmap': 'Upskilling Roadmap',
  '/jobs':    'Job Data Explorer',
};

export default function Layout() {
  const location = useLocation();
  const title = pageTitles[location.pathname] || 'Dashboard';

  return (
    <div className="app-layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="sidebar-brand-icon">🎯</div>
          <h1>SkillGap<span>AI Analyzer</span></h1>
        </div>

        <nav className="sidebar-nav">
          {navItems.map(item => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
            >
              {item.icon}
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="sidebar-avatar">
            {'HR'.split(' ').map(n => n[0]).join('')}
          </div>
          <div className="sidebar-footer-info">
            <h4>Kumail Raza</h4>
            <p>BS CS · Sem 8</p>
          </div>
        </div>
      </aside>

      {/* Main */}
      <main className="main-content">
        <header className="topbar">
          <h2 className="topbar-title">{title}</h2>
          <div className="topbar-actions">
            <div className="search-box">
              <HiOutlineSearch />
              <input placeholder="Search skills, jobs…" />
            </div>
          </div>
        </header>

        <div className="page-content">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
