/**
 * Cinematic Scroll-Triggered Animation Engine & Live GitHub Telemetry
 * Portfolio of Aman Kumar Singh (@gangasagar5928)
 * Hardware-Enforced Fail-Closed Systems & On-Device AI
 */

(() => {
  'use strict';

  // --- Configuration ---
  const TOTAL_FRAMES = 300;
  const FRAME_DIR = 'frames';
  const FRAME_PREFIX = 'ezgif-frame-';
  const FRAME_EXT = '.jpg';
  const LERP_FACTOR = 0.12; // Responsive and smooth interpolation

  // --- DOM Elements ---
  const preloader = document.getElementById('preloader');
  const progressBar = document.getElementById('progress-bar');
  const progressPercentage = document.getElementById('progress-percentage');
  const loadCountEl = document.getElementById('load-count');

  const canvas = document.getElementById('hero-canvas');
  const ctx = canvas.getContext('2d', { alpha: false });


  const milestones = document.querySelectorAll('.milestone');
  const navbar = document.getElementById('navbar');
  const navLinks = document.querySelectorAll('.nav-link');
  const copyEmailBtn = document.getElementById('copy-email-btn');
  const copyBtnText = document.getElementById('copy-btn-text');

  // --- State Variables ---
  const images = new Array(TOTAL_FRAMES);
  const isLoadedMap = new Uint8Array(TOTAL_FRAMES);
  let loadedCount = 0;
  let isPreloaderComplete = false;

  let targetProgress = 0;
  let currentProgress = 0;
  let targetFrame = 0;
  let currentFrame = 0;
  let lastDrawnFrame = -1;

  // --- Format Frame File Path ---
  function getFrameSrc(index) {
    const frameNum = String(index + 1).padStart(3, '0');
    return `${FRAME_DIR}/${FRAME_PREFIX}${frameNum}${FRAME_EXT}`;
  }

  // --- Canvas Sizing & High DPI Handling ---
  let canvasWidth = 0;
  let canvasHeight = 0;

  function resizeCanvas() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvasWidth = window.innerWidth;
    canvasHeight = window.innerHeight;

    canvas.width = Math.round(canvasWidth * dpr);
    canvas.height = Math.round(canvasHeight * dpr);

    ctx.scale(dpr, dpr);

    // Force redraw of current frame on resize
    renderNearestFrame(Math.round(currentFrame));
  }

  window.addEventListener('resize', () => {
    resizeCanvas();
    updateScrollProgress();
  }, { passive: true });
  resizeCanvas();

  // --- Aspect Ratio "Cover" Math ---
  function drawImageCover(ctx, img, w, h) {
    if (!img || !img.complete || img.naturalWidth === 0) return;

    const imgWidth = img.naturalWidth;
    const imgHeight = img.naturalHeight;
    const imgRatio = imgWidth / imgHeight;
    const canvasRatio = w / h;

    let renderWidth, renderHeight, offsetX, offsetY;

    if (canvasRatio > imgRatio) {
      renderWidth = w;
      renderHeight = w / imgRatio;
      offsetX = 0;
      offsetY = (h - renderHeight) / 2;
    } else {
      renderWidth = h * imgRatio;
      renderHeight = h;
      offsetX = (w - renderWidth) / 2;
      offsetY = 0;
    }

    ctx.drawImage(img, 0, 0, imgWidth, imgHeight, offsetX, offsetY, renderWidth, renderHeight);
  }

  // --- Safe Frame Renderer (Finds nearest loaded neighbor if needed) ---
  function renderNearestFrame(requestedIndex) {
    const clampedIndex = Math.min(Math.max(requestedIndex, 0), TOTAL_FRAMES - 1);
    
    // Check target frame first
    if (isLoadedMap[clampedIndex] && images[clampedIndex]?.complete && images[clampedIndex]?.naturalWidth > 0) {
      drawImageCover(ctx, images[clampedIndex], canvasWidth, canvasHeight);
      lastDrawnFrame = clampedIndex;
      return;
    }

    // Search nearest available frame within range to prevent stuttering
    for (let delta = 1; delta < 30; delta++) {
      const forward = clampedIndex + delta;
      if (forward < TOTAL_FRAMES && isLoadedMap[forward] && images[forward]?.complete) {
        drawImageCover(ctx, images[forward], canvasWidth, canvasHeight);
        lastDrawnFrame = forward;
        return;
      }
      const backward = clampedIndex - delta;
      if (backward >= 0 && isLoadedMap[backward] && images[backward]?.complete) {
        drawImageCover(ctx, images[backward], canvasWidth, canvasHeight);
        lastDrawnFrame = backward;
        return;
      }
    }
  }

  // --- Image Sequence Preloader ---
  function preloadImages() {
    for (let i = 0; i < TOTAL_FRAMES; i++) {
      const img = new Image();
      img.src = getFrameSrc(i);

      img.onload = () => {
        isLoadedMap[i] = 1;
        onImageLoaded(i);
      };

      img.onerror = () => {
        isLoadedMap[i] = 0;
        onImageLoaded(i);
      };

      images[i] = img;
    }
  }

  function onImageLoaded(index) {
    loadedCount++;

    // Draw first frame immediately once available
    if (index === 0) {
      renderNearestFrame(0);
    }

    const pct = Math.floor((loadedCount / TOTAL_FRAMES) * 100);
    if (progressBar) progressBar.style.width = `${pct}%`;
    if (progressPercentage) progressPercentage.textContent = pct;
    if (loadCountEl) loadCountEl.textContent = loadedCount;

    // Dismiss preloader once sequence is cached
    if (loadedCount >= TOTAL_FRAMES && !isPreloaderComplete) {
      isPreloaderComplete = true;
      setTimeout(() => {
        if (preloader) preloader.classList.add('fade-out');
        renderNearestFrame(0);
      }, 300);
    }
  }

  // Fallback timer: unlock page after 3.5s regardless of network delays
  setTimeout(() => {
    if (!isPreloaderComplete) {
      isPreloaderComplete = true;
      if (preloader) preloader.classList.add('fade-out');
      renderNearestFrame(0);
    }
  }, 3500);

  // --- Scroll Tracking Engine (Full Page Through Footer) ---
  function updateScrollProgress() {
    const scrollHeight = document.documentElement.scrollHeight;
    const clientHeight = window.innerHeight || document.documentElement.clientHeight;
    const maxScroll = Math.max(scrollHeight - clientHeight, 1);

    const rawProgress = window.scrollY / maxScroll;
    targetProgress = Math.min(Math.max(rawProgress, 0), 1);
    targetFrame = targetProgress * (TOTAL_FRAMES - 1);

    // Navbar state
    if (navbar) {
      if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    }
  }

  window.addEventListener('scroll', updateScrollProgress, { passive: true });

  // --- Milestone & HUD Updates ---
  function updateMilestones(progress, frameIndex) {
    const clampedProgress = Math.min(Math.max(progress, 0), 1);
    const pctInt = Math.round(clampedProgress * 100);


    // Continuous Milestone Coverage (Zero Gaps)
    if (milestones && milestones.length > 0) {
      milestones.forEach((el) => {
        const start = parseFloat(el.getAttribute('data-start'));
        const end = parseFloat(el.getAttribute('data-end'));

        const isVisible = (clampedProgress >= start && clampedProgress <= end) ||
                          (start === 0.75 && clampedProgress >= 0.75);

        if (isVisible) {
          if (!el.classList.contains('active')) el.classList.add('active');
        } else {
          if (el.classList.contains('active')) el.classList.remove('active');
        }
      });
    }
  }

  // --- Main Animation Loop (rAF with sub-pixel Lerp) ---
  function animationLoop() {
    currentProgress += (targetProgress - currentProgress) * LERP_FACTOR;
    currentFrame += (targetFrame - currentFrame) * LERP_FACTOR;

    const activeFrame = Math.round(currentFrame);

    if (activeFrame !== lastDrawnFrame) {
      renderNearestFrame(activeFrame);
    }

    updateMilestones(currentProgress, activeFrame);

    requestAnimationFrame(animationLoop);
  }


  // --- Smooth Anchor Navigation ---
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', (e) => {
      const targetId = anchor.getAttribute('href');
      if (targetId === '#') return;
      const targetEl = document.querySelector(targetId);
      if (targetEl) {
        e.preventDefault();
        targetEl.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // --- Copy Email Clipboard Action ---
  if (copyEmailBtn) {
    copyEmailBtn.addEventListener('click', () => {
      const email = copyEmailBtn.getAttribute('data-email');
      if (navigator.clipboard) {
        navigator.clipboard.writeText(email).then(() => {
          if (copyBtnText) copyBtnText.textContent = 'Copied!';
          setTimeout(() => {
            if (copyBtnText) copyBtnText.textContent = 'Copy Email';
          }, 2000);
        }).catch(() => {
          window.prompt('Copy email:', email);
        });
      } else {
        window.prompt('Copy email:', email);
      }
    });
  }

  // --- Active Nav Link on Scroll ---
  const sections = document.querySelectorAll('section[id]');
  function highlightNavOnScroll() {
    const scrollY = window.pageYOffset;
    sections.forEach((current) => {
      const sectionHeight = current.offsetHeight;
      const sectionTop = current.offsetTop - 120;
      const sectionId = current.getAttribute('id');

      if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
        navLinks.forEach((link) => {
          link.classList.remove('active');
          if (link.getAttribute('href') === `#${sectionId}`) {
            link.classList.add('active');
          }
        });
      }
    });
  }
  window.addEventListener('scroll', highlightNavOnScroll, { passive: true });

  // --- GitHub Live API Telemetry Sync ---
  const langColors = {
    'Python': '#3572A5',
    'TypeScript': '#3178c6',
    'JavaScript': '#f1e05a',
    'C++': '#f34b7d',
    'C': '#555555',
    'Dart': '#00B4AB',
    'HTML': '#e34c26'
  };

  async function syncGitHubData() {
    try {
      const [userRes, reposRes] = await Promise.all([
        fetch('https://api.github.com/users/gangasagar5928'),
        fetch('https://api.github.com/users/gangasagar5928/repos?sort=updated&per_page=20')
      ]);

      if (userRes.ok) {
        const user = await userRes.json();
        const reposCountEl = document.getElementById('gh-repos-count');
        const repoCountTitle = document.getElementById('repo-count-title');
        if (reposCountEl) reposCountEl.textContent = user.public_repos || '8';
        if (repoCountTitle) repoCountTitle.textContent = user.public_repos || '8';
      }

      if (reposRes.ok) {
        const repos = await reposRes.json();
        const container = document.getElementById('live-repos-container');
        if (container && Array.isArray(repos) && repos.length > 0) {
          // Filter out special profile repo
          const filtered = repos.filter(r => r.name !== 'gangasagar5928');
          container.innerHTML = filtered.map(r => {
            const color = langColors[r.language] || '#888888';
            const desc = r.description || 'Defense-grade engineering & hardware-interlocked system architecture.';
            return `
              <div class="repo-tile glass-panel">
                <div class="repo-tile-top">
                  <a href="${r.html_url}" target="_blank" rel="noreferrer" class="repo-tile-title">${r.name} ↗</a>
                  <span class="repo-star-pill">★ ${r.stargazers_count}</span>
                </div>
                <p class="repo-tile-desc">${desc}</p>
                <div class="repo-tile-meta">
                  <span class="repo-lang-dot" style="background:${color};"></span>
                  <span>${r.language || 'Embedded / Systems'}</span>
                </div>
              </div>
            `;
          }).join('');
        }
      }
    } catch (err) {
      // Graceful degradation: keeps static fallback content
      console.log('GitHub API offline or rate-limited. Static fallback active.');
    }
  }

  syncGitHubData();

  // --- Initialize Application ---
  preloadImages();
  updateScrollProgress();
  requestAnimationFrame(animationLoop);

})();
