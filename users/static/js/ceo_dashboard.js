document.addEventListener('DOMContentLoaded', function () {
    // Example chart setup for Sales Trends
    var ctxSalesTrends = document.getElementById('salesTrendsChart').getContext('2d');
    var salesTrendsChart = new Chart(ctxSalesTrends, {
        type: 'line',
        data: {
            labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
            datasets: [{
                label: 'Sales Trends',
                data: [10, 20, 15, 25, 30, 20, 35],
                backgroundColor: 'rgba(0, 123, 255, 0.2)',
                borderColor: 'rgba(0, 123, 255, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Example chart setup for Popular Menu Items
    var ctxPopularMenuItems = document.getElementById('popularMenuItemsChart').getContext('2d');
    var popularMenuItemsChart = new Chart(ctxPopularMenuItems, {
        type: 'bar',
        data: {
            labels: ['Item 1', 'Item 2', 'Item 3', 'Item 4'],
            datasets: [{
                label: 'Popular Menu Items',
                data: [300, 500, 400, 600],
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
