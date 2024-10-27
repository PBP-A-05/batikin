// Mobile menu toggle
function toggleMenu() {
    const menu = document.getElementById('mobile-menu');
    menu.classList.toggle('hidden');
}

// Account menu toggle
function toggleAccountMenu() {
    const menu = document.getElementById('account-menu');
    const isHidden = menu.classList.contains('opacity-0');
    
    if (isHidden) {
        // Show menu
        menu.classList.remove('opacity-0', 'scale-95', '-translate-y-2', 'pointer-events-none');
        menu.classList.add('opacity-100', 'scale-100', 'translate-y-0', 'pointer-events-auto');
    } else {
        // Hide menu
        menu.classList.remove('opacity-100', 'scale-100', 'translate-y-0', 'pointer-events-auto');
        menu.classList.add('opacity-0', 'scale-95', '-translate-y-2', 'pointer-events-none');
    }
}

// Add event listeners when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
        const menu = document.getElementById('account-menu');
        const accountButton = event.target.closest('button');
        
        if (menu && !accountButton && !menu.contains(event.target) && menu.classList.contains('opacity-100')) {
            toggleAccountMenu();
        }
    });

    // Close menu when pressing Escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            const menu = document.getElementById('account-menu');
            if (menu && menu.classList.contains('opacity-100')) {
                toggleAccountMenu();
            }
        }
    });
});