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

// Custom file input handling
document.addEventListener("DOMContentLoaded", () => {
  const fileInputs = document.querySelectorAll('.file-input');

  fileInputs.forEach(input => {
    const fileText = input.parentElement.querySelector('.file-input-text');
    const fileButton = input.parentElement.querySelector('.file-input-button');

    // Update text when file is selected
    input.addEventListener('change', () => {
      if (input.files.length > 0) {
        fileText.textContent = input.files[0].name;
      } else {
        fileText.textContent = 'Choose file';
      }
    });

    // Trigger file input when button is clicked
    if (fileButton) {
      fileButton.addEventListener('click', (e) => {
        e.preventDefault();
        input.click();
      });
    }
  });

  // Live preview for image uploads
  const avatarInput = document.getElementById('avatar');
  const bannerInput = document.getElementById('banner');

  if (avatarInput) {
    avatarInput.addEventListener('change', function() {
      if (this.files && this.files[0]) {
        const preview = document.querySelector('.preview-avatar-img');
        const avatarCircle = document.querySelector('.profile-preview-avatar .avatar-circle');

        if (preview) {
          preview.src = URL.createObjectURL(this.files[0]);
        } else if (avatarCircle) {
          // Replace avatar circle with image
          const img = document.createElement('img');
          img.src = URL.createObjectURL(this.files[0]);
          img.alt = 'Profile avatar';
          img.className = 'preview-avatar-img';

          avatarCircle.parentNode.replaceChild(img, avatarCircle);
        }
      }
    });
  }

  if (bannerInput) {
    bannerInput.addEventListener('change', function() {
      if (this.files && this.files[0]) {
        const preview = document.querySelector('.preview-banner-img');
        const placeholder = document.querySelector('.preview-banner-placeholder');

        if (preview) {
          preview.src = URL.createObjectURL(this.files[0]);
        } else if (placeholder) {
          // Replace placeholder with image
          const img = document.createElement('img');
          img.src = URL.createObjectURL(this.files[0]);
          img.alt = 'Profile banner';
          img.className = 'preview-banner-img';

          placeholder.parentNode.replaceChild(img, placeholder);
        }
      }
    });
  }
});
