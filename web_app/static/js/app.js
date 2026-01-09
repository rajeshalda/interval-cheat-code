// Global state
let workTypes = [];
let tasks = [];
let entryCount = 0;
let config = {};

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadConfig();
    await loadWorkTypes();
    await loadTasks();
    addEntry(); // Add first entry by default
    setupEventListeners();
});

// Load configuration
async function loadConfig() {
    try {
        const response = await fetch('/api/config');
        const data = await response.json();
        config = data;
    } catch (error) {
        console.error('Failed to load config:', error);
    }
}

// Load work types from API
async function loadWorkTypes() {
    try {
        const response = await fetch('/api/work-types');
        const data = await response.json();

        if (data.success) {
            workTypes = data.work_types;
        } else {
            showError('Failed to load work types');
        }
    } catch (error) {
        showError('Error loading work types: ' + error.message);
    }
}

// Load tasks from API
async function loadTasks() {
    try {
        const response = await fetch('/api/tasks');
        const data = await response.json();

        if (data.success) {
            tasks = data.tasks;
        } else {
            console.warn('Failed to load tasks');
        }
    } catch (error) {
        console.warn('Error loading tasks:', error);
    }
}

// Setup event listeners
function setupEventListeners() {
    document.getElementById('addEntryBtn').addEventListener('click', addEntry);
    document.getElementById('previewBtn').addEventListener('click', showPreview);
    document.getElementById('submitBtn').addEventListener('click', submitEntries);
    document.getElementById('importJsonBtn').addEventListener('click', () => {
        document.getElementById('importModal').style.display = 'block';
    });
    document.getElementById('confirmImportBtn').addEventListener('click', importFromJson);
    document.getElementById('confirmSubmitBtn').addEventListener('click', submitEntries);

    // Modal close buttons
    document.querySelectorAll('.close, .close-modal').forEach(el => {
        el.addEventListener('click', (e) => {
            e.target.closest('.modal').style.display = 'none';
        });
    });

    // Close modal on outside click
    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            e.target.style.display = 'none';
        }
    });
}

// Add new entry form
function addEntry(data = {}) {
    entryCount++;
    const container = document.getElementById('entriesContainer');

    const entryCard = document.createElement('div');
    entryCard.className = 'entry-card';
    entryCard.dataset.entryId = entryCount;

    entryCard.innerHTML = `
        <div class="entry-header">
            <span class="entry-number">Entry #${entryCount}</span>
            <button class="remove-btn" onclick="removeEntry(${entryCount})">✕ Remove</button>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label>Date</label>
                <input type="date" class="entry-date" value="${data.date || config.today || ''}" required>
            </div>

            <div class="form-group">
                <label>Work Type</label>
                <select class="entry-worktype" required>
                    <option value="">Select work type...</option>
                    ${workTypes.map(wt => `
                        <option value="${wt.id}" ${data.work_type === wt.name || data.work_type_id == wt.id ? 'selected' : ''}>
                            ${wt.name}
                        </option>
                    `).join('')}
                </select>
            </div>

            <div class="form-group">
                <label>Duration (hours)</label>
                <input type="number" class="entry-time" step="0.25" min="0.25" value="${data.time || '8.00'}" required>
            </div>
        </div>

        <div class="form-row">
            <div class="form-group" style="grid-column: 1 / -1;">
                <label>Task</label>
                <select class="entry-task" required>
                    <option value="">Select task...</option>
                    ${tasks.map(task => `
                        <option value="${task.id}" ${data.task_id == task.id ? 'selected' : ''}>
                            ${task.title} - ${task.project}
                        </option>
                    `).join('')}
                </select>
            </div>
        </div>

        <div class="form-row">
            <div class="form-group" style="grid-column: 1 / -1;">
                <label>Description</label>
                <textarea class="entry-description" placeholder="What did you work on?">${data.description || ''}</textarea>
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <div class="checkbox-group">
                    <input type="checkbox" class="entry-billable" id="billable-${entryCount}" ${data.billable ? 'checked' : ''}>
                    <label for="billable-${entryCount}">Billable</label>
                </div>
            </div>
        </div>
    `;

    container.appendChild(entryCard);
}

// Remove entry
function removeEntry(entryId) {
    const entryCard = document.querySelector(`[data-entry-id="${entryId}"]`);
    if (entryCard) {
        entryCard.remove();
    }

    // Renumber remaining entries
    const remainingEntries = document.querySelectorAll('.entry-card');
    remainingEntries.forEach((card, index) => {
        const numberSpan = card.querySelector('.entry-number');
        numberSpan.textContent = `Entry #${index + 1}`;
    });
}

