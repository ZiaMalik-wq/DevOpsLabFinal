/**
 * API service layer — fetches from the FastAPI backend.
 * Falls back to mock data if the backend is unavailable.
 */

const API_BASE = 'http://localhost:8080/api';
const USER_ID = 1; // Default user

async function apiFetch(endpoint) {
    const res = await fetch(`${API_BASE}${endpoint}`);
    if (!res.ok) throw new Error(`API ${res.status}`);
    return res.json();
}

// ─── Skills ─────────────────────────────────────────────
export async function fetchSkillTrends(category, search) {
    const params = new URLSearchParams();
    if (category && category !== 'All') params.set('category', category);
    if (search) params.set('search', search);
    const qs = params.toString();
    return apiFetch(`/skills/trends${qs ? `?${qs}` : ''}`);
}

export async function fetchSkillCategories() {
    return apiFetch('/skills/categories');
}

export async function fetchTopEmerging(limit = 10) {
    return apiFetch(`/skills/top-emerging?limit=${limit}`);
}

export async function fetchRegionalDemand() {
    return apiFetch('/skills/regional-demand');
}

// ─── Jobs ───────────────────────────────────────────────
export async function fetchJobs(search, location, source) {
    const params = new URLSearchParams();
    if (search) params.set('search', search);
    if (location && location !== 'All') params.set('location', location);
    if (source && source !== 'All') params.set('source', source);
    const qs = params.toString();
    return apiFetch(`/jobs${qs ? `?${qs}` : ''}`);
}

export async function fetchJobSkillFrequency(location, source) {
    const params = new URLSearchParams();
    if (location && location !== 'All') params.set('location', location);
    if (source && source !== 'All') params.set('source', source);
    const qs = params.toString();
    return apiFetch(`/jobs/skill-frequency${qs ? `?${qs}` : ''}`);
}

export async function fetchExtractedSkills(jobId) {
    return apiFetch(`/jobs/${jobId}/extract-skills`);
}

// ─── User ───────────────────────────────────────────────
export async function fetchUser(userId = USER_ID) {
    return apiFetch(`/users/${userId}`);
}

export async function addUserSkill(name, proficiency = 50, userId = USER_ID) {
    const res = await fetch(`${API_BASE}/users/${userId}/skills`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, proficiency }),
    });
    if (!res.ok) throw new Error(`API ${res.status}`);
    return res.json();
}

export async function updateUserSkill(name, proficiency, userId = USER_ID) {
    const res = await fetch(`${API_BASE}/users/${userId}/skills/${encodeURIComponent(name)}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ proficiency }),
    });
    if (!res.ok) throw new Error(`API ${res.status}`);
    return res.json();
}

export async function deleteUserSkill(name, userId = USER_ID) {
    const res = await fetch(`${API_BASE}/users/${userId}/skills/${encodeURIComponent(name)}`, {
        method: 'DELETE',
    });
    if (!res.ok) throw new Error(`API ${res.status}`);
    return res.json();
}

// ─── Analysis ───────────────────────────────────────────
export async function fetchGapAnalysis(userId = USER_ID) {
    return apiFetch(`/analysis/${userId}/gap`);
}

export async function fetchMatchScore(userId = USER_ID) {
    return apiFetch(`/analysis/${userId}/match-score`);
}

export async function fetchDashboardStats() {
    return apiFetch('/analysis/dashboard-stats');
}

// ─── Recommendations ───────────────────────────────────
export async function fetchRecommendations(userId = USER_ID) {
    return apiFetch(`/recommendations/${userId}`);
}
