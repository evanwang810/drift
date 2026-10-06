/**
 * Interactive features for the Drift website
 * Handles chart rendering, filtering, sorting, and search
 */

// --- Chart rendering for runs.html ---
const COLORS = {stopped: 'var(--ok)', out_of_turns: 'var(--warn)', out_of_time: 'var(--warn)',
                api_error: 'var(--bad)', crashed: 'var(--bad)'};
const LABELS = {stopped: 'stopped on its own', out_of_turns: 'ran out of turns',
                out_of_time: 'ran out of time', api_error: 'API would not answer', crashed: 'crashed'};
const NS = 'http://www.w3.org/2000/svg';

function drawChart(runs) {
  const svg = document.getElementById('chart');
  const W = 1000, H = 360, L = 56, R = 12, T = 12, B = 36;
  svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
  const maxRun = runs[runs.length - 1].run;
  const maxTokens = Math.max(...runs.map(r => r.tokens), 1);
  const x = n => L + (n - 1) / Math.max(maxRun - 1, 1) * (W - L - R);
  const y = t => H - B - t / maxTokens * (H - T - B);

  for (let i = 0; i <= 4; i++) {
    const t = maxTokens * i / 4, yy = y(t);
    const line = document.createElementNS(NS, 'line');
    line.setAttribute('x1', L);
    line.setAttribute('x2', W - R);
    line.setAttribute('y1', yy);
    line.setAttribute('y2', yy);
    line.setAttribute('class', 'grid');
    svg.appendChild(line);
    const text = document.createElementNS(NS, 'text');
    text.setAttribute('x', L - 8);
    text.setAttribute('y', yy + 4);
    text.setAttribute('class', 'axis');
    text.setAttribute('text-anchor', 'end');
    text.textContent = t >= 1e6 ? (t / 1e6).toFixed(1) + 'M' : Math.round(t / 1e3) + 'k';
    svg.appendChild(text);
  }

  const step = maxRun > 300 ? 100 : 50;
  for (let n = step; n <= maxRun; n += step) {
    const text = document.createElementNS(NS, 'text');
    text.setAttribute('x', x(n));
    text.setAttribute('y', H - B + 22);
    text.setAttribute('class', 'axis');
    text.setAttribute('text-anchor', 'middle');
    text.textContent = 'run ' + n;
    svg.appendChild(text);
  }

  const tip = document.getElementById('tip');
  for (const r of runs) {
    const dot = document.createElementNS(NS, 'circle');
    dot.setAttribute('cx', x(r.run));
    dot.setAttribute('cy', y(r.tokens));
    dot.setAttribute('r', 4.5);
    dot.setAttribute('tabindex', 0);
    dot.setAttribute('fill', COLORS[r.outcome] || 'var(--muted)');
    dot.setAttribute('class', 'dot');
    const show = () => {
      tip.innerHTML = `<b>Run ${r.run}</b> <span>${r.when} UTC</span>
        <div>${LABELS[r.outcome] || r.outcome} &middot; ${r.turns} turns &middot; ${r.tokens.toLocaleString()} tokens</div>
        ${r.note && r.note !== 'used every turn' ? `<p>${r.note.replace(/</g, '&lt;')}</p>` : ''}`;
      tip.hidden = false;
    };
    dot.addEventListener('mouseenter', show);
    dot.addEventListener('focus', show);
    dot.addEventListener('click', show);
    svg.appendChild(dot);
  }
}

function drawLegend(runs) {
  const count = {};
  for (const r of runs) count[r.outcome] = (count[r.outcome] || 0) + 1;
  const legend = document.getElementById('legend');
  for (const [k, n] of Object.entries(count).sort((a, b) => b[1] - a[1])) {
    const li = document.createElement('li');
    li.innerHTML = `<i style="background:${COLORS[k] || 'var(--muted)'}"></i>${LABELS[k] || k} <b>${n}</b>`;
    legend.appendChild(li);
  }
}

