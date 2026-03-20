document.addEventListener('DOMContentLoaded', function () {
    const greetingText = document.getElementById('greeting-text');

    function getCurrentGreeting() {
        const currentHour = new Date().getHours();

        if (currentHour >= 4 && currentHour < 12) {
            return 'Good Morning!';
        } else if (currentHour >= 12 && currentHour < 18) {
            return 'Good Afternoon!';
        } else {
            return 'Good Evening!';
        }
    }

    function updateGreeting() {
        const greeting = getCurrentGreeting();
        greetingText.textContent = greeting;
    }

    updateGreeting();

    setInterval(updateGreeting, 60000);
});