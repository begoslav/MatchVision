// Main JavaScript file for MatchVision

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initTooltips();
    
    // Auto-refresh live matches every 30 seconds
    setInterval(refreshLiveMatches, 30000);
});

/**
 * Initialize Bootstrap tooltips
 */
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Refresh live matches via API
 */
function refreshLiveMatches() {
    fetch('/api/live-matches')
        .then(response => response.json())
        .then(data => {
            if (data.count === 0) {
                console.log('No live matches');
            }
        })
        .catch(error => console.error('Error refreshing matches:', error));
}

/**
 * Create a chart for team form (last 5 matches)
 */
function createFormChart(canvasId, labels, wins, draws, losses) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Výhry',
                    data: wins,
                    backgroundColor: 'rgba(40, 167, 69, 0.7)',
                    borderColor: '#28a745',
                    borderWidth: 1
                },
                {
                    label: 'Remízy',
                    data: draws,
                    backgroundColor: 'rgba(255, 193, 7, 0.7)',
                    borderColor: '#ffc107',
                    borderWidth: 1
                },
                {
                    label: 'Prohry',
                    data: losses,
                    backgroundColor: 'rgba(220, 53, 69, 0.7)',
                    borderColor: '#dc3545',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color: '#e0e0e0'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#999'
                    },
                    grid: {
                        color: '#333'
                    }
                },
                x: {
                    ticks: {
                        color: '#999'
                    },
                    grid: {
                        color: '#333'
                    }
                }
            }
        }
    });
}

/**
 * Create a doughnut chart for match statistics
 */
function createStatsChart(canvasId, homeLabel, homeValue, awayLabel, awayValue, title = '') {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: [homeLabel, awayLabel],
            datasets: [{
                data: [homeValue, awayValue],
                backgroundColor: [
                    'rgba(0, 123, 255, 0.7)',
                    'rgba(220, 53, 69, 0.7)'
                ],
                borderColor: [
                    '#007bff',
                    '#dc3545'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color: '#e0e0e0'
                    }
                },
                title: {
                    display: !!title,
                    text: title,
                    color: '#e0e0e0'
                }
            }
        }
    });
}

/**
 * Create a line chart for goals progression
 */
function createGoalsChart(canvasId, matchDays, homeGoals, awayGoals) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: matchDays,
            datasets: [
                {
                    label: 'Domácí týmy - góly',
                    data: homeGoals,
                    borderColor: '#007bff',
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    borderWidth: 2,
                    tension: 0.4
                },
                {
                    label: 'Hostující týmy - góly',
                    data: awayGoals,
                    borderColor: '#dc3545',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    borderWidth: 2,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color: '#e0e0e0'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#999'
                    },
                    grid: {
                        color: '#333'
                    }
                },
                x: {
                    ticks: {
                        color: '#999'
                    },
                    grid: {
                        color: '#333'
                    }
                }
            }
        }
    });
}

/**
 * Format date to Czech locale
 */
function formatDate(dateString) {
    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString('cs-CZ', options);
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    const alertClass = {
        'success': 'alert-success',
        'error': 'alert-danger',
        'warning': 'alert-warning',
        'info': 'alert-info'
    }[type] || 'alert-info';

    const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    const container = document.querySelector('.container-fluid');
    const alertDiv = document.createElement('div');
    alertDiv.innerHTML = alertHtml;
    container.insertBefore(alertDiv.firstElementChild, container.firstChild);
}

/**
 * Add favorite team via API
 */
function addTeamToFavorites(teamId) {
    fetch(`/teams/${teamId}/favorite`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Tým přidán do oblíbených!', 'success');
            setTimeout(() => location.reload(), 1500);
        } else {
            showNotification(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Chyba při přidávání do oblíbených', 'error');
    });
}

/**
 * Remove favorite team via API
 */
function removeTeamFromFavorites(teamId) {
    if (!confirm('Opravdu chcete odstranit tento tým z oblíbených?')) {
        return;
    }

    fetch(`/teams/${teamId}/favorite`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Tým odstraněn z oblíbených', 'success');
            setTimeout(() => location.reload(), 1500);
        } else {
            showNotification(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Chyba při odebírání z oblíbených', 'error');
    });
}

/**
 * Search teams
 */
function searchTeams(query) {
    if (query.length < 2) {
        return;
    }

    fetch(`/teams/search?q=${encodeURIComponent(query)}`)
        .then(response => response.text())
        .then(html => {
            document.body.innerHTML = html;
        })
        .catch(error => console.error('Error:', error));
}

/**
 * Format time (HH:MM)
 */
function formatTime(dateString) {
    return new Date(dateString).toLocaleTimeString('cs-CZ', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Export data to CSV
 */
function exportTableToCSV(tableId, filename = 'data.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;

    let csv = [];
    let rows = table.querySelectorAll('tr');

    rows.forEach(row => {
        let cells = row.querySelectorAll('td, th');
        let csvRow = [];
        cells.forEach(cell => {
            csvRow.push('"' + cell.textContent.trim() + '"');
        });
        csv.push(csvRow.join(','));
    });

    downloadCSV(csv.join('\n'), filename);
}

/**
 * Download CSV file
 */
function downloadCSV(csv, filename) {
    let csvFile;
    let downloadLink;

    csvFile = new Blob([csv], { type: 'text/csv' });
    downloadLink = document.createElement('a');
    downloadLink.setAttribute('href', URL.createObjectURL(csvFile));
    downloadLink.setAttribute('download', filename);
    downloadLink.click();
}

/**
 * Debounce function for search
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
