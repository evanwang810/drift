document.addEventListener('DOMContentLoaded', function() {
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
});
