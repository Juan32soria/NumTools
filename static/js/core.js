document.addEventListener("DOMContentLoaded", () => {
	const heroBackground = document.querySelector(".hero-background");
	const particles = document.querySelectorAll(".particle");

	function setRandomPosition(particle) {
		const x = Math.random() * 100;
		const y = Math.random() * 100;
		particle.style.left = `${x}%`;
		particle.style.top = `${y}%`;
	}

	function animateParticle(particle) {
		const duration = 15 + Math.random() * 15;
		const scale = 0.5 + Math.random() * 0.5;

		particle.style.transition = `all ${duration}s linear`;
		particle.style.transform = `translate(${Math.random() * 100 - 50}px, ${
			Math.random() * 100 - 50
		}px) scale(${scale})`;
	}

	particles.forEach((particle) => {
		setRandomPosition(particle);
		animateParticle(particle);

		particle.addEventListener("transitionend", () => {
			setRandomPosition(particle);
			animateParticle(particle);
		});
	});

	const canvas = document.getElementById("particleCanvas");
	const ctx = canvas.getContext("2d");
	let particlesArray;
	let animationId;
	let mouse = {
		x: null,
		y: null,
		radius: 150,
	};

	function resizeCanvas() {
		const section = canvas.closest(".animate-section");
		canvas.width = section.clientWidth;
		canvas.height = section.clientHeight;
	}

	class Particle {
		constructor(x, y) {
			this.x = x;
			this.y = y;
			this.size = Math.random() * 5 + 1;
			this.baseX = this.x;
			this.baseY = this.y;
			this.density = Math.random() * 30 + 1;
		}

		draw() {
			ctx.fillStyle = "rgba(106, 13, 173, 0.8)";
			ctx.beginPath();
			ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
			ctx.closePath();
			ctx.fill();
		}

		update() {
			let dx = mouse.x - this.x;
			let dy = mouse.y - this.y;
			let distance = Math.sqrt(dx * dx + dy * dy);
			let forceDirectionX = dx / distance;
			let forceDirectionY = dy / distance;
			let maxDistance = mouse.radius;
			let force = (maxDistance - distance) / maxDistance;
			let directionX = forceDirectionX * force * this.density;
			let directionY = forceDirectionY * force * this.density;

			if (distance < mouse.radius) {
				this.x -= directionX;
				this.y -= directionY;
			} else {
				if (this.x !== this.baseX) {
					let dx = this.x - this.baseX;
					this.x -= dx / 10;
				}
				if (this.y !== this.baseY) {
					let dy = this.y - this.baseY;
					this.y -= dy / 10;
				}
			}
		}
	}

	function init() {
		particlesArray = [];
		let numberOfParticles = (canvas.height * canvas.width) / 9000;
		for (let i = 0; i < numberOfParticles; i++) {
			let x = Math.random() * canvas.width;
			let y = Math.random() * canvas.height;
			particlesArray.push(new Particle(x, y));
		}
	}

	function animate() {
		ctx.clearRect(0, 0, canvas.width, canvas.height);
		for (let i = 0; i < particlesArray.length; i++) {
			particlesArray[i].draw();
			particlesArray[i].update();
		}
		connectParticles();
		animationId = requestAnimationFrame(animate);
	}

	function connectParticles() {
		let opacityValue = 1;
		for (let a = 0; a < particlesArray.length; a++) {
			for (let b = a; b < particlesArray.length; b++) {
				let distance =
					(particlesArray[a].x - particlesArray[b].x) *
						(particlesArray[a].x - particlesArray[b].x) +
					(particlesArray[a].y - particlesArray[b].y) *
						(particlesArray[a].y - particlesArray[b].y);
				if (distance < (canvas.width / 7) * (canvas.height / 7)) {
					opacityValue = 1 - distance / 20000;
					ctx.strokeStyle = `rgba(106, 13, 173, ${opacityValue})`;
					ctx.lineWidth = 1;
					ctx.beginPath();
					ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
					ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
					ctx.stroke();
				}
			}
		}
	}

	canvas.addEventListener("mousemove", function (event) {
		let rect = canvas.getBoundingClientRect();
		mouse.x = event.clientX - rect.left;
		mouse.y = event.clientY - rect.top;
	});

	canvas.addEventListener("mouseleave", function () {
		mouse.x = undefined;
		mouse.y = undefined;
	});

	function startAnimation() {
		if (animationId) {
			cancelAnimationFrame(animationId);
		}
		resizeCanvas();
		init();
		animate();
	}

	window.addEventListener("resize", startAnimation);
	startAnimation();

	// Create floating math symbols
	function createFloatingSymbols() {
		const symbols = ["∑", "∫", "π", "∞", "∆", "∇"];
		const container = document.querySelector(".floating-symbols");
		const symbolElements = [];

		// Remove existing symbols
		container.innerHTML = "";

		// Create new symbols
		for (let i = 0; i < 15; i++) {
			const symbol = document.createElement("span");
			const randomSymbol = symbols[Math.floor(Math.random() * symbols.length)];

			symbol.textContent = randomSymbol;
			symbol.style.position = "absolute";
			symbol.style.left = `${Math.random() * 100}%`;
			symbol.style.top = `${Math.random() * 100}%`;
			symbol.style.color = "var(--primary)";
			symbol.style.opacity = "0.2";
			symbol.style.fontSize = "16px";
			symbol.style.transition = "all 0.3s ease";

			// Random animation duration between 15-25s
			const duration = 15 + Math.random() * 10;

			// Random animation delay
			const delay = Math.random() * 5;

			symbol.style.animation = `
      symbolFloat ${duration}s linear ${delay}s infinite
    `;

			container.appendChild(symbol);
			symbolElements.push(symbol);
		}

		// Add keyframe animation dynamically
		const styleSheet = document.createElement("style");
		styleSheet.textContent = `
    @keyframes symbolFloat {
      0% {
        transform: translate(0, 0) rotate(0deg);
        opacity: 0.2;
      }
      50% {
        opacity: 0.4;
      }
      100% {
        transform: translate(50px, 50px) rotate(360deg);
        opacity: 0.2;
      }
    }
  `;
		document.head.appendChild(styleSheet);
	}

	// Handle mini profile toggling
	function initializeMiniProfiles() {
		const memberCards = document.querySelectorAll(".member-card");

		memberCards.forEach((card) => {
			const expandBtn = card.querySelector(".expand-btn");

			expandBtn.addEventListener("click", (e) => {
				e.stopPropagation();

				// Close other open profiles
				memberCards.forEach((otherCard) => {
					if (otherCard !== card && otherCard.classList.contains("active")) {
						otherCard.classList.remove("active");
					}
				});

				// Toggle current profile
				card.classList.toggle("active");
			});
		});

		// Close mini profile when clicking outside
		document.addEventListener("click", (e) => {
			if (!e.target.closest(".member-card")) {
				memberCards.forEach((card) => card.classList.remove("active"));
			}
		});
	}

	createFloatingSymbols();
	initializeMiniProfiles();

	const logos = document.querySelectorAll(".logo-item, .math-symbol");

	logos.forEach((item) => {
		item.addEventListener("click", () => {
			if (item.classList.contains("logo-item")) {
				const svg = item.querySelector("svg");
				if (svg) {
					const randomColor = Math.floor(Math.random() * 16777215).toString(16);
					svg.style.fill = "#" + randomColor;
				}
			} else if (item.classList.contains("math-symbol")) {
				const randomColor = Math.floor(Math.random() * 16777215).toString(16);
				item.style.color = "#" + randomColor;
			}
		});
	});

	const track = document.querySelector(".carousel-track");
	const cards = document.querySelectorAll(".method-card");
	const prevBtn = document.querySelector(".prev-btn");
	const nextBtn = document.querySelector(".next-btn");
	const pagination = document.querySelector(".pagination");

	let currentIndex = 0;
	const cardWidth = cards[0].offsetWidth + 16; // 16px for margin-right
	const cardsPerPage = 2;
	const totalPages = Math.ceil(cards.length / cardsPerPage);

	// Create pagination dots
	for (let i = 0; i < totalPages; i++) {
		const dot = document.createElement("div");
		dot.classList.add("pagination-dot");
		if (i === 0) dot.classList.add("active");
		pagination.appendChild(dot);
	}

	const updateCarousel = () => {
		track.style.transform = `translateX(-${
			currentIndex * cardWidth * cardsPerPage
		}px)`;
		updatePagination();
	};

	const updatePagination = () => {
		const dots = document.querySelectorAll(".pagination-dot");
		dots.forEach((dot, index) => {
			dot.classList.toggle("active", index === currentIndex);
		});
	};

	prevBtn.addEventListener("click", () => {
		currentIndex = (currentIndex - 1 + totalPages) % totalPages;
		updateCarousel();
	});

	nextBtn.addEventListener("click", () => {
		currentIndex = (currentIndex + 1) % totalPages;
		updateCarousel();
	});

	// Animate graphs
	const animateGraph = (canvas, method) => {
		const ctx = canvas.getContext("2d");
		const width = canvas.width;
		const height = canvas.height;

		ctx.clearRect(0, 0, width, height);
		ctx.strokeStyle = "var(--primary)";
		ctx.lineWidth = 2;

		ctx.beginPath();
		ctx.moveTo(0, height / 2);

		switch (method) {
			case "bisection":
				for (let x = 0; x < width; x++) {
					const y = height / 2 + Math.sin(x / 10) * 20;
					ctx.lineTo(x, y);
				}
				break;
			case "newton":
				for (let x = 0; x < width; x++) {
					const y = height / 2 - Math.pow(x / 20 - 5, 2) * 2 + 50;
					ctx.lineTo(x, y);
				}
				break;
			case "secant":
				for (let x = 0; x < width; x++) {
					const y = height / 2 - Math.tan(x / 30) * 10;
					ctx.lineTo(x, y);
				}
				break;
			case "fixed-point":
				for (let x = 0; x < width; x++) {
					const y = height / 2 - Math.cos(x / 10) * 30;
					ctx.lineTo(x, y);
				}
				break;
			case "gradient-descent":
				for (let x = 0; x < width; x++) {
					const y = height / 2 - Math.pow(x / 20 - 5, 2) * 2 + 50;
					ctx.lineTo(x, y);
				}
				ctx.moveTo(0, height);
				for (let i = 0; i < 5; i++) {
					ctx.lineTo(i * 50, height - i * 20);
				}
				break;
		}

		ctx.stroke();
	};

	const canvases = document.querySelectorAll(".graph-canvas");
	canvases.forEach((canvas) => {
		const method = canvas.dataset.method;
		animateGraph(canvas, method);
	});

	// Animate graphs every 3 seconds
	setInterval(() => {
		canvases.forEach((canvas) => {
			const method = canvas.dataset.method;
			animateGraph(canvas, method);
		});
	}, 3000);

	// Handle calculate button clicks
	const calculateBtns = document.querySelectorAll(".calculate-btn");
	calculateBtns.forEach((btn) => {
		btn.addEventListener("click", () => {
			const methodName = btn
				.closest(".method-card")
				.querySelector("h3").textContent;
			alert(`Calculating using ${methodName}...`);
		});
	});
});
