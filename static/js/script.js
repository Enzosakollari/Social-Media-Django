// Handle "Message" buttons that redirect to chat views
document.addEventListener("DOMContentLoaded", () => {
  const chatButtons = document.querySelectorAll(".chat-btn");

  chatButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const url = btn.getAttribute("data-chat-url");
      if (url) {
        window.location.href = url;
      }
    });
  });
});
// Scroll animation trigger
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, observerOptions);

// Observe all post cards and other elements
document.querySelectorAll('.post-card, .conversation-item, .fade-in').forEach(el => {
  observer.observe(el);
});

// Image lazy loading with fade-in
document.querySelectorAll('.post-image').forEach(img => {
  if (img.complete) {
    img.classList.add('loaded');
  } else {
    img.addEventListener('load', () => {
      img.classList.add('loaded');
    });
  }
});