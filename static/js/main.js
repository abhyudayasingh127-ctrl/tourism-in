document.addEventListener('DOMContentLoaded', () => {
    // 1. User Auth Status Check call
    checkAuthStatus();

    // 2. Budget Input Event Listener Attach
    const budgetInput = document.getElementById('budgetInput');
    if (budgetInput) {
        budgetInput.addEventListener('input', calculateBudgetSplit);
    }

    // 3. Dark/Light Mode Theme Initialization & Toggle Listener
    initThemeToggle();

    // 4. Instant Client-Side Search Setup
    initInstantSearch();
});

// User Logged-In check karne ka function
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

// User Logout function
async function logout() {
    await fetch('/api/logout', { method: 'POST' });
    window.location.href = '/';
}

// Budget Calculation Logic (Hotel, Food, Boat Split)
function calculateBudgetSplit() {
    const budgetVal = document.getElementById('budgetInput').value;
    const total = parseFloat(budgetVal) || 0;

    // Budget Percent Breakdown
    // Hotel: 45% | Food: 35% | Boat Booking: 20%
    const hotelCost = Math.round(total * 0.45);
    const foodCost = Math.round(total * 0.35);
    const boatCost = Math.round(total * 0.20);

    // Dynamic UI Update
    const hotelElem = document.getElementById('hotelBudget');
    const foodElem = document.getElementById('foodBudget');
    const boatElem = document.getElementById('boatBudget');

    if (hotelElem) hotelElem.innerText = `₹${hotelCost}`;
    if (foodElem) foodElem.innerText = `₹${foodCost}`;
    if (boatElem) boatElem.innerText = `₹${boatCost}`;
}

// -------------------------------------------------------------
// Lightweight Hacks & Feature Additions
// -------------------------------------------------------------

// 1. Dark/Light Mode Toggle Functionality
function initThemeToggle() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);

    const themeToggleBtn = document.getElementById('theme-toggle');
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }
}

// 2. Client-Side Instant Fuzzy Search Filter
function initInstantSearch() {
    const searchInput = document.getElementById('instant-search');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            const items = document.querySelectorAll('.searchable-item');

            items.forEach(item => {
                const text = item.textContent.toLowerCase();
                item.style.display = text.includes(query) ? '' : 'none';
            });
        });
    }
}

// 3. Ultra-Light Open-Meteo Weather Fetcher (No API Key Required)
async function fetchWeather(lat, lon, elementId) {
    const container = document.getElementById(elementId);
    if (!container) return;

    try {
        const response = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true`);
        const data = await response.json();
        const temp = data.current_weather.temperature;
        container.innerHTML = `🌤️ ${temp}°C`;
    } catch (err) {
        container.innerHTML = `🌤️ N/A`;
    }
}
