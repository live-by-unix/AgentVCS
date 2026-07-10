// Fake nano editor
let files = {};

function launchNano(filename, terminal) {
  terminal.textContent += `Opening nano editor for ${filename}\nType your text below. CTRL+O to save, CTRL+X to exit.\n`;
  const input = document.getElementById('input');

  let buffer = "";
  const handler = e => {
    if (e.ctrlKey && e.key.toLowerCase() === 'o') {
      files[filename] = buffer;
      terminal.textContent += `\nSaved ${filename}\n`;
      e.preventDefault();
    } else if (e.ctrlKey && e.key.toLowerCase() === 'x') {
      terminal.textContent += `\nExited nano.\n`;
      input.removeEventListener('keydown', handler);
      e.preventDefault();
    } else if (e.key.length === 1) {
      buffer += e.key;
      terminal.textContent += e.key;
    } else if (e.key === "Backspace") {
      buffer = buffer.slice(0, -1);
      terminal.textContent = terminal.textContent.slice(0, -1);
    }
  };

  input.addEventListener('keydown', handler);
}
