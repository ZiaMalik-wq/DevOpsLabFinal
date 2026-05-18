import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import SkillTrends from './pages/SkillTrends';
import Profile from './pages/Profile';
import Roadmap from './pages/Roadmap';
import JobExplorer from './pages/JobExplorer';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="trends" element={<SkillTrends />} />
          <Route path="profile" element={<Profile />} />
          <Route path="roadmap" element={<Roadmap />} />
          <Route path="jobs" element={<JobExplorer />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
