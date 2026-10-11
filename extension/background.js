let port = null;

// Abre la conexión con el host solo cuando hace falta
function getPort() {
  if (!port) {
    port = browser.runtime.connectNative("url_logger");
    port.onDisconnect.addListener(() => {
      const err = browser.runtime.lastError || port.error;
      if (err) console.error("Host desconectado:", err.message);
      port = null; // se reconectará en la próxima navegación
    });
  }
  return port;
}

browser.webNavigation.onCompleted.addListener(async (details) => {
  // Solo el documento principal, no iframes
  if (details.frameId !== 0) return;

  // Solo páginas web normales
  if (!/^https?:\/\//.test(details.url)) return;

  // Ignorar ventanas privadas
  try {
    const tab = await browser.tabs.get(details.tabId);
    if (tab.incognito) return;
  } catch (e) {
    return;
  }

  try {
    getPort().postMessage({
      time: new Date().toLocaleString("sv-SE"),
      url: details.url
    });
  } catch (e) {
    console.error("Error enviando al host:", e);
    port = null;
  }
});