document.addEventListener('DOMContentLoaded', () => {
    checkAuthStatus();
});

async function checkAuthStatus() {
    try {
        const res = await fetch('/api/profile');
        if (res.ok) {
            const data = await res.json();
            const authNav = document.getElementById('auth-nav');
            if (authNav) {
                authNav.innerHTML = `
                    <li class="nav-item"><a class="nav-link" href="/dashboard">Dashboard (${data.user.name})</a></li>
                    ${data.user.is_admin ? '<li class="nav-item"><a class="nav-link text-warning" href="/admin">Admin Panel</a></li>' : ''}
                    <li class="nav-item"><a class="nav-link" href="#" onclick="logout()">Logout</a></li>
                `;
            }
        }
    } catch (err) {
        console.error("Auth check failed", err);
    }
}

async function logout() {
    await fetch('/api/logout', { method: 'POST' });
    window.location.href = '/';
}
