# TUI vs Web UI: OneTrainer UI Rebuild Decision

A structured debate was conducted between two advocates to determine the best replacement for OneTrainer's aging CustomTkinter GUI. Both explored the full codebase before arguing their case.

---

## The Case for TUI (Textual)

### Core Argument
OneTrainer's architecture is a thin UI layer over a JSON config editor + progress monitor. A TUI fits this naturally, stays pure Python, and runs anywhere without a browser or build toolchain.

### Key Points

- **CustomTkinter is dying.** A comment in the codebase (`modules/util/ui/components.py:91-96`) notes the maintainer "admitted to forgetting how to maintain CTK." No new release in 12+ months.
- **Architecture already wants to be a TUI.** `TrainCallbacks` (6 callbacks), `TrainCommands` (5 commands), and `TrainConfig` (JSON) form a clean, thin UI contract. Training already works headlessly via `scripts/train.py`.
- **Pure Python, zero build tooling.** One dependency (`textual`) added to `pyproject.toml`. No npm, no Node.js, no TypeScript, no Vite.
- **Single process, no IPC.** Training and UI share a Python process. Textual's `worker` + `post_message()` replaces fragile `threading.Thread` + `self.after(0, ...)` without needing WebSocket/REST serialization.
- **SSH/cloud-native.** Runs natively over SSH on RunPod, Vast.ai, Lambda. No port forwarding, no browser, no X11.
- **Textual maps 1:1 to current UI.** `TabbedContent` replaces `CTkTabview`, `ProgressBar` replaces double progress bars, `Screen` replaces `CTkToplevel` modals. All ~487 component calls have direct Textual equivalents.
- **Image display via textual-image.** Kitty Graphics Protocol and Sixel render images in supporting terminals. Fallback: auto-open in external viewer or use TensorBoard (already integrated).
- **textual-web.** Same codebase can be served as a web app via `textual-web serve` for browser access.
- **Built-in testing.** `App.run_test()` enables programmatic UI testing — currently impossible with CustomTkinter.
- **Video is a non-issue.** `BaseModelSampler.py:41-42`: *"do not transfer videos; they are not shown anyway."* Both approaches save video to disk.

### Proposed Framework: Textual
- Modern Python TUI framework by Textualize
- CSS-based styling with live reload
- Reactive attributes system (`reactive()` + watchers)
- Rich widget library (tabs, inputs, selects, progress bars, modals)
- Async-first with proper worker thread support

---

## The Case for SvelteKit Web UI

### Core Argument
OneTrainer trains models that produce visual output. The browser is the superior rendering environment for images, and every successful ML training tool in the ecosystem uses a web UI.

### Key Points

- **Image display is the killer feature.** The browser provides native `<img>`/`<canvas>` with hardware-accelerated rendering, zoom, pan, comparison sliders, responsive galleries, and drag-and-drop. The current UI is limited to a single 512x512 static preview.
- **Industry precedent.** ComfyUI (70K stars), A1111 (140K stars), Kohya_ss (10K stars), InvokeAI — all web UIs. No successful ML training tool uses a TUI.
- **Reactive state eliminates boilerplate.** Svelte's `bind:value` replaces the 316-line `UIState` class and 700+ manual component placement calls. Compile-time reactivity means zero runtime overhead.
- **WebSocket is safer than threading.** `TrainCallbacks` map to WebSocket messages out, `TrainCommands` map to messages in. Naturally serialized, no race conditions, no `contextlib.suppress(Exception)` wrapping.
- **Remote training works natively.** Forward one port, open a browser. No X11/VNC. Users already open a browser for TensorBoard.
- **SvelteKit over Gradio.** Gradio is too rigid for OneTrainer's complex conditional UI (model type changes which fields appear, training method changes which tabs are visible). Kohya_ss uses Gradio and its UI is widely criticized.
- **SvelteKit over React.** Smaller bundles (1.6KB vs 42KB+ runtime), simpler syntax (`bind:value` vs hooks), HTML-first approach is more accessible for Python developers.
- **Clean architecture.** FastAPI serves the API, SvelteKit renders the UI. The `TrainCallbacks`/`TrainCommands` interfaces become the API contract. All training backend code is untouched.
- **Video support.** Native `<video>` tag for Hunyuan Video model outputs (though currently not displayed in UI by design).

### Rebuttal of textual-web
**textual-web does not support image rendering.** The textual-image library documentation states: *"textual-serve is not supported... it would be a completely different implementation that may be added one day but not in the near future."* In browser mode, the TUI can display text but not training samples — defeating its purpose for a visual ML tool.

---

## Verdict: SvelteKit

### Decision Rationale

The deciding factor is **image display**. The user requirement to show training samples is non-negotiable, and the TUI's image story has too many caveats:

1. Terminal image protocols (Kitty/Sixel) have spotty support across terminals, no zoom/gallery, and flickering on scroll.
2. textual-web — the TUI's strongest argument — **cannot display images** in browser mode.
3. Fallback to external image viewer is a UX regression.

### Scorecard

| Factor | TUI (Textual) | SvelteKit | Winner |
|---|---|---|---|
| Image display | Kitty/Sixel (limited) | Native browser rendering | **SvelteKit** |
| Video playback | Not possible in terminal | Native `<video>` | **SvelteKit** |
| Developer simplicity | Pure Python, one dep | JS toolchain, two languages | **TUI** |
| Remote/headless | SSH native; no images in textual-web | Port forward + browser | **SvelteKit** |
| Reactive state | `reactive()` — good | `bind:value` — equally good | **Tie** |
| Real-time updates | In-process `post_message()` | WebSocket (serialized) | **Tie** |
| Industry precedent | No ML tool uses TUI | Kohya, ComfyUI, A1111 | **SvelteKit** |
| Testing | Built-in `App.run_test()` | Playwright (heavier) | **TUI** |
| Contributor friction | Python devs contribute easily | Requires JS/Svelte knowledge | **TUI** |
| Architecture | Single process, no IPC | API forces clean separation | **SvelteKit** |

**SvelteKit wins 5, TUI wins 3, 2 ties.**

### Ink (React for CLIs) — Rejected

[Ink](https://github.com/vadimdemedes/ink) requires Node.js (same toolchain cost as SvelteKit) but renders to the terminal (same image limitations as Textual). No native Python integration. Strictly dominated by both options.

### What the TUI Advocate Got Right

These points should inform the SvelteKit implementation:

- **Keep it lean.** The UI is fundamentally a form editor + progress monitor. Don't over-engineer.
- **Use existing interfaces.** `TrainCallbacks` and `TrainCommands` are the natural API contract.
- **Minimize contributor friction.** SvelteKit's HTML-first syntax was chosen specifically because Python devs can read and modify it.
- **Video display is not a current requirement.** The codebase explicitly skips video preview.

### Proposed Architecture

```
OneTrainer/
  modules/
    api/                    # FastAPI + WebSocket backend
      server.py             # Serves API + built frontend static files
      routes/
        config.py           # TrainConfig CRUD
        training.py         # Start/stop + WebSocket for TrainCallbacks
        samples.py          # Serve sample images from workspace/
        concepts.py         # Concept management + image upload
    trainer/                # UNCHANGED
    model*/                 # UNCHANGED
    dataLoader/             # UNCHANGED
  frontend/                 # SvelteKit (adapter-static)
    src/routes/             # File-based routing = one file per tab
    src/lib/
      stores/               # Svelte stores wrapping WebSocket
      components/           # Reusable form components
  start-ui.sh              # Launches FastAPI server, opens browser
```
