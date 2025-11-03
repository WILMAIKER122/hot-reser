document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('customSidebar');
    const toggleButton = document.getElementById('sidebarToggle');
    const toggleButtonMobile = document.getElementById('sidebarToggleMobile');

    // Función para manejar el estado de la sidebar
    const toggleSidebar = () => {
        sidebar.classList.toggle('expanded');
    };

    // 1. Manejo en Desktop (Sidebar:hover en CSS)
    // El hover se maneja principalmente con el CSS para las transiciones.
    
    // 2. Manejo en Mobile (Sidebar:click en JS)
    // Usamos los botones de toggle para abrir/cerrar la sidebar en pantallas pequeñas
    if (toggleButton) {
        toggleButton.addEventListener('click', toggleSidebar); // Botón X en la sidebar
    }
    if (toggleButtonMobile) {
        toggleButtonMobile.addEventListener('click', toggleSidebar); // Botón hamburguesa en la navbar
    }

    // Ocultar la sidebar automáticamente al redimensionar a desktop si estaba expandida en móvil
    window.addEventListener('resize', () => {
        if (window.innerWidth >= 992 && sidebar.classList.contains('expanded')) {
            sidebar.classList.remove('expanded');
        }
    });
});