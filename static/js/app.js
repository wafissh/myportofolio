
document.addEventListener('DOMContentLoaded', () => {
  window.addEventListener('scroll', () => {
    const scrollPos = window.pageYOffset;

    const cloudBack = document.getElementById('cloud-back');
    const cloudMid = document.getElementById('cloud-mid');
    const cloudFront = document.getElementById('cloud-front');
    const cloudFront2 = document.getElementById('cloud-front-2');
    const cloudbottom = document.getElementById('cloud-bottom')
    // Gerakan parallax berdasarkan kecepatan masing-masing layer
    if (cloudBack) cloudBack.style.transform = `translateY(${scrollPos * -0.35}px)`;
    if (cloudMid) cloudMid.style.transform = `translateY(${scrollPos * -0.35}px)`;
    if (cloudFront) cloudFront.style.transform = `translateY(${scrollPos * -0.65}px)`;
    if (cloudFront2) cloudFront2.style.transform = `translateY(${scrollPos * -0.65}px)`;
    if(cloudbottom) cloudbottom.style.transform = `translateY(${scrollPos * -0.035}px)`;

  });
});