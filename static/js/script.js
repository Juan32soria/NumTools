// navbar.js
document.addEventListener("DOMContentLoaded", function () {
	// Elements
	const hamburger = document.querySelector(".hamburger");
	const navLinks = document.querySelector(".nav-links");
	const scrollTopBtn = document.querySelector(".scroll-top");

	// Toggle mobile menu
	hamburger?.addEventListener("click", () => {
		hamburger.classList.toggle("active");
		navLinks.classList.toggle("active");
	});

	// Scroll to top functionality
	scrollTopBtn?.addEventListener("click", () => {
		window.scrollTo({
			top: 0,
			behavior: "smooth",
		});
	});

	// Close mobile menu when clicking outside
	document.addEventListener("click", (e) => {
		if (!navLinks.contains(e.target) && !hamburger.contains(e.target)) {
			navLinks.classList.remove("active");
			hamburger.classList.remove("active");
		}
	});

	// Add hover effect for links
	const links = document.querySelectorAll("a");
	links.forEach((link) => {
		link.addEventListener("mouseenter", createRipple);
	});

	function createRipple(e) {
		const ripple = document.createElement("div");
		ripple.classList.add("ripple");

		const rect = e.target.getBoundingClientRect();
		const x = e.clientX - rect.left;
		const y = e.clientY - rect.top;

		ripple.style.left = `${x}px`;
		ripple.style.top = `${y}px`;

		e.target.appendChild(ripple);

		setTimeout(() => {
			ripple.remove();
		}, 600);
	}
});

// Add this to your existing script.js file or create a new one

function showNotification(message, type) {
	const container = document.getElementById("notification-container");
	const notification = document.createElement("div");
	notification.className = `notification ${type}`;
	notification.textContent = message;

	container.appendChild(notification);

	setTimeout(() => {
		notification.style.animation = "fadeOut 0.5s ease forwards";
		setTimeout(() => {
			container.removeChild(notification);
		}, 500);
	}, 5000);
}

// Example usage:
// showNotification('Calculation successful!', 'success');
// showNotification('An error occurred.', 'error');

document.addEventListener("DOMContentLoaded", function () {
	const form = document.getElementById("methodForm");

	form.addEventListener("submit", function (e) {
		e.preventDefault();

		// Here you would normally send the form data to the server
		// For demonstration purposes, we'll just show a success message
		showNotification("Calculation in progress...", "success");

		// Simulate form submission
		setTimeout(() => {
			// This is where you'd normally handle the server response
			// For now, we'll just show another notification
			showNotification("Calculation completed!", "success");

			// You might want to update the results section here as well
		}, 2000);
	});
});