// --- Knowledge base filtering and sorting ---
function initKnowledgeBase() {
    const entries = document.querySelectorAll('.knowledge-entry');
    const filterButtons = document.querySelectorAll('.filter-btn[data-filter]');
    const searchInput = document.getElementById('search-input');
    const sortButtons = document.querySelectorAll('.sort-btn[data-sort]');
    const tagCheckboxes = document.querySelectorAll('.tag-filter');

    let currentFilter = 'all';
    let currentSort = 'title';
    let searchQuery = '';
    let activeTags = new Set();

    // Type filtering
    filterButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            filterButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentFilter = this.dataset.filter;
            filterAndSort();
        });
    });

    // Tag filtering
    tagCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                activeTags.add(this.value);
            } else {
                activeTags.delete(this.value);
            }
            filterAndSort();
        });
    });

    // Search
    searchInput.addEventListener('input', function() {
        searchQuery = this.value.toLowerCase().trim();
        filterAndSort();
    });

    // Sorting
    sortButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            sortButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentSort = this.dataset.sort;
            filterAndSort();
        });
    });

    function filterAndSort() {
        let filtered = Array.from(entries);

        // Apply type filter
        if (currentFilter !== 'all') {
            filtered = filtered.filter(entry => entry.dataset.type === currentFilter);
        }

        // Apply tag filter
        if (activeTags.size > 0) {
            filtered = filtered.filter(entry => {
                const entryTags = entry.dataset.tags.toLowerCase().split(' ');
                return Array.from(activeTags).some(tag => entryTags.includes(tag.toLowerCase()));
            });
        }

        // Apply search filter
        if (searchQuery) {
            filtered = filtered.filter(entry => {
                const text = entry.textContent.toLowerCase();
                return text.includes(searchQuery);
            });
        }

        // Sort
        filtered.sort((a, b) => {
            const aData = { title: a.querySelector('h3').textContent.toLowerCase(), type: a.dataset.type };
            const bData = { title: b.querySelector('h3').textContent.toLowerCase(), type: b.dataset.type };

            switch(currentSort) {
                case 'title':
                    return aData.title.localeCompare(bData.title);
                case 'type':
                    return aData.type.localeCompare(bData.type);
                case 'date':
                    return parseFloat(a.dataset.date) - parseFloat(b.dataset.date);
                case 'relevance':
                    const aRelevance = calculateRelevance(a, searchQuery);
                    const bRelevance = calculateRelevance(b, searchQuery);
                    return bRelevance - aRelevance;
                default:
                    return 0;
            }
        });

        // Update display
        entries.forEach(entry => {
            entry.style.display = filtered.includes(entry) ? '' : 'none';
        });
    }

    function calculateRelevance(entry, query) {
        if (!query) return 0;
        const text = entry.textContent.toLowerCase();
        const title = entry.querySelector('h3').textContent.toLowerCase();

        let score = 0;
        if (title.includes(query)) score += 10;
        if (text.includes(query)) score += 5;

        const tags = entry.dataset.tags.toLowerCase().split(' ');
        tags.forEach(tag => {
            if (tag.includes(query)) score += 3;
        });

        return score;
    }
}

// --- Search functionality for search.html ---
function initSearch() {
    const searchInput = document.getElementById('search-input');
    const resultsContainer = document.getElementById('results-container');
    const searchBtn = document.getElementById('search-btn');

    async function performSearch() {
        const query = searchInput.value.trim();
        if (!query) {
            resultsContainer.innerHTML = '<p class="no-results">Enter a search term to find content</p>';
            return;
        }

        try {
            const response = await fetch(`../search_index.json?q=${encodeURIComponent(query)}`);
            if (!response.ok) throw new Error('Search failed');
            const data = await response.json();
            displayResults(data.results, query);
        } catch (error) {
            console.error('Search error:', error);
            resultsContainer.innerHTML = '<p class="no-results">Search failed. Please try again.</p>';
        }
    }

    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performSearch();
    });

    // Auto-search on input (debounced)
    let debounceTimer;
    searchInput.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(performSearch, 300);
    });

    function displayResults(results, query) {
        const countEl = document.querySelector('.results-count');
        if (countEl) countEl.textContent = `${results.length} results for "${query}"`;

        if (results.length === 0) {
            resultsContainer.innerHTML = '<p class="no-results">No results found. Try a different search term.</p>';
            return;
        }

        resultsContainer.innerHTML = results.map(item => {
            const typeBadge = {
                knowledge: 'badge knowledge',
                documentation: 'badge documentation',
                posts: 'badge posts'
            }[item.type] || 'badge';
            return `
            <div class="result-item">
                <div class="result-header">
                    <span class="${typeBadge}">${item.type}</span>
                    <span class="result-score">${Math.round(item.score)}%</span>
                </div>
                <div class="result-title">${item.title}</div>
                <div class="result-description">${item.description.substring(0, 150)}...</div>
                <div class="result-tags">Tags: ${item.tags.join(', ')}</div>
            </div>`;
        }).join('');
    }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on runs page
    if (document.getElementById('chart')) {
        fetch('../runs.json')
            .then(r => r.json())
            .then(runs => {
                drawChart(runs);
                drawLegend(runs);
            });
    }

    // Check if we're on knowledge base page
    if (document.getElementById('knowledge-list')) {
        initKnowledgeBase();
    }

    // Check if we're on search page
    if (document.getElementById('search-input')) {
        initSearch();
    }
});
