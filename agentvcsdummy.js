// Fake AgentVCS commands
let commits = [];
let branches = ["main"];

function runCommand(cmd, terminal) {
  const parts = cmd.split(" ");
  const base = parts[0];

  if (base === "agentvcs") {
    const sub = parts[1];
    switch (sub) {
      case "--version":
      case "-v":
        terminal.textContent += "AgentVCS 0.9.0-browser-demo\n";
        break;
      case "commit":
        const intentIndex = parts.indexOf("--intent");
        const intent = intentIndex !== -1 ? parts[intentIndex+1] : "no-intent";
        commits.push({ intent, time: new Date().toLocaleTimeString() });
        terminal.textContent += `Committed with intent: ${intent}\n`;
        break;
      case "branch":
        const branchName = parts[2] || "unnamed";
        branches.push(branchName);
        terminal.textContent += `Created branch ${branchName}\nBranches: ${branches.join(", ")}\n`;
        break;
      case "log":
        if (commits.length === 0) {
          terminal.textContent += "No commits yet.\n";
        } else {
          commits.forEach((c, i) => {
            terminal.textContent += `${i+1}: [${c.time}] intent=${c.intent}\n`;
          });
        }
        break;
      case "nano":
        launchNano(parts[2] || "untitled.txt", terminal);
        break;
      default:
        terminal.textContent += "This command requires the full CLI. Install AgentVCS for production use!\n";
    }
  } else {
    terminal.textContent += "Unknown command.\n";
  }
}
