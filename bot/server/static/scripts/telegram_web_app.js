const tg = window.Telegram.WebApp;
tg.requestFullscreen()

tg.onEvent('viewportChanged', () => {

    const safeAreaTop = tg.ContentSafeAreaInset.top || 0;
    console.log(safeAreaTop)
    document.documentElement.style.setProperty('--tg-safe-area-inset-top', `${safeAreaTop}px`);
});