// Collect all entry data
function collectEntries() {
    const entries = [];
    const entryCards = document.querySelectorAll('.entry-card');

    entryCards.forEach(card => {
        const entry = {
            date: card.querySelector('.entry-date').value,
            work_type_id: card.querySelector('.entry-worktype').value,
            time: card.querySelector('.entry-time').value,
            task_id: card.querySelector('.entry-task').value,
            description: card.querySelector('.entry-description').value,
            billable: card.querySelector('.entry-billable').checked
        };

        // Validate
        if (entry.date && entry.work_type_id && entry.time && entry.task_id) {
            entries.push(entry);
        }
    });

    return entries;
}

// Show preview modal
function showPreview() {
    const entries = collectEntries();

    if (entries.length === 0) {
        showError('Please add at least one complete entry');
        return;
    }

    const previewContent = document.getElementById('previewContent');
    previewContent.innerHTML = entries.map((entry, index) => {
        const workType = workTypes.find(wt => wt.id == entry.work_type_id);
        return `
            <div class="preview-item">
                <strong>Entry ${index + 1}</strong><br>
                Date: ${entry.date}<br>
                Work Type: ${workType ? workType.name : entry.work_type_id}<br>
                Duration: ${entry.time} hours<br>
                Task ID: ${entry.task_id}<br>
                Description: ${entry.description || '(none)'}<br>
                Billable: ${entry.billable ? 'Yes' : 'No'}
            </div>
        `;
    }).join('');

    document.getElementById('previewModal').style.display = 'block';
}

// Submit entries
async function submitEntries() {
    const entries = collectEntries();

    if (entries.length === 0) {
        showError('Please add at least one complete entry');
        return;
    }

    // Close preview modal if open
    document.getElementById('previewModal').style.display = 'none';

    // Show loading state
    const submitBtn = document.getElementById('submitBtn');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Submitting...';
    submitBtn.disabled = true;

    try {
        const response = await fetch('/api/post-time', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ entries })
        });

        const data = await response.json();

        // Show results
        showResults(data);

        // Clear form if all successful
        if (data.success) {
            document.getElementById('entriesContainer').innerHTML = '';
            entryCount = 0;
            addEntry();
        }

    } catch (error) {
        showError('Error submitting entries: ' + error.message);
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

// Show results modal
function showResults(data) {
    const resultsContent = document.getElementById('resultsContent');

    if (data.success) {
        resultsContent.innerHTML = `
            <div class="result-item result-success">
                <strong>Success!</strong><br>
                All ${data.results.length} entries were posted successfully.
            </div>
            ${data.results.map(result => `
                <div class="result-item result-success">
                    Entry ID: ${result.entry_id}<br>
                    Date: ${result.date}<br>
                    Time: ${result.time} hours<br>
                    Description: ${result.description || '(none)'}
                </div>
            `).join('')}
        `;
    } else {
        resultsContent.innerHTML = data.results.map(result => {
            if (result.success) {
                return `
                    <div class="result-item result-success">
                        <strong>Success</strong><br>
                        Entry ID: ${result.entry_id}<br>
                        Description: ${result.description || '(none)'}
                    </div>
                `;
            } else {
                return `
                    <div class="result-item result-error">
                        <strong>Failed</strong><br>
                        Description: ${result.description || '(none)'}<br>
                        Error: ${result.error}
                    </div>
                `;
            }
        }).join('');
    }

    document.getElementById('resultsModal').style.display = 'block';
}

// Import from JSON
function importFromJson() {
    const jsonText = document.getElementById('jsonInput').value;

    try {
        const data = JSON.parse(jsonText);

        // Clear existing entries
        document.getElementById('entriesContainer').innerHTML = '';
        entryCount = 0;

        // Add entries from JSON
        if (data.entries && Array.isArray(data.entries)) {
            data.entries.forEach(entry => {
                // Merge with defaults from top level
                const mergedEntry = {
                    task_id: entry.task_id || data.task_id,
                    work_type_id: entry.work_type_id || data.work_type_id,
                    work_type: entry.work_type || data.work_type,
                    time: entry.time || data.time,
                    billable: entry.billable !== undefined ? entry.billable : data.billable,
                    date: entry.date,
                    description: entry.description
                };
                addEntry(mergedEntry);
            });
        }

        document.getElementById('importModal').style.display = 'none';
        document.getElementById('jsonInput').value = '';

    } catch (error) {
        showError('Invalid JSON: ' + error.message);
    }
}

// Show error message
function showError(message) {
    alert(message); // Simple for now, can be improved with toast notifications
}
