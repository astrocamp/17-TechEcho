import "./fontawesome"
import Alpine from 'alpinejs';

window.Alpine = Alpine;

Alpine.start();

document.getElementById('search-input').addEventListener('input', function() {
    const query = this.value;

    if (query.trim() !== '') {
        fetch(`${searchUrl}?q=${encodeURIComponent(query)}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('search-results').innerHTML = data.html;
        })
        .catch(error => console.error('Error fetching search results:', error));
    } else {
        document.getElementById('search-results').innerHTML = ''; // Clear results if query is empty
    }
});