function openGoogleMaps(event, lat, lng, placeName) {
  event.preventDefault();
  
  // Check if mobile device
  const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
  
  if (isMobile) {
    // For mobile devices, try to open in Google Maps app
    // iOS
    if (/iPhone|iPad|iPod/i.test(navigator.userAgent)) {
      window.location.href = `maps://maps.google.com/maps?q=${lat},${lng}&ll=${lat},${lng}&z=16`;
      // Fallback to web version after short delay
      setTimeout(() => {
        window.open(`https://www.google.com/maps/search/?api=1&query=${lat},${lng}`, '_blank');
      }, 500);
    } 
    // Android
    else if (/Android/i.test(navigator.userAgent)) {
      window.location.href = `geo:${lat},${lng}?q=${lat},${lng}(${encodeURIComponent(placeName)})`;
      // Fallback to web version after short delay
      setTimeout(() => {
        window.open(`https://www.google.com/maps/search/?api=1&query=${lat},${lng}`, '_blank');
      }, 500);
    }
  } else {
    // For desktop, open in new browser tab
    window.open(`https://www.google.com/maps/search/?api=1&query=${lat},${lng}`, '_blank');
  }
}