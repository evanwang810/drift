// Knowledge Base Enhanced JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // State
    let allEntries = [];
    let filteredEntries = [];
    let activeCategories = new Set();
    let activeTags = new Set();
    let searchTerm = '';

    // Category definitions
    const categories = {
        'Tool Fixes': {
            type: 'tool_fix',
            icon: '🔧',
            color: '#1976d2'
        },
        'Discoveries': {
            type: 'discovery',
            icon: '💡',
            color: '#f57c00'
        },
        'Platform': {
            type: 'platform',
            icon: '🖥️',
            color: '#388e3c'
        },
        'Research': {
            type: ['research', 'tool_improvement', 'tool_limitation'],
            icon: '🔬',
            color: '#7b1fa2'
        },
        'Workflow': {
            type: 'workflow',
            icon: '⚙️',
            color: '#009688'
        }
    };

    // Fetch entries from JSON
    async function fetchEntries() {
        try {
            const response = await fetch('knowledge_base.json');
            allEntries = await response.json();
            filteredEntries = [...allEntries];
            renderAll();
        } catch (error) {
            console.error('Error fetching entries:', error);
            document.getElementById('entries-grid').innerHTML = `
                <div class="empty-state">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                    </svg>
                    <p>Error loading knowledge base entries.</p>
                </div>
            `;
        }
    }

    // Filter entries
    function filterEntries() {
        filteredEntries = allEntries.filter(entry => {
            // Category filter
            const typeMatches = activeCategories.size === 0 ||
                entry.type === 'tool_fix' ||
                entry.type === 'discovery' ||
                entry.type === 'platform' ||
                ['research', 'tool_improvement', 'tool_limitation'].includes(entry.type) ||
                entry.type === 'workflow';

            // Tag filter
            const tagsMatch = activeTags.size === 0 ||
                entry.tags.some(tag => activeTags.has(tag));

            // Search filter
            const searchMatch = !searchTerm ||
                entry.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                entry.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                entry.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));

            return typeMatches && tagsMatch && searchMatch;
        });

        updateResultsCount();
        renderEntries();
    }

    // Update results count
    function updateResultsCount() {
        const countEl = document.getElementById('results-count');
        if (countEl) {
            countEl.textContent = `Showing ${filteredEntries.length} of ${allEntries.length} entries`;
        }
    }

    // Render category buttons
    function renderCategories() {
        const container = document.getElementById('category-filters');
        if (!container) return;

        container.innerHTML = Object.entries(categories).map(([name, data]) => `
            <button class="category-btn ${activeCategories.has(name) ? 'active' : ''}"
                    data-category="${name}">
                ${data.icon} ${name}
            </button>
        `).join('');

        // Add event listeners
        container.querySelectorAll('.category-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const category = btn.dataset.category;
                if (activeCategories.has(category)) {
                    activeCategories.delete(category);
                } else {
                    activeCategories.add(category);
                }
                btn.classList.toggle('active', activeCategories.has(category));
                filterEntries();
            });
        });
    }

    // Render tag checkboxes
    function renderTags() {
        const container = document.getElementById('tag-filters');
        if (!container) return;

        // Collect all unique tags
        const allTags = new Set();
        allEntries.forEach(entry => {
            entry.tags.forEach(tag => allTags.add(tag));
        });

        const sortedTags = Array.from(allTags).sort();

        container.innerHTML = `
            <label>Tags:</label>
            <div class="tag-grid">
                ${sortedTags.map(tag => `
                    <label class="tag-checkbox ${activeTags.has(tag) ? 'active' : ''}">
                        <input type="checkbox" value="${tag}" ${activeTags.has(tag) ? 'checked' : ''}>
                        ${tag}
                    </label>
                `).join('')}
            </div>
        `;

        // Add event listeners
        container.querySelectorAll('.tag-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', () => {
                const tag = checkbox.value;
                if (checkbox.checked) {
                    activeTags.add(tag);
                    checkbox.classList.add('active');
                } else {
                    activeTags.delete(tag);
                    checkbox.classList.remove('active');
                }
                filterEntries();
            });
        });
    }

    // Render entries
    function renderEntries() {
        const container = document.getElementById('entries-grid');
        if (!container) return;

        if (filteredEntries.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                    </svg>
                    <p>No entries match your filters.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = filteredEntries.map(entry => {
            const category = getCategoryByType(entry.type);
            return `
                <article class="entry-card ${category ? 'category-' + category : ''}">
                    <div class="entry-card-header">
                        <h3>${escapeHtml(entry.title)}</h3>
                        <span class="entry-type-badge type-${entry.type}">${entry.type}</span>
                    </div>
                    <div class="entry-card-body">
                        <p class="entry-description">${escapeHtml(entry.description)}</p>
                        <div class="entry-meta">
                            <span class="entry-source">
                                📝 ${escapeHtml(entry.source)}
                            </span>
                            ${entry.impact ? `<span class="entry-impact">✓ Impact: ${escapeHtml(entry.impact)}</span>` : ''}
                        </div>
                        ${entry.tags && entry.tags.length > 0 ? `
                            <div class="entry-tags">
                                ${entry.tags.map(tag => `<span class="entry-tag">${escapeHtml(tag)}</span>`).join('')}
                            </div>
                        ` : ''}
                        ${entry.implementation ? `
                            <div class="entry-implementation">
                                <strong>Implementation:</strong> ${escapeHtml(entry.implementation)}
                            </div>
                        ` : ''}
                        ${entry.verification ? `
                            <div class="entry-verification">
                                <strong>Verification:</strong> ${escapeHtml(entry.verification)}
                            </div>
                        ` : ''}
                    </div>
                </article>
            `;
        }).join('');
    }

    // Render all components
    function renderAll() {
        renderCategories();
        renderTags();
        renderEntries();
    }

    // Get category by type
    function getCategoryByType(type) {
        for (const [name, data] of Object.entries(categories)) {
            if (Array.isArray(data.type)) {
                if (data.type.includes(type)) return name.toLowerCase().replace(' ', '_');
            } else if (data.type === type) {
                return name.toLowerCase().replace(' ', '_');
            }
        }
        return null;
    }

    // Escape HTML
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Search functionality
    function setupSearch() {
        const searchInput = document.getElementById('search-input');
        if (!searchInput) return;

        let debounceTimer;

        searchInput.addEventListener('input', (e) => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                searchTerm = e.target.value.trim();
                filterEntries();
            }, 300);
        });
    }

    // Initialize
    fetchEntries().then(() => {
        setupSearch();
        renderAll();
    });
});
