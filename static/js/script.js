document.addEventListener('DOMContentLoaded', function() {
    const articleContent = document.querySelector('.prose'); // Assuming your article content is in a div with class 'prose'
    if (articleContent) {
        let startTime;

        function startTimer() {
            startTime = new Date().getTime();
            console.log("Article timer started.");
        }

        function endTimer() {
            if (startTime) {
                const endTime = new Date().getTime();
                const timeSpentSeconds = Math.round((endTime - startTime) / 1000);
                console.log(`Time spent on article: ${timeSpentSeconds} seconds.`);
                // Here, you would typically send this data to your Flask backend
                // via an AJAX request to update the UserInteraction record.
                // Example (conceptual, requires fetch API and backend endpoint):
                /*
                const articleId = articleContent.dataset.articleId; // You'd need to add data-article-id to your article.html
                fetch(`/api/record_time_spent/${articleId}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ time_spent: timeSpentSeconds })
                }).then(response => response.json())
                  .then(data => console.log('Time spent recorded:', data))
                  .catch(error => console.error('Error recording time spent:', error));
                */
                startTime = null; // Reset timer
            }
        }

        // Start timer when article is visible (e.g., page loaded)
        startTimer();

        // End timer when user leaves the page or navigates away
        window.addEventListener('beforeunload', endTimer);
    }
});
