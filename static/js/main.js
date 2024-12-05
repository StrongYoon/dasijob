// static/js/main.js
import LocationSearch from './components/LocationSearch.js';

document.addEventListener('DOMContentLoaded', () => {
    const locationSearchRoot = document.getElementById('location-search-root');
    if (locationSearchRoot) {
        ReactDOM.render(React.createElement(LocationSearch), locationSearchRoot);
    }
